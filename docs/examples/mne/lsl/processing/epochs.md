# Epoching & Event Handling
---

Extract event-related time segments from continuous EEG streams from your Wearable Sensing headset. Epoching allows you to analyze brain responses time-locked to specific events like stimuli, responses, or experimental triggers.

```{admonition} Prerequisites
:class: note
Understanding of {doc}`stream connection <connect>` and stimulus markers in your Wearable Sensing LSL stream
```

## What is Real-Time Epoching?

Epoching segments continuous EEG data into fixed-length windows around events of interest. In real-time applications with MNE-LSL, the `EpochsStream` class continuously monitors an LSL stream for trigger events and automatically extracts epochs as events occur.

**Key concepts:**
- **Event markers:** Digital triggers or codes sent through a dedicated channel
  - **Wearable Sensing devices:** Use 'Trigger' or 'TRG' channel (DSI-24, DSI-VR300, DSI-7)
  - **Alternative names:** 'TRIG', 'STI 014' (for compatibility with other systems)
- **Event ID:** Mapping of event codes to meaningful labels (e.g., `{'target': 1, 'nontarget': 2}`)
- **Time window:** Period before (`tmin`) and after (`tmax`) each event to extract
- **Baseline correction:** Removes DC offset by subtracting pre-stimulus activity

**Common use cases:**
- **Event-Related Potentials (ERPs):** Average epochs to reveal time-locked brain responses (P300, N170, etc.)
- **Frequency analysis:** Compute time-frequency representations on epochs to study oscillatory activity
- **BCI classification:** Extract features from epochs for real-time machine learning

---

## Creating an EpochsStream

The `EpochsStream` wraps a `StreamLSL` object and monitors it for events in real-time:

```{code-block} python
:caption: Create an EpochsStream to extract event-related data

from mne_lsl.stream import StreamLSL, EpochsStream
import time

# Connect to stream and apply filtering
stream = StreamLSL(bufsize=10, name="DSI-24").connect()
stream.filter(l_freq=0.5, h_freq=40.0)

# Create epochs stream
epochs_stream = EpochsStream(
    stream=stream,           # StreamLSL object to monitor
    bufsize=20,              # Maximum number of epochs to store
    event_id={'stimulus': 1},  # Event code 1 = 'stimulus'
    event_channels='Trigger',  # Channel containing event markers
    tmin=-0.2,               # Start 200ms before event
    tmax=0.8,                # End 800ms after event
    baseline=(-0.2, 0),      # Baseline correction period
).connect()

print(f"Epoch duration: {epochs_stream.tmax - epochs_stream.tmin:.2f}s")
print(f"Monitoring for events on channel: {epochs_stream.event_channels}")
```

**Parameters explained:**
- `bufsize`: Number of epochs to keep in memory (older epochs are discarded when full)
- `event_id`: Dictionary mapping event labels to numeric codes in the trigger channel
- `tmin/tmax`: Define the epoch window relative to the event onset (in seconds, negative for pre-stimulus)
- `baseline`: Time period for baseline correction (typically pre-stimulus, e.g., `(-0.2, 0)` for 200ms before event)

**Multiple event types:**
```{code-block} python
:caption: Monitor multiple event types simultaneously

epochs_stream = EpochsStream(
    stream=stream,
    bufsize=50,
    event_id={'left_hand': 1, 'right_hand': 2, 'feet': 3},
    event_channels='Trigger',
    tmin=-0.5,
    tmax=3.0,
).connect()
```

**Artifact rejection:**
```{code-block} python
:caption: Apply automatic artifact rejection to epochs

epochs_stream = EpochsStream(
    stream=stream,
    bufsize=20,
    event_id={'stimulus': 1},
    event_channels='Trigger',
    tmin=-0.2,
    tmax=0.8,
    reject={'eeg': 100e-6},  # Reject epochs with EEG > 100 μV
).connect()
```

---

## Retrieving Epoch Data

Once epochs are being collected, retrieve them using the `get_data()` method:

```{code-block} python
:caption: Retrieve accumulated epochs from stream

# Wait for epochs to accumulate
print("Waiting for epochs...")
while epochs_stream.n_new_epochs < 10:
    time.sleep(0.5)
    print(f"  Collected: {epochs_stream.n_new_epochs} new epochs")

# Get all epochs from buffer
epochs = epochs_stream.get_data()
print(f"Epochs shape: {epochs.shape}")  # (n_epochs, n_channels, n_times)
print(f"Time points per epoch: {len(epochs_stream.times)}")

# Get only the most recent epochs
new_epochs = epochs_stream.get_data(n_epochs=5)
print(f"Retrieved last 5 epochs: {new_epochs.shape}")

# Clean up
epochs_stream.disconnect()
stream.disconnect()
```

The returned array has shape `(n_epochs, n_channels, n_times)`:
- **n_epochs:** Number of trials/events
- **n_channels:** Number of EEG channels
- **n_times:** Samples in the epoch time window

---

## Using Epoch Data

After retrieving epochs, you can analyze them for ERPs, classification, or other analyses:

### Computing Event-Related Potentials (ERPs)

Average across trials to reveal consistent brain responses:

```{code-block} python
:caption: Compute ERP from real-time epochs

import numpy as np

# Collect 30 stimulus epochs
while epochs_stream.n_new_epochs < 30:
    time.sleep(0.5)

epochs = epochs_stream.get_data()

# Compute ERP (average across trials)
erp = epochs.mean(axis=0)  # Shape: (n_channels, n_times)

# Find peak response at Pz electrode
pz_idx = epochs_stream.info['ch_names'].index('Pz')
peak_idx = np.argmax(np.abs(erp[pz_idx, :]))
peak_time = epochs_stream.times[peak_idx]
peak_amplitude = erp[pz_idx, peak_idx]

print(f"Peak at Pz: {peak_amplitude*1e6:.2f} μV at {peak_time*1000:.0f} ms")
```

### Converting to MNE Epochs Object

For advanced offline analysis, convert to MNE's `Epochs` object:

```{code-block} python
:caption: Convert EpochsStream to MNE Epochs for offline analysis

import mne

# Get epoch data and info
epochs_data = epochs_stream.get_data()
info = epochs_stream.info

# Create MNE Epochs object
# Note: You'll need to create an events array
n_epochs = epochs_data.shape[0]
events = np.column_stack([
    np.arange(n_epochs),           # Event sample indices
    np.zeros(n_epochs, dtype=int), # Duration (unused)
    np.ones(n_epochs, dtype=int)   # Event IDs
])

mne_epochs = mne.EpochsArray(
    epochs_data,
    info,
    events=events,
    tmin=epochs_stream.tmin,
    event_id={'stimulus': 1}
)

# Now use MNE analysis tools
mne_epochs.plot_image(picks='Pz')
mne_epochs.average().plot()
```

### Extracting Features for Classification

Use epoch data as input to machine learning models:

```{code-block} python
:caption: Extract bandpower features from epochs for ML

# Compute bandpower features per epoch
from scipy.integrate import simpson
from mne.time_frequency import psd_array_welch

features = []
for epoch in epochs:
    # Compute PSD for each channel
    psd, freqs = psd_array_welch(epoch, sfreq=epochs_stream.info['sfreq'], 
                                   fmin=8, fmax=13, verbose=False)
    # Average alpha power across channels
    alpha_power = simpson(psd, dx=freqs[1]-freqs[0], axis=-1).mean()
    features.append(alpha_power)

features = np.array(features)
print(f"Alpha power per epoch: {features}")
```

See {doc}`../classification/bci` for complete classification examples.

---

## Monitoring Real-Time Performance

Track epoch collection in real-time loops:

```{code-block} python
:caption: Monitor and process epochs in real-time loop

from mne_lsl.stream import StreamLSL, EpochsStream
import time

stream = StreamLSL(bufsize=10, name="DSI-24").connect()
stream.filter(l_freq=0.5, h_freq=40.0)

epochs_stream = EpochsStream(
    stream=stream,
    bufsize=50,
    event_id={'target': 1, 'nontarget': 2},
    event_channels='Trigger',
    tmin=-0.2,
    tmax=0.8,
    baseline=(-0.2, 0),
).connect()

print("Monitoring for events... (Press Ctrl+C to stop)")

try:
    while True:
        if epochs_stream.n_new_epochs > 0:
            # Process new epochs
            new_epochs = epochs_stream.get_data(n_epochs=epochs_stream.n_new_epochs)
            print(f"Processed {new_epochs.shape[0]} new epoch(s)")
            
            # Example: Check average amplitude
            avg_amp = np.abs(new_epochs).mean()
            print(f"  Average amplitude: {avg_amp*1e6:.2f} μV")
        
        time.sleep(0.1)
        
except KeyboardInterrupt:
    print(f"\nTotal epochs collected: {len(epochs_stream.get_data())}")
    
finally:
    epochs_stream.disconnect()
    stream.disconnect()
```

---

## Troubleshooting

**No epochs are created:**
- Verify trigger channel name matches your hardware setup
  - For Wearable Sensing devices: Common names are `'Trigger'`, `'TRIG'`, or `'STI 014'`
  - Check DSI-Streamer configuration for your trigger channel name
- Check event codes match what your stimulus software sends
- Ensure trigger channel is properly configured in DSI-Streamer
- Verify triggers are being sent (monitor trigger channel in {doc}`StreamViewer <../visualization/viewer>`)

**Missing epochs:**
- Increase `bufsize` in StreamLSL to capture events further back
- Check that `tmin` doesn't require data before the event that isn't buffered
- Verify event timing aligns with data availability

**Memory issues:**
- Reduce `bufsize` in EpochsStream to keep fewer epochs in memory
- Process epochs in smaller batches using `get_data(n_epochs=N)`

---

## Resources

- [EpochsStream API](https://mne.tools/mne-lsl/stable/generated/api/mne_lsl.stream.EpochsStream.html) | [MNE-LSL Epoching Tutorial](https://mne.tools/mne-lsl/stable/generated/tutorials/40_epochs.html)
- [Real-time Evoked Responses Example](https://mne.tools/mne-lsl/stable/generated/examples/30_real_time_evoked_responses.html)
- {doc}`MNE-Python Epochs <../../python/processing/epochs>` | {doc}`Filtering <filter>`
