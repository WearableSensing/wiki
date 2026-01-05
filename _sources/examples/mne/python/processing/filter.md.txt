# Filtering
---

This section will guide you through the process of filtering EEG data using MNE-Python. Filtering is a crucial step in EEG data preprocessing, as it helps to remove noise and artifacts from the signal.

```{admonition} Prerequisites
:class: note
This guide assumes you have loaded your EEG data into a `raw` object. See {doc}`Load Data <../core/load>` for details on loading EDF files.
```

## Understanding Filtering

Filters remove unwanted frequency components from your signal:

- **High-pass filter:** Removes slow drifts (< cutoff frequency)
- **Low-pass filter:** Removes high-frequency noise (> cutoff frequency)
- **Band-pass filter:** Keeps only frequencies within a range
- **Notch filter:** Removes specific frequencies (e.g., 50/60 Hz line noise)

```{admonition} Filtering Resources
:class: tip
See [Background on Filtering](https://mne.tools/stable/auto_tutorials/preprocessing/25_background_filtering.html) and [Filtering and Resampling](https://mne.tools/stable/auto_tutorials/preprocessing/30_filtering_resampling.html) for comprehensive filtering guidance.
```

---

## Basic Filtering

### Band-Pass Filter

The most common filter type - keeps frequencies within a specified range:

```python
import mne

# Load data
raw = mne.io.read_raw_edf('recording.edf', preload=True)

# Visualize before filtering
raw.plot(n_channels=20, duration=10, title='Before Filtering')

# Apply band-pass filter (1-40 Hz)
raw.filter(l_freq=1.0, h_freq=40.0)

# Visualize after filtering
raw.plot(n_channels=20, duration=10, title='After Filtering')
```

**Common frequency ranges:**
- **ERP analysis:** 0.1 - 50 Hz
- **Spectral analysis:** 0.5 - 50 Hz
- **Beta/gamma analysis:** 1 - 100 Hz
- **Sleep staging:** 0.3 - 35 Hz

### High-Pass Filter Only

Remove slow drifts and DC offset:

```python
# Remove frequencies below 1 Hz
raw.filter(l_freq=1.0, h_freq=None)
```

### Low-Pass Filter Only

Remove high-frequency noise:

```python
# Remove frequencies above 40 Hz
raw.filter(l_freq=None, h_freq=40.0)
```

---

## Notch Filtering

Remove power line noise (50 Hz in Europe, 60 Hz in North America):

```python
# Remove 60 Hz line noise
raw.notch_filter(freqs=60.0, filter_length='auto', phase='zero')

# Remove 60 Hz and harmonics
raw.notch_filter(freqs=[60, 120, 180], filter_length='auto', phase='zero')

# For 50 Hz regions
raw.notch_filter(freqs=50.0, filter_length='auto', phase='zero')
```

### Visualizing Line Noise

Check if line noise is present before filtering:

```python
# Plot power spectral density
raw.plot_psd(fmax=100, average=False)
# Look for peaks at 50/60 Hz and harmonics
```

---

## Filter Parameters

### Filter Type (FIR vs IIR)

**FIR (Finite Impulse Response) - Default:**
- Linear phase (no temporal distortion)
- Symmetric impulse response
- Longer computational time
- Recommended for most EEG applications

```python
# FIR filter (default)
raw.filter(l_freq=1.0, h_freq=40.0, method='fir')
```

**IIR (Infinite Impulse Response):**
- Non-linear phase (can distort timing)
- Sharper frequency cutoffs
- Faster computation
- Use with caution for ERP analysis

```python
# IIR filter (4th order Butterworth)
raw.filter(l_freq=1.0, h_freq=40.0, method='iir', iir_params=dict(order=4, ftype='butter'))
```

### Filter Window

Controls the shape of the filter frequency response:

```python
# Hamming window (default)
raw.filter(l_freq=1.0, h_freq=40.0, fir_window='hamming')

# Hann window (smoother frequency response)
raw.filter(l_freq=1.0, h_freq=40.0, fir_window='hann')

# Blackman window (better stopband attenuation)
raw.filter(l_freq=1.0, h_freq=40.0, fir_window='blackman')
```

### Filter Length

Longer filters have sharper cutoffs but introduce more edge artifacts:

```python
# Automatic length (recommended)
raw.filter(l_freq=1.0, h_freq=40.0, filter_length='auto')

# Specific length (in samples)
raw.filter(l_freq=1.0, h_freq=40.0, filter_length='10s')  # 10 seconds

# Very sharp filter
raw.filter(l_freq=1.0, h_freq=40.0, filter_length='30s')
```

### Phase

Controls whether filtering introduces time delays:

```python
# Zero-phase (default) - no time delay, but processes data twice
raw.filter(l_freq=1.0, h_freq=40.0, phase='zero')

# Minimum phase - introduces time delay but processes once
raw.filter(l_freq=1.0, h_freq=40.0, phase='minimum')
```

---

## Advanced Filtering

### Transition Bandwidth

Control the sharpness of frequency cutoffs:

```python
# Wider transition (faster, less ringing)
raw.filter(l_freq=1.0, h_freq=40.0, l_trans_bandwidth=0.5, h_trans_bandwidth=5.0)

# Narrower transition (sharper cutoff, more ringing)
raw.filter(l_freq=1.0, h_freq=40.0, l_trans_bandwidth=0.1, h_trans_bandwidth=1.0)

# Automatic (recommended)
raw.filter(l_freq=1.0, h_freq=40.0, l_trans_bandwidth='auto', h_trans_bandwidth='auto')
```

### Filtering Specific Channels

```python
# Filter only EEG channels
raw.filter(l_freq=1.0, h_freq=40.0, picks='eeg')

# Filter specific channels
raw.filter(l_freq=1.0, h_freq=40.0, picks=['EEG Cz-LE', 'EEG Pz-LE'])
```

### Filtering in Place vs Copy

```python
# Modify original data (in-place)
raw.filter(l_freq=1.0, h_freq=40.0)

# Create filtered copy (preserves original)
raw_filtered = raw.copy().filter(l_freq=1.0, h_freq=40.0)
```

---

## Filter Design Visualization

Visualize filter characteristics before applying:

```python
from mne.viz import plot_filter

# Design filter parameters
h = mne.filter.create_filter(
    raw.get_data(), raw.info['sfreq'],
    l_freq=1.0, h_freq=40.0,
    method='fir', fir_window='hamming'
)

# Plot frequency and impulse response
plot_filter(h, raw.info['sfreq'])
```

---

## Resampling

Reduce sampling rate to decrease file size and processing time:

```python
# Original sampling rate
print(f'Original sampling rate: {raw.info["sfreq"]} Hz')

# Resample to 250 Hz
raw.resample(sfreq=250)

print(f'New sampling rate: {raw.info["sfreq"]} Hz')
```

**Common resampling targets:**
- 250 Hz - Standard for EEG analysis
- 500 Hz - Higher temporal resolution
- 1000 Hz - For high-frequency analysis

```{admonition} Filter Before Resampling
:class: warning
Always filter BEFORE resampling to avoid aliasing artifacts. The correct order is:
1. Notch filter (if needed)
2. Band-pass filter
3. Resample
```

---

## Comparing Filter Effects

Visualize the impact of different filters:

```python
# Create copies with different filters
raw_1hz = raw.copy().filter(l_freq=1.0, h_freq=40.0)
raw_01hz = raw.copy().filter(l_freq=0.1, h_freq=40.0)

# Plot power spectral density for comparison
import matplotlib.pyplot as plt

fig, axes = plt.subplots(3, 1, figsize=(10, 8))

raw.plot_psd(ax=axes[0], show=False, average=True)
axes[0].set_title('Unfiltered')

raw_1hz.plot_psd(ax=axes[1], show=False, average=True)
axes[1].set_title('1-40 Hz')

raw_01hz.plot_psd(ax=axes[2], show=False, average=True)
axes[2].set_title('0.1-40 Hz')

plt.tight_layout()
plt.show()
```

---

## Common Filter Combinations

Filter settings for specific analysis types:

```python
# ERP analysis (preserve slow components)
raw.filter(l_freq=0.1, h_freq=40.0)

# Oscillatory analysis (alpha, beta)
raw.filter(l_freq=1.0, h_freq=50.0)

# Sleep staging
raw.filter(l_freq=0.3, h_freq=35.0)

# Remove only line noise (preserve everything else)
raw.notch_filter(freqs=60.0)
```

---

## Best Practices

1. **Filter early** in your preprocessing pipeline
2. **Filter before resampling** to avoid aliasing
3. **Use FIR filters** for ERP analysis (linear phase)
4. **Document filter settings** in your methods
5. **Visualize effects** using PSD plots

---

## Additional Resources

**MNE Documentation:**
- [Background on Filtering](https://mne.tools/stable/auto_tutorials/preprocessing/25_background_filtering.html)
- [Filtering and Resampling](https://mne.tools/stable/auto_tutorials/preprocessing/30_filtering_resampling.html)
- [Filter Design](https://mne.tools/stable/auto_examples/visualization/plot_filter_basics.html)

**API References:**
- [`raw.filter()`](https://mne.tools/stable/generated/mne.io.Raw.html#mne.io.Raw.filter)
- [`raw.notch_filter()`](https://mne.tools/stable/generated/mne.io.Raw.html#mne.io.Raw.notch_filter)
- [`raw.resample()`](https://mne.tools/stable/generated/mne.io.Raw.html#mne.io.Raw.resample)
- [`mne.filter.create_filter()`](https://mne.tools/stable/generated/mne.filter.create_filter.html)

**External Resources:**
- [Neural Data Science in Python](https://neuraldatascience.io/intro.html)
- [Widmann et al. (2015) - Digital filter design for EEG](https://doi.org/10.1016/j.jneumeth.2014.08.002)
