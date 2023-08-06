# IDUN Guardian mock library / client

This is a client library for the IDUN Guardian which mocks out the physical device, intended for development and building tests for the IDUN Guardian.
The [`data_generator`](idun_mock/data_generator) generates random device packets.
The [`client`](idun_mock/client) is a command-line utility that sends them to the Guardian API.

## Features

- Mock device data generator
- Send mocked device data to a Cloud endpoint

## Sending mock data to the cloud API (client)

You can start sending mock data to the cloud API by installing the poetry project and running the `idun_mock.client` module:

```
# at this directory
poetry install
poetry run python -m idun_mock.client -w <websocket_url>
```

The websocket URL is where the data should be sent. Change the generator parameters according to what scenario you want to simulate (look in [`idun_mock/client/__main__.py`](idun_mock/client/__main__.py)).

## Troubleshooting: sending mock data to Kinesis, bypassing the API

If you have IDUN AWS credentials, you can also send mock data directly to Kinesis, bypassing the API:

```
# Set these environment variables:
#   AWS_ACCESS_KEY_ID
#   AWS_SECRET_ACCESS_KEY
#   AWS_DEFAULT_REGION

poetry run python -m idun_mock.client -k <kinesis_stream_name> [-e <aws_endpoint>]
```
