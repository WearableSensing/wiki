# Filtering
---

Apply frequency filters to remove noise and isolate signals of interest.

## Applying Filters

1. **Tools → Filter data**
2. Set filter parameters:
   - **High-pass:** Removes slow drifts (e.g., 0.5 Hz)
   - **Low-pass:** Removes high-frequency noise (e.g., 40 Hz)
   - **Notch:** Removes specific frequencies (e.g., 50/60 Hz line noise)
3. Click **Apply**

## Common Filter Settings

Different analyses require different filter settings:

### ERP Analysis

**Recommended:** 0.1 - 50 Hz

For specific ERP components, see:
> Zhang, G., Garrett, D. R., & Luck, S. J. (2024). Optimal filters for ERP research II: Recommended settings for seven common ERP components. Psychophysiology, 61, e14530. https://doi.org/10.1111/psyp.14530

### Spectral Analysis

**Recommended:** 0.5 - 50 Hz
- Removes very slow drifts while preserving oscillatory activity
- Adjust upper limit based on sampling rate and analysis goals

### Time-Frequency Analysis

**Recommended:** 1 - 40 Hz
- Broader than spectral to avoid edge artifacts in wavelet analysis

## Filter Types

MNELAB uses FIR (Finite Impulse Response) filters by default:

**Advantages:**
- Linear phase (no temporal distortion)
- Stable and predictable

**Considerations:**
- Introduces group delay
- Can create edge artifacts (use longer recordings or crop after filtering)

```{admonition} Filter Order
:class: note
MNELAB automatically calculates appropriate filter order based on your settings. Higher-order filters have sharper cutoffs but longer edge artifacts.
```

## Visualizing Filter Effects

After filtering, compare before and after:

1. Use the sidebar version selector to switch between original and filtered data
2. **Plot → Plot power spectral density** to see frequency content changes

---

## Performance Issues

**Problem:** MNELAB is slow with large files  
**Solution:**
- Close other applications to free memory
- Consider downsampling: **Tools → Resample**
- Process data in shorter segments
