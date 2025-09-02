# Photodiode Experiment
--------------------------------------------------------------------------------------

This [lsl-tool](https://github.com/WearableSensing/lsl-tools) displays a simple visual stimulus (e.g., a flashing square) intended to be captured by a photodiode. Its primary purpose is to generate events that can be used to measure and correct for timing offsets between the stimulus presentation computer and an LSL-streaming data acquisition system (e.g., a DSI headset).

## Hardware Setup
--------------------------------------------------------------------------------------

You will need to set up a lightdiode as well as a MMBT-S (a device used for sending hardware event markers in neuroscience experiments) for this experiment. You can find instructions on that [here](../../help/tutorials/hardware.rst#mmbt-s-trigger-box-setup-with-e-prime) or visit the [MMBT-S documentation](https://wearablesensing.com/mmbt/). Make sure to place the lightdiode on the top right corner of the screen for this experiment.

## How to Run the Software
--------------------------------------------------------------------------------------

To start the experiment, run the main.py script from your terminal:

```bash
python main.py
```

The script will present a menu. You can press ```Enter``` to select the default choice and begin the interactive setup.

### 1. MMBT-S Hardware Triggers

This configures the connection to an MMBT-S device for sending hardware-timed event markers.

> ```Do you want to connect a MMBTS? (y/n):```

- **y / Default:** Use if you are connecting an MMBTS device.
- **n:** Use if you are not using an MMBTS device.

> ```What is the COM port for MMBTS? (DEFAULT: COM10):```

- This prompt only appears if you answered **yes** above.
- Enter the COM port your MMBTS is connected to (DEFAULT: COM10).

### 2. Software Triggers

This configures a software-based LSL marker stream for sending event markers directly from the script.

> ```Do you want to send software triggers? (y/n):```

- **y / Default:** Creates a new LSL marker stream.
- **n:** Skips the creation of a software marker stream.

> ```Create a marker stream name (DEFAULT: PsychoPyMarkers):```

- This provides a unique name to identify your software LSL stream on the network.

> ```Input a unique software integer trigger (DEFAULT: 3):```

- Enter a specific integer value that will be sent as the marker.

### 3. Experiment Parameters

These prompts control the behavior of the photodiode flash sequence.

> ```How many trials do you want to run? (DEFAULT: 25):```

- Defines the total number of flashes (trials) for the experiment.

> ```At what rate do you want the flashes to run? (DEFAULT: 0.25):```

- Sets the duration (in seconds) of each flash and the pause that follows. A value of 0.25 means a 0.25s flash followed by a 0.25s pause.

> ```At what rate do you want to offset? (DEFAULT: 0):```

- Sets a timing offset value in seconds.

### 4. Recording

This option automatically records the LSL streams you have configured.

> ```Do you want to record? (y/n):```

- **y / Default:** Starts the recorder (tools/consume/unified_receive.py) as a background process.
- The recording begins just before the experiment and stops automatically after it finishes.
- The output is saved as photodiode_exp.csv in the same directory.

## Example Walkthrough
--------------------------------------------------------------------------------------

Here is an example of a complete interaction:

```bash
Please select an option:
    1. Photodiode
Enter your choice (1): 1

Do you want to connect a MMBTS? (y/n): [PRESS ENTER]
What is the COM port for MMBTS? (DEFAULT: COM10): [PRESS ENTER] 

Do you want to send software triggers? (y/n): [PRESS ENTER]
Create a marker stream name (DEFAULT: PsychoPyMarkers): [PRESS ENTER]
Input a unique software integer trigger (DEFAULT: 3): [PRESS ENTER]

How many trials do you want to run?(DEFAULT: 25): 10
At what rate do you want the flashes to run? ( DEFAULT: 0.25): [PRESS ENTER]
At what rate do you want to offset? ( DEFAULT: 0.0): [PRESS ENTER]

Do you want to record? (y/n): y
```

### Outcome of this experiment
--------------------------------------------------------------------------------------

- The experiment will connect to an MMBTS on COM10.

- It will create a software LSL stream named PsychoPyMarkers that sends the integer marker 3.

- The photodiode will flash 10 times with a 0.25-second rate.

- The recorder script will launch in the background, recording both the hardware stream and the PsychoPyMarkers into a file named photodiode_exp.csv.

An analysis can be run on the file created by this experiment. You can find it on the next page.
