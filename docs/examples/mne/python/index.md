# MNE-Python

MNE-Python is an open-source Python package for exploring, visualizing, and analyzing human neurophysiological data. Use it to perform offline analysis of recordings from your Wearable Sensing DSI-24, DSI-VR300, DSI-7, or DSI-Flex headsets.

```{admonition} Installation Required
:class: note
Before starting, install MNE-Python following the [official installation guide](https://mne.tools/stable/install/index.html). These tutorials use MNE version 1.9.0 and demonstrate workflows with Wearable Sensing EDF files exported from DSI-Streamer.
```
---

## Getting Started

Learn how to work with Wearable Sensing EEG data in MNE-Python through step-by-step tutorials covering data loading, preprocessing, and analysis.

---

### Quick Navigation

````{grid} 2
:gutter: 3

```{grid-item-card} Core Operations
:link: core/load
:link-type: doc
:text-align: center
---
Load data and configure channels
```

```{grid-item-card} Data Processing
:link: processing/filter
:link-type: doc
:text-align: center
---
Filter, clean, and epoch your data
```

````

---

## Tutorial Sections

The tutorials are organized into two main sections: Core Operations and Data Processing.

(core-operations)=
### Core Operations

```{admonition} Start Here
:class: tip
Begin with loading your data, then configure channels and references for analysis.
```

- {doc}`core/load` - Load EDF files from DSI-Streamer
- {doc}`core/channels` - Set channel types, manage selections, and configure referencing

---
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


## Resources

- [MNE Documentation](https://mne.tools/stable/documentation/index.html) | [Tutorials](https://mne.tools/stable/auto_tutorials/index.html) | [GitHub](https://github.com/mne-tools/mne-python)
- {doc}`MNE-LSL <../lsl/index>` | {doc}`MNELAB <../mnelab/index>` | {doc}`EEGLAB <../../eeglab/index>` | [MNE Forum](https://mne.discourse.group/)



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