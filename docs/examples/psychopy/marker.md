# Marker

```{admonition} LSL
:class: sidebar note
The following tutorials will use pylsl in pair with PsychoPy
```

This tutorial explains how to send digital event markers from PsychoPy into an EEG data stream. Sending these markers is the essential step for accurately synchronizing your stimuli with the recorded neural data.

## Setting up the Stream

The script below creates a basic LSL outlet stream, which serves as a simple example. For a real EEG experiment, this PsychoPy marker stream is intended to be recorded simultaneously alongside the separate data stream coming from your EEG amplifier. LSL automatically time-synchronizes both streams, allowing you to perfectly align your stimulus events with the neural data during analysis. You will require additional tools to record the data.

```{code-block} python
:caption: Creating a lsl outlet
from psychopy import visual, core
from pylsl import StreamInfo, StreamOutlet

marker_stream_info = StreamInfo(
    name='PsychoPyMarkers',
    type='Markers',
    channel_count=1,          # Number of channels (1 for a single marker stream)
    nominal_srate=0,          # The rate is irregular, so we set it to 0
    channel_format='int32',   # Data type of the markers
    source_id='some_id_12345' # A unique identifier
)

# Naming the channel
description = marker_stream_info.desc()
channels_node = description.append_child("channels")
ch_node = channels_node.append_child("channel")
ch_node.append_child_value("label", "EventMarker")

# Create the stream outlet
outlet = StreamOutlet(marker_stream_info)
```

## Sending Markers

This example runs a simple experiment that displays a fixation cross five times, each for one second. A corresponding marker is sent to the LSL outlet every time the fixation appears on screen. The ```win.flip()``` command is the precise moment the visual stimulus is displayed. By immediately pushing the marker with ```outlet.push_sample()```, you ensure that the marker's high-precision LSL timestamp is as close as possible to the actual time of the visual event.

```{code-block} python
:caption: Sending Markers
# Set up the PsychoPy Window and Stimuli
win = visual.Window([800, 600], monitor="testMonitor", units="pix", color="gray")
fixation = visual.TextStim(win, text="+")

# Example Trial Loop (runs 5 times) 
for trial in range(5):
    fixation.draw()
    # Show the stimulus and send the marker almost simultaneously
    win.flip()
    outlet.push_sample([trial + 1]) # Send marker (e.g., 1 for trial 1, 2 for trial 2, etc.)
    core.wait(1.0) # fixation appears for 1 second

    # wait for 2s
    win.flip()
    core.wait(2.0) 

win.close()
core.quit()
```

```{admonition} Consumed Data
:class: sidebar note
:wifth: 75%
The image on the left is the recorded data using {doc}`LSL-Tools <tools>`. From this image, you can see the EventMarker channel defined in the code above, and the markers that got sent to the channels at there according time, around 3 seconds apart, 1 for the fixation, and the 2 idle time. 
```

```{image} ../../_static/psychopy-mark.png
:width: 50%
```

## Resources

* [pylsl](https://github.com/labstreaminglayer/pylsl)
