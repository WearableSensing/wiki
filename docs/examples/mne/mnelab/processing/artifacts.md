# Artifact Handling
---

Remove or correct artifacts such as eye blinks, muscle activity, and bad segments.

## Manual Artifact Rejection

Mark bad segments manually:

1. **Plot → Plot data**
2. **Tools → Annotations** to enable annotation mode
3. Mark artifacts by clicking and dragging on the plot
4. Label annotations (e.g., "blink", "movement")

```{admonition} Annotations vs. Rejection
:class: tip
Annotated segments are marked but not deleted. This allows you to:
- Exclude them from epochs/analysis later
- Review annotations before committing
- Keep a record of data quality
```

## Independent Component Analysis (ICA)

Use ICA for automated artifact correction:

### Fitting ICA

1. **Tools → ICA**
2. Click **Fit ICA**
3. Choose number of components (default: all channels)
4. Wait for decomposition (may take time for long recordings)

### Identifying Artifact Components

After fitting, MNELAB displays:
- Time courses of each component
- Topographic maps
- Power spectra

**Common artifacts to look for:**
- **Eye blinks:** Frontal topography, low frequency
- **Lateral eye movements:** Temporal topography, horizontal pattern
- **Muscle activity:** Temporal topography, high frequency
- **Cardiac:** Regular rhythmic pattern

### Removing Components

1. Select artifact components (click to highlight)
2. Click **Apply** to remove selected components
3. A new dataset is created with artifacts removed

```{admonition} ICA Best Practices
:class: note
- Filter data (1-40 Hz) before ICA for better decomposition
- Use enough data (at least 1-2 minutes) for stable components
- Remove extreme artifacts manually before ICA
- Verify component removal doesn't affect signal of interest
```

## Marking Bad Channels

If specific channels are consistently noisy:

1. **Plot → Plot data**
2. Right-click on channel name
3. Select **Mark as bad**
4. Bad channels are excluded from average reference and analyses

```{admonition} Bad Channel Interpolation
:class: tip
After marking bad channels, use **Tools → Interpolate bad channels** to replace them with interpolated values from neighboring channels.
```
