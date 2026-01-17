# Brain-Computer Interfaces
---

Brain-Computer Interfaces (BCIs) enable direct communication between brain activity and external devices. This guide demonstrates how to build real-time BCIs using EEG data from Wearable Sensing DSI-24, DSI-VR300, and DSI-7 headsets.

```{admonition} Prerequisites
:class: note
- Wearable Sensing headset streaming via LSL (see {doc}`LSL Setup <../../../../lsl/index>`)
- Understanding of {doc}`epochs <../processing/epochs>` and {doc}`filtering <../processing/filter>`
```

```{admonition} Important Note
:class: warning
The examples here are simplified demonstrations for learning purposes. Production BCIs require extensive testing, subject-specific calibration, and validation procedures. Many advanced methods (connectivity analysis, adaptive algorithms, specialized signal processing) are beyond the scope of this guide.
```

## BCI Approaches

Different BCI applications use different EEG features:

- **Alpha neurofeedback (8-13 Hz):** Relaxation training, stress reduction, peak performance
- **Sensorimotor rhythms (SMR, 12-15 Hz):** Motor control and epilepsy management
- **Motor Imagery:** Classify imagined movements (C3, C4, Cz channels)
- **P300 speller:** Detect attention responses for spelling and selection
- **SSVEP:** Steady-state visual evoked potentials for fast selection
- **Error-related potentials:** Error correction in BCI control

---

## Alpha Neurofeedback Example

This section provides a complete, working example of a bandpower-based neurofeedback BCI. The system helps users learn to increase alpha wave activity through real-time feedback.

```{admonition} Source
:class: tip
Adapted from the [MNE-LSL bandpower example](https://mne.tools/mne-lsl/stable/generated/examples/20_bandpower.html)
```

### Overview

This BCI helps users learn to increase alpha wave activity (8-13 Hz) through operant conditioning. The system:

1. Connects to your EEG stream and applies filtering
2. Calibrates a personalized threshold based on your resting alpha power
3. Provides real-time feedback when you exceed the threshold
4. Tracks your success rate over the session

Alpha training is commonly used for relaxation, stress reduction, and peak performance applications.

### How It Works

**Bandpower Computation**

The system uses Welch's method to estimate the power spectral density (PSD) of your EEG signal. The PSD is then integrated over the alpha frequency band (8-13 Hz) using Simpson's rule. This provides a robust, noise-resistant measure of alpha oscillatory activity.

**Baseline Calibration**

Before training begins, the system measures your typical alpha power during a 10-second rest period. It collects 20 samples and uses the 70th percentile as the target threshold. This creates a challenging but achievable goal that's personalized to your baseline brain activity.

**Feedback Loop**

During training, the system continuously computes your current alpha power and compares it to the threshold. When you exceed the threshold, you receive immediate feedback ("SUCCESS!"), creating a learning signal that enables self-regulation of brain activity through operant conditioning.

### Implementation

**Getting Started**
1. **Start your LSL stream** from DSI-Streamer with your Wearable Sensing device
2. **Run the script below** - it will connect and apply filtering
3. **Calibration phase (10 seconds)** - relax with eyes closed to establish your baseline
4. **Training phase** - try to increase alpha power:
   - Close your eyes
   - Focus on breathing
   - Relax facial and body muscles
5. **Monitor feedback** - SUCCESS messages indicate you exceeded the threshold
6. **Press Ctrl+C** when finished to see your final success rate

The complete code is structured in three main steps: stream setup, baseline calibration, and the training loop.

```{code-block} python
:caption: Alpha neurofeedback

from mne_lsl.stream import StreamLSL
import numpy as np
from scipy.integrate import simpson
import time

def compute_bandpower(data, sfreq, band):
    """
    Compute power in a frequency band using Welch's method.
    
    See MNE-LSL bandpower example:
    https://mne.tools/mne-lsl/stable/generated/examples/20_bandpower.html
    
    Parameters
    ----------
    data : array, shape (n_channels, n_samples)
        EEG data
    sfreq : float
        Sampling frequency in Hz
    band : tuple
        (low_freq, high_freq) in Hz
    
    Returns
    -------
    power : array, shape (n_channels,)
        Bandpower for each channel in uV²
    """
    from mne.time_frequency import psd_array_welch
    
    # Compute power spectral density using Welch's method
    # MNE's psd_array_welch returns (psd, freqs)
    psd, freqs = psd_array_welch(
        data, 
        sfreq=sfreq, 
        fmin=band[0], 
        fmax=band[1],
        n_fft=min(256, data.shape[-1]),
        verbose=False
    )
    
    # Integrate PSD over the frequency band using Simpson's rule
    freq_res = freqs[1] - freqs[0]
    bandpower = simpson(psd, dx=freq_res)
    
    return bandpower


# Step 1: Connect to Stream and Apply Filters

print("Connecting to stream...")
stream = StreamLSL(bufsize=10, name="DSI-24").connect()

# Apply bandpass filter to remove DC drift and high-frequency noise
stream.filter(l_freq=0.5, h_freq=50.0, picks='eeg')

# Wait for filter to stabilize and buffer to fill with data
print("Initializing (2 seconds)...")
time.sleep(2.0)

# Step 2: Baseline Calibration
# Collect resting alpha power to establish a personalized threshold

print("\nBASELINE CALIBRATION")
print("=" * 50)
print("Relax with eyes closed for 10 seconds...")

baseline = []
for i in range(20):
    # Get 2 seconds of data from occipital channels (primary alpha generators)
    # DSI-24: O1, O2 | DSI-VR300: Oz, PO7, PO8 | DSI-7: P3, Pz, P4 (closest to occipital)
    data, ts = stream.get_data(winsize=2.0, picks=['O1', 'O2', 'Oz'])
    
    # Compute alpha power (8-13 Hz) and store mean across channels
    power = compute_bandpower(data, stream.info['sfreq'], (8, 13))
    baseline.append(power.mean())
    
    # Show progress every 5 samples
    if (i + 1) % 5 == 0:
        print(f"Calibration: {(i+1)/20*100:.0f}% complete")
    
    time.sleep(0.5)

# Set threshold at 70th percentile (moderately challenging target)
threshold = np.percentile(baseline, 70)
baseline_mean = np.mean(baseline)

print(f"Baseline mean: {baseline_mean:.2e} uV²")
print(f"Target threshold (70th percentile): {threshold:.2e} uV²")
print(f"Required increase: {(threshold/baseline_mean - 1)*100:.1f}%")

# Step 3: Neurofeedback Training
# Real-time feedback loop to train alpha self-regulation

print("\nNEUROFEEDBACK TRAINING")
print("=" * 50)
print("Try to increase your alpha power by relaxing with eyes closed.")
print("You'll see 'SUCCESS' when you exceed the threshold.")
print("Press Ctrl+C to stop.")

score = 0
trials = 0

try:
    while True:
        # Get 2 seconds of recent data from occipital channels
        data, ts = stream.get_data(winsize=2.0, picks=['O1', 'O2', 'Oz'])
        
        # Compute current alpha power
        power = compute_bandpower(data, stream.info['sfreq'], (8, 13)).mean()
        
        # Update trial statistics
        trials += 1
        success_rate = (score / trials) * 100
        
        # Provide immediate feedback
        if power > threshold:
            score += 1
            print(f"SUCCESS! Power: {power:.2e} uV² | Success: {success_rate:.1f}% ({score}/{trials})")
        else:
            # Show how close to threshold
            progress = (power / threshold) * 100
            print(f"Continue... Power: {power:.2e} uV² ({progress:.0f}% of target) | Success: {success_rate:.1f}%")
        
        # Update every 0.5 seconds for smooth feedback
        time.sleep(0.5)

except KeyboardInterrupt:
    print("\n\nTraining session ended.")
    print(f"Final success rate: {success_rate:.1f}% ({score}/{trials} trials)")
    
finally:
    stream.disconnect()
    print("Stream disconnected.")
```

---

## Customizing Your BCI

### Training Different Frequency Bands

You can modify the BCI to train other brain rhythms by changing the frequency band:

**Different frequency bands:**
```{code-block} python
:caption: Compute power in different frequency bands

# Theta training (4-8 Hz)
power = compute_bandpower(data, stream.info['sfreq'], (4, 8))

# Beta training (13-30 Hz)
power = compute_bandpower(data, stream.info['sfreq'], (13, 30))

# SMR training (12-15 Hz)
data, ts = stream.get_data(winsize=2.0, picks=['C3', 'C4', 'Cz'])
power = compute_bandpower(data, stream.info['sfreq'], (12, 15))
```

### Implementing Adaptive Thresholding

Adaptive thresholding automatically adjusts difficulty based on your performance:

```{code-block} python
:caption: Implement adaptive threshold adjustment

power_history = []

while True:
    # Get data and compute power
    data, ts = stream.get_data(winsize=2.0, picks=['O1', 'O2', 'Oz'])
    power = compute_bandpower(data, stream.info['sfreq'], (8, 13)).mean()
    power_history.append(power)
    
    trials += 1
    
    # Update threshold every 50 trials based on recent performance
    if trials % 50 == 0 and trials > 0:
        # Use last 50 samples to recalculate threshold
        recent_power = power_history[-50:]
        threshold = np.percentile(recent_power, 70)
        print(f"\nThreshold updated: {threshold:.2e} uV²\n")
    
    # Feedback logic continues...
    if power > threshold:
        score += 1
        print(f"SUCCESS! Power: {power:.2e} uV² | Success: {success_rate:.1f}%")
    
    time.sleep(0.5)
```
---

## Advanced BCI Paradigms

For more advanced BCI applications, refer to the MNE-LSL documentation:

- **[Motor Imagery Classification](https://mne.tools/mne-lsl/stable/generated/examples/40_decode.html)** - Decode imagined movements using EpochsStream and machine learning
- **[P300 Detection](https://mne.tools/mne-lsl/stable/generated/examples/30_real_time_evoked_responses.html)** - Detect event-related potentials for spelling and selection
- **[Real-time Connectivity](https://mne.tools/mne-lsl/stable/generated/examples/10_peak_detection.html)** - Analyze functional connectivity between brain regions

---

## Resources

- [Bandpower Example](https://mne.tools/mne-lsl/stable/generated/examples/20_bandpower.html) | [Decoding Example](https://mne.tools/mne-lsl/stable/generated/examples/40_decode.html)
- [MNE-LSL API Reference](https://mne.tools/mne-lsl/stable/api.html)
- {doc}`Epoching <../processing/epochs>` | {doc}`Filtering <../processing/filter>` | {doc}`Visualization <../visualization/viewer>`
