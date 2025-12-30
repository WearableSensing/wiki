# EEGLab
---

The Wearable Sensing EEGLab plugin allows you to import DSI-Streamer CSV files directly into EEGLab for advanced processing and analysis.

```{admonition} Download & Installation
:class: note

**Recommended: Install via EEGLab Plugin Manager**
1. Open EEGLab in MATLAB.
2. Navigate to **File → Manage EEGLAB extensions**.
3. Search for `WearableSensing` in the extension manager.
4. Click **Install/Update**.

**Alternative: Manual Download**
If you prefer to install manually, you can download the plugin directly:
[Download Plugin (v1.16)](https://wearablesensing.com/wp-content/uploads/2025/12/WearableSensing_1.16.zip)

**Manual Installation Steps:**
1. Locate your EEGLAB plugins directory: `/eeglab(VERSION)/plugins/`
2. Extract the `WearableSensing` folder from the .zip file into that directory.
3. Restart MATLAB and run EEGLAB.
```

## Key Features

- **Universal Compatibility**: Works with CSV files from any version of DSI-Streamer.
- **Automatic Headset Detection**: Supports DSI-7, DSI-24, DSI-Flex, and VR300.
- **Batch Import**: Select multiple files to process them all at once.
- **Filtering**: Option to apply FIR filters during import

## Important Considerations

To ensure accurate analysis, the plugin enforces specific data requirements:

- **Raw CSV Files Only**: The plugin is designed to import **raw, unfiltered data**. It will not accept files that have already been filtered or processed in DSI-Streamer (e.g., "Recorded by Montage" or "Filtered").
- **DSI-Streamer Format**: Files must be in the standard `.csv` export format from DSI-Streamer. Customized or manually edited CSVs may fail to load.

## Data Integrity Check

The plugin performs an automatic quality check during import to detect data loss.

```{admonition} Packet Loss Detection
:class: warning
If lost data is detected in the recording:
1. A **Data Integrity Report** will be displayed in the command window.
2. **Boundary Events** are inserted into the data at the exact location of the gap.
3. This ensures that downstream processing tools (like Artifact Subspace Reconstruction) treat the data as discontinuous, preventing artifacts from "smearing" across the gap.
```

## Documentation

````{grid} 2
:gutter: 3

```{grid-item-card} GUI Guide
:link: gui/index
:link-type: doc
:text-align: center

Step-by-step guide to using the import window
```

```{grid-item-card} Scripting & Command Line
:link: scripting/index
:link-type: doc
:text-align: center

Automate your analysis pipeline
```

````

```{toctree}
:maxdepth: 2
:hidden:

GUI Guide <gui/index>
Scripting & Command Line <scripting/index>
```
