# MNELAB
---

MNELAB is a graphical user interface (GUI) for [MNE-Python](https://mne.tools/stable/index.html) that provides an intuitive point-and-click interface for EEG/MEG analysis. While independent from the MNE-Python team, MNELAB is actively maintained, peer-reviewed ([JOSS publication](https://doi.org/10.21105/joss.04650)), and provides seamless integration with Wearable Sensing EDF files.


```{figure} ../../../_static/images/mne_lab.png
:alt: MNELAB GUI screenshot
:width: 75%

The MNELAB GUI displaying a loaded DSI-24 EEG recording.
```

## Installation

Download the latest standalone installer for your platform—no Python knowledge required:

- **[Download MNELAB](https://github.com/cbrnr/mnelab/releases)** (Windows & macOS)

## Getting Started

Learn how to work with Wearable Sensing data in MNELAB through step-by-step tutorials covering data loading, processing, and visualization.

```{admonition} Tutorial Roadmap
:class: note
**New to MNELAB?** Follow this sequence:
1. {doc}`Load Wearable Sensing Data <core/load>` - Export from DSI-Streamer and open in MNELAB
2. {doc}`Channel Configuration <core/channels>` - Set channel types and reference
3. {doc}`Filtering <processing/filter>` - Remove noise and artifacts
4. {doc}`Artifact Handling <processing/artifacts>` - Use ICA or manual rejection
5. {doc}`Epoching & Event Handling <processing/epochs>` - Analyze event-related data

**Already familiar?** Use Quick Navigation below to jump to specific topics.
```

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

Filter and preprocess signals
```

````
---

## Integration with MNE-Python

Files preprocessed in MNELAB can be loaded directly into MNE-Python for advanced analysis. It is recommended to save your processed data in the FIF format for compatibility.

```python
import mne

# Load file preprocessed in MNELAB
raw = mne.io.read_raw_fif('preprocessed_data.fif', preload=True)

# Continue with programmatic analysis
# Apply additional processing, source localization, connectivity analysis, etc.
```

---

## Additional Resources

### Official Documentation

- [MNELAB Documentation](https://mnelab.readthedocs.io/)
- [MNELAB GitHub Repository](https://github.com/cbrnr/mnelab)
- [MNELAB JOSS Paper](https://doi.org/10.21105/joss.04650)

### MNE Ecosystem

- [MNE-Python Documentation](https://mne.tools/stable/index.html)
- [MNE-Python Tutorials](https://mne.tools/stable/auto_tutorials/index.html)
- [MNE Forum](https://mne.discourse.group/)

### Related Wearable Sensing Tutorials

- [MNE-Python Integration](../python/index.md) - Programmatic analysis
- [MNE-LSL Integration](../lsl/index.md) - Real-time streaming
- [EEGLab Plugin](../../eeglab/index.md) - Alternative GUI-based workflow

---

```{admonition} Need Help?
:class: tip
- **MNELAB Issues:** [GitHub Issues](https://github.com/cbrnr/mnelab/issues)
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