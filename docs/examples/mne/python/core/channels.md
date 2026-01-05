# Channel Configuration
---

Configure channel properties, manage channel selection, and set up referencing for your EEG data.

```{admonition} Prerequisites
:class: note
This guide assumes you have already loaded your EEG data into a `raw` object. See {doc}`Load Wearable Sensing Data <load>` for details on loading EDF files.
```

## Setting Channel Types

MNE uses channel types to apply appropriate processing and visualization. For Wearable Sensing headsets, most channels will be EEG, but you may have auxiliary channels (EMG, EOG, ECG).

```python
import mne

# Set channel types for auxiliary channels
raw.set_channel_types({
    'EEG X1:EMG-Pz': 'emg',
    'EEG X2:EOG-Pz': 'eog',
    'Trigger': 'stim',
    'Event': 'stim'
})

print('Channel types:', raw.get_channel_types())
```

**Common channel types:**
- `'eeg'` - EEG channels (default)
- `'eog'` - Electrooculography (eye movements)
- `'emg'` - Electromyography (muscle activity)
- `'ecg'` - Electrocardiography (heart activity)
- `'stim'` - Stimulus/trigger channels

```{admonition} Channel Type Resources
:class: tip
See [MNE Channel Types](https://mne.tools/stable/auto_tutorials/intro/40_sensor_locations.html) for more information on channel types and how they affect processing.
```

---

## Managing Channels

### Dropping Unwanted Channels

Remove channels that are not relevant to your analysis:

```python
# Remove auxiliary and reference channels
channels_to_remove = ['EEG X1:EMG-Pz', 'EEG X2:EOG-Pz', 'EEG X3:-Pz', 'CM']
raw.drop_channels(channels_to_remove)

print('Remaining channels:', raw.ch_names)
```

### Selecting Specific Channels

Pick only the channels you need:

```python
# Select only EEG channels
raw_eeg = raw.copy().pick('eeg')

# Select specific channels by name
selected_channels = ['EEG F3-Pz', 'EEG F4-Pz', 'EEG C3-Pz', 'EEG C4-Pz']
raw_selected = raw.copy().pick(selected_channels)
```

### Marking Bad Channels

Identify and mark channels with excessive noise:

```python
# Mark channels as bad
raw.info['bads'] = ['EEG Fp1-Pz', 'EEG T3-Pz']

# Bad channels will be excluded from average reference and can be interpolated later
print('Bad channels:', raw.info['bads'])
```

```{admonition} Interpolating Bad Channels
:class: note
After marking bad channels, you can interpolate them using `raw.interpolate_bads()`. This replaces bad channel data with interpolated values from neighboring channels. See [Handling Bad Channels](https://mne.tools/stable/auto_tutorials/preprocessing/15_handling_bad_channels.html) for details.
```

### Reordering Channels

Organize channels in a preferred order for visualization:

```python
# Define desired channel order (DSI-24 example)
desired_order = [
    'EEG Fp1-Pz', 'EEG Fp2-Pz', 'EEG Fz-Pz', 'EEG F3-Pz', 'EEG F4-Pz',
    'EEG F7-Pz', 'EEG F8-Pz', 'EEG Cz-Pz', 'EEG C3-Pz', 'EEG C4-Pz',
    'EEG T3-Pz', 'EEG T4-Pz', 'EEG T5-Pz', 'EEG T6-Pz',
    'EEG Pz-Pz', 'EEG P3-Pz', 'EEG P4-Pz', 'EEG O1-Pz', 'EEG O2-Pz',
    'EEG A1-Pz', 'EEG A2-Pz', 'Trigger', 'Event'
]

# Only reorder channels that exist in data
channels_to_reorder = [ch for ch in desired_order if ch in raw.ch_names]
raw = raw.reorder_channels(channels_to_reorder)

print('Reordered channels:', raw.ch_names)
```

---

## EEG Referencing

The reference electrode provides the baseline for voltage measurements. Wearable Sensing headsets use Pz as the hardware reference, but you can re-reference to other schemes.

### Understanding References

**Hardware Reference (Factory Default):**
- **DSI-24 / DSI-7:** Pz
- **VR300:** P4
- Data from DSI-Streamer uses this reference

**Linked Ears Reference:**
- Average of A1 and A2 electrodes (A1/2+A2/2)
- Common in EEG research
- Good general-purpose reference

**Average Reference:**
- Average of all EEG channels
- Useful for topographic mapping and source localization
- Required for some analyses

### Re-Referencing to Linked Ears

```python
# Re-reference to linked ears (average of A1 and A2)
ref_channels = ['EEG A1-Pz', 'EEG A2-Pz']
raw.set_eeg_reference(ref_channels=ref_channels)

print(f'Reference set to: {raw.info["custom_ref_applied"]}')
```

### Re-Referencing to Average

```python
# Re-reference to average of all EEG channels
raw.set_eeg_reference(ref_channels='average')

print('Reference set to average of all EEG channels')
```

### Re-Referencing to a Single Channel

```python
# Re-reference to a specific channel (e.g., Cz)
raw.set_eeg_reference(ref_channels=['EEG Cz-Pz'])
```

### Renaming Channels After Re-Referencing

After re-referencing, update channel names to reflect the new reference:

```python
# Rename channels from '-Pz' to '-LE' (Linked Ears)
rename_dict = {}
for ch_name in raw.ch_names:
    if '-Pz' in ch_name:
        rename_dict[ch_name] = ch_name.replace('-Pz', '-LE')
    elif ch_name == 'Pz':
        rename_dict[ch_name] = 'Pz-LE'

raw.rename_channels(rename_dict)
print('Renamed channels:', raw.ch_names)
```

Or rename to standard 10-20 names (removes reference suffix):

```python
# Remove reference suffix for standard naming
rename_dict = {}
for ch_name in raw.ch_names:
    if '-Pz' in ch_name:
        rename_dict[ch_name] = ch_name.replace('-Pz', '')
    # Note: Pz becomes the reference when re-referencing, so it may need special handling

raw.rename_channels(rename_dict)
```

```{admonition} Reference Best Practices
:class: tip
- **For ERPs:** Linked ears or mastoid reference is common
- **For source localization:** Average reference is often required
- **For connectivity analysis:** Average reference is recommended
- See [Setting the EEG Reference](https://mne.tools/stable/auto_tutorials/preprocessing/55_setting_eeg_reference.html) for detailed guidance
```

---

## Complete Channel Setup Example

Here's a complete workflow combining channel management and referencing:

```python
import mne

# Load data
raw = mne.io.read_raw_edf('recording.edf', preload=True)

# Set channel types
raw.set_channel_types({
    'EEG X1:EMG-Pz': 'emg',
    'EEG X2:EOG-Pz': 'eog',
    'Trigger': 'stim',
    'Event': 'stim'
})

# Mark bad channels (if any)
raw.info['bads'] = ['EEG Fp1-Pz']  # Example: noisy channel

# Interpolate bad channels
raw.interpolate_bads(reset_bads=True)

# Drop auxiliary channels for EEG analysis
raw.drop_channels(['EEG X1:EMG-Pz', 'EEG X2:EOG-Pz', 'EEG X3:-Pz', 'CM'])

# Re-reference to linked ears
raw.set_eeg_reference(ref_channels=['EEG A1-Pz', 'EEG A2-Pz'])

# Rename channels to reflect new reference
rename_dict = {ch: ch.replace('-Pz', '-LE') 
               for ch in raw.ch_names if '-Pz' in ch}
if 'Pz' in raw.ch_names:
    rename_dict['Pz'] = 'Pz-LE'
raw.rename_channels(rename_dict)

# Verify setup
print(f'Channels: {len(raw.ch_names)}')
print(f'Bad channels: {raw.info["bads"]}')
print(f'Reference: {raw.info["custom_ref_applied"]}')
```

---

## Additional Resources

**MNE Documentation:**
- [Handling Bad Channels](https://mne.tools/stable/auto_tutorials/preprocessing/15_handling_bad_channels.html)
- [Setting the EEG Reference](https://mne.tools/stable/auto_tutorials/preprocessing/55_setting_eeg_reference.html)
- [Channel Types Tutorial](https://mne.tools/stable/auto_tutorials/intro/40_sensor_locations.html)

**API References:**
- [`raw.set_channel_types()`](https://mne.tools/stable/generated/mne.io.Raw.html#mne.io.Raw.set_channel_types)
- [`raw.set_eeg_reference()`](https://mne.tools/stable/generated/mne.io.Raw.html#mne.io.Raw.set_eeg_reference)
- [`raw.drop_channels()`](https://mne.tools/stable/generated/mne.io.Raw.html#mne.io.Raw.drop_channels)
- [`raw.interpolate_bads()`](https://mne.tools/stable/generated/mne.io.Raw.html#mne.io.Raw.interpolate_bads)
