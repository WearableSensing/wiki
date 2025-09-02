# Update Reference Channel
--------------------------------------------------------------------------------------

This section will guide you through the process of updating the reference channel in your EEG data using MNE-Python. The DSI-24 system uses Pz as the hardware reference point, but it is often beneficial to re-reference to a more common standard, such as Linked Ears (average of A1 and A2 electrodes).

The `raweegdata` object is assumed to be your loaded EEG data, as shown in the previous sections. See {doc}`MNE Load <../core/load>` for more details on loading EEG data.

## Re-Referencing EEG Data
--------------------------------------------------------------------------------------

This code will change the reference to a more commonly used Linked Ear Reference, which is calculated as the average of the A1 and A2 electrodes.

```{code-block} python
:caption: Update Reference Channel

ref_channels_for_average = ['EEG A1-Pz', 'EEG A2-Pz'] # Insert in this List the Channels you want to reference
raweegdata.set_eeg_reference(ref_channels=ref_channels_for_average)
print('Available channels (After Re-Referencing):', raweegdata.ch_names)
```

This code sets the original EEG Data to a new reference which is Linked Ears (Average of A1 and A2). Make sure the channels are spelled correctly and exist in your EEG Data.

## Renaming Channel References to Reflect Linked-Ears (LE) Average
--------------------------------------------------------------------------------------

Even after the EEG Data has been Re-Referenced to the average of the A1 and A2 electrodes (Linked Ears, or LE), the channel names ending with '-Pz' still persist. The next part of the code will change such names ending with '-Pz' to '-LE' and reflect the changes visually.

```{code-block} python
:caption: Rename Reference Channels
# For loop that renames every channel ending with '-Pz' to '-LE' (Linked Ears, '-A1/A2 Average')
renamed_channels = {}
for ch_name in raweegdata.ch_names:
    if '-Pz' in ch_name:
        renamed_channels[ch_name] = ch_name.replace('-Pz', '-LE')
    elif ch_name == 'Pz': # Assuming 'Pz' was the channel that was originally being referenced
        renamed_channels[ch_name] = 'Pz-LE' # Now 'Pz' is referenced to Linked Ears (LE)

# Apply the new channel names to the object
raweegdata.rename_channels(renamed_channels)
print('Available channels (After Renaming):', raweegdata.ch_names)
```

It may be preferable to rename the channels as the base channel name, regardless of reference as several methods in MNE will require valid 10-20 channel names. This code will rename the channels ending with '-Pz' to '-LE' (Linked Ears) and reflect the changes visually.
