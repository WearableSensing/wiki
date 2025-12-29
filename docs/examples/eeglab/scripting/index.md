# Scripting & Command Line
---

You can automate data import using the `pop_WearableSensing` function in your MATLAB scripts.

## Basic Usage

To import a single file:

```matlab
EEG = pop_WearableSensing('C:\Path\To\Your\File.csv');
```

## Arguments

You can pass additional arguments as name-value pairs.

| Argument | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `channels` | Integer Array | All | Vector of channel indices to import. <br>Ex: `[1 3 5]` |
| `blockrange` | [Min Max] | All | Time range in seconds to import. <br>Ex: `[0 60]` |
| `highpass` | Float | Empty | Highpass filter cutoff frequency in Hz. |
| `lowpass` | Float | Empty | Lowpass filter cutoff frequency in Hz. |
| `reref` | String | 'Linked Ears' | Reference scheme: `'Linked Ears'` or `'Hardware Reference'` |
| `removeaux` | String | 'on' | Remove DSI-24 Aux channels? `'on'` or `'off'` |
| `importevent` | String | 'on' | Import trigger events? `'on'` or `'off'` |

### Example

Import the first 60 seconds of data, apply a 1Hz highpass filter, and keep the hardware reference:

```matlab
EEG = pop_WearableSensing('subject01.csv', ...
    'blockrange', [0 60], ...
    'highpass', 1.0, ...
    'reref', 'Hardware Reference');
```

## Batch Processing

The `pop_WearableSensing` function operates on a single file at a time. To process multiple files in a script, use a standard MATLAB `for` loop.

### Example: Import all CSVs in a folder

```matlab
% Define your data directory
dataDir = 'C:\MyExperiments\Study1\';
files = dir(fullfile(dataDir, '*.csv'));

% Loop through each file
for i = 1:length(files)
    fileName = files(i).name;
    fullPath = fullfile(dataDir, fileName);
    
    fprintf('Importing %s...\n', fileName);
    
    % Import the data
    EEG = pop_WearableSensing(fullPath, ...
        'highpass', 0.1, ...
        'lowpass', 70);
        
    % Assign a set name
    EEG.setname = fileName;
    
    % Store in ALLEEG (standard EEGLAB workflow)
    [ALLEEG, EEG, CURRENTSET] = eeg_store(ALLEEG, EEG, 0);
end

eeglab redraw;
```
