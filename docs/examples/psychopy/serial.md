# Sending Triggers Through a Serial Port

As an alternative to network-based synchronization like LSL, you can send triggers directly to your EEG hardware for precise event marking. This method uses your computer's serial port to transmit a signal from PsychoPy to a trigger hub that connects to the EEG Headset. This tutorial provides a simple explaination on how to send these hardware triggers.

## Connecting

If you are using multiple triggers on the trigger hub, then you need to set the Trigger value to one that is not being used. If you are only using this serial trigger then it can be any value from 1-255.

```{code-block} python
:caption: Connecting the port

from psychopy import visual, core
import serial

port = serial.Serial('COM10') #Change the COM port to match your setup

Trigger = 1 # trigger code must be between 1-255
```

## Experiment

In this simple experiment, a fixation cross is displayed on the screen. A white box also appears in the top right corner to serve as a light trigger for a photodiode.

```{code-block} python
:caption: Setting up the experiment

# Set up the PsychoPy Window and Stimuli
win = visual.Window([800, 600], monitor="testMonitor", units="pix", color="gray")
win_width, win_height = win.size
# Rectangle to represent the trigger light
rect_size = (100, 100)
top_right_x = (win_width / 2) - (rect_size[0] / 2)
top_right_y = (win_height / 2) - (rect_size[1] / 2)
top_right_pos = (top_right_x, top_right_y)
lightTrig = visual.Rect(win, size=rect_size, fillColor="white", pos=top_right_pos)

fixation = visual.TextStim(win, text="+") # Fixation cross
```

## Sending the Signal

* In this example, you will see a cross flash on the screen five times. Every time the cross flashes, the device sends a signal through the serial port.

* Watch the screen: a cross will flash 5 times. A signal is sent out the serial port upon each flash.

```{code-block} python
:caption: Sending the signal

for trial in range(5):
    fixation.draw()
    # Show the stimulus and send the marker almost simultaneously
    win.callOnFlip(port.write,  bytes(chr(Trigger), 'utf-8'))
    win.flip()
    core.wait(1.0) # fixation appears for 1 second

    # wait for 2s
    win.callOnFlip(port.write,  bytes(chr(0), 'utf-8'))
    win.flip()
    core.wait(2.0) 

# Cleanup
port.write(bytes(chr(0), 'utf-8'))  # Reset the trigger
win.close()
core.quit()
port.close()
```

### Write to Port (```win.callOnFlip()```)

This function will call a function immediately after the next win.flip() command.
The first argument should be the function to call, followed by the args exactly as you would for your normal call to the function.

## Resource

For more in-depth documentation and API reference, please refer to:

* [psychopy-serial-port](https://www.psychopy.org/hardware/serialPortInstr.html)
