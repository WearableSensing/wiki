# MNE Integration
---

MNE is a comprehensive ecosystem for working with neurophysiological data. Use these integrations to analyze EEG data from Wearable Sensing devices with powerful Python tools.


## Getting Started

```{admonition} Installation Required
:class: note
Each integration requires separate installation. Click on the cards below to access detailed setup instructions and tutorials.
```

## Choose Your Integration

````{grid} 1 2 3 3
:gutter: 3

```{grid-item-card} MNE-Python
:link: python/index
:link-type: doc
:text-align: center

**Offline Analysis & Visualization**

Open-source Python package for exploring, visualizing, and analyzing EEG, MEG, sEEG, and ECoG data.

Perfect for: Post-processing, advanced analysis, research workflows
```

```{grid-item-card} MNE-LSL
:link: lsl/index
:link-type: doc
:text-align: center

**Real-Time Streaming & Processing**

Bridge between MNE-Python and Lab Streaming Layer for real-time data streaming and visualization.

Perfect for: Live monitoring, real-time analysis, BCI applications
```

```{grid-item-card} MNELAB
:link: mnelab/index
:link-type: doc
:text-align: center

**GUI-Based Analysis**

Graphical user interface for MNE-Python. Point-and-click workflows for EEG analysis without coding.

Perfect for: Visual workflows, EDF files, users new to Python
```

````

---

### What Can You Do?

**With MNE-Python:**
- Load and analyze EEG recordings
- Apply advanced preprocessing and filtering
- Perform time-frequency analysis and source localization
- Create publication-ready visualizations

**With MNE-LSL:**
- Stream data in real-time from Wearable Sensing devices
- Visualize EEG signals during data collection
- Monitor signal quality in real-time
- Implement online processing pipelines

**With MNELAB:**
- Open and visualize files through an intuitive GUI
- Apply filters and re-referencing with point-and-click
- Perform artifact rejection and ICA decomposition
- Export processed data for further analysis

---

## Additional Resources

**Official MNE Documentation:**
- [MNE-Python Documentation](https://mne.tools/stable/index.html)
- [MNE-LSL Documentation](https://mne.tools/mne-lsl/stable/index.html)
- [MNELAB Documentation](https://mnelab.readthedocs.io/)

**Related Integrations:**
- {doc}`LSL Integration <../lsl/index>` - Set up LSL streaming with Wearable Sensing devices

```{toctree}
:maxdepth: 3
:hidden:

MNE-Python <python/index>
MNE-LSL <lsl/index>
MNELAB <mnelab/index>
```
