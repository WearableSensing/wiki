# MNE-LSL Integration
---

MNE-LSL is a Python package that bridges MNE-Python and Lab Streaming Layer (LSL), enabling real-time streaming, visualization, and processing of EEG data. This integration allows you to monitor and analyze data as it's being recorded from your Wearable Sensing devices.

MNE-LSL enables you to:
- Stream data in real-time from Wearable Sensing devices via LSL
- Visualize EEG signals as they're being recorded
- Apply real-time preprocessing and filtering
- Monitor signal quality during data collection
- Implement real-time analysis pipelines


Install MNE-LSL following the [official installation guide](https://mne.tools/mne-lsl/stable/resources/install.html). MNE-LSL requires the liblsl library. Follow their instructions to install it on your system or install pylsl via pip: `pip install pylsl`

---

## Getting Started

### Basic Workflow

1. **Start LSL streaming** from your Wearable Sensing device using `dsi2lslGUI` or similar tool. See our {doc}`LSL Integration <../lsl/index>` guide for more instructions.
2. **Connect to the stream** using MNE-LSL
3. **Visualize and process** data in real-time
4. **Record or analyze** as needed

---

### Quick Example

```python
from mne_lsl.stream_viewer import StreamViewer

# The viewer will open showing your real-time EEG data, similar to the figure below.
stream_name = "YourStreamName"  # Replace with your stream name (e.g., "WS-default", "DSI-24", "DSI-VR300")
stream_viewer = StreamViewer(stream_name=stream_name)
stream_viewer.start()
```

The image below shows an LSL connection streaming data from a DSI-VR300 device with real-time visualization of eyes-closed alpha activity.

```{figure} ../../_static/images/mne-lsl/mne_lsl_vr_300.png
:alt: MNE-LSL streaming from DSI-VR300 showing eyes-closed alpha activity
:width: 100%

Real-time LSL streaming with MNE-LSL viewer displaying eyes-closed alpha activity from a DSI-VR300 headset.
```

---

### Access data in real-time

After connecting to an LSL stream, you can access the stream info, channel types, and real-time data as shown in the example below.

```python
from mne_lsl.stream import StreamLSL as Stream

# Connect to the LSL stream
source_id = "YourStreamName"  # Replace with your stream name
bufsize = 10  # Buffer size in seconds
stream = Stream(bufsize=bufsize, source_id=source_id).connect()

# Access the stream info
stream_info = stream.info
print(stream_info)

# Access the channel types. You can select unique types or channels using .pick().
channel_types = stream.get_channel_types(unique=True)
print(channel_types)

# Access data in real-time
winsize = stream.n_new_samples / stream.info["sfreq"]

# Retrieve data from the stream
picks = ("Fz", "Oz")  # Example channel picks
data, ts = stream.get_data(winsize, picks=picks)

# Disconnect from the stream when done
stream.disconnect()
```
See the MNE-LSL tutorials for more examples on real-time processing and visualization: [MNE-LSL Tutorials](https://mne.tools/mne-lsl/stable/generated/tutorials/index.html)

---

## Additional Resources

**Official MNE-LSL Documentation:**
- [MNE-LSL Documentation](https://mne.tools/mne-lsl/stable/index.html)
- [MNE-LSL Tutorials](https://mne.tools/mne-lsl/stable/generated/tutorials/index.html)
- [MNE-LSL Examples](https://mne.tools/mne-lsl/stable/generated/examples/index.html) * this shows real time analysis examples *
- [MNE-LSL GitHub Repository](https://github.com/mne-tools/mne-lsl)
- [Lab Streaming Layer](https://labstreaminglayer.readthedocs.io/)

**Related Pages:**
- {doc}`LSL Integration <../lsl/index>` - Set up LSL streaming with Wearable Sensing devices
- {doc}`MNE-Python Integration <../mne/index>` - Analysis with MNE-Python
