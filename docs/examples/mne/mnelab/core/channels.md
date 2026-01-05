# Channel Configuration
---

Learn how to configure channel properties and references in MNELAB.

## Setting Channel Properties

If channels aren't automatically recognized or need adjustment:

1. **Edit → Channel properties**
2. Select channel and edit:
   - **Type:** EEG, EOG, ECG, etc.
   - **Units:** µV, mV
   - **Label:** Channel name

```{admonition} Channel Types
:class: note
Correctly setting channel types is important for many processing steps. MNELAB will use this information to apply appropriate filters and analysis methods.
```

## Re-referencing

To change from the default reference:

1. **Tools → Set reference**
2. Choose a reference option:
   - **Average reference:** Uses all EEG channels
   - **Specific channel:** e.g., Pz
   - **Custom:** Specify multiple channels

### Common Reference Schemes

**Average Reference:**
- Uses the mean of all EEG channels
- Good for topographic mapping and source localization
- Not recommended if channels have very different noise levels

**Linked Ears/Mastoids:**
- Default for most Wearable Sensing headsets
- DSI-24: A1/2+A2/2 (average of A1 and A2)
- DSI-7/VR300: LE (pre-averaged)

**Hardware Reference:**
- Pz (DSI-24, DSI-7)
- P4 (VR300)
- Use when you need the original factory reference

```{admonition} Re-referencing Creates New Dataset
:class: tip
Any re-referencing operation creates a new version of your data in MNELAB. The original remains accessible via the sidebar selector on the left, allowing you to compare different reference schemes.
```
