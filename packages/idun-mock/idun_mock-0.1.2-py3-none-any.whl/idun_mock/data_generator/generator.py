import threading, random, time, asyncio
from idun_data_models import Message
from idun_tools import logger
from .connection_pool import DeviceConnectionPool, GeneratorTime


async def generate_queue(
    logger,
    message_queue: asyncio.Queue,
    recordingID_queue: asyncio.Queue,
    devices: int,
    connections_per_device: int,
    p_connection_end: float,
    generator_time_type: GeneratorTime,
    delay: float = 0,
    mock_recorded: bool = False,
    random_seed: int = 0,
    stop: asyncio.Event = asyncio.Event(),
    finish_generating: asyncio.Event = asyncio.Event(),
    enableStreamer: bool = True,
    first_device=0,
) -> set[Message]:
    """
    Generate random device messages and put them on the `message_queue`.
    When the connection pool finishes or a stop signal arrives, it terminates, and returns a set of all messages.

    Parameters:
    - `message_queue`: queue where messages will be put
    - `recordingID_queue`: only 1 item will be put in the queue: a list of the generated recordingIDs
    """
    connectionPool = DeviceConnectionPool(
        devices=devices,
        connections_per_device=connections_per_device,
        p_connection_end=p_connection_end,
        p_impedance_measurement=0,
        mock_recorded=mock_recorded,
        random_seed=random_seed,
        generator_time_type=generator_time_type,
        enableStreamer=enableStreamer,
        first_device=first_device,
    )
    logger.info("> Generating test data")
    logger.info(
        f"> Recording and Device ID for all recordings that should be produced after running this generator to completion: {connectionPool.allRecordingIDs()}"
    )
    await recordingID_queue.put(connectionPool.allRecordingIDs())
    messageSet = set()
    while not stop.is_set() and not connectionPool.done():
        data = connectionPool.next_message()
        if data:
            try:
                await asyncio.wait_for(message_queue.put(data), timeout=6.0)
                messageSet.add(data)
                await asyncio.sleep(delay / devices)
            except asyncio.TimeoutError:
                if message_queue.full():
                    logger.error("Generator queue full! Stopping generation")
                else:
                    logger.error("Generator timeout! Stopping generation")
                stop.set()
    finish_generating.set()
    logger.info("> Stop generating test data")
    return messageSet


def generate_kinesis(
    kinesis_client,
    devices: int,
    connections_per_device: int,
    p_connection_end: float,
    p_impedance_measurement: float = 0,
    mock_recorded: bool = False,
    random_seed: int = 0,
    stop: threading.Event = threading.Event(),
) -> set[Message]:
    """
    Generate random device messages and put them on the Kinesis stream.
    When the connection pool finishes or a stop signal arrives, it terminates, and returns a set of all messages.
    """
    logger.info("> Generating test data")
    connectionPool = DeviceConnectionPool(
        devices=devices,
        connections_per_device=connections_per_device,
        p_connection_end=p_connection_end,
        p_impedance_measurement=p_impedance_measurement,
        mock_recorded=mock_recorded,
        random_seed=random_seed,
    )
    messageSet = set()
    while not stop.is_set() and not connectionPool.done():
        data = connectionPool.next_message()
        if data:
            kinesis_client.put_record(
                Data=data.dict(),
                PartitionKey=data.deviceID,
            )
            messageSet.add(data)
    logger.info("> Stop generating test data")
    return messageSet


def randomDecodedPayload():
    "Return a random, decoded payload. Mock the decoding function."
    return {
        "eeg_ch1": list(
            map(
                lambda x: {
                    "timestamp": time.time(),
                    "value": random.random(),
                },
                range(0, 20),
            )
        ),
        "acc": list(
            map(
                lambda x: {
                    "timestamp": time.time(),
                    "x": random.random(),
                    "y": random.random(),
                    "z": random.random(),
                },
                range(0, 3),
            )
        ),
        "magn": list(
            map(
                lambda x: {
                    "timestamp": time.time(),
                    "x": random.random(),
                    "y": random.random(),
                    "z": random.random(),
                },
                range(0, 3),
            )
        ),
        "gyro": list(
            map(
                lambda x: {
                    "timestamp": time.time(),
                    "x": random.random(),
                    "y": random.random(),
                    "z": random.random(),
                },
                range(0, 3),
            )
        ),
    }
