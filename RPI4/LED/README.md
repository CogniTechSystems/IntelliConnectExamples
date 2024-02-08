# IntelliConnect RPI 4 LED Example

![IntelliConnect RPI 4 LED Example](assets/img/rpi4-led.jpg)

This IntelliConnect example takes you through creating a IoT connected LED device with the Raspberry Pi 4. This is a simple example of how businesses can easily prototype IoT devices, however, any IoT device that is programmable can be connected to IntelliConnect.

# Hardware Requirements

- [Raspberry Pi 4](https://thepihut.com/products/raspberry-pi-4-model-b) (Other models should work fine)
- [Breadboard](https://thepihut.com/products/full-sized-breadboard)
- Generic LED
- [Wires](https://thepihut.com/products/thepihuts-jumper-bumper-pack-120pcs-dupont-wire)

# Hardware Setup

![IntelliConnect RPI 4 LED Example](assets/img/wiring.jpg)

To set up your circuit follow the diagram above. Below you will find a pin map.

| RPI    | LED |
| -------- | ------- |
| GPIO 17  | Long leg (Via 330ohm resistor)    |
| Ground    | Short leg    |

# Software Setup

The following software assumes Windows.

- [GIT](https://git-scm.com/download/)

First install the software listed above. Next to install the program software, navigate to the directory where you would like set up the project and run:

```
git clone https://github.com/Innov8DigitalMediaTech/IntelliConnectExamples
cd IntelliConnectExamples/RPI4/LED
sh install.sh
```

You will also need an API key from [IPInfo.io](https://ipinfo.io/).

# Data Structure

IoT devices that connect to IntelliConnect must have a uniform data structure in a format that IntelliConnect can read. Below is the data format for a device that has actuators:

```
{
    "_id": "IntelliConnect Device ID",
    "Data": [{
        "Actuator": "LED",
        "Data": {
            "State": "State (ON or OFF)"
        }
    }],
    "State": {
        "CPU": "CPU Usage Percentage",
        "Memory": "Memory Usage Percentage",
        "Diskspace": "Diskspace Usage Percentage",
        "CPUTemp": "CPU Temperature",
        "IP": "Device IP",
        "MAC": "Device MAC"
    },
    "Location": {
        "Longitude": "Longitude",
        "Latitude": "Latitude"
    }
}
```

# IntelliConnect Setup

In your business TMS head over to the IntelliConnect section and click on `Assets` then click on the `Actions` tab and select `Create Individual Asset`.

![IntelliConnect RPI 4 LED Example](assets/img/device-enrollment.jpg)

## Individual Device Enrollment

Enter or select the following:

- **Asset Name** - *Your new device name (Must be unique)*
- **Asset Type** - *Select Device*
- **Asset Category** - *Select LED*
- **Asset Site Location** - *Select the IntelliConnect Site this device will be installed in*
- **Asset Site Zone** - *Select the IntelliConnect Zone this device will be installed in*
- **Regsitration ID** - *You will need this value for your certificate*

### Device Security Certificate

Before you complete the device enrollment process you need to upload your device security certificate. There are two ways to do this, the first is by self-signing a certificate, and the second is by purchasing an X.509 CA certificate. Self-signed certificates are fine when testing in a non-public environment, but should absolutely not be used in production or public environments. If you are ready to deploy in production you should purchase an X.509 CA certificate that you can use to sign your asset certificates.

In both cases the common name (CN) needs to be set to the registration ID you are using to enroll your device.

#### Self Signed Certificate

**WARNING: This method should only be used for development environments and testing.**

##### Windows

To create a certificate on Windows you will need to have the required software listed above installed and then open a `GitBash` prompt.

Navigate to the directory you want to create the certificates in and run the following command, replacing `Your-Registration-ID` with the value found in the `Registration ID` field on the `Create IntelliConnect Asset` page. In the screen shot above you will see for this example the registration ID is `beb0b639-186d-4847-9d10-0be8d9f5e180` however this will change for you each time you create a new device.

```
winpty openssl req -outform PEM -x509 -sha256 -newkey rsa:4096 -keyout device-key.pem -out device-cert.pem -days 30 -extensions usr_cert -addext extendedKeyUsage=clientAuth -subj "//CN=Your-Registration-ID"
```
You will be asked to enter a PEM password. In development and test environments you can use any value for you this but it is good to get into the habbit of using secure passwords so use a secure password here and make sure you keep it safe as you will need it later.

You should now have two files:

- `device-key.pem`
- `device-cert.pem`

You need to copy these files to to the certs directory in your project in the following location:

```
IntelliConnectExamples/RPI4/LED/certs
```
### Complete The Enrollment

Now you can complete the enrollment of your new device. This step will create an enrollment for your device and once it starts running it will automatically be registered to the IntelliConnect network and will sit waiting for commands to be sent to it from TMS.

The system will also create training data for your Intelligent Systems Assistant (ISA) that will allow you to query the state of the device and the LED, and send commands to turn it on or off.

![IntelliConnect RPI 4 LED Example](assets/img/asset.jpg)

To complete the enrollment, ensure you have filled out all of the information and uploaded your certificate and click `Create`. Once the process completes you will redirected to the asset page.

# Configure Your Device

In the `config/configs.json` file you will find the required configuration for your device.

```
{
    "host": "global.azure-devices-provisioning.net",
    "id_scope": "",
    "device_id": "",
    "registration_id": "",
    "ipinfo": "",
    "cert" : {
        "cert_file": "./certs/device-cert.pem",
        "key_file": "./certs/device-key.pem",
        "pass_phrase": ""
    }
}
```
Open this file in your editor and edit the following values:

- `id_scope` Your provisioning server ID Scope find on the related `Site` page in TMS.
- `device_id` Your device ID found at the top right of the map on the asset page in TMS.
- `registration_id` The registration ID you used to create the certificate and device.
- `ipinfo` Your IpInfo.io API key.
- `pass_phrase` The pass phrase you used to create your certificate.

Once you have made the above changes upload the file to the same location on your Raspberry Pi.

# Run Your Device

Now its time to run your device. In `main.py` you will see the following:

```
core.run("test")
#core.run()
```

By default the system will run in test mode which will loop turing the LED on and off. When you are ready to send commands to the device you should comment out `core.run("test")` and uncomment `#core.run()`. Once you run the device the system will automatically register your device and connect it to the IntelliConnect platform, you will see the program print out `Connected to IntelliConnect IoT` .

![IntelliConnect RPI 4 LED Example](assets/img/console.jpg)

You will notice the `Provisioning` stat on the asset page will change from `Enrolled` to `Registered` and you will start to see real-time data coming in from your device.

# Control The LED

On the top right of the asset page in TMS you will see the LED actuator listed in the `Asset Actuators` box. You click `ON` or `OFF` to send a command to the device which will turn the LED on or off instantly, no matter where in the world the device is.

You can also tell ISA, the Intelligent Systems Assistant to do it for you, see below for more information.

# Training Your Intelligent Systems Assistant

Now you need to train your Intelligent Systems Assistant so that you can query the device in natural language using AI. When you created the device training data was automatically created.

![IntelliConnect RPI 4 LED Example](assets/img/isa-data.jpg)

Head over to the `ISA` control panel and head to `Model` then click on `Create New` in the `Create ISA Dataset` section. Once the new dataset has been generated you will be notified on screen and you will receive an email to your TMS contact email.

![IntelliConnect RPI 4 LED Example](assets/img/isa-model-trained.jpg)

Next you need to train the ISA model. To do this click on the `Train` button and wait for it to complete. Once the new training has completed you will be notified on screen and you will receive an email to your TMS contact email.

![IntelliConnect RPI 4 LED Example](assets/img/isa-model-deployed.jpg)

Finally you need to deploy the new ISA model. To do this click on the `Deploy` button and wait for it to complete. Once the new deployment has completed you will be notified on screen and you will receive an email to your TMS contact email.

![IntelliConnect RPI 4 LED Example](assets/img/query-isa.jpg)

With your Intelligent Systems Assistant now aware of your new device, you can now query the status of the device and LED, and turn the LED on and off by speaking to ISA. Examples of queries are:

- Turn the `Actuator Name` in the `Zone` off. IE: **Turn the LED in the office off**
- Is the `Device Name` in the `Zone` online? IE: **Is the Simple LED Device in the office online?**
- What is the `Actuator` in the `Zone` on? IE: **Is the LED in the office on?**

# More About IntelliConnect

IntelliConnect IoT is a new product by [Innov8 Digital Media Tech](https://tech.innov8digitalmedia.com/) that allows businesses to easily prototype, provision, deploy and scale intelligent IoT networks. For more information on IntelliConnect or to schedule a demo please [contact sales](https://tech.innov8digitalmedia.com/contact)

