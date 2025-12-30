# Getting Started with Python

> **Python tutorial** — Learn to connect, configure, and acquire EEG data using the DSI API in Python.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Tutorial 1: Basic Connection](#tutorial-1-basic-connection)
- [Tutorial 2: Channel Configuration](#tutorial-2-channel-configuration)
- [Tutorial 3: Data Acquisition](#tutorial-3-data-acquisition)
- [Tutorial 4: Background Acquisition](#tutorial-4-background-acquisition)
- [Common Tasks](#common-tasks)
- [Next Steps](#next-steps)

---

## Prerequisites

### Required Components

- Python 2.6 or later (Python 3.x highly recommended)
- DSI API library (`DSI.dll` / `DSI.so` / `DSI.dylib`)
- Python wrapper and demo scripts (`DSI.py`)

### Installation

1. Download the latest API release from the [Downloads](../../help/downloads/index.md) page
2. Copy `DSI.py` and the platform-specific library to your project directory:
   - **Windows:** `DSI.dll`
   - **Linux:** `DSI.so`
   - **macOS:** `DSI.dylib`

No additional packages are required - the Python wrapper uses only standard library components.

---

## Quick Start

This minimal example demonstrates the essential steps to connect to a headset, configure channels, and acquire data. Copy this code to get started quickly, then explore the detailed tutorials below for more information.

```python
from DSI import Headset

# Connect to headset
h = Headset()
h.Connect(None)  # None uses DSISerialPort environment variable
print("Connected!")

# Configure channels
# Using "" for reference lets API use its auto-detected default
# (linked ears if available, otherwise factory reference)
h.ChooseChannels("P3,Pz,P4", "", True)

# Start acquisition
h.StartDataAcquisition()

# Collect data using Channels() helper
for i in range(10):
    h.Idle(0.1)  # Process for 100ms
    
    # Read buffered samples from first channel
    channels = h.Channels()
    if channels and channels[0].GetNumberOfBufferedSamples() > 0:
        value = channels[0].ReadBuffered()
        print(f"Sample {i}: {channels[0].GetName()} = {value:.2f} µV")

# Cleanup
h.StopDataAcquisition()
```

### Quick Test

The `DSI.py` file is runnable as-is for quick testing:

```bash
# The default port is COM6 for Windows, or /dev/cu.DSI7-*.BluetoothSeri for macOS
# You can edit the default_port variable in DSI.py if needed
python DSI.py

# Or pass port as command-line argument
python DSI.py COM4                                   # Windows
python DSI.py /dev/ttyUSB0                           # Linux
python DSI.py /dev/cu.DSI24-023-BluetoothSerial      # macOS

# Optional second argument for reference or impedance mode
python DSI.py COM4 A1+A2      # Use A1+A2 reference
python DSI.py COM4 impedances # Run impedance test
```

---

## Tutorial 1: Basic Connection

This tutorial walks through establishing a connection to your DSI headset. You'll learn how to import the API, specify serial ports, create headset objects, and handle errors using Python's exception mechanism.

### Step 1: Import the API

The Python wrapper provides a simple object-oriented interface to the DSI API. Start by importing the `Headset` class, which represents your EEG device.

```python
from DSI import Headset
```

### Step 2: Specify Port or Use Environment Variable

The headset connects via a serial port, which varies by platform and connection type (Bluetooth, USB). You can either specify the port directly or use an environment variable for convenience.

**Port specification by platform:**
- **Windows:** COM ports (e.g., `'COM4'`, `'COM5'`, `'COM6'`)
- **Linux:** `'/dev/ttyUSB0'`, `'/dev/ttyUSB1'`, `'/dev/ttyACM0'`, `'/dev/ttyACM1'`
- **macOS:** `'/dev/cu.DSI24-xxxxx-BluetoothSerial'` or `'/dev/tty.usbserial-xxxxx'`
- **Environment variable:** Set `DSISerialPort` and pass `None`

```python
import sys

# Option 1: Use environment variable
port = None  # None uses DSISerialPort env variable

# Option 2: Specify port directly
if sys.platform.startswith('win'):
    port = 'COM4'  # Windows
elif sys.platform.startswith('darwin'):
    port = '/dev/cu.DSI24-023-BluetoothSerial'  # macOS
else:
    port = '/dev/ttyUSB0'  # Linux

print(f"Using port: {port if port else 'from DSISerialPort env var'}")
```

### Step 3: Create and Connect Headset Object

```python
try:
    # Create headset object
    h = Headset()
    
    # Connect to the serial port
    h.Connect(port)  # port can be None to use env variable
    
except Exception as e:
    print(f"Failed to connect: {e}")
    exit(1)
```

**What happens during connection:**
1. `Headset()` allocates the headset object
2. `.Connect(port)` opens serial port
3. Queries hardware model and firmware
4. Initializes communication

### Step 4: Verify Connection

After connecting, you can verify the connection status and retrieve device information. This is useful for logging and troubleshooting.

```python
if not h.IsConnected():
    print("Not connected!")
    exit(1)

# Get device information
print(h.GetInfoString())
```

### Step 5: Error Handling

Python exceptions are raised automatically for errors. See [Error Codes](../error_codes.md) for details.

```python
try:
    h = Headset()
    h.Connect(port)
    
except Exception as e:
    print(f"Connection failed: {e}")
    exit(1)
```

### Complete Connection Example

```python
def connect_to_headset(port=None):
    """Connect to DSI headset.
    
    Args:
        port: Serial port path, or None to use DSISerialPort env variable
    
    Returns:
        Headset object if successful, None otherwise
    """
    try:
        # Create and connect
        h = Headset()
        h.Connect(port)  # None uses DSISerialPort env variable
        
        # Get device info
        print(h.GetInfoString())
        
        return h
    except Exception as e:
        print(f"Connection failed: {e}")
        return None

# Usage
h = connect_to_headset()
if h is None:
    exit(1)
```

---

## Tutorial 2: Channel Configuration

Channel configuration (also called montage selection) determines which electrodes to record from and how to reference them. This tutorial covers listing available electrodes, choosing references, and configuring both referential and bipolar montages.

### Understanding Montages

A **montage** defines which electrodes to use and how to reference them.

**Syntax:** `"electrode1,electrode2,electrode3"`

**Common montage examples:**
- `"P3,Pz,P4,O1,O2"` — Five posterior channels
- `"Fp1,Fp2,F3,F4,C3,C4"` — Frontal and central channels  
- `"@1,@2,@3,@4"` — First four sensors (numbered indexing)

**Available channels by model:**

- **DSI-24:** Fp1, Fp2, Fz, F3, F4, F7, F8, Cz, C3, C4, T7/T3, T8/T4, Pz, P3, P4, P7/T5, P8/T6, O1, O2, A1, A2
- **DSI-7:** F3, F4, C3, C4, P3, Pz, P4, LE
- **DSI-VR300:** FCz, Pz, P3, P4, PO7, PO8, Oz, LE

### Step 1: List Available Sources

```python
# Pythonic way: Use the Sources() helper method
for src in h.Sources():
    print(f"{src.GetName()}")

# Or iterate by index
n_sources = h.GetNumberOfSources()
print(f"Total sources: {n_sources}")

for i in range(n_sources):
    src = h.GetSourceByIndex(i)
    print(f"{i}: {src.GetName()}")
```

**Note:** The `Sources()` method is a Python helper that returns a list of all Source objects. This is more Pythonic than the C-style iteration pattern.

### Step 2: Choose Reference

The reference electrode determines the baseline for measuring voltage. **By default, the API automatically uses linked ears (A1+A2 on DSI-24, LE on DSI-7/VR300) as the reference.** You only need to call reference functions if you want to change from this default.

#### Default Reference (Automatic)

No API calls needed - just pass empty string `""` to `ChooseChannels()`:

```python
# Uses default linked ears automatically
h.ChooseChannels("P3,Pz,P4", "", True)
```

**Default reference by model:**
- **DSI-24:** `A1+A2` (average of A1 and A2 channels)
- **DSI-7:** `LE` (pre-averaged linked ear channel)
- **DSI-VR300:** `LE` (pre-averaged linked ear channel)

#### Change to Hardware Reference

To use the hardware/factory reference instead of linked ears:

```python
# Option 1: Use "FACTORY" keyword
h.SetDefaultReference("FACTORY", True)
h.ChooseChannels("P3,Pz,P4", "", True)

# Option 2: Specify hardware reference electrode directly
h.ChooseChannels("P3,Pz,P4", "Pz", True)  # DSI-24/DSI-7
h.ChooseChannels("P3,Pz,P4", "P4", True)  # VR300
```

**Hardware reference by model:**
- **DSI-24:** `Pz`
- **DSI-7:** `Pz`
- **DSI-VR300:** `P4`

#### Change to Custom Reference

To use any electrode as reference (e.g., P3, Cz):

```python
# Option 1: Set default reference, then configure channels
h.SetDefaultReference("P3", True)
h.ChooseChannels("Pz,P4,O1,O2", "", True)

# Option 2: Specify directly in ChooseChannels
h.ChooseChannels("Pz,P4,O1,O2", "P3", True)
```

**To check which reference is active:**
```python
ref = h.GetReferenceString()
print(f"Current reference: {ref}")
```

### Step 3: Configure Channels

```python
# ChooseChannels(montage, reference, autoswap)

# Recommended: Use empty string for default linked ear reference
h.ChooseChannels("P3,Pz,P4,O1,O2", "", True)

# To use hardware reference instead, specify electrode explicitly:
# h.ChooseChannels("P3,Pz,P4,O1,O2", "Pz", True)  # DSI-24/DSI-7
# h.ChooseChannels("P3,Pz,P4,O1,O2", "P4", True)  # VR300

print(f"Configured {h.GetNumberOfChannels()} channels")
```

**Parameters:**
- `montage` — Comma-separated electrode names
- `reference` — Reference electrode(s) specification
- `autoswap` — Automatically swap signal/reference if needed (use `True`)

**Error handling:**
```python
try:
    h.ChooseChannels("P3,Pz,P4,O1,O2", "", True)  # Use auto-detected default
except Exception as e:
    print(f"Montage error: {e}")
    # Troubleshoot: List available sources
    print("Available sources:")
    for src in h.Sources():
        print(f"  {src.GetName()}")
    exit(1)
```

### Step 4: Inspect Channels

Once channels are configured, you can iterate through them to inspect their properties. This helps verify your montage was set up correctly.

```python
n_channels = h.GetNumberOfChannels()

for i in range(n_channels):
    ch = h.GetChannelByIndex(i)
    
    info = f"Channel {i}: {ch.GetName()}"
    
    if ch.IsReferentialEEG():
        info += " (EEG)"
    if ch.IsTrigger():
        info += " (Trigger)"
    
    print(info)
```

### Step 5: Access Channels

The Channels() helper method returns a list of all configured channels, making it easy to iterate and access channel data. This is the pattern used in DSI.py examples.

```python
# Get all channels as a list
channels = h.Channels()

# Access first channel
if channels:
    ch0 = channels[0]
    print(f"First channel: {ch0.GetName()}")

# Find a specific channel by name
pz = None
for ch in channels:
    if ch.GetName() == "Pz":
        pz = ch
        break

if pz:
    print(f"Found channel: {pz.GetName()}")
else:
    print("Channel 'Pz' not found")

# Or use list comprehension (Pythonic)
pz_channels = [ch for ch in channels if ch.GetName() == "Pz"]
if pz_channels:
    pz = pz_channels[0]
```

### Advanced: Bipolar Montages

Bipolar montages record the voltage difference between pairs of electrodes. This is useful for certain EEG analyses like sleep staging or seizure detection.

```python
# Bipolar: Each channel is difference between two electrodes
# Syntax: "electrode1-electrode2"
h.ChooseChannels("Fp1-F3,F3-C3,C3-P3,P3-O1", "", True)

# This creates 4 channels:
# - Fp1-F3 (voltage at Fp1 minus voltage at F3)
# - F3-C3
# - C3-P3
# - P3-O1
```

### Complete Montage Example

```python
def configure_montage(h):
    """Configure a standard posterior montage."""
    
    # Configure a standard posterior montage
    montage = "P3,Pz,P4,O1,O2"
    reference = ""  # Default linked ears
    
    print(f"Montage: {montage}")
    print(f"Reference: {reference}")
    
    try:
        h.ChooseChannels(montage, reference, True)
        print(f"Configured {h.GetNumberOfChannels()} channels")
        return True
    except Exception as e:
        print(f"Montage failed: {e}")
        return False

# Usage
if not configure_montage(h):
    exit(1)
```

---

## Tutorial 3: Data Acquisition

Once your headset is connected and channels are configured, you can start acquiring EEG data. This tutorial covers sampling rate configuration, buffer management, starting/stopping acquisition, and reading data from channels.

### Step 1: Configure Sampling

The default sampling rate is 300 Hz. If the SampleRate feature is unlocked, all DSI headsets can configure rates up to 600 Hz.

```python
# NOTE: The default sampling rate is 300 Hz. If the SampleRate feature is unlocked,
# all DSI headsets can configure rates up to 600 Hz. Check feature availability first:
if h.GetFeatureAvailability("SampleRate"):
    print("Custom sampling rates are available (up to 600 Hz)")
    h.ConfigureADC(600, 0)  # Use 600 Hz when unlocked
else:
    print("Using default sampling rate of 300 Hz (feature not unlocked)")
    h.ConfigureADC(300, 0)  # Default 300 Hz

# Verify actual sampling rate
fs = h.GetSamplingRate()
print(f"Sampling rate: {fs:.0f} Hz")
```

**Filter modes:**
- `0` - No filtering (default)
- `1` - Low-pass filter
- `2` - High-pass filter
- `3` - Band-pass filter

### Step 2: Understanding Buffers

The API automatically manages ring buffers for each channel. Buffers store incoming samples until you read them with `ReadBuffered()`. Understanding buffer management helps prevent data loss.

```python
# Channel buffers are allocated automatically when you configure channels.
# The default buffer size is sufficient for most real-time applications.

# Manual buffer reallocation is only needed if:
# 1. You need to store more than a few seconds of data
# 2. You're using custom processing stages that require larger lookback windows

# Example: Allocate 10 seconds for signal, 5 seconds for impedance
h.ReallocateBuffers(10.0, 5.0)

# Check buffer status during acquisition
buffered = h.GetNumberOfBufferedSamples()
print(f"Buffered samples: {buffered}")
```

### Step 3: Start Acquisition

Once configured, start the data acquisition process. This commands the headset to begin streaming EEG data over the serial connection.

```python
try:
    h.StartDataAcquisition()
    print("Acquisition started")
except Exception as e:
    print(f"Failed to start acquisition: {e}")
    exit(1)
```

### Step 4: Receive Data

The `Idle()` method processes incoming serial data and fills channel buffers. Call it regularly in your main loop, then read buffered samples from each channel.

```python
fs = h.GetSamplingRate()
block_duration = 0.5  # 0.5 second blocks

acquiring = True
while acquiring:
    # Process events and receive data for specified time
    h.Idle(block_duration)
    
    # Read buffered data from each channel (using Channels() helper)
    for ch in h.Channels():
        # Get number of buffered samples
        buffered = ch.GetNumberOfBufferedSamples()
        
        # Read buffered samples one at a time
        for j in range(buffered):
            value = ch.ReadBuffered()
            process_data(ch.GetName(), value)
```

### Step 5: Stop Acquisition

```python
h.StopDataAcquisition()
print("Acquisition stopped")
```

### Complete Acquisition Example

```python
def acquire_data(h, duration_seconds):
    """Acquire data for specified duration."""
    
    block_duration = 0.1  # 100ms blocks
    num_blocks = int(duration_seconds / block_duration)
    
    print(f"Acquiring {duration_seconds:.1f} seconds of data...")
    
    # Start acquisition
    try:
        h.StartDataAcquisition()
    except Exception as e:
        print(f"Start failed: {e}")
        return
    
    # Collect data blocks
    for block in range(num_blocks):
        h.Idle(block_duration)
        
        # Show progress
        if block % 10 == 0:
            progress = 100.0 * block / num_blocks
            print(f"Progress: {progress:.0f}%", end='\r')
        
        # Check for alarms
        if h.GetNumberOfAlarms() > 0:
            alarm = h.GetAlarm(True)  # True = remove from queue
            print(f"\nAlarm: {alarm}")
    
    print("\nAcquisition complete")
    h.StopDataAcquisition()

# Usage
acquire_data(h, 10.0)  # Acquire 10 seconds
```

---

## Tutorial 4: Background Acquisition

Background acquisition runs data collection in a separate thread, freeing your main application to perform other tasks (UI updates, analysis, etc.). This tutorial shows how to set up callbacks that execute automatically when new data arrives.

### Step 1: Set Sample Callback

**Important:** Callback functions must be decorated with `@SampleCallback` or wrapped properly. The callback receives a raw pointer that must be wrapped in a `Headset` object.

```python
from DSI import Headset, SampleCallback

@SampleCallback
def my_sample_callback(headset_ptr, packet_time, user_data):
    """Called automatically when new data arrives.
    
    Args:
        headset_ptr: Raw headset pointer (must wrap with Headset())
        packet_time: Timestamp of the data packet in seconds
        user_data: Optional user data passed to SetSampleCallback
    """
    # Wrap the raw pointer to get a usable Headset object
    h = Headset(headset_ptr)
    
    # Read buffered samples from channels (using Channels() helper)
    for ch in h.Channels():
        value = ch.ReadBuffered()
        print(f"{ch.GetName()}: {value:.2f} µV (time: {packet_time:.3f})")

# Register callback (None for user_data if not needed)
h.SetSampleCallback(my_sample_callback, None)
```

### Step 2: Start Background Acquisition

Background acquisition creates a separate thread that continuously processes serial data and calls your callback function. This frees your main thread for other tasks.

```python
try:
    h.StartBackgroundAcquisition()
    print("Background acquisition running...")
except Exception as e:
    print(f"Background acquisition failed: {e}")
    exit(1)
```

### Step 3: Application Continues

With background acquisition running, your main application thread is free to perform other tasks like updating a UI, running analyses, or monitoring system health.

```python
import time

# Your application can continue other work
# Data collection happens in background thread

for i in range(100):
    # Do other work
    print(f"Main loop iteration {i}")
    time.sleep(0.1)
    
    # Check buffer status
    buffered = h.GetNumberOfBufferedSamples()
    print(f"  Buffered samples: {buffered}")
```

### Step 4: Stop Background Acquisition

```python
h.StopBackgroundAcquisition()
print("Background acquisition stopped")
```

### Complete Background Acquisition Example

```python
import time
from DSI import Headset, SampleCallback

# Global flag to control acquisition
g_acquiring = True

@SampleCallback
def sample_callback(headset_ptr, packet_time, user_data):
    """Process each sample as it arrives."""
    global sample_count
    sample_count = sample_count + 1 if 'sample_count' in globals() else 1
    
    # Wrap the raw headset pointer
    h = Headset(headset_ptr)
    
    # Get channel data using ReadBuffered() like DSI.py examples
    channels = h.Channels()
    pz = None
    for ch in channels:
        if ch.GetName() == "Pz":
            pz = ch
            break
    
    if pz:
        value = pz.ReadBuffered()
        
        # Print every 100 samples
        if sample_count % 100 == 0:
            print(f"Sample {sample_count}: Pz = {value:.2f} µV")

def main():
    global g_acquiring
    
    # Connect and configure
    h = connect_to_headset()
    if h is None:
        exit(1)
    
    if not configure_montage(h):
        exit(1)
    
    # Set callback and start
    h.SetSampleCallback(sample_callback, None)
    h.StartBackgroundAcquisition()
    
    print("Acquiring... Press Ctrl+C to stop")
    
    # Main loop: monitor health
    try:
        while g_acquiring:
            time.sleep(5.0)
            
            # Check for overflow
            overflow = h.GetNumberOfOverflowedSamples()
            if overflow > 0:
                print(f"WARNING: {overflow} samples lost!")
            
            # Check for alarms
            while h.GetNumberOfAlarms() > 0:
                alarm = h.GetAlarm(True)  # True = remove from queue
                print(f"Alarm: {alarm}")
    except KeyboardInterrupt:
        print("\nStopping acquisition...")
    
    h.StopBackgroundAcquisition()

if __name__ == "__main__":
    main()
```

---

## Common Tasks

These practical examples demonstrate frequently needed operations: saving data to files, checking electrode impedances, monitoring battery levels, and integrating with NumPy for numerical analysis.

### Task: Save Data to CSV File

Export EEG data to CSV format for analysis in other tools. This example saves data in a simple time-series format with one row per sample.

```python
import time

def save_to_csv(h, filename, duration):
    """Save data to CSV file."""
    
    with open(filename, 'w') as f:
        # Write header
        f.write("Sample")
        for ch in h.Channels():
            f.write(f",{ch.GetName()}")
        f.write("\n")
        
        # Acquire and save data
        fs = h.GetSamplingRate()
        samples_per_block = int(fs * 0.1)
        num_blocks = int(duration / 0.1)
        
        h.StartDataAcquisition()
        
        sample_number = 0
        
        for block in range(num_blocks):
            h.Idle(samples_per_block / fs)  # Process one block duration
            
            # Read buffered samples (using Channels() helper)
            channels = h.Channels()
            buffered = channels[0].GetNumberOfBufferedSamples()
            
            for samp in range(buffered):
                # Write sample number
                f.write(f"{sample_number}")
                
                # Write channel values
                for ch in channels:
                    value = ch.ReadBuffered()
                    f.write(f",{value:.6f}")
                
                f.write("\n")
                sample_number += 1
        
        h.StopDataAcquisition()
    
    print(f"Saved {filename}")

# Usage
save_to_csv(h, "eeg_data.csv", 10.0)  # Save 10 seconds
```

### Task: Check Impedances

Electrode impedance testing verifies proper skin contact. Lower impedances (below 1MΩ) generally provide better signal quality. Run this before each recording session.

```python
import time

def check_impedances(h):
    """Check electrode impedances."""
    
    print("Starting impedance test...")
    
    # Start impedance driver
    try:
        h.StartImpedanceDriver()
    except Exception as e:
        print(f"Failed to start impedance driver: {e}")
        return
    
    # Wait for readings to stabilize
    time.sleep(2.0)
    
    # Read impedances using Sources() helper (more Pythonic)
    print("\nImpedance readings:")
    print(f"{'Electrode':<10} {'Impedance':>10}")
    print("-" * 24)
    
    for src in h.Sources():
        if src.IsReferentialEEG() and not src.IsFactoryReference():
            name = src.GetName()
            impedance = src.GetImpedanceEEG()
            
            # Quality indicator (thresholds in Ohms)
            if impedance < 1000000:
                quality = "Good"
            elif impedance < 2000000:
                quality = "Fair"
            else:
                quality = "Poor"
            
            print(f"{name:<10} {impedance/1000.0:8.0f} kΩ {quality}")
    
    # Get common-mode fault metric
    cmf = h.GetImpedanceCMF()
    print(f"\nCommon-mode fault: {cmf:.1f}")
    
    h.StopImpedanceDriver()
    print("Impedance test complete")

# Usage
check_impedances(h)
```

### Task: Monitor Battery Level

Monitoring battery level helps prevent unexpected disconnections during recordings. Check battery status before long recording sessions.

```python
import time

def monitor_battery(h):
    """Monitor battery level."""
    
    # Send battery query
    h.SendBatteryQuery()
    
    # Wait for response
    time.sleep(0.5)
    
    # Read level (0 = main battery)
    level = h.GetBatteryLevel(0)
    
    if level < 10.0:
        status = "CRITICAL - Charge now!"
    elif level < 20.0:
        status = "LOW - Charge soon"
    else:
        status = "OK"
    
    print(f"Battery: {level:.1f}% {status}")

# Usage
monitor_battery(h)
```

### Task: Integration with NumPy

For signal processing and analysis, NumPy arrays provide efficient operations. This function acquires data directly into a NumPy array ready for filtering, FFT, or machine learning.

```python
import numpy as np

def acquire_to_numpy(h, duration):
    """Acquire data and return as NumPy array.
    
    Args:
        h: Connected Headset object
        duration: Duration in seconds
        
    Returns:
        tuple: (data array of shape (n_samples, n_channels), sampling_rate)
    """
    # Start acquisition
    h.StartDataAcquisition()
    
    # Get acquisition parameters
    fs = h.GetSamplingRate()
    channels = h.Channels()
    n_channels = len(channels)
    n_samples = int(fs * duration)
    
    # Preallocate array (samples × channels)
    data = np.zeros((n_samples, n_channels))
    
    # Acquire data
    samples_collected = 0
    while samples_collected < n_samples:
        h.Idle(0.1)
        
        # Read from each channel
        for ch_idx, ch in enumerate(channels):
            buffered = ch.GetNumberOfBufferedSamples()
            
            for _ in range(buffered):
                if samples_collected < n_samples:
                    data[samples_collected, ch_idx] = ch.ReadBuffered()
                    if ch_idx == n_channels - 1:
                        samples_collected += 1
    
    h.StopDataAcquisition()
    
    return data, fs

# Usage
data, fs = acquire_to_numpy(h, 5.0)  # 5 seconds
print(f"Acquired data shape: {data.shape}")
print(f"Sampling rate: {fs} Hz")
```

---

## Next Steps

### Explore Advanced Features

- [Quick Reference](../quick_reference.md) - Quick lookup guide for all API functions
- [Error Codes](../error_codes.md) - Complete error code reference
- [C Getting Started](start_c.md) - C version of this guide

### Integration Examples

- [MNE-Python Integration](../../examples/mne/python/index.md) - Use DSI headsets with MNE-Python
- [LSL Integration](../../examples/lsl/index.md) - Stream data via Lab Streaming Layer

### Sample Code

Check the `DSI.py` file in the release package for a complete working example with additional features.

### Support

**Technical support:** Contact WearableSensing support team via the [contact page](../../help/index.md).

---

[Back to Getting Started](index.md) | [Back to API Index](../index.md)
