# LSL-Tools

Wearable Sensing has created some tools that can work with LabStreamingLayer. You can find them at Wearable Sensing's [github](https://github.com/WearableSensing/lsl-tools).

## Recording Data from DSI2LSL

1. Start ```dsi2lslGUI```
2. While ```dsi2lslGUI``` is running, execute the ```receive.py``` script.

This will create a ```.csv``` file with the data received from the headset.

```{admonition} Note
:class: note
There are program requirements to run ```receive.py```, they can be found in the README of [```lsl-tools```](https://github.com/WearableSensing/lsl-tools).
```

```{code-block} sh
:caption: Terminal Usage and Examples
Usage: 
       --output
          The path where data should be written to (default: '.').
       --stream
          The stream name configured in the LSL app (default: 'WS-default').
       --duration
          The duration in seconds for the data collection to run (default: 10).
Example:
        python receive.py --output='./thisFolder' --stream='aStreamName' --duration=2
        python receive.py --duration=5
```
