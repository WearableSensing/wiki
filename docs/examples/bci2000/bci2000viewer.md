# Connecting DSI Headset

This guide will walk you through how to connect your Wearable Sensing DSI headset to BCI2000 for data acquisition.

```{admonition} Note
:class: sidebar note
Please ensure BCI2000 is already installed on your system. If you haven't installed it yet, you can find the download instructions [here](https://www.bci2000.org/mediawiki/index.php/DownloadBCI2000).
```

## Update the DSI API Driver

BCI2000 includes a community-contributed module specfically for supporting Wearable Sensing DSI EEG systems. Luckily, the module is already built into BCI2000.

However, we will need to update the module's driver file with the latest version directly from the Wearable Sensing API. This is the only file you need to manually place.

**Steps to Download the Latest API**

1. Download the latest Wearable Sensing DSI API
   * [DSI API (Version 1.20.3)](https://wearablesensing.com/wp-content/uploads/2025/07/DSI_API_v1.20.3_06202025.zip)

2. Locate and copy the `.dll` file.

   * Open the unzipped folder and find the dynamic library file related to your system. This tutorial is using windows so I will copy the `.dll` with the name `libDSI-Windows-x86_64.dll`

3. Paste into the `prog` directory.

   * Locate where you installed the latest version of BCI2000 and locate the `prog` directory. Inside `prog` paste your `.dll` file named `libDSI-Windows-x86_64.dll`. Your path should look similar to this:

   ```sh
   BCI2000\BCI2000 v3.6.beta.R7385\BCI2000.x64.bundled\prog
   ```

<!-- To access it, you will need to download the source code from the SVN repository:
[http://www.bci2000.org/svn/trunk/src/contrib/SignalSource/DSISerial](http://www.bci2000.org/svn/trunk/src/contrib/SignalSource/DSISerial)

```{admonition} Note
:class: attention
Accessing the DSISerial SVN repository requires an existing BCI2000 account and an SVN client, as these links cannot be downloaded directly via a browser.

If you're unfamiliar with SVN tools, we recommend [TortoiseSVN](https://tortoisesvn.net/downloads.html) for Windows users, which provides a simple to use interface to download and manage SVN repositories.
``` -->

### Set the Environment Variable

After downloading and placing the DSI API into the correct directory, you'll need to conifugre your environment variable so it points to the correct COM port for your DSI headset. This allows BCI2000 to automatically detect the device is the easiest method recommended by BCI2000.

**Steps to Add the Environment Variable**

1. Open the Control Panel.

2. Navigate to:

```sh
System->Advanced system settings->Environment Variables
```

3. Under *System Variables*, click New.

4. Enter the following into the new variable:

   * Variable name: `DSISerialPort`

   * Variable value: `COM#`
Replace `#` with the COM port number assigned to your DSI headset.

If you use a different headset in the future, you will just need to update the `DSISerialPort` variable value to match its assigned COM port.

```{admonition} How to Find Your Headset's COM Port

1. Open Device Manager

2. Expand the category that matches your connection type:

   * A wireless connection will be listed under the Bluetooth section.

   * A wired connection will be found under Ports (COM & LPT).

3. Find your device in the list. Its name will be followed by the assigned port in parentheses (e.g., `DSI-Headset (COM3)`). Only take note of `COM#`—you’ll use this in the "Variable value" field from the previous step.

```

## Run BCI2000Launcher

With all configuration complete, you're now ready to launch BCI2000 and test the connection to your DSI headset.

### 1. Open the BCI2000 Launcher

* Navigate to your BCI2000 `prog` directory and open `BCI2000Launcher.exe`

### 2. Select the Test Modules

   When the launcher opens, you'll see four module slots.

* Signal Source: `DSISerial`
* Signal Processing: `DummySignalProcessing`
* Application: `DummyApplication`
* Other: (*Leave this one unselected*)

> `DummySignalProcessing` and `DummyApplication` don't perform any actual signal processing or user interaction. In essence they're placeholders used for testing the signal connection to the DSI headset without needing to setup a full experiment.

### 3. Configure and Launch the System

   Once you've selected all three modules:

   1. Click ***Launch***

      * The *Launch* button will set up all three modules, and create a new window called *Operator*.

   2. [Optional] Click ***Config*** in the ***Operator*** window.

      * This opens a menu titled *Parameter Configuration*, which is responsible for customizing your current experiment.

   3. Click ***Set Config***
      * This step will apply all the current parameter settings and initializes all the modules you selected. You will know if this launch was successful if no error logs were displayed and both the Timing and Source Signal windows were opened.

   4. Click ***Start***
      * This begins the mock data stream. If successful, you'll see the following message at the bottom of the *Operator* window:

   ```sh
   Running DSISerial running DummySignalProcessing running DummyApplication running
   ```

#### Resources

For additional documentation and support, please refer to the following:

* [Contributions:DSISerial](https://www.bci2000.org/mediawiki/index.php/Contributions:DSISerial)

* [BCI2000 BCI system User manual](https://manualzz.com/doc/6917512/bci2000-bci-system-user-manual)
