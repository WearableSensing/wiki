# Epoching & Event Handling
---

Learn to extract and analyze event-related data by creating epochs around stimulus events or experimental triggers.

```{admonition} Prerequisites
:class: note
This guide assumes you have loaded, filtered, and cleaned your EEG data. See {doc}`Load Data <../core/load>`, {doc}`Filtering <filter>`, and {doc}`Artifact Handling <artifacts>` for details.
```

## Understanding Epochs

**Epochs** are time-locked segments of data centered around specific events (e.g., stimulus presentation, button press). Epoching is essential for:
- Event-Related Potential (ERP) analysis
- Time-frequency analysis
- Statistical comparison between conditions
- Averaging across trials

---

## Finding Events

Events are markers in your data that indicate when something happened (stimulus, response, etc.). For Wearable Sensing data, these typically come from the Trigger channel.

### Finding Events from Trigger Channel

```{code-block} python
:caption: Extract events from trigger channel

import mne

# Load data
raw = mne.io.read_raw_edf('recording.edf', preload=True)

# Find events from trigger channel
events = mne.find_events(raw, stim_channel='Trigger', min_duration=0.002)

print(f'Found {len(events)} events')
print(f'Event IDs: {set(events[:, 2])}')

# Visualize events
mne.viz.plot_events(events, sfreq=raw.info['sfreq'], 
                     first_samp=raw.first_samp)
```

**Event array structure:**
- Column 1: Sample number
- Column 2: Previous trigger value (usually 0)
- Column 3: Event ID (trigger code)

### Creating Event Dictionary

Map event IDs to meaningful names:

```{code-block} python
:caption: Create event dictionary for condition labels

event_id = {
    'auditory/left': 1,
    'auditory/right': 2,
    'visual/left': 3,
    'visual/right': 4,
    'response': 5
}
```

---

## Creating Epochs

### Basic Epoch Creation

```{code-block} python
:caption: Create epochs with baseline correction

# Create epochs around events
epochs = mne.Epochs(
    raw,
    events,
    event_id=event_id,
    tmin=-0.2,      # Start 200 ms before event
    tmax=0.8,       # End 800 ms after event
    baseline=(-0.2, 0),  # Baseline period for correction
    preload=True
)

print(epochs)
```

**Key parameters:**
- `tmin`, `tmax`: Time window around events (in seconds)
- `baseline`: Period used for baseline correction (tuple or None)
- `preload`: Load data into memory (needed for many operations)

### Epoch Selection by Condition

```{code-block} python
:caption: Select epochs by experimental condition

# Create epochs for specific conditions
epochs_auditory = epochs['auditory']
epochs_visual = epochs['visual']
epochs_left = epochs['auditory/left', 'visual/left']

print(f'Auditory epochs: {len(epochs_auditory)}')
print(f'Visual epochs: {len(epochs_visual)}')
```

### Visualizing Epochs

```{code-block} python
:caption: Visualize epochs and ERPs interactively

# Plot all epochs
epochs.plot(n_epochs=10, n_channels=20, scalings='auto')

# Plot average across epochs (ERP)
epochs.plot_image(picks='eeg', sigma=1.0)

# Plot ERP with standard error
epochs.average().plot()
```

---

## Baseline Correction

Remove pre-stimulus activity to isolate event-related responses:

```{code-block} python
:caption: Apply baseline correction to epochs

# Baseline correct using pre-stimulus period
epochs.apply_baseline(baseline=(-0.2, 0))

# Or specify during epoch creation
epochs = mne.Epochs(raw, events, event_id=event_id,
                    tmin=-0.2, tmax=0.8,
                    baseline=(-0.2, 0),  # Apply automatically
                    preload=True)
```

**Baseline options:**
- `(None, 0)`: Use time from start to t=0
- `(-0.2, 0)`: Use 200 ms before event
- `None`: No baseline correction

---

## Epoch Rejection

### Manual Rejection

```{code-block} python
:caption: Interactively reject bad epochs

# Interactively reject bad epochs
epochs.plot(n_epochs=10, block=True)
# Click on epochs to mark as bad
```

### Automatic Rejection

Set amplitude thresholds to automatically reject noisy epochs:

```{code-block} python
:caption: Set automatic rejection thresholds

# Define rejection criteria (in volts)
reject_criteria = dict(
    eeg=100e-6,      # 100 µV for EEG channels
    eog=200e-6       # 200 µV for EOG channels
)

# Apply during epoch creation
epochs = mne.Epochs(raw, events, event_id=event_id,
                    tmin=-0.2, tmax=0.8,
                    baseline=(-0.2, 0),
                    reject=reject_criteria,
                    preload=True)

print(f'Rejected {len(epochs.drop_log) - len(epochs)} epochs')
```

### Peak-to-Peak Rejection

```{code-block} python
:caption: Reject epochs with extreme amplitudes or flatlines

# Reject based on peak-to-peak amplitude
reject_criteria = dict(eeg=100e-6)
flat_criteria = dict(eeg=1e-6)  # Also reject flat channels

epochs = mne.Epochs(raw, events, event_id=event_id,
                    tmin=-0.2, tmax=0.8,
                    reject=reject_criteria,
                    flat=flat_criteria,
                    preload=True)
```

### Visualizing Rejection

```{code-block} python
:caption: View rejection statistics and drop log

# Plot drop log showing why epochs were rejected
epochs.plot_drop_log()

# Show rejection statistics
print(epochs.drop_log)
```

---

## Computing Evoked Responses (ERPs)

Average epochs to compute Event-Related Potentials:

```{code-block} python
:caption: Compute and plot evoked responses (ERPs)

# Average all epochs
evoked_all = epochs.average()

# Average by condition
evoked_auditory = epochs['auditory'].average()
evoked_visual = epochs['visual'].average()

# Plot ERPs
evoked_all.plot()
evoked_auditory.plot()

# Plot with spatial colors
evoked_all.plot(spatial_colors=True, gfp=True)
```

### Comparing Conditions

```{code-block} python
:caption: Compare ERPs across experimental conditions

# Plot multiple conditions
evokeds = [epochs[cond].average() for cond in event_id.keys()]
mne.viz.plot_compare_evokeds(evokeds)

# Statistical comparison
from mne.stats import permutation_cluster_test
# See MNE statistics tutorials for details
```

---

## Topographic Analysis

### Topographic Maps

```{code-block} python
:caption: Plot ERP topography at specific time points

# Plot topography at specific time points
times = [0.1, 0.2, 0.3]
evoked.plot_topomap(times=times, ch_type='eeg')

# Interactive topomap
evoked.plot_topomap(times='auto', ch_type='eeg', nrows='auto')
```

### Joint Plot (Butterfly + Topomap)

```{code-block} python
:caption: Combine timecourse and topography visualization

# Combine timecourse and topography
evoked.plot_joint(times=[0.1, 0.2, 0.3])

# Automatically select peak times
evoked.plot_joint(times='peaks')
```

---

## Time-Frequency Analysis

Analyze oscillatory activity in epochs:

```{code-block} python
:caption: Compute time-frequency representation with Morlet wavelets

from mne.time_frequency import tfr_morlet

# Compute time-frequency representation
freqs = range(4, 40, 2)  # Frequencies from 4-40 Hz
n_cycles = freqs / 2.0   # Number of cycles per frequency

power = tfr_morlet(epochs, freqs=freqs, n_cycles=n_cycles,
                   return_itc=False, average=True)

# Plot
power.plot(baseline=(-0.2, 0), mode='logratio', title='Power')
```

### Event-Related Spectral Perturbation (ERSP)

```{code-block} python
:caption: Compute ERSP for specific channels

# Compute for specific channels
power = tfr_morlet(epochs, picks=['EEG C3-LE', 'EEG C4-LE'],
                   freqs=freqs, n_cycles=n_cycles,
                   return_itc=False, average=True)

power.plot_topo(baseline=(-0.2, 0), mode='logratio')
```

---

## Saving and Loading Epochs

### Save Epochs

```{code-block} python
:caption: Save epochs to FIF format

# Save epochs to disk
epochs.save('epochs-epo.fif', overwrite=True)

# Save specific conditions
epochs['auditory'].save('epochs_auditory-epo.fif', overwrite=True)
```

### Load Epochs

```{code-block} python
:caption: Load epochs from saved FIF file

# Load saved epochs
epochs = mne.read_epochs('epochs-epo.fif', preload=True)
```

### Export to Other Formats

```{code-block} python
:caption: Export epochs to NumPy, DataFrame, or CSV

# Export to NumPy array
data = epochs.get_data()  # Shape: (n_epochs, n_channels, n_times)

# Export to DataFrame
df = epochs.to_data_frame()

# Export to CSV
df.to_csv('epochs.csv', index=False)
```

---

## Complete Epoching Workflow

```{code-block} python
:caption: Complete workflow from loading to ERP comparison

import mne

# Load and preprocess data
raw = mne.io.read_raw_edf('recording.edf', preload=True)
raw.filter(l_freq=0.1, h_freq=40.0)
raw.set_eeg_reference(ref_channels='average')

# Find events
events = mne.find_events(raw, stim_channel='Trigger')

# Define event IDs
event_id = {
    'condition_1': 1,
    'condition_2': 2,
    'response': 5
}

# Create epochs with rejection
reject_criteria = dict(eeg=100e-6)
epochs = mne.Epochs(raw, events, event_id=event_id,
                    tmin=-0.2, tmax=0.8,
                    baseline=(-0.2, 0),
                    reject=reject_criteria,
                    preload=True)

print(f'Created {len(epochs)} epochs')

# Compute ERPs
evoked_1 = epochs['condition_1'].average()
evoked_2 = epochs['condition_2'].average()

# Visualize
evoked_1.plot_joint(times=[0.1, 0.2, 0.3])
evoked_2.plot_joint(times=[0.1, 0.2, 0.3])

# Compare conditions
mne.viz.plot_compare_evokeds({'Condition 1': evoked_1, 
                               'Condition 2': evoked_2})

# Save results
epochs.save('epochs-epo.fif', overwrite=True)
evoked_1.save('condition_1-ave.fif', overwrite=True)
evoked_2.save('condition_2-ave.fif', overwrite=True)
```

---

## Next Steps

After creating epochs:
1. Compute statistics and contrasts between conditions
2. Perform time-frequency analysis on epochs
3. {doc}`MNE-LSL real-time epochs <../../lsl/processing/epochs>` - Compare with real-time epoching

---

## Resources

- [Epoching Tutorial](https://mne.tools/stable/auto_tutorials/epochs/10_epochs_overview.html) | [ERP/ERF Analysis](https://mne.tools/stable/auto_tutorials/evoked/index.html) | [Time-Frequency Analysis](https://mne.tools/stable/auto_tutorials/time-freq/index.html)
- [mne.Epochs API](https://mne.tools/stable/generated/mne.Epochs.html) | [mne.find_events API](https://mne.tools/stable/generated/mne.find_events.html)
- [Visualizing Evoked Data](https://mne.tools/stable/auto_tutorials/evoked/20_visualize_evoked.html) | [plot_compare_evokeds API](https://mne.tools/stable/generated/mne.viz.plot_compare_evokeds.html)
