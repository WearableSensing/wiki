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

If you have any issues running the GUI please refer to {doc}`How to Use <gui>`.

### 2. Run the Recording Script

Make sure you virtual environment is active, then run the following in your terminal alongside your active LSL stream:

```sh
python tools/consume/receive.py
```

If the script was ran successfully, you should see a **.csv** file saved to your specified path.

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

Client Arguments that you can write in the terminal, without having to manually edit the code.

## Example

```sh
python tools/consume/receive.py --output='./thisFolder' --stream='aStreamName' --duration=2
```

This script will record a stream named **'aStreamName'** and save it to the path **'./thisFolder'** recording 2 seconds.
