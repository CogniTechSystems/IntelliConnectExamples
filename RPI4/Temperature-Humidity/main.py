import asyncio

from imports.confs import confs
from imports.intelliconnect import intelliconnect

import time
import board
import adafruit_dht

# Sensor data pin is connected to GPIO 4
sensor = adafruit_dht.DHT11(board.D4)

confs = confs()
config = confs.config

async def main():

    intelliconn = intelliconnect(config)

    pclient = intelliconn.createProvisioningClient()
    result = await pclient.register()

    if result.status == "assigned":

        dclient = intelliconn.createDeviceClient(result)

        # Connect the client.
        await dclient.connect()
        print("Connected to IntelliConnect IoT")

        while True:
            try:
                # Send sensor data to IntelliConnect
                temp = sensor.temperature
                humidity = sensor.humidity
                await intelliconn.send_test_message(temp, humidity, dclient)
            except RuntimeError as error:
                time.sleep(3.0)
                continue
            except Exception as error:
                sensor.exit()
                raise error

            time.sleep(3.0)

if __name__ == "__main__":
    asyncio.run(main())