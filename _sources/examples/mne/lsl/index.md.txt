# MNE-LSL Integration

```{admonition} Version
:class: note
This wiki section was written for **mne-lsl 1.12.0**.
```

MNE-LSL is a Python package that bridges MNE-Python with the Lab Streaming Layer (LSL) for real-time EEG data streaming, processing, and visualization.

```{figure} ../../../_static/images/examples/mne/mne_lsl_vr_300.png
:alt: MNE-LSL StreamViewer
:width: 75%

StreamViewer displaying real-time EEG with eyes-closed alpha activity.
```

---

## Installation

- **[Installation Guide](https://mne.tools/mne-lsl/stable/resources/install.html)** - Full documentation with dependencies and troubleshooting

Install MNE-LSL using pip:

```bash
pip install mne-lsl
```

For real-time visualization with StreamViewer, install with Qt backend:

```bash
pip install mne-lsl PyQt5
```

---

## Quick Navigation

````{grid} 3
:gutter: 3

```{grid-item-card} Processing
:link: processing/connect
:link-type: doc
:text-align: center
---
Connect, filter, and epoch streams
```

```{grid-item-card} Classification
:link: classification/bci
:link-type: doc
:text-align: center
---
Build closed-loop BCIs
```

```{grid-item-card} Visualization
:link: visualization/viewer
:link-type: doc
:text-align: center
---
Real-time EEG monitoring
```

````

---

## Quick Examples

**View real-time data from your Wearable Sensing headset:**
```{code-block} python
:caption: Launch StreamViewer for real-time monitoring

from mne_lsl.stream_viewer import StreamViewer

stream_name = "DSI-24"  # Or DSI-VR300, DSI-7, WS-default
StreamViewer(stream_name=stream_name).start()
```

**Replay pre-recorded data**

This example replays data from an EDF file, such as those exported by DSI-Streamer, as an LSL stream for testing:

```{code-block} python
:caption: Replay EDF file as LSL stream for testing

import time
from mne.io import read_raw_edf
from mne_lsl.player import PlayerLSL as Player

path_to_edf = "C:/path/to/your/data.edf"  # Replace with your EDF file path
raw = read_raw_edf(path_to_edf, preload=True)
player = Player(raw, chunk_size=200, n_repeat=1, name="example-edf-replay").start()

while player.running:
    time.sleep(0.5)

del player
``` 

---

## Tutorial Sections

### Processing

- {doc}`processing/connect` - Discover and connect to LSL streams
- {doc}`processing/filter` - Apply real-time filters
- {doc}`processing/epochs` - Create event-related epochs

### Classification

- {doc}`classification/bci` - Build BCIs with bandpower and machine learning

### Visualization

- {doc}`visualization/viewer` - StreamViewer for real-time monitoring

---

## Resources

- [MNE-LSL Docs](https://mne.tools/mne-lsl/stable/) | [Tutorials](https://mne.tools/mne-lsl/stable/generated/tutorials/index.html) | [Examples](https://mne.tools/mne-lsl/stable/generated/examples/index.html)
- {doc}`LSL Setup <../../lsl/index>` | {doc}`MNE-Python <../python/index>` | [MNE Forum](https://mne.discourse.group/)

```{toctree}
:maxdepth: 2
:hidden:
:caption: Processing

processing/connect
processing/filter
processing/epochs
```

```{toctree}
:maxdepth: 2
:hidden:
:caption: Visualization

visualization/viewer
```

```{toctree}
:maxdepth: 2
:hidden:
:caption: Classification

classification/bci
```