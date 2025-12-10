# MNE Integration
---

MNE is a comprehensive ecosystem for working with neurophysiological data. Use these integrations to analyze EEG data from Wearable Sensing devices with powerful Python tools.

## Choose Your Integration

````{grid} 1 2 2 2
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

````

---

## Getting Started

```{admonition} Installation Required
:class: note
Each integration requires separate installation. Click on the cards above to access detailed setup instructions and tutorials.
```

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

---

## Additional Resources

**Official MNE Documentation:**
- [MNE-Python Documentation](https://mne.tools/stable/index.html)
- [MNE-LSL Documentation](https://mne.tools/mne-lsl/stable/index.html)

**Related Integrations:**
- {doc}`LSL Integration <../lsl/index>` - Set up LSL streaming with Wearable Sensing devices

```{toctree}
:maxdepth: 1
:hidden:

MNE-Python <python/index>
MNE-LSL <lsl/index>
```
