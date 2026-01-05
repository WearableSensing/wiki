# Artifact Handling
---

Learn to identify and remove artifacts from your EEG data using manual rejection, ICA, and regression methods.

```{admonition} Prerequisites
:class: note
This guide assumes you have loaded and filtered your EEG data. See {doc}`Load Data <../core/load>` and {doc}`Filtering <filter>` for details.
```

## Overview of Artifact Types

Common artifacts in EEG data include:

- **Eye blinks and movements** - High amplitude, frontal distribution
- **Muscle activity (EMG)** - High frequency, temporal regions
- **Cardiac activity (ECG)** - Regular rhythmic pattern
- **Line noise** - 50/60 Hz electrical interference
- **Movement artifacts** - Large amplitude, variable patterns

```{admonition} Artifact Detection Resources
:class: tip
See [Overview of Artifact Detection](https://mne.tools/stable/auto_tutorials/preprocessing/10_preprocessing_overview.html) for a comprehensive overview of artifact types and detection methods.
```

---

## Manual Artifact Rejection

### Marking Bad Data Spans

Visually inspect data and mark bad segments:

```python
import mne

# Interactive visualization for marking bad spans
raw.plot(n_channels=20, block=True)
# Click and drag to mark bad spans as annotations
# These will be excluded from epoching
```

### Using Annotations

Programmatically create annotations for bad segments:

```python
from mne import Annotations

# Create annotations for bad segments (times in seconds)
onset = [10.0, 45.2, 60.5]  # Start times of bad segments
duration = [2.0, 1.5, 3.0]  # Duration of each segment
description = ['bad_movement', 'bad_blink', 'bad_noise']

annot = Annotations(onset, duration, description, orig_time=raw.info['meas_date'])
raw.set_annotations(annot)

# Visualize with annotations
raw.plot()
```

```{admonition} Annotation Resources
:class: note
See [Rejecting Bad Data Spans](https://mne.tools/stable/auto_tutorials/preprocessing/20_rejecting_bad_data.html) for more information on annotations and automatic detection methods.
```

---

## Independent Component Analysis (ICA)

ICA decomposes EEG signals into independent components, allowing you to identify and remove artifact sources.

### Fitting ICA

```python
from mne.preprocessing import ICA

# Create ICA object
ica = ICA(n_components=20, random_state=97, max_iter='auto')

# Fit ICA on filtered data (1-40 Hz recommended)
raw_filt = raw.copy().filter(l_freq=1.0, h_freq=40.0)
ica.fit(raw_filt)

print(f'Fitted {ica.n_components_} components')
```

### Visualizing Components

```python
# Plot component time courses
ica.plot_sources(raw_filt)

# Plot component topographies
ica.plot_components()

# Plot detailed properties of specific components
ica.plot_properties(raw_filt, picks=[0, 1, 2])
```

### Identifying Artifact Components

**Eye blinks:** Frontal topography, low frequency, large amplitude

```python
# Find components correlated with EOG channel
eog_indices, eog_scores = ica.find_bads_eog(raw_filt, ch_name='EEG X2:EOG-Pz')
print(f'EOG components: {eog_indices}')

# Visualize EOG scores
ica.plot_scores(eog_scores)
```

**Cardiac artifacts:** Regular rhythmic pattern

```python
# Find components correlated with ECG
ecg_indices, ecg_scores = ica.find_bads_ecg(raw_filt)
print(f'ECG components: {ecg_indices}')
```

### Removing Components

```python
# Mark components as bad
ica.exclude = [0, 2, 5]  # Component indices to remove

# Apply ICA to remove marked components
raw_clean = ica.apply(raw.copy())

# Compare before and after
raw.plot(n_channels=10, title='Before ICA')
raw_clean.plot(n_channels=10, title='After ICA')
```

### Complete ICA Workflow

```python
import mne
from mne.preprocessing import ICA

# Load and filter data
raw = mne.io.read_raw_edf('recording.edf', preload=True)
raw.filter(l_freq=1.0, h_freq=40.0)

# Fit ICA
ica = ICA(n_components=15, random_state=97, max_iter='auto')
ica.fit(raw)

# Automatically find bad components
# Use EOG channel if available, or frontal channel (Fp1)
eog_indices, _ = ica.find_bads_eog(raw, ch_name='Fp1')
ecg_indices, _ = ica.find_bads_ecg(raw)

# Combine and set as bad
ica.exclude = list(set(eog_indices + ecg_indices))
print(f'Excluding components: {ica.exclude}')

# Plot for verification
ica.plot_components(picks=ica.exclude)

# Apply ICA
raw_clean = ica.apply(raw.copy())

# Save cleaned data
raw_clean.save('recording_ica_clean.fif', overwrite=True)
```

```{admonition} ICA Best Practices
:class: tip
- Filter data (1-40 Hz) before ICA for better decomposition
- Use at least 1-2 minutes of data for stable components
- Remove extreme artifacts manually before ICA
- Verify components visually before removal
- See [ICA Tutorial](https://mne.tools/stable/auto_tutorials/preprocessing/40_artifact_correction_ica.html) for detailed guidance
```

---

## Regression-Based Artifact Removal

Use regression to remove artifacts when you have reference channels (EOG, ECG).

### EOG Artifact Removal

```python
# Create EOG events from EOG channel
eog_events = mne.preprocessing.find_eog_events(raw, ch_name='EEG X2:EOG-Pz')

# Create EOG epochs
eog_epochs = mne.preprocessing.create_eog_epochs(raw, ch_name='EEG X2:EOG-Pz')

# Compute and apply SSP projectors
projs, _ = mne.preprocessing.compute_proj_eog(raw, ch_name='EEG X2:EOG-Pz', 
                                               n_eeg=2, average=True)
raw.add_proj(projs)
raw.apply_proj()
```

### ECG Artifact Removal

```python
# Find ECG events
ecg_events = mne.preprocessing.find_ecg_events(raw, ch_name='EEG X1:ECG-Pz')

# Create ECG epochs
ecg_epochs = mne.preprocessing.create_ecg_epochs(raw, ch_name='EEG X1:ECG-Pz')

# Compute and apply SSP projectors
projs, _ = mne.preprocessing.compute_proj_ecg(raw, ch_name='EEG X1:ECG-Pz',
                                               n_eeg=2, average=True)
raw.add_proj(projs)
raw.apply_proj()
```

```{admonition} Regression Resources
:class: note
See [Repairing Artifacts with Regression](https://mne.tools/stable/auto_tutorials/preprocessing/35_artifact_correction_regression.html) and [SSP Tutorial](https://mne.tools/stable/auto_tutorials/preprocessing/50_artifact_correction_ssp.html) for more information.
```

---

## Automatic Artifact Detection

MNE provides automated methods for detecting artifacts in continuous data.

### Peak-to-Peak Amplitude

```python
# Detect flat and high-amplitude segments
annot_auto, scores = mne.preprocessing.annotate_amplitude(
    raw, 
    peak='neg',
    flat=1e-6,  # Flat if below this value (V)
    bad_percent=10  # Mark as bad if >10% of channels affected
)

raw.set_annotations(annot_auto)
```

### Muscle Artifacts

```python
# Detect muscle artifacts
annot_muscle, scores = mne.preprocessing.annotate_muscle_zscore(
    raw,
    threshold=5,  # Z-score threshold
    min_length_good=0.2  # Minimum length of good data
)

raw.set_annotations(raw.annotations + annot_muscle)
```

---

## Epoch-Based Rejection

Reject bad epochs based on amplitude thresholds:

```python
import mne

# Create epochs (see Epoching section for details)
events = mne.find_events(raw, stim_channel='Trigger')
epochs = mne.Epochs(raw, events, event_id={'stimulus': 1},
                    tmin=-0.2, tmax=0.8, baseline=(-0.2, 0),
                    preload=True)

# Set rejection criteria (values in V for EEG)
reject_criteria = dict(
    eeg=100e-6,  # 100 µV
    eog=200e-6   # 200 µV
)

# Apply rejection
epochs.drop_bad(reject=reject_criteria)

print(f'Kept {len(epochs)} / {len(epochs) + len(epochs.drop_log)} epochs')
```

### Visualizing Dropped Epochs

```python
# Plot drop log
epochs.plot_drop_log()

# Plot rejected epochs
epochs.plot(picks='eeg', scalings='auto')
```

---

## Additional Resources

**MNE Preprocessing Tutorials:**
- [Overview of Artifact Detection](https://mne.tools/stable/auto_tutorials/preprocessing/10_preprocessing_overview.html)
- [Handling Bad Channels](https://mne.tools/stable/auto_tutorials/preprocessing/15_handling_bad_channels.html)
- [Rejecting Bad Data Spans](https://mne.tools/stable/auto_tutorials/preprocessing/20_rejecting_bad_data.html)
- [ICA Tutorial](https://mne.tools/stable/auto_tutorials/preprocessing/40_artifact_correction_ica.html)
- [Regression-Based Correction](https://mne.tools/stable/auto_tutorials/preprocessing/35_artifact_correction_regression.html)
- [SSP Correction](https://mne.tools/stable/auto_tutorials/preprocessing/50_artifact_correction_ssp.html)

**API References:**
- [`mne.preprocessing.ICA`](https://mne.tools/stable/generated/mne.preprocessing.ICA.html)
- [`mne.Annotations`](https://mne.tools/stable/generated/mne.Annotations.html)
- [`mne.preprocessing.find_bads_eog`](https://mne.tools/stable/generated/mne.preprocessing.find_bads_eog.html)
