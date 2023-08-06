import asyncio, argparse, boto3, os
import websockets.client, websockets.exceptions
from idun_tools import logger
from ..data_generator import GeneratorTime
from . import MockGuardianDataGenerator


generator = MockGuardianDataGenerator()


async def generate_send(
    websocket_url,
    rest_api_url,
    devices=3,
    connections_per_device=1,
    p_connection_end=1e-3,
    delay=0,
    enableStreamer=True,
):
    if delay > 0:
        GENERATOR_TIME_TYPE = GeneratorTime.IDEAL_DEVICE
    else:
        GENERATOR_TIME_TYPE = GeneratorTime.CLIENT
    async with asyncio.TaskGroup() as tg:
        tasks = {}
        tasks["generator"] = tg.create_task(
            generator.generate(
                devices,
                connections_per_device,
                p_connection_end,
                GENERATOR_TIME_TYPE,
                delay=delay,
                enableStreamer=enableStreamer,
                first_device=1,
            )
        )
        # POST the recording at the REST endpoint
        await generator.register_recordings(rest_api_url)

        # Connect to the websocket and send data
        try:
            async for websocket in websockets.client.connect(websocket_url):
                reconnect = False
                try:
                    async with asyncio.TaskGroup() as websocket_tg:
                        websocket_tg.create_task(generator.send(websocket))
                        websocket_tg.create_task(generator.log_stream(websocket))
                except* (
                    websockets.exceptions.ConnectionClosed,
                    websockets.exceptions.ConnectionClosedError,
                ) as err:
                    # This also captures ConnectionClosedOK. We still want to reconnect even if the cloud legitimately closes the connection.
                    logger.bind(error=err).info(
                        "Websocket disconnected; reconnecting..."
                    )
                    reconnect = True
                except* (asyncio.CancelledError, asyncio.TimeoutError):
                    logger.info("Websocket timeout; reconnecting...")
                    reconnect = True

                if not reconnect:
                    break
        except* Exception as err:
            logger.bind(error=err).info("Websocket error")
        finally:
            generator.stop.set()
            await generator.stop_recordings(rest_api_url)


async def generate_send_kinesis(
    kinesis_stream_name,
    aws_endpoint_url,
    devices=3,
    connections_per_device=1,
    p_connection_end=1e-3,
    delay=0,
    enableStreamer=True,
):
    if delay > 0:
        GENERATOR_TIME_TYPE = GeneratorTime.IDEAL_DEVICE
    else:
        GENERATOR_TIME_TYPE = GeneratorTime.CLIENT
    await asyncio.gather(
        generator.generate(
            devices,
            connections_per_device,
            p_connection_end,
            GENERATOR_TIME_TYPE,
            delay=delay,
            enableStreamer=enableStreamer,
        ),
        generator.send_kinesis(
            boto3.client("kinesis", endpoint_url=aws_endpoint_url), kinesis_stream_name
        ),
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="MockDeviceDataGenerator",
        description="Send mocked device data to the cloud (for tests)",
    )
    data_endpoint = parser.add_mutually_exclusive_group(required=True)
    data_endpoint.add_argument(
        "-w", "--websocket", help="Websocket URL where data will be sent"
    )
    data_endpoint.add_argument(
        "-k",
        "--kinesis_stream_name",
        help="Kinesis stream name where data will be sent; specify together with `--aws_endpoint_url`",
    )
    parser.add_argument(
        "-r",
        "--rest_api_url",
        required=True,
        help="URL of the REST API where recordings are registered",
    )
    parser.add_argument(
        "--aws_endpoint_url",
        help="AWS endpoint URL; specify together with `--kinesis_stream_name`",
    )
    parser.add_argument(
        "--avg_duration",
        default=1e3,
        type=float,
        help="Average length of recording in messages",
    )
    parser.add_argument(
        "-d",
        "--devices",
        default=5,
        type=int,
        help="Number of devices streaming simultaneously",
    )
    parser.add_argument(
        "--delay_sec",
        default=0,
        type=float,
        help="Add a delay between generated messages per device. Delay of a real device is 0.080",
    )
    parser.add_argument(
        "--disable_live_stream",
        action="store_true",
        help="Toggle the live streaming of samples",
    )
    args = parser.parse_args()

    try:
        os.remove("latency.log")
    except FileNotFoundError:
        pass

    # NOTE: Connections per device can't be > 1 because we register all the recordings together in the beginning
    if args.websocket:
        asyncio.run(
            generate_send(
                args.websocket,
                args.rest_api_url,
                p_connection_end=1 / args.avg_duration,
                devices=args.devices,
                delay=args.delay_sec,
                enableStreamer=not args.disable_live_stream,
            )
        )
    elif args.kinesis_stream_name:
        asyncio.run(
            generate_send_kinesis(
                args.kinesis_stream_name,
                args.aws_endpoint_url,
                p_connection_end=1 / args.avg_duration,
                devices=args.devices,
                delay=args.delay_sec,
                enableStreamer=not args.disable_live_stream,
            )
        )
