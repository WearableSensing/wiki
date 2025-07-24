# Filtering EEG Data 

This section will guide you through the process of filtering EEG data using MNE-Python. Filtering is a crucial step in EEG data preprocessing, as it helps to remove noise and artifacts from the signal. 

## Basic Filtering

To filter your EEG data, you can use the `filter` method provided by MNE on any `Raw` or `Epochs` objects. This method allows you to apply a band-pass filter to your data, which is essential for isolating the frequency bands of interest. By default, MNE applies an FIR zero-phase Butterworth filter, which is suitable for most EEG applications. See the MNE documentation on the filter method for more details: ([mne.io.Raw.filter](https://mne.tools/stable/generated/mne.io.Raw.html#mne.io.Raw.filter)).

We will filter the data between 1 Hz and 40 Hz, which is a common range for EEG analysis, especially for cognitive tasks. The `raweegdata` object is assumed to be your loaded EEG data, as shown in the previous sections, although this will work with any `Raw` or `Epochs` object you have defined. See {doc}`MNE Load <../core/load>` for more details on loading EEG data.

```{admonition} Note

```{code-block} python
:caption: Basic Filtering

# scroll the data without changing the original data
raweegdata.plot()


# filter the data between 1 and 40 Hz
raweegdata.filter(l_freq=1.0, h_freq=40.0)

# scroll the data after filtering
raweegdata.plot()
```

This code will apply a band-pass filter to your EEG data, allowing frequencies between 1 Hz and 40 Hz to pass through while attenuating frequencies outside this range. The `l_freq` parameter sets the lower cutoff frequency, and the `h_freq` parameter sets the upper cutoff frequency. Visualizing the data before and after filtering helps you see the effects of the filter on your EEG signal.

## Advanced Filtering Options

For more advanced filtering options, you can specify additional parameters such as the filter type, the number of taps, and whether to apply a notch filter. MNE provides flexibility in how you apply filters, allowing you to customize the filtering process to suit your specific needs. See the MNE documentation on notch filters for more details: ([mne.io.Raw.notch_filter](https://mne.tools/stable/generated/mne.io.Raw.html#mne.io.Raw.notch_filter)).

```{code-block} python
:caption: Advanced Filtering Options

# Apply a notch filter at 50 Hz to remove power line noise
raweegdata.notch_filter(freqs=50.0, filter_length='auto', phase='zero')

# Apply a band-pass filter with a custom filter window; the default is 'hamming'. 'blackman' is another common choice.
raweegdata.filter(l_freq=1.0, h_freq=40.0, fir_window='hann')

# Apply an IIR band-pass filter with a custom filter type, by default it is a 4th order Butterworth filter
raweegdata.filter(l_freq=1.0, h_freq=40.0, method='iir')
```

### Resources

For more information on processing data in MNE-Python, you can refer to the following resources:

- [MNE Filtering Documentation](https://mne.tools/stable/auto_tutorials/preprocessing/30_filtering_resampling.html)
- [Neural Data Science In Python](https://neuraldatascience.io/intro.html)