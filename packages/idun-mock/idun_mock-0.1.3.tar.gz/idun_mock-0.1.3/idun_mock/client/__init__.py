import asyncio, json, csv, httpx
import websockets.exceptions
from datetime import datetime
from idun_data_models import RecordingIn, RecordingStatusIn, RecordingConfig, DataStreams
from idun_tools import logger
from ..data_generator import generate_queue, GeneratorTime


class MockGuardianDataGenerator:
    def __init__(self):
        self.message_queue = asyncio.Queue(maxsize=int(1e7))
        self.recordingID_queue = asyncio.Queue(maxsize=10)
        self.recordingIDs = []
        self.stop = asyncio.Event()

    async def generate(
        self,
        devices: int,
        connections_per_device: int,
        p_connection_end: float,
        generator_time_type: GeneratorTime,
        delay: float = 0,
        mock_recorded: bool = False,
        random_seed: int = 0,
        stop: asyncio.Event = None,
        finish_generating: asyncio.Event = asyncio.Event(),
        enableStreamer: bool = True,
        first_device=0,
    ):
        if stop is None:
            stop = self.stop
        return await generate_queue(
            logger,
            self.message_queue,
            self.recordingID_queue,
            devices,
            connections_per_device,
            p_connection_end,
            generator_time_type,
            delay,
            mock_recorded,
            random_seed,
            stop,
            finish_generating,
            enableStreamer,
            first_device,
        )

    async def gather_recordingIDs(self) -> list[dict]:
        if len(self.recordingIDs) == 0:
            self.recordingIDs = await self.recordingID_queue.get()
        return self.recordingIDs

    async def register_recordings(self, rest_api_url: str) -> None:
        async def register_recording(client, deviceID, recordingID):
            payload = RecordingIn(
                recordingID=recordingID,
                deviceID=deviceID,
                displayName="mock data generator",
                config=RecordingConfig(data_stream_subscription=DataStreams(bandpass_eeg=True)),
            )
            logger.bind(payload=payload).info("Registering recording")
            await http_post(
                client,
                f"{rest_api_url}/devices/{deviceID}/recordings",
                auth=(deviceID, ""),
                content=payload.json(),
            )

        recordingIDs = await self.gather_recordingIDs()
        async with httpx.AsyncClient() as client, asyncio.TaskGroup() as tg:
            for i in recordingIDs:
                tg.create_task(register_recording(client, i["deviceID"], i["recordingID"]))
        logger.info("Recordings registered")

    async def stop_recordings(self, rest_api_url: str) -> None:
        async def stop_recording(client, deviceID, recordingID):
            await http_put(
                client,
                f"{rest_api_url}/devices/{deviceID}/recordings/{recordingID}/status",
                auth=(deviceID, ""),
                content=RecordingStatusIn(stopped=True).json(),
            )

        recordingIDs = await self.gather_recordingIDs()
        async with httpx.AsyncClient() as client, asyncio.TaskGroup() as tg:
            for i in recordingIDs:
                tg.create_task(stop_recording(client, i["deviceID"], i["recordingID"]))
        logger.info("Recordings stopped")

    async def send(self, websocket, stop: asyncio.Event = None):
        "Given a connected Websocket, `send` will directly put data in it from the queue."

        if stop is None:
            stop = self.stop

        async def may_block():
            message = await self.message_queue.get()
            try:
                await websocket.send(message.json())
            except websockets.exceptions.ConnectionClosedError:
                await self.message_queue.put(message)
                raise

        try:
            while not stop.is_set():
                await asyncio.wait_for(may_block(), timeout=6.0)
        except asyncio.TimeoutError:
            if self.message_queue.empty():
                logger.info("Sending timed out. Queue empty; stopping")
                stop.set()
            else:
                logger.info(
                    f"Sending timed out. Messages in queue: {self.message_queue.qsize()}; reconnecting to websocket"
                )
                raise

    async def log_stream(self, websocket, stop: asyncio.Event = None):
        "Given a connected Websocket, `read_stream` will read data from it and log it."

        if stop is None:
            stop = self.stop

        async def may_block(latency_f):
            message = json.loads(await websocket.recv())
            if "bp_filter_eeg" in message:
                ts = message["bp_filter_eeg"]["timestamp"][0]
                latency = datetime.now().timestamp() - ts
                samples_in_message = len(message["bp_filter_eeg"]["timestamp"])
                logger.info(f"Latency: {latency} ({samples_in_message} samples in message)")
                latency_f.writerow(
                    {
                        "timestamp": ts,
                        "deviceID": message["deviceID"],
                        "latency": latency,
                    }
                )

        try:
            with open("latency.log", "a") as latency_f:
                latency_csv = csv.DictWriter(
                    latency_f,
                    dialect="excel",
                    fieldnames=["timestamp", "deviceID", "latency"],
                )
                if latency_f.tell() == 0:
                    latency_csv.writeheader()
                while not stop.is_set():
                    await asyncio.wait_for(may_block(latency_csv), timeout=6.0)
        except asyncio.TimeoutError:
            logger.info("Receiving timed out")

    async def send_kinesis(self, kinesis_client, stream_name, stop: asyncio.Event = None):
        "Put data to Kinesis from the queue"

        if stop is None:
            stop = self.stop

        async def may_block():
            message = await self.message_queue.get()
            kinesis_client.put_record(
                StreamName=stream_name,
                Data=json.dumps(apiGatewayTransform(message)),
                PartitionKey=message["deviceID"],
            )

        try:
            while not stop.is_set():
                await asyncio.wait_for(may_block(), timeout=6.0)
        except asyncio.TimeoutError:
            logger.info("Sending timed out, stopping.")
            stop.set()


async def http_post(client: httpx.AsyncClient, url: str, auth, content=None):
    try:
        response = await client.post(
            url,
            content=content,
            auth=auth,
            headers=httpx.Headers({"Content-Type": "application/json"}),
        )
        response.raise_for_status()
    except httpx.HTTPStatusError as err:
        status_code = err.response.status_code
        logger.bind(
            request=err.request,
            response=err.response,
            reason=err.response.reason_phrase,
            reason_text=err.response.text,
            status_code=status_code,
            http_version=err.response.http_version,
            http_headers=err.response.headers,
            elapsed_sec=err.response.elapsed.total_seconds(),
        ).warning(f"Received error code from POST {url}")
    except httpx.RequestError as err:
        logger.bind(error=err).error("HTTP request error")


async def http_put(client: httpx.AsyncClient, url: str, auth, content=None):
    try:
        response = await client.put(
            url,
            content=content,
            auth=auth,
            headers=httpx.Headers({"Content-Type": "application/json"}),
        )
        response.raise_for_status()
    except httpx.HTTPStatusError as err:
        status_code = err.response.status_code
        logger.bind(
            request=err.request,
            response=err.response,
            reason=err.response.reason_phrase,
            reason_text=err.response.text,
            status_code=status_code,
            http_version=err.response.http_version,
            http_headers=err.response.headers,
            elapsed_sec=err.response.elapsed.total_seconds(),
        ).warning(f"Received error code from PUT {url}")
    except httpx.RequestError as err:
        logger.bind(error=err).error("HTTP request error")


def apiGatewayTransform(message: dict):
    "Wrap message with the API gateway's template transform"
    message["connectionID"] = "a"
    return message
