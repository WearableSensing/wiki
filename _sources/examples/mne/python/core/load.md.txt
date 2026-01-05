# Load Wearable Sensing Data
---

This will be a guide on loading Wearable Sensing data using MNE-Python.

```{admonition} Experiment
:class: note
The data were collected using a DSI-24 at a sampling rate of 300Hz. There were two conditions in which the user was asked to close and open their eyes.
```

## Example Data
---

To follow along with this tutorial, you can download a sample data file from this [dropbox](https://www.dropbox.com/scl/fi/n1yhaco7fy397pu69l14u/Sample_DSI_24_Eyes_Closed.edf?rlkey=2vco7a100hhevg86i6vol1nmx&e=1&dl=0).

## Import using MNE
---

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

```{Admonition} Preload option
:class: hint
The `preload=True` option loads the data into memory, allowing for faster access and manipulation. By default, MNE does not preload the data, which means it will read the data from disk each time you access it.
```

---

## Next Steps

After loading your data:
1. {doc}`Configure channels and references <channels>` - Set channel types and re-reference
2. {doc}`Filter your data <../processing/filter>` - Remove noise and isolate frequency bands
3. {doc}`Remove artifacts <../processing/artifacts>` - Clean data using ICA
4. {doc}`Create epochs <../processing/epochs>` - Extract event-related segments

---

## Resources

For more in-depth documentation and API reference, please refer to: ([mne.io.read_raw_edf](https://mne.tools/stable/generated/mne.io.read_raw_edf.html))
