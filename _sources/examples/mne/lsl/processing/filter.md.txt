# Filtering

Apply filters to live data streams from your Wearable Sensing headset for cleaner signals and better analysis. MNE-LSL by default uses IIR (Infinite Impulse Response) causal filters that process incoming data in real-time without introducing delays, making them suitable for neurofeedback and BCI applications.

```{admonition} Prerequisites
:class: note
Familiarity with {doc}`connecting to Wearable Sensing streams <connect>` and MNE-Python {doc}`filtering concepts <../../python/processing/filter>`
```
---

## Why Filter Real-Time Data?

Real-time filtering removes unwanted signal components as data arrives from your Wearable Sensing DSI-24, DSI-VR300, or DSI-7 headset:

- **Band-pass filtering** isolates specific frequency ranges of interest (e.g., alpha waves, motor rhythms)
- **Notch filtering** eliminates powerline interference (50/60 Hz) and harmonics
- **High-pass filtering** removes slow drifts and DC offsets
- **Low-pass filtering** reduces high-frequency noise and muscle artifacts

---


## Applying Filters to Streams

Filters are applied directly to the `StreamLSL` object and automatically process all new data as it arrives. Once applied, the filter persists until explicitly removed with `stream.del_filter()` or the stream is disconnected.

### Band-Pass Filter

Band-pass filtering keeps only frequencies within a specified range, combining high-pass and low-pass characteristics. This is commonly used to focus on specific brain rhythms or remove both DC drift and high-frequency noise simultaneously.

```{code-block} python
:caption: Apply real-time band-pass filter to LSL stream

from mne_lsl.stream import StreamLSL
import time

# Connect to stream
stream = StreamLSL(bufsize=10, name="DSI-24").connect()

# Apply band-pass filter (1-40 Hz) to EEG channels
# This removes DC drift below 1 Hz and high-frequency noise above 40 Hz
stream.filter(l_freq=1.0, h_freq=40.0, picks='eeg')

print("Applied 1-40 Hz band-pass filter")

# Wait for buffer to fill with filtered data
time.sleep(2.0)

# Get filtered data
data, timestamps = stream.get_data(winsize=5.0)
print(f"Retrieved {data.shape[1]} samples of filtered data")

stream.disconnect()
```
---

## Notch Filtering

Notch filters remove narrow frequency bands, typically powerline noise at 50 Hz (Europe/Asia) or 60 Hz (North America). Removing these artifacts is essential for clean EEG analysis.

```{code-block} python
:caption: Remove 60 Hz powerline noise with notch filter

from mne_lsl.stream import StreamLSL
import time

stream = StreamLSL(bufsize=10, name="DSI-24").connect()

# Remove 60 Hz powerline noise (use 50.0 for Europe/Asia)
stream.notch_filter(freqs=60.0, picks='eeg')

print("Applied 60 Hz notch filter")
time.sleep(2.0)

data, ts = stream.get_data(winsize=5.0)
stream.disconnect()
```

---

## Combining Filters

You can apply multiple filters in sequence to achieve comprehensive signal cleaning. The order matters: typically apply notch filters before band-pass filters for optimal results.

```{code-block} python
:caption: Combine notch and band-pass filters sequentially

from mne_lsl.stream import StreamLSL
import time

stream = StreamLSL(bufsize=10, name="DSI-24").connect()

# Step 1: Remove powerline noise
stream.notch_filter(freqs=60.0, picks='eeg')

# Step 2: Apply band-pass filter
stream.filter(l_freq=0.5, h_freq=40.0, picks='eeg')

print("Applied notch + band-pass filters")
time.sleep(2.0)

# All retrieved data is now filtered
data, ts = stream.get_data(winsize=5.0)
print(f"Data shape: {data.shape}")

stream.disconnect()
```

```{admonition} Best Practices
:class: tip
**Filter order:** Apply notch filters before band-pass filters to remove line noise first, then shape the frequency response.

**Channel selection:** Use `picks='eeg'` to apply filters only to EEG channels, avoiding re-referencing or trigger channels.
```

---

## High-Pass and Low-Pass Filters

You can apply high-pass or low-pass filters individually by setting one frequency to `None`:

**High-pass only (remove slow drifts):**
```{code-block} python
:caption: Apply high-pass filter to remove slow drifts

stream = StreamLSL(bufsize=10, name="DSI-24").connect()
stream.filter(l_freq=0.5, h_freq=None, picks='eeg')  # Remove < 0.5 Hz
```

**Low-pass only (remove high-frequency noise):**
```{code-block} python
:caption: Apply low-pass filter to remove high-frequency noise

stream = StreamLSL(bufsize=10, name="DSI-24").connect()
stream.filter(l_freq=None, h_freq=40.0, picks='eeg')  # Remove > 40 Hz
```

---

## Monitoring Filter State

Check which filters are currently applied to your stream:

```{code-block} python
:caption: Check active filters on stream

stream = StreamLSL(bufsize=10, name="DSI-24").connect()
stream.filter(l_freq=1.0, h_freq=40.0, picks='eeg')
stream.notch_filter(freqs=60.0, picks='eeg')

print(f"Active filters: {len(stream.filters)}")
for i, filt in enumerate(stream.filters):
    print(f"  Filter {i}: {filt}")
```

**Remove filters:**
```{code-block} python
:caption: Remove active filters from stream

# Remove all filters
stream.del_filter('all')

# Remove specific filter by index
stream.del_filter(idx=0)
```

---

## Custom Filtering with Callbacks

For advanced processing beyond the built-in filters, use the `add_callback()` method to apply custom transformations to your data stream. Callbacks are functions that process data as it arrives.

**Callback signature:**
```{code-block} python
:caption: Custom callback function signature

def my_callback(data, timestamps, info):
    """
    Process incoming data.
    
    Parameters
    ----------
    data : array, shape (n_times, n_channels)
        Data array from the stream
    timestamps : array, shape (n_times,)
        Timestamp array
    info : mne.Info
        Stream metadata (sampling rate, channel names, etc.)
    
    Returns
    -------
    data : array, shape (n_times, n_channels)
        Modified data
    timestamps : array, shape (n_times,)
        Modified or unchanged timestamps
    """
    # Your custom processing here
    # Example: simple scaling
    data = data * 2.0
    
    return data, timestamps
```

**Using callbacks:**
```{code-block} python
:caption: Apply custom filter using callback function

from mne_lsl.stream import StreamLSL
import time

# Define your custom processing
def alpha_band_filter(data, timestamps, info):
    """Apply custom alpha band filter (8-13 Hz)."""
    # Your filtering implementation here
    # Can use scipy, custom algorithms, etc.
    return data, timestamps

# Connect and add callback
stream = StreamLSL(bufsize=10, name="DSI-24").connect()
stream.add_callback(alpha_band_filter)

print("Applied custom filter via callback")

# Data retrieved will be automatically processed
data, ts = stream.get_data(winsize=5.0)

stream.disconnect()
```

---

## Next Steps

Now that you can filter streams in real-time:
1. {doc}`Visualize filtered streams <../visualization/viewer>` - See filtering effects in real-time
2. {doc}`Create epochs <epochs>` from filtered data - Extract event-related segments
3. {doc}`Build BCIs <../classification/bci>` - Use clean signals for neurofeedback and classification


## Resources

- [filter API](https://mne.tools/mne-lsl/stable/generated/api/mne_lsl.stream.StreamLSL.html#mne_lsl.stream.StreamLSL.filter) | [notch_filter API](https://mne.tools/mne-lsl/stable/generated/api/mne_lsl.stream.StreamLSL.html#mne_lsl.stream.StreamLSL.notch_filter)
- {doc}`MNE-Python filtering concepts <../../python/processing/filter>` | {doc}`Stream Connection <connect>`

