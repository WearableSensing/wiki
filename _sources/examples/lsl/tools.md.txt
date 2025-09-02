# LSL-Tools
--------------------------------------------------------------------------------------

Wearable Sensing has created some examples to demonstrate working with LabStreamingLayer. You can find them at Wearable Sensing's [github](https://github.com/WearableSensing/lsl-tools), where they are easy to clone and run.

## Recording Data from DSI2LSL
--------------------------------------------------------------------------------------

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

Make sure your virtual environment is active and dependencies are installed, then run the following in your terminal alongside your active LSL stream:

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

This allows you to edit you recording configurations without having to change the code.

## Example
--------------------------------------------------------------------------------------

```sh
python tools/consume/receive.py --output='./thisFolder' --stream='aStreamName' --duration=2
```

This script will record a stream named **'aStreamName'** and save it to the path **'./thisFolder'** recording **2** seconds. The default stream name is **'WS-default'** and the default output path is the current working directory. The default duration is **10** seconds.

## Resources
--------------------------------------------------------------------------------------

For additional information and comprehensive documentation about pylsl and LabStreamingLayer, please visit the following links:

* [pylsl-example-usage](https://github.com/labstreaminglayer/pylsl/tree/main/src/pylsl/examples)

* [pylsl-github](https://github.com/labstreaminglayer/pylsl)

* [labstreaminglayer-documentation](https://labstreaminglayer.readthedocs.io/)

* [labstreaminglayer-github](https://github.com/sccn/labstreaminglayer)
