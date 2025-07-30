# Connecting DSI Headset

This guide will walk you through how to connect your Wearable Sensing DSI headset to BCI2000 for data acquisition.

```{admonition} Note
:class: sidebar note
Please ensure BCI2000 is already installed on your system. If you haven't installed it yet, you can find the download instructions [here](https://www.bci2000.org/mediawiki/index.php/DownloadBCI2000).
```

## Update the DSI API Driver

BCI2000 includes a community-contributed module specfically for supporting Wearable Sensing DSI EEG systems. Luckily, the module is already built into BCI2000

However, we will need to update the module's driver file with the latest version directly from the Wearable Sensing API. This is the only file you need to manually place.

**Steps to Download the Latest API**

1. Download the latest Wearable Sensing DSI API
   * [DSI API (Version 1.20.3) NEED TO UPDATE LINK](https://wearablesensing.com/files/DSI-API_Current.zip)

2. Locate and copy the `.dll` file.

Open the unzipped folder and find the dynamic library file related to your system. This tutorial is using windows so I will copy the `.dll` with the name `libDSI-Windows-x86_64.dll`

3. Paste into the `prog` directory.

Locate where you installed the latest version of BCI2000 and locate the `prog` directory. Inside `prog` paste your `.dll` file named `libDSI-Windows-x86_64.dll`. Your path should look similar to this:

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

After downloading the DSISerial module, you'll need to conifugre your environment variable so it points to the correct COM port for your DSI headset. This enables BCI2000 to easily recognize the device.

**Steps to Add the Environment Variable**

1. Open the Control Panel.

2. Navigate to:

```sh
System->Advanced system settings->Environment Variables
```

3. Under System Variables, click New.

4. Enter the following into the new variable:

   * Variable name: `DSISerialPort`

   * Variable value: `COM#`
Replace `#` with the COM port number assigned to your DSI headset.



```{admonition} How to Find Your Headset's COM Port

1. Open Device Manager

2. Expand the category that matches your connection type:

   * A wireless connection will be listed under the Bluetooth section.

   * A wired connection will be found under Ports (COM & LPT).

3. The device will be listed with its assigned port (e.g., `COM3`, `COM5`). Make a note of this exact name to use as the "Variable value" in the previous step.

```

## Run BCI2000Launcher

With all the configuration complete, you are now ready to run BCI2000Launcher and test our connection to the DSI headset.

### 1. Open the BCI2000 Launcher

* Navigate to your BCI2000 `prog` directory and open `BCI2000Launcher.exe`

### 2. Select the Test Modules

   After launching the program you will see 4 modules, we can choose to ignore the 'Other' module as we are only testing the headset connection.

* Signal Source: `DSISerial`
* Signal Processing: `DummySignalProcessing`
* Application: `DummyApplication`

### 3. Click the launch button

   After selecting the correct modules, you can now launch your experiment. This will launch all the modules, and You will know if your headset was successfully conencted if Set Config returns no errors.

   If the BCI2000/Operator displays this at the bottom of hte window, your connection was a success:

   ```sh
   Running DSISerial running DummySignalProcessing running DummyApplication running
   ```


#### Resources

For additional documentation and support, please refer to the following:

* [Contributions:DSISerial](https://www.bci2000.org/mediawiki/index.php/Contributions:DSISerial)
