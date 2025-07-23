# LSL-Tools

Wearable Sensing has created some tools that can work with LabStreamingLayer. You can find them at Wearable Sensing's [github](https://github.com/WearableSensing/lsl-tools).

This tool utilizes the ```pylsl``` interface to accomplish its task. For further information regarding ```pylsl``` please visit their official [page](https://github.com/labstreaminglayer/pylsl).

## Recording Data from DSI2LSL

```{admonition} Note
:class: attention
The recording script, ```receive.py```, is compatible with any modern version of Python (3.8+).

This documentation only offers a brief decription on how to use this tool, please refer to [```lsl-tools```](https://github.com/WearableSensing/lsl-tools) for more descriptive information.
```

### 1. Start the LSL Stream

Ensure your Wearable Sensing device is properly connected to your computer.

* Launch the ```dsi2lslGUI``` application to begin streaming EEG data using LabStreamingLayer:
* If you have any issue with this please refer to {doc}`How to Use <gui>`

### 2. Run the Recording Script

```{admonition} Note
:class: note
Make sure your virtual environment is active
```

Run the following in your terminal while your LSL stream is running:

```sh
python tools/consume/receive.py
```

If the script was ran successfully, you should see a .csv file saved to your specified path.

```{code-block} text
:caption: Client Arguments
Usage: 
       --output
          The path where data should be written to (default: '.').
       --stream
          The stream name configured in the LSL app (default: 'WS-default').
       --duration
          The duration in seconds for the data collection to run (default: 10).
```

```{code-block} sh
:caption: Example
python tools/consume/receive.py --output='./thisFolder' --stream='aStreamName' --duration=2
```

For the example above, the script will record a stream named 'aStreamName' and save it to the path './thisFolder' recording 2 seconds.

```{admonition} Note
:class: tip
You can exclude certain Client Argument to use their default values. 
```
