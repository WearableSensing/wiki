# Running BCI2000
--------------------------------------------------------------------------------------

With all configuration complete, you're now ready to launch BCI2000 and verify your DSI headset connection by running a mock experiment. This test ensures that BCI2000 can successfully communicate with your headset and properly open the Source Signal and Timing visualization windows.

## Launch BCI2000

Follow these steps to launch BCI2000 with your DSI headset:

### 1. Open the BCI2000 Launcher

* Navigate to your BCI2000 `prog` directory and open `BCI2000Launcher.exe`

**If successful, the following window will appear:**

```{figure} ../../_static/images/bci2000-1.png

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
  
   ```{figure} ../../_static/images/bci2000-2.png

   *Operator* Window
   ```

   2. **Optional:** Click ***Config*** in the ***Operator*** window.

      * This opens a menu titled *Parameter Configuration*, which is responsible for customizing your current experiment.

   3. Click ***Set Config***
      * This step will apply all the current parameter settings and initializes all the modules you selected. You will know if this launch was successful if no error logs were displayed and both the Timing and Source Signal windows were opened.

   ```{figure} ../../_static/images/bci2000-3.png
   :name: bci2000-config
   :align: center

   *BCI2000* *Source Signal* and *Timing Window*
   ```

   If *Set Config* was not successful, a window called *System Log* will appear showing an error such as <span style="color: red;">"Unable to start the amplifier"</span>. This usually happens when the headset wasn’t properly turned on or connected before clicking *Set Config*, so make sure to double-check that your DSI headset is powered on and connected beforehand.

   4. Click ***Start***
      * This begins the mock data stream. If successful, you'll see the following message at the bottom of the *Operator* window:

   ```sh
   Running DSISerial running DummySignalProcessing running DummyApplication running
   ```

## Resources
--------------------------------------------------------------------------------------

This documentation only covers setup. For full usage, configuration, and advanced module options, please visit following links:

* [User Tutorial](https://www.bci2000.org/mediawiki/index.php/User_Tutorial)

* [Contributions:DSISerial](https://www.bci2000.org/mediawiki/index.php/Contributions:DSISerial)

* [BCI2000 BCI system User manual](https://manualzz.com/doc/6917512/bci2000-bci-system-user-manual)
