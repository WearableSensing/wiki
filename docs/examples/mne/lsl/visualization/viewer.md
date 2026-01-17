# Stream Viewer
---

Visualize real-time EEG data from Wearable Sensing devices using MNE-LSL's StreamViewer.

## Launch LSL Stream Viewer
---

```{figure} ../../../../_static/images/mne-lsl/mne_lsl_vr_300.png
:alt: MNE-LSL StreamViewer
:width: 100%

StreamViewer displaying real-time EEG with eyes-closed alpha activity.
```

Once your LSL stream is running (see {doc}`LSL Setup <../../../../lsl/index>`), use the following code with the stream name to start StreamViewer and visualize the data in real-time:

```{code-block} python
:caption: Launch StreamViewer for real-time DSI visualization

from mne_lsl.stream import StreamViewer

stream_name = "WS-default"  # Common options: DSI-24, DSI-VR300, WS-default

viewer = StreamViewer(stream_name=stream_name)
viewer.start()
```

```{admonition} Finding Your Stream Name
:class: tip
If unsure of your stream name, check DSI-Streamer settings or use {doc}`stream discovery <../processing/connect>` to list available streams.
```

---

## Customize the Viewer by Channel and Duration

The StreamViewer can be customized to display specific channels and adjust the time window shown using the GUI tools, or programmatically as follows:

```{code-block} python
:caption: Customize StreamViewer with specific channels and time window

from mne_lsl.stream import StreamViewer

stream_name = "WS-default"  # Change to your stream name
viewer = StreamViewer(
    stream_name=stream_name,
    window_duration=10.0,  # Show 10 seconds
    picks=['Cz'],  # Specific channels
)
viewer.start()
```

---

## View Filtered Streams from StreamLSL

If you want to visualize filtered data, first create a `StreamLSL` object, apply filters, and then pass it to `StreamViewer`:

```{code-block} python
:caption: Visualize filtered streams in real-time

from mne_lsl.stream import StreamLSL, StreamViewer

stream_name = "WS-default"  # Change to your stream name

# Filter the stream using StreamLSL built in methods
stream = StreamLSL(bufsize=10, name=stream_name).connect()
stream.filter(l_freq=1.0, h_freq=40.0)
stream.notch_filter(freqs=60.0)

# Visualize the filtered stream
viewer = StreamViewer(stream=stream)
viewer.start()

stream.disconnect()
```

---

## Next Steps

Now that you can visualize your data in real-time:
1. {doc}`Apply filtering <../processing/filter>` - Clean signals and remove noise
2. {doc}`Create epochs <../processing/epochs>` - Extract event-related segments
3. {doc}`Build BCIs <../classification/bci>` - Develop neurofeedback and classification systems
4. {doc}`MNE-Python analysis <../../python/index>` - Offline analysis and advanced processing

---

## Troubleshooting

**Window won't open:** See {doc}`Installation <../index>` and ensure dependencies are met

**Choppy display:** Reduce window duration or number of channels  

**No signal:** Check stream is running and accessible

---

## Resources

- [StreamViewer API](https://mne.tools/mne-lsl/stable/generated/api/mne_lsl.stream.StreamViewer.html)
- {doc}`Stream Connection <../processing/connect>` | {doc}`Filtering <../processing/filter>`
