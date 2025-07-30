# Sending Triggers Through a Serial Port

As an alternative to network-based synchronization like LSL, you can send triggers directly to your EEG hardware for precise event marking. This method uses your computer's serial port to transmit a signal from PsychoPy to a trigger hub that connects to the EEG Headset. This tutorial provides a simple explaination on how to send these hardware triggers.

## Connecting

```{code-block} python
:caption: Connecting the port

from psychopy import visual, core
import serial

port = serial.Serial('COM10') #Change the COM port to match your setup

# Set up the PsychoPy Window and Stimuli
win = visual.Window([800, 600], monitor="testMonitor", units="pix", color="gray")
fixation = visual.TextStim(win, text="+")
Trigger = 1 # trigger code must be between 1-255 
```

```{admonition} Trigger Value
:class: note
If you are using multiple triggers on the trigger hub, then you need to set the Trigger value to one that is not being used. 
```

## Sending

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

* [psychopy-serial-port](https://www.psychopy.org/hardware/serialPortInstr.html)