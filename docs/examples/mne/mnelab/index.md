# MNELAB
---

MNELAB is a graphical user interface (GUI) for [MNE-Python](https://mne.tools/stable/index.html) that provides an intuitive point-and-click interface for EEG/MEG analysis. While independent from the MNE-Python team, MNELAB is actively maintained, peer-reviewed ([JOSS publication](https://doi.org/10.21105/joss.04650)), and provides seamless integration with Wearable Sensing EDF files.

```{admonition} What is MNELAB?
:class: tip
MNELAB makes MNE-Python's powerful analysis tools accessible through a user-friendly GUI. Perfect for users who prefer visual workflows or are new to Python-based EEG analysis.
```

## Installation

The easiest way to get started—no Python knowledge required:

- **Windows:** [MNELAB 1.0.8 Installer](https://github.com/cbrnr/mnelab/releases/download/v1.0.8/MNELAB-1.0.8.exe)
- **macOS:** [MNELAB 1.0.8 DMG](https://github.com/cbrnr/mnelab/releases/download/v1.0.8/MNELAB-1.0.8.dmg)

After installation, launch MNELAB like any other application from your applications menu.

---

## Working with Wearable Sensing Data

MNELAB can open EDF files exported from DSI-Streamer, making it easy to analyze recordings from DSI-7, DSI-24, DSI-VR300, and DSI-Flex headsets. In addition, MNELAB can read FIF files created from other MNE-Python workflows. See our [MNE-Python integration tutorial](../python/index.md) for more information.

### Exporting EDF from DSI-Streamer

Before using MNELAB, export your data from DSI-Streamer:

1. Open your recording in DSI-Streamer
2. Navigate to the **Record** tab
3. Select the **EDF** raw format checkbox
4. Under **Export Files** header, Click **Export**
5. Save your file (e.g., `recording.edf`) to the desired location using the file dialog window

```{admonition} EDF vs CSV
:class: note
MNELAB works best with EDF files, which preserve metadata like channel names, sampling rates, and sensor information. While CSV files can be imported into MNE-Python programmatically, EDF is the recommended format for GUI-based workflows.
```

### Opening Files in MNELAB

Once you've exported an EDF file:

1. **Launch MNELAB** from your applications menu or command line
2. **Click the "Open" icon** in the toolbar, or select **File → Open**
3. **Browse to your EDF file** and click Open

The file will load, and the sidebar will display the dataset name while the main panel shows metadata about the recording, including:
- Number of channels
- Sampling rate
- Recording duration
- Channel types
- Annotations (if any)
- Montage information

### Viewing Your Data

To visualize the time-series data:

1. Select **Plot → Plot data** from the menu
2. A new window will open showing all channels over time
3. Use your mouse to:
   - **Scroll**: Navigate through time
   - **Zoom**: Adjust the time scale
   - **Select channels**: Click channel names to highlight
4. Click the **Help** button in the plot window for more interaction options, including:
   - Adjusting scaling
   - Toggling channel visibility
   - Measuring time intervals
   - Adding annotations
   - Marking bad segments / channels

```{admonition} Interactive Plotting
:class: tip
MNELAB's plotting window is fully interactive. You can scroll through the entire recording, adjust scaling, add annotations, and toggle channels on/off for clearer visualization.
```

---

## Common Workflows

### Basic Preprocessing Pipeline

A typical preprocessing workflow in MNELAB. Any new processing steps will create a new version of the data, preserving the original raw file. This allows you to track changes and revert if needed using the sidebar version selector on the left.

#### 1. Load Data
**File → Open** → Select your `.edf` file

#### 2. Inspect Channel Information
The info panel shows your montage. For Wearable Sensing headsets, you should see:
- **DSI-24:** Fp1, Fp2, Fz, F3, F4, F7, F8, Cz, C3, C4, T3, T4, T5 (P7), T6 (P8), Pz, P3, P4, O1, O2, A1, A2, X1, X2, X3, Trigger, Event
- **DSI-7:** F3, F4, C3, C4, P3, Pz, P4, LE
- **VR300:** FCz, Pz, P3, P4, PO7, PO8, Oz, LE
- **VRVEP:** FCz, POz, PO3/4, O1/O2, Oz, LE

Ensure all expected channels are present.

#### 3. Set Channel Label, Types, Units (if needed)
If channels aren't automatically recognized:
1. **Edit → Channel properties**
2. Select channel and edit type (EEG, EOG, etc.) or units (µV, mV) or label (name)

#### 4. Re-reference
To change from the reference:
1. **Tools → Set reference**
2. Choose a reference option:
   - **Average reference:** All EEG channels
   - **Specific channel:** e.g., Pz
   - **Custom:** Specify multiple channels

#### 5. Filter Data
Apply frequency filters to remove noise:
1. **Tools → Filter data**
2. Set filter parameters:
   - **High-pass:** 0.5 Hz (removes slow drifts)
   - **Low-pass:** 40 Hz (removes high-frequency noise)
3. Click **Apply**

```{admonition} Filter Settings
:class: note
Common filter configurations:
- **ERP analysis:** 0.1 - 50 Hz; See Zhang et al., 2024 for guidelines on your specific analysis.

Zhang, G., Garrett, D. R., & Luck, S. J. (2024). Optimal filters for ERP research II: Recommended settings for seven common ERP components. Psychophysiology, 61, e14530. https://doi.org/10.1111/psyp.14530
```

#### 6. Artifact Removal
For manual artifact rejection:
1. **Plot → Plot data**
2. **Tools → Annotations** to mark bad segments
3. Mark artifacts by clicking and dragging on the plot

For automated artifact correction:
1. **Tools → ICA** (Independent Component Analysis)
2. Click **Fit ICA**
3. Review components and select artifacts (eye blinks, muscle activity)
4. Click **Apply** to remove selected components

#### 7. Export Processed Data
Save your cleaned data:
1. **File → Export**
2. Choose format:
   - **EDF:** For use in other EEG software
   - **FIF:** For use in MNE-Python scripts
   - **CSV:** For custom analysis

---

## Power Spectral Density Analysis

Analyze frequency content of your EEG data:

### Using the GUI

1. **Plot → Plot power spectral density**
2. Configure settings:
   - **Frequency range:** e.g., 0.5 - 50 Hz
   - **Method:** Welch (default)
3. View the PSD plot showing power across frequencies

---

## Event-Related Potentials (ERPs)

If your recording includes event markers (triggers from DSI-Streamer):

### Viewing Events

1. Events appear in the info panel if present in the EDF file
2. **Edit → Events** to view all event markers
3. Events show timestamp and event codes

### Creating Epochs

To analyze time-locked responses:

1. **Tools → Create epochs**
2. Configure:
   - **Event type:** Select trigger codes
   - **Time window:** e.g., -0.2 to 1.0 seconds
   - **Baseline:** e.g., -0.2 to 0 seconds
3. Click **Create**

### Visualizing ERPs

1. After creating epochs, select **Plot → Plot epochs**
2. View averaged responses across trials
3. Export epochs for further analysis

---

## Saving and Exporting

### Saving MNELAB Sessions

MNELAB works with MNE-Python's native FIF format:

**File → Save as** → Choose `.fif` extension

This preserves all preprocessing steps, events, and annotations.

### Exporting for Other Software

- **EDF:** Compatible with most EEG software
- **CSV:** For Excel, R, custom analysis
- **FIF:** For MNE-Python scripts

---

## Advanced Features

### Batch Processing

While MNELAB is primarily GUI-based, you can process multiple files using MNE-Python scripts that leverage MNELAB's functionality. See the [MNE-Python integration](../python/index.md) for scripting examples.

### Integration with MNE-Python

Files preprocessed in MNELAB can be loaded directly into MNE-Python for advanced analysis:

```python
import mne

# Load file preprocessed in MNELAB
raw = mne.io.read_raw_fif('preprocessed_data.fif', preload=True)

# Continue with programmatic analysis
# Apply additional processing, source localization, connectivity analysis, etc.
```

---

## Troubleshooting

### File Won't Load

**Problem:** EDF file fails to open  
**Solution:**
- Ensure the file was exported from DSI-Streamer (not manually edited)
- Check that the file extension is `.edf` (not `.EDF` or `.edf.txt`)
- Try re-exporting from DSI-Streamer

### Missing Channels

**Problem:** Some channels don't appear  
**Solution:**
- Check the info panel to see which channels were loaded
- Verify the original recording included all expected channels
- Check DSI-Streamer export settings

### Performance Issues

**Problem:** MNELAB is slow with large files  
**Solution:**
- Close other applications to free memory
- Consider downsampling: **Tools → Resample**
- Process data in shorter segments

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

## Support

```{admonition} Need Help?
:class: tip
- **MNELAB Issues:** [GitHub Issues](https://github.com/cbrnr/mnelab/issues)
- **Wearable Sensing Support:** [Contact Support](../../../help/index.md)
- **MNE Community:** [MNE Forum](https://mne.discourse.group/)
```
