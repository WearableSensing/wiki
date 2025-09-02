# Channel Management and Reordering
--------------------------------------------------------------------------------------

It's important to be able to remove channels that are not relevant to your analysis, contain excessive noise, or are redundant. The following code snippet demonstrates how to remove unwanted channels from your data. Please see the previous section for how to load your data into the `raweegdata` object used below.


The `raweegdata` object is assumed to be your loaded EEG data, as shown in the previous sections. See {doc}`MNE Load <../core/load>` for more details on loading EEG data.

## Remove Unwanted Channels
--------------------------------------------------------------------------------------

```{code-block} python
:caption: Remove Unwanted Channels

channels_to_remove = ['EEG X1:EMG-Pz', 'EEG X2:EOG-Pz','EEG X3:-Pz', 'CM']

raweegdata.drop_channels(channels_to_remove) # Drop specified channels from list

print('Available channels (After Removal):', raweegdata.ch_names)
```

### Defining Channels to Remove (`channels_to_remove`)

Here you can specify channels you want to remove. Remember to spell the Channel Names correct, put quotes for each channel inside of the list and include a Comma after channel you insert. Keep in mind, in the example data file, channels X1 and X2 include the auxiliary sensor name “EMG” and “EOG”, respectively, which may not be the case for your own data file. Furthermore, if you want to include the auxiliary sensor data in your analysis, there is no need to remove these channels

### Dropping Channels (`raweegdata.drop_channels`)

This function modifies your raweegdata object by removing the specified channels from it, these dropped channels won't be visible anymore in your future EEG data processing or visualization. ['EEG X1:EMG-Pz', 'EEG X2:EOG-Pz','EEG X3:-Pz', 'CM'] are in the list, so they will not appear in the final plot.

## Reordering Channels
--------------------------------------------------------------------------------------

After dropping unwanted channels, it may be beneficial to reorder the remaining channels. This helps create easier-to-read plots and match the order of similar software such as DSI-Streamer.

```{code-block} python
:caption: Reorder Channels
# Desired order for channels
desired_channel_order = [
    'EEG Fp1-Pz', 'EEG Fp2-Pz', 'EEG Fz-Pz', 'EEG F3-Pz','EEG F4-Pz',
    'EEG F7-Pz','EEG F8-Pz','EEG Cz-Pz','EEG C3-Pz','EEG C4-Pz',
    'EEG T3-Pz','EEG T4-Pz','EEG T5-Pz','EEG T6-Pz',
    'EEG P3-Pz','Pz','EEG P4-Pz','EEG O1-Pz','EEG O2-Pz','EEG A1-Pz',
    'EEG A2-Pz','EEG X1:EMG-Pz','EEG X2:EOG-Pz', 'EEG X3:-Pz',
    'Trigger','Event'
]
final_reorder_list = [] # Final list with correct order of channels

# For loop that goes through desired_channel_order and puts it into final_reorder_list
for ch in desired_channel_order:
    if ch in raweegdata.info['ch_names']:
        final_reorder_list.append(ch) # Appending channels from eeg data
    else:
        print(f"Warning: Channel '{ch}' from desired_channel_order not found in raweegdata object. Skipping it for reordering.")

# Adds any leftover channels that were not found in desired_order_list
for ch in raweegdata.info['ch_names']:
    if ch not in final_reorder_list:
        final_reorder_list.append(ch)
        print(f"Info: Channel '{ch}' from raweegdata object added to the end of the reorder list.") 

# Applies desired channel order to the raw EEG data object
raweegdata = raweegdata.reorder_channels(final_reorder_list)
print('Available channels (After Reordering):', raweegdata.ch_names)
```

### Defining (`desired_channel_order`)

Here you create a Python list with the names of your channels and order you want them to be in. This is the template your raweegdata object will follow.

### Applying Reorder (`raweegdata.reorder_channels`)

This function takes in the final_reorder_list and updates the raweegdata object to the new order.