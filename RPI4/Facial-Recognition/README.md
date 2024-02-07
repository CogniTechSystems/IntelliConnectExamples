# IntelliConnect RPI Facial Recognition Example

![IntelliConnect RPI Facial Recognition Example](assets/img/rpi4-facial-recognition.jpg)

This IntelliConnect example takes you through creating a facial recognition device with the Intel Neural Compute Stick 2 and Raspberry Pi 4.

# Hardware Requirements

- [Raspberry Pi 4](https://thepihut.com/products/raspberry-pi-4-model-b) (Other models should work fine)
- [Intel Neural Compute Stick 2](https://www.intel.com/content/www/us/en/developer/articles/tool/neural-compute-stick.html)
- USB camera

# Hardware Setup

![IntelliConnect RPI Facial Recognition Example](assets/img/intel-ncs2-rpi4.jpg)

The hardware setup is very simple, plug your NCS2 and USB camera to your Raspberry Pi and you are good to go.

# Software Setup

The following software assumes Windows.

- [GIT](https://git-scm.com/download/)

First install the software listed above. Next to install the program software, navigate to the directory where you would like set up the project and run:

```
git clone https://github.com/Innov8DigitalMediaTech/IntelliConnectExamples
cd IntelliConnectExamples/RPI4/Facial-Recognition
sh install.sh
```

You will also need an API key from [IPInfo.io](https://ipinfo.io/).

# Data Set Up

You should add a single image for each user that has access to your TMS system. The image should be a front on shot and clear, and the file name should be the user's TMS ID. IE, if you have a staff member called `Joe Blogs`, and their user ID is `1`, then the file you use should be `1.jpg`.

You should place your images of known people in the `model/data/known` directory. You can also add test images to the `model/data/test` directory. The images you add to the test directory should be different from the ones in the known directory.

# IntelliConnect Setup

In your business TMS head over to the IntelliConnect section and click on `Assets` then click on the `Actions` tab and select `Create Individual Asset`.

![IntelliConnect RPI Facial Recognition Example](assets/img/device-enrollment.jpg)

## Individual Device Enrollment

Enter or select the following:

- **Asset Name** - *Your new device name (Must be unique)*
- **Asset Type** - *Select Device*
- **Asset Category** - *Select SecurityCamera*
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

Navigate to the directory you want to create the certificates in and run the following command, replacing `Your-Registration-ID` with the value found in the `Registration ID` field on the `Create IntelliConnect Asset` page. In the screen shot above you will see for this example the registration ID is `66fceeb0-2d38-4b5c-9690-0398b2241627` however this will change for you each time you create a new device.

```
winpty openssl req -outform PEM -x509 -sha256 -newkey rsa:4096 -keyout device-key.pem -out device-cert.pem -days 30 -extensions usr_cert -addext extendedKeyUsage=clientAuth -subj "//CN=Your-Registration-ID"
```

You will be asked to enter a PEM password. In development and test environments you can use any value for you this but it is good to get into the habbit of using secure passwords so use a secure password here and make sure you keep it safe as you will need it later.

You should now have two files:

- `device-key.pem`
- `device-cert.pem`

You need to copy these files to to the certs directory in your project in the following location:

```
IntelliConnectExamples/RPI4/Facial-Recognition/certs
```
### Complete The Enrollment

Now you can complete the enrollment of your new device. This step will create an enrollment for your device and once it starts running it will automatically be registered to the IntelliConnect network and begin publishing sensor data.

The system will also create training data for your Intelligent Systems Assistant (ISA) that will allow you to query the state of the device and its sensors.

![IntelliConnect RPI Facial Recognition Example](assets/img/asset.jpg)

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
    "cert": {
        "cert_file": "./certs/device-cert.pem",
        "key_file": "./certs/device-key.pem",
        "pass_phrase": ""
    },
    "openvino": {
        "detection": "model/face-detection-retail-0004.xml",
        "reidentification": "model/face-reidentification-retail-0095.xml",
        "landmarks": "model/landmarks-regression-retail-0009.xml",
        "runas": "MYRIAD",
        "known": "model/data/known/",
        "test": "model/data/test/",
        "threshold": 1.20
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

Now its time to run your device. Once you run the device the system will automatically register your device and connect it to the IntelliConnect platform, you will see the program print out `Connected to IntelliConnect IoT` before beginning to see the data that is being sent to IntelliConnect.

![IntelliConnect RPI Facial Recognition Example](assets/img/console.jpg)

You will notice the `Provisioning` stat on the asset page will change from `Enrolled` to `Registered` and you will start to see real-time data coming in from your device.

# View The Stream

The program will start a stream on your local network that can be accessed via a browser. For production environments you would need to portforward from your router to the port on your Raspberry Pi if you would like to view this stream outside of your network. We will publish a tutorial on how to do that in the future.

![IntelliConnect RPI Facial Recognition Example](assets/img/facial-recognition-stream.jpg)

If you are on the same network that the Raspberry Pi is on, you can access the stream with the following URL:

```
http://YourIP:8383/?stream.mjpg
```

# Training Your Intelligent Systems Assistant

Now you need to train your Intelligent Systems Assistant so that you can query the device in natural language using AI. When you created the device training data was automatically created.

![IntelliConnect RPI Facial Recognition Example](assets/img/isa-data.jpg)

Head over to the `ISA` control panel and head to `Model` then click on `Create New` in the `Create ISA Dataset` section. Once the new dataset has been generated you will be notified on screen and you will receive an email to your TMS contact email.

![IntelliConnect RPI Facial Recognition Example](assets/img/isa-model-trained.jpg)

Next you need to train the ISA model. To do this click on the `Train` button and wait for it to complete. Once the new training has completed you will be notified on screen and you will receive an email to your TMS contact email.

![IntelliConnect RPI Facial Recognition Example](assets/img/isa-model-deployed.jpg)

Finally you need to deploy the new ISA model. To do this click on the `Deploy` button and wait for it to complete. Once the new deployment has completed you will be notified on screen and you will receive an email to your TMS contact email.

# Querying The User's Location

![IntelliConnect RPI Facial Recognition Example](assets/img/query-isa.jpg)

When the AI detects one of the TMS users, it will send the user ID to IntelliConnect, which will update the user's TMS account with the zone that they are in and the time they were seen in it.

Through the use of the Intelligent Systems Assistant (ISA), you can ask `Where is Joe Blogs`, and ISA will respond with the zone they were last seen in and what time, if they were seen within the last hour.

- Where is `User Name`?
- Have you seen `User Name`?

It is likely that the speech recognition could get confused with the spelling of names, in some cases it may best to type the query into chat rather than speak.

# Future Features

Future features of this system include:

- The ability to add miss spellings of the user's name to the account to increase accuracy of identifications.

- The ability to specifiy which zones user's have access to, and rules that trigger if they are located in an out of bounds zone.

# More About IntelliConnect

IntelliConnect IoT is a new product by [Innov8 Digital Media Tech](https://tech.innov8digitalmedia.com/) that allows businesses to easily prototype, provision, deploy and scale intelligent IoT networks. For more information on IntelliConnect or to schedule a demo please [contact sales](https://tech.innov8digitalmedia.com/contact)

