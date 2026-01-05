# Epoching & Event Handling
---

Analyze event-related potentials and create epochs from continuous data.

## Viewing Events

If your recording includes event markers (triggers from DSI-Streamer):

1. Events appear in the info panel if present in the EDF file
2. **Edit → Events** to view all event markers
3. Events show timestamp and event codes

### Importing Events from Separate Files

If events are stored in a separate file (common with FIF format):

1. **File → Import events**
2. Select the event file (e.g., `.fif` or `.eve` format)
3. Click **Open**
4. Events will now appear in the info panel

## Creating Epochs

To analyze time-locked responses:

1. **Tools → Create epochs**
2. Configure parameters:
   - **Event type:** Select trigger codes of interest
   - **Time window:** e.g., -0.2 to 1.0 seconds
   - **Baseline:** e.g., -0.2 to 0 seconds
3. Click **Create**

```{admonition} Epoch Parameters
:class: note
- **Time window:** Defines the time range around each event
- **Baseline:** Period used for baseline correction (typically pre-stimulus)
- **Event codes:** Can select multiple codes or specific values
```

## Dropping Bad Epochs

Remove epochs with excessive artifacts:

1. **Tools → Drop bad epochs**
2. Configure rejection criteria:
   - **Activate Reject:** Check this box
   - **Enter threshold:** e.g., 0.0001 (corresponding to 100 µV peak-to-peak)
3. Click **OK**

Epochs exceeding the threshold will be automatically rejected.

## Visualizing Evoked Responses

### Butterfly Plots

View averaged evoked potentials across all channels:

1. **Plot → Plot evoked**
2. Select event types of interest
3. Optional settings:
   - **Spatial colors:** Color-code channels by location
   - **GFP:** Show Global Field Power
4. Click **OK**

Separate butterfly plots will appear for each event type.

### Topographic Maps

Create topomaps showing spatial distribution at specific time points:

1. **Plot → Plot evoked topomaps**
2. Select event type
3. Choose time points:
   - **Automatic:** Based on peaks
   - **Manual:** Enter specific times (e.g., "-0.2, 0.1, 0.4")
4. Click **OK**

### Joint Plots

Combine butterfly plots with topomaps:

1. **Plot → Plot evoked**
2. Select event type
3. Enable:
   - **GFP:** Show Global Field Power
   - **Spatial colors:** Color-coded channels
   - **Topomaps:** Set to "Peaks" for automatic time selection
4. Click **OK**

Topomaps will show at the three largest GFP peaks.

### Comparing Conditions

Directly compare evoked responses between different event types:

1. **Plot → Plot evoked comparison**
2. Select channels to compare (e.g., frontal channels for auditory responses)
3. Select event types to compare
4. Choose **Combine channels:** mean or individual
5. Click **OK**

Shaded ribbons represent 95% confidence intervals.

```{admonition} Channel Selection for Comparisons
:class: tip
Use **Plot → Plot channel locations** to identify channel groups (frontal, central, parietal, etc.) before creating comparison plots. This helps you select appropriate channels for your analysis.
```

## Individual Epoch Inspection

View individual trials before averaging:

1. **Plot → Plot epochs** to view individual trials
2. **Plot → Plot image** for a 2D representation across trials

## Exporting Epochs

Save epochs for further analysis:

1. **File → Export**
2. Choose format:
   - **FIF:** For MNE-Python scripts
   - **CSV:** For custom analysis in other software

## Power Spectral Density

Analyze frequency content of your epochs:

1. **Plot → Plot power spectral density**
2. Configure settings:
   - **Frequency range:** e.g., 0.5 - 50 Hz
   - **Method:** Welch (default)
3. View the PSD plot showing power across frequencies
