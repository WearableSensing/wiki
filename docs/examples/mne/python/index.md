# MNE-Python Integration
---

MNE-Python is an open-source Python package for exploring, visualizing, and analyzing human neurophysiological data such as MEG, EEG, sEEG, ECoG, and more.

```{admonition} Installation Required
:class: note
Before starting, install MNE-Python following the [official installation guide](https://mne.tools/stable/install/index.html). These tutorials use MNE version 1.9.0.
```

## Getting Started

Learn how to work with Wearable Sensing data in MNE-Python through step-by-step tutorials covering data loading, processing, and visualization.

### Quick Navigation

````{grid} 2
:gutter: 3

```{grid-item-card} Core Operations
:link: core/load
:link-type: doc
:text-align: center

Load data and configure channels
```

```{grid-item-card} Data Processing
:link: processing/filter
:link-type: doc
:text-align: center

Filter, clean, and epoch your data
```

````

---

## Tutorial Sections

(core-operations)=
### Core Operations

```{admonition} Start Here
:class: tip
Begin with loading your data, then configure channels and references for analysis.
```

- {doc}`core/load` - Load EDF files from DSI-Streamer
- {doc}`core/channels` - Set channel types, manage selections, and configure referencing

(data-processing)=
### Data Processing

```{admonition} Preprocessing Pipeline
:class: note
Follow these tutorials in sequence for a complete preprocessing workflow:
1. **Filter** - Remove noise and isolate frequency bands
2. **Artifacts** - Clean data using ICA and rejection methods
3. **Epochs** - Extract event-related segments for analysis
```

- {doc}`processing/filter` - Apply frequency filters and resampling
- {doc}`processing/artifacts` - Remove artifacts with ICA and rejection
- {doc}`processing/epochs` - Create epochs and compute ERPs

---


## Additional Resources

**Official MNE Documentation:**
- [MNE GitHub Repository](https://github.com/mne-tools/mne-python)
- [MNE Documentation](https://mne.tools/stable/documentation/index.html)
- [MNE Tutorials](https://mne.tools/stable/auto_tutorials/index.html)

### Related Wearable Sensing Tutorials

- [MNE-LSL Integration](../lsl/index.md) - Real-time streaming
- [MNELAB Integration](../mnelab/index.md) - GUI-based analysis
- [EEGLab Plugin](../../eeglab/index.md) - Alternative GUI-based workflow



```{admonition} Need Help?
:class: tip
- **MNE Community:** [MNE Forum](https://mne.discourse.group/)
- **Wearable Sensing Support:** [Contact Support](../../../help/index.md)
```

```{toctree}
:maxdepth: 2
:hidden:
:caption: Core Operations

core/load
core/channels
```

```{toctree}
:maxdepth: 2
:hidden:
:caption: Data Processing

processing/filter
processing/artifacts
processing/epochs
```