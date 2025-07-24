# Load Wearable Sensing Data

This will be a guide on loading Wearable Sensing data using MNE-Python.

```{admonition} Experiment
:class: sidebar note
The data were collected using a DSI-24 at a sampling rate of 300Hz. There were two conditions in which the user was asked to close and open their eyes.
```

## Example Data

To follow along with this tutorial, you can download a sample data file from this [dropbox](https://www.dropbox.com/scl/fi/n1yhaco7fy397pu69l14u/Sample_DSI_24_Eyes_Closed.edf?rlkey=2vco7a100hhevg86i6vol1nmx&e=1&dl=0).

## Import using MNE

```{code-block} python
:caption: Load Wearable Sensing EDF
import mne

# Define the file path of the EDF file on you computer
edf_file_path = 'Sample_DSI_24_Eyes_Closed.edf'

# Load data with mne
wearable_sensing_data = mne.io.read_raw_edf(edf_file_path, preload = True)
```

`mne.io.read_raw_edf()` is designed by the MNE-Python library to read data from EDF files. When this EDF file is read, we capture the data and create a raw object that holds not only the actual EEG data, but all the relevant metadata. This includes:

* Channel Names

* Channel Types

* Sampling Frequency

* Event Markers

* And lots more!

## Resources

For more in-depth documentation and API reference, please refer to: ([mne.io.read_raw_edf](https://mne.tools/stable/generated/mne.io.read_raw_edf.html))
