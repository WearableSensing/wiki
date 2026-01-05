# Load Wearable Sensing Data
---

MNELAB can open EDF files exported from DSI-Streamer, making it easy to analyze recordings from DSI-7, DSI-24, DSI-VR300, and DSI-Flex headsets.

## Exporting EDF from DSI-Streamer

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

## Opening Files in MNELAB

Once you've exported an EDF file:

1. **Launch MNELAB** from your applications menu
2. **Click the "Open" icon** in the toolbar, or select **File → Open**
3. **Browse to your EDF file** and click Open

The file will load, and the sidebar will display the dataset name while the main panel shows metadata about the recording, including:
- Number of channels
- Sampling rate
- Recording duration
- Channel types
- Annotations (if any)
- Montage information

## Data Selection & Cropping

### Cropping Time Range

To work with a specific time segment:

1. **Edit → Crop data**
2. Enter **Start time** and **Stop time** (in seconds)
3. Click **OK**

A new cropped dataset will be created in the sidebar.

### Picking Channels by Type

To select specific channel types:

1. **Edit → Pick channels**
2. Choose selection method:
   - **By type:** Select EEG, MEG, EOG, etc.
   - **By name:** Manually select individual channels
3. Choose whether to create new dataset or overwrite
4. Click **OK**

```{admonition} Working with Multiple Datasets
:class: tip
MNELAB preserves your analysis history by creating new datasets for each processing step. Use the sidebar to switch between versions and compare results.
```

## Viewing Your Data

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

## Viewing Channel Locations

To visualize sensor positions:

1. **Plot → Plot channel locations**
2. A 2D topographic view of channel positions appears
3. Bad channels are highlighted in red

This is useful for:
- Verifying montage configuration
- Identifying spatial relationships between channels
- Planning channel selections for analysis

## Expected Channels

For Wearable Sensing headsets, you should see:

- **DSI-24:** Fp1, Fp2, Fz, F3, F4, F7, F8, Cz, C3, C4, T3, T4, T5 (P7), T6 (P8), Pz, P3, P4, O1, O2, A1, A2, X1, X2, X3, Trigger, Event
- **DSI-7:** F3, F4, C3, C4, P3, Pz, P4, LE
- **VR300:** FCz, Pz, P3, P4, PO7, PO8, Oz, LE
- **VRVEP:** FCz, POz, PO3/4, O1/O2, Oz, LE

## FIF Files

In addition to EDF files, MNELAB can read FIF files created from other MNE-Python workflows. See our [MNE-Python integration tutorial](../../python/index.md) for more information.

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
