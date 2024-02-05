from azure.iot.device import X509
from azure.iot.device.aio import ProvisioningDeviceClient
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import Message

import json
import psutil
import uuid
import re

from imports.geolocation import geolocation

class intelliconnect():

    def __init__(self, configs):

        self.configs = configs
        self.geolocation = geolocation(configs)

        self.ip = self.geolocation.get_ip()
        self.mac = self.get_mac()

    def createX50(self):
        return X509(
            cert_file=self.configs["cert"]["cert_file"],
            key_file=self.configs["cert"]["key_file"],
            pass_phrase=self.configs["cert"]["pass_phrase"],
        )

    def createProvisioningClient(self):
        return ProvisioningDeviceClient.create_from_x509_certificate(
            provisioning_host=self.configs["host"],
            registration_id=self.configs["registration_id"],
            id_scope=self.configs["id_scope"],
            x509=self.createX50(),
        )

    def createDeviceClient(self, result):
        return IoTHubDeviceClient.create_from_x509_certificate(
            x509=self.createX50(),
            hostname=result.registration_state.assigned_hub,
            device_id=result.registration_state.device_id,
        )

    def get_mac(self):
        
        return ':'.join(re.findall('..', '%012x' % uuid.getnode()))

    async def send_test_message(self, temp, humidity, client):

            loc = self.geolocation.get_location()

            data = {
                "_id": str(self.configs["device_id"]),
                "Data": [{
                    "Sensor": "TempHumidity",
                    "Data": {
                        "Temperature": str(temp),
                        "Humidity": str(humidity)
                    }
                }],
                "State": {
                    "CPU": str(psutil.cpu_percent()),
                    "Memory": str(psutil.virtual_memory()[2]),
                    "Diskspace": str(psutil.disk_usage('/').percent),
                    "CPUTemp": str(psutil.sensors_temperatures()['cpu_thermal'][0].current),
                    "IP": str(self.ip),
                    "MAC": str(self.mac)
                },
                "Location": {
                    "Longitude": str(loc[1]),
                    "Latitude": str(loc[0])
                }
            }

            print(data)

            msg = Message(
                 json.dumps(data),
                 content_encoding="utf-8",
                 content_type="application/json")
            msg.message_id = uuid.uuid4()
            await client.send_message(msg)
            print("Message sent to IntelliConnect IoT")
