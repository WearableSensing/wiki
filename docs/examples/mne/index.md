# MNE-Python Integration

MNE-Python is an open-source Python package for exploring, visualizing, and analyzing human neurophysiological data such as MEG, EEG, sEEG, ECoG, and more.

```{admonition} Installation Required
:class: note
Before starting, install MNE-Python following the [official installation guide](https://mne.tools/stable/install/index.html). These tutorials use MNE version 1.9.0.
```

---

## Getting Started

Learn how to work with Wearable Sensing data in MNE-Python through step-by-step tutorials covering data loading, processing, and visualization.

### Quick Navigation

````{grid} 2
:gutter: 3

```{grid-item-card} General
:link: core/load
:link-type: doc
:text-align: center

Load data and configure channels
```

```{grid-item-card} Processing
:link: processing/filter
:link-type: doc
:text-align: center

Filter and preprocess signals
```

````

---

(core-operations)=
## General

```{toctree}
:maxdepth: 1

Load Wearable Sensing Data <core/load>
Update Channel Information <core/update_channel>
Update Reference Channel <core/update_ref>
```

(data-processing)=
## Data Processing

```{toctree}
:maxdepth: 1

Filtering Data <processing/filter>
```

---

## Additional Resources

**Official MNE Documentation:**
- [MNE GitHub Repository](https://github.com/mne-tools/mne-python)
- [MNE Documentation](https://mne.tools/stable/documentation/index.html)
- [MNE Tutorials](https://mne.tools/stable/auto_tutorials/index.html)
