# Connecting DSI Headset

This guide will walk you through how to connect your Wearable Sensing DSI headset to BCI2000 for data acquisition.

```{admonition} Note
:class: sidebar note
Please ensure BCI2000 is already installed on your system. If you haven't installed it yet, you can find the download instructions [here](https://www.bci2000.org/mediawiki/index.php/DownloadBCI2000).
```

## Update the DSI API Driver

BCI2000 includes a community-contributed module called DSISerial, which supports Wearable Sensing DSI EEG systems. This module is already built into BCI2000, but you need to update its driver manually to ensure full compatibility.

1. Download the Compatible Driver File

   * Download the driver that was built alongside the current version of *DSISerial*. Although new versions of the Wearable Sensing *DSI API* exist, they have not yet been tested with *DSISerial* and may not work correctly.

   * [DSI_API version 1.20.1](https://www.bci2000.org/svn/trunk/src/contrib/SignalSource/DSISerial/DSI_API/)

   > Choose the `.dll` file that matches your system architecture.

2. Locate and copy the `.dll` file.

   * Open the unzipped folder and find the dynamic library file related to your system. This tutorial is using windows so I will copy the `.dll` with the name `libDSI-Windows-x86_64.dll`

3. Paste into the `prog` directory.

   * Locate where you installed the latest version of *BCI2000* and locate the `prog` directory. Inside `prog` paste your `.dll` file named `libDSI-Windows-x86_64.dll`. Your path should look similar to this:

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

1. Open the Windows Search Bar.

2. Search "Edit the system environment Variables"

3. Inside the *System Variables* box, you'll see a button called **New**, click it to add a new variable.

4. Enter the following into the new variable:

   * Variable name: `DSISerialPort`

   * Variable value: `COM#`
Replace `#` with the COM port number assigned to your DSI headset.

> **Note:** If you switch to a different headset -- or change how its connected (e.g., from USB to Bluetooth) -- you'll need to update the `DSISerialPort` variable value to match the new COM port.

## Run BCI2000Launcher

With all configuration complete, you're now ready to launch BCI2000 and test the connection to your DSI headset.

### 1. Open the BCI2000 Launcher

* Navigate to your BCI2000 `prog` directory and open `BCI2000Launcher.exe`

```{figure} ../../_static/bci2000-1.png

*BCI2000 Launcher* Interface
```

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
  
   ```{figure} ../../_static/bci2000-2.png

   *Operator* Window
   ```

   2. [Optional] Click ***Config*** in the ***Operator*** window.

      * This opens a menu titled *Parameter Configuration*, which is responsible for customizing your current experiment.

   3. Click ***Set Config***
      * This step will apply all the current parameter settings and initializes all the modules you selected. You will know if this launch was successful if no error logs were displayed and both the Timing and Source Signal windows were opened.

   ```{figure} ../../_static/bci2000-3.png
   :name: bci2000-config
   :align: center

   *BCI2000 SetConfig* Success
   ```

   If *Set Config* was not successful, a window called *System Log* will appear showing an error such as <span style="color: red;">"Unable to start the amplifier"</span>. This usually happens when the headset wasn’t properly turned on or connected before clicking *Set Config*, so make sure to double-check that your DSI headset is powered on and connected beforehand.

   4. Click ***Start***
      * This begins the mock data stream. If successful, you'll see the following message at the bottom of the *Operator* window:

   ```sh
   Running DSISerial running DummySignalProcessing running DummyApplication running
   ```

#### Resources

This documentation only covers connection/setup. For full usage, configuration, and advanced module options, please visit following links:

* [User Tutorial](https://www.bci2000.org/mediawiki/index.php/User_Tutorial)

* [Contributions:DSISerial](https://www.bci2000.org/mediawiki/index.php/Contributions:DSISerial)

* [BCI2000 BCI system User manual](https://manualzz.com/doc/6917512/bci2000-bci-system-user-manual)
