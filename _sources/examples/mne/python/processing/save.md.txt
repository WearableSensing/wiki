# Save data using MNE

## Saving Raw Data 

### MNE Format

### Brain Vision Format

### EDF/BDF Format

## Saving Epoched data

### MNE Format


## BIDS Format (Brain Imaging Data Structure)

If data are processed using MNE, using the MNE-BIDS library (https://mne.tools/mne-bids/stable/index.html) can facilitate saving in BIDS format. For example, the following code snippet demonstrates how to save a raw MNE object in BIDS format:

```python
import mne
from mne_bids import BIDSPath, save_bids

# Load your raw data
raw = mne.io.read_raw_fif('path/to/your/file.fif', preload=True)

# Define the BIDS path
bids_path = BIDSPath(subject='01', session='01', task='rest', root='path/to/bids/dataset')

# Save the raw data in BIDS format
save_bids(raw, bids_path)
```

Reading the data from any valid BIDS format is straightforward using the MNE library. Here's an example of how to read BIDS data:

```python
import mne
from mne_bids import BIDSPath, read_bids

# Define the BIDS path
bids_path = BIDSPath(subject='01', session='01', task='rest', root='path/to/bids/dataset')

# Read the BIDS data
raw = read_bids(bids_path)
```