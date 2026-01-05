# GUI Guide
---

To import data from DSI-Streamer into EEGLab:

1. Launch EEGLab in MATLAB.
2. Navigate to: **File → Import Data → Using EEGLAB functions and plugins → From WearableSensing CSV files**

## Import Configuration

The import dialog allows you to customize how the data is loaded and pre-processed.

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| **Channels** | Array or List | All | Specific channels to import. Enter as a space-separated list (e.g., `1 2 3`) or MATLAB vector (e.g., `[1:10]`). Leave empty to import all. |
| **Data Range** | [Min Max] | All | Time range in seconds to crop the file. Enter `[Start End]` (e.g., `[0 60]`). Leave empty for full file. |
| **Highpass Filter** | Float (Hz) | 0.1 | Lower cutoff frequency for FIR filter. Removes slow drifts. |
| **Lowpass Filter** | Float (Hz) | 70.0 | Upper cutoff frequency for FIR filter. Removes high-frequency noise. |
| **Reference** | Option | Linked Ears | **Linked Ears** (Standard) or **Hardware Reference**. See details below. |
| **Import Triggers**| Checkbox | Checked | Imports digital triggers from the data stream as EEGLab events. |
| **Remove Aux** | Checkbox | Checked | Removes DSI-24 auxiliary channels (X1-X3) used for external sensors (ECG, EMG, etc.). Uncheck to keep them. |


### Reference Details

The plugin offers two reference schemes. **Linked Ears** is the most common choice for DSI systems.

```{admonition} Linked Ears vs. Hardware Reference
:class: tip

**Linked Ears (Recommended)**
Re-references the data to the average of the ear clips (A1/A2) or the LE sensor.
- **Advantages**: Symmetrical reference that avoids lateral bias; standard for most ERP and quantitative EEG analysis.

**Hardware Reference**
Keeps the data referenced exactly as it was recorded.
- **Reference Location**: Pz (DSI-24/DSI-7), P4 (VR300), or Variable (DSI-Flex).
- **Use Case**: Choose this if you plan to perform your own re-referencing pipeline later or specifically require the hardware reference.
```

---

## Batch Import

You can streamline your workflow by importing multiple recordings at once.

1. In the file selection dialog, hold **Ctrl** (Windows) or **Cmd** (Mac) to select multiple `.csv` files.
2. The plugin will validate that all selected files are compatible DSI-Streamer recordings.
3. The import settings (filters, reference) configured above will be applied **identically** to every file.
4. Each file is loaded as a separate, named dataset in the EEGLab workspace.

```{admonition} Batch Processing Tip
:class: note
Batch import via the GUI is perfect for loading a session's worth of data (e.g., 5-10 files). for very large datasets (100+ files), consider using a [script-based approach](../scripting/index) to avoid running out of memory.
```


