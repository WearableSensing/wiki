# Stream Viewer

Visualize real-time EEG data from Wearable Sensing devices using MNE-LSL's StreamViewer.

---

## Launch LSL Stream Viewer

```{figure} ../../../../_static/images/examples/mne/mne_lsl_vr_300.png
:alt: MNE-LSL StreamViewer
:width: 100%

StreamViewer displaying real-time EEG with eyes-closed alpha activity.
```

Once your LSL stream is running (see {doc}`LSL Setup <../../../lsl/index>`), use the following code with the stream name to start StreamViewer and visualize the data in real-time:

```{code-block} python
:caption: Launch StreamViewer for real-time DSI visualization

from mne_lsl.stream_viewer import StreamViewer

stream_name = "WS-default"  # Or DSI-24, DSI-VR300, WS-default

viewer = StreamViewer(stream_name=stream_name)
viewer.start()
```

```{admonition} Finding Your Stream Name
:class: tip
If unsure of your stream name, check the LSL GUI or use {doc}`stream discovery <../processing/connect>` to list available streams.
```

---

## Customize the Viewer by Channel and Duration

Channel selection and time window duration are adjusted interactively through the StreamViewer GUI after launch. There are no constructor parameters for these in v1.12.0.

---

## View Filtered Streams from StreamLSL

```{admonition} Note
:class: note
In mne-lsl 1.12.0, `StreamViewer` connects directly to a raw LSL stream by name. It does not accept a pre-filtered `StreamLSL` object. For filtered visualization, apply filters via {doc}`StreamLSL <../processing/filter>` and retrieve data with `get_data()` to plot with your preferred plotting library.
```

To use `StreamLSL` for filtered data processing alongside the viewer, run them as separate scripts or processes — `StreamViewer.start()` is blocking and calls `sys.exit()` when the window closes, so code after it will not execute.

```{code-block} python
:caption: Script 1 — Filtered data acquisition with StreamLSL

from mne_lsl.stream import StreamLSL
import time

stream_name = "WS-default"  # Change to your stream name
stream = StreamLSL(bufsize=10, name=stream_name).connect()
stream.filter(l_freq=1.0, h_freq=40.0)
stream.notch_filter(freqs=60.0)

# Process filtered data here
while True:
    data, ts = stream.get_data(winsize=1.0)
    time.sleep(0.1)
```

```{code-block} python
:caption: Script 2 — StreamViewer for raw stream monitoring (run separately)

from mne_lsl.stream_viewer import StreamViewer

stream_name = "WS-default"  # Change to your stream name
viewer = StreamViewer(stream_name=stream_name)
viewer.start()  # Blocking — exits the process when window closes
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

**Window won't open:** See {doc}`Installation <../index>` and ensure dependencies are met.

**Choppy display:** Reduce window duration or number of channels. 

**No signal:** Check stream is running and accessible.

---

## Resources

- [StreamViewer API](https://mne.tools/mne-lsl/stable/generated/api/mne_lsl.stream_viewer.StreamViewer.html#mne_lsl.stream_viewer.StreamViewer)
- {doc}`Stream Connection <../processing/connect>` | {doc}`Filtering <../processing/filter>`
