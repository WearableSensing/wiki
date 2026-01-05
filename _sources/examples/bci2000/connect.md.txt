# Connecting DSI Headset
---

This guide will walk you through how to connect your Wearable Sensing DSI headset to BCI2000 for data acquisition.

> **Note:** Please ensure BCI2000 is already installed on your system. If you haven't installed it yet, you can find the download instructions [here](https://www.bci2000.org/mediawiki/index.php/DownloadBCI2000).

## Configure the DSISerial Module
---

BCI2000 includes a community-contributed module called DSISerial, which supports Wearable Sensing DSI EEG systems. This module is already built into BCI2000, so no additional downloads or driver installations are required.

### Set the Environment Variable

After downloading and placing the DSI API into the correct directory, you'll need to conifugre your environment variable so it points to the correct COM port for your DSI headset. This allows BCI2000 to automatically detect the device and is the easiest method recommended by BCI2000.

#### Steps to Add the Environment Variable

1. Open the Windows Search Bar.

2. Search "Edit the System Environment Variables"

3. A window with a title *System Properties* should open. Click the `Environment Variables` button near the bottom. This will open another window.

4. There are two panels, inside the bottom one titled *System Variables*, you'll see a button called `New`, click it to add a new variable.

5. Enter the following into the new variable:

   * Variable name: `DSISerialPort`

   * Variable value: `COM#`
Replace `#` with the COM port number assigned to your DSI headset.

> **Note:** If you switch to a different headset -- or change how its connected (e.g., from USB to Bluetooth) -- you'll need to update the `DSISerialPort` variable value to match the new COM port.

If you need help establishing your DSI hardware connection, see our [DSI Software Tutorial](https://code.wearablesensing.com/help/tutorials/software.html).

## Resources
---

This documentation only covers connection. For full usage, configuration, and advanced module options, please visit following links:

* [User Tutorial](https://www.bci2000.org/mediawiki/index.php/User_Tutorial)

* [Contributions:DSISerial](https://www.bci2000.org/mediawiki/index.php/Contributions:DSISerial)

* [BCI2000 BCI system User manual](https://manualzz.com/doc/6917512/bci2000-bci-system-user-manual)
