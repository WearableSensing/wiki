# Connect a Device

Discover and connect to LSL streams from your Wearable Sensing DSI-24, DSI-VR300, or DSI-7 headset.

```{admonition} Prerequisites
:class: note
- MNE-LSL installed (see {doc}`Installation <../index>`)
- LSL stream running from your Wearable Sensing device (see {doc}`LSL Setup <../../../../lsl/index>`)
```

## Key Concepts

- **Stream Name:** Device identifier (e.g., "DSI-24", "DSI-VR300", "WS-default")
- **Buffer Size:** Seconds of historical data to keep in memory (default: 10s)

---

## Discovering Streams

Before connecting to a specific stream, you can discover what LSL streams are available on your network. This is useful when you're unsure of the stream name or want to verify your device is broadcasting.

```{code-block} python
:caption: Discover available LSL streams on the network

from mne_lsl.lsl import resolve_streams

# Find all streams
streams = resolve_streams()
print(f"Found {len(streams)} stream(s):")
for stream in streams:
    print(f"  - {stream.name} ({stream.stype}) @ {stream.sfreq} Hz")

# Or filter by name/type
eeg_streams = resolve_streams(timeout=5.0, stype='EEG')
print(f"\nFound {len(eeg_streams)} EEG stream(s)")

dsi_stream = resolve_streams(timeout=5.0, name='DSI-24')
if dsi_stream:
    print(f"\nFound DSI-24 stream: {dsi_stream[0].name}")
```

```{admonition} Troubleshooting Stream Discovery
:class: tip
If no streams are found:
1. Ensure your Wearable Sensing device is streaming via LSL (check `dsi2lslGUI` or equivalent)
2. Check firewall settings - LSL uses UDP multicast
3. Verify devices are on the same network
4. Increase the timeout parameter
```

---

## Connecting to a Stream by Name

Once you know your stream name, create a `StreamLSL` object to connect and start buffering data. The buffer stores recent data in memory for retrieval.

```{code-block} python
:caption: Connect to a stream by name and start buffering

from mne_lsl.stream import StreamLSL

stream_name = "DSI-24"  # Example: DSI-24, DSI-VR300, WS-default

# Connect to stream
stream = StreamLSL(bufsize=10, name=stream_name).connect()

print(f"Connected: {stream.info['name']} @ {stream.info['sfreq']} Hz")
print(f"Channels: {len(stream.ch_names)}")
```

**Parameters:**
- `bufsize`: Seconds of data to buffer (default: 10)
- `name`: Stream name, or use `source_id` for unique identification

---

## Accessing Stream Information

After connecting, the stream's `info` object provides metadata about your device including sampling rate, channel names, and channel types. This information is essential for processing and analysis.

```{code-block} python
:caption: Access stream metadata and information

# Get stream metadata
info = stream.info
print(f"Device name: {info['name']}")
print(f"Sampling frequency: {info['sfreq']} Hz")
print(f"Number of channels: {info['nchan']}")
print(f"Channel names: {info['ch_names']}")

# Get channel types
channel_types = stream.get_channel_types()
print(f"Channel types: {set(channel_types)}")

# Check buffer status
n_samples = stream.n_buffer
print(f"Samples in buffer: {n_samples}")
```

---

## Retrieving Data

The `get_data()` method retrieves data from the buffer. You can request a specific time window, select channels, or get only new samples since the last call.

```{code-block} python
:caption: Retrieve data from stream buffer

# Get recent data
data, timestamps = stream.get_data(winsize=2.0)  # Last 2 seconds

# Get from specific channels
data, ts = stream.get_data(winsize=2.0, picks=['Fz', 'Cz', 'Pz'])

# Get only new samples
n_new = stream.n_new_samples
if n_new > 0:
    data, ts = stream.get_data(n_new / stream.info['sfreq'])
```

---

## Continuous Acquisition Example

This example demonstrates a continuous acquisition loop that processes new data as it arrives. This pattern is common for real-time applications like BCIs and monitoring systems.

```{code-block} python
:caption: Continuous real-time data acquisition loop

from mne_lsl.stream import StreamLSL
import time

stream = StreamLSL(bufsize=10, name="DSI-24").connect()
time.sleep(2)

try:
    while True:
        n_new = stream.n_new_samples
        if n_new > 0:
            data, ts = stream.get_data(n_new / stream.info['sfreq'])
            print(f"Received {n_new} samples")
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Stopping acquisition")
finally:
    stream.disconnect()
```

---

## Next Steps

Now that you know how to connect to streams:
1. {doc}`Visualize data in real-time <../visualization/viewer>` - Use StreamViewer for live monitoring
2. {doc}`Apply real-time filtering <filter>` - Clean data as it arrives
3. {doc}`Create epochs <epochs>` - Extract event-related data
4. {doc}`Build BCIs <../classification/bci>` - Develop neurofeedback and classification systems


## Resources

- [Stream API](https://mne.tools/mne-lsl/stable/generated/api/mne_lsl.stream.StreamLSL.html) | [MNE-LSL Tutorial](https://mne.tools/mne-lsl/stable/generated/tutorials/00_introduction.html)
- {doc}`LSL Setup <../../../../lsl/index>` | {doc}`Visualization <../visualization/viewer>`
