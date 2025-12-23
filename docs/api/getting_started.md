# Getting Started

> **Step-by-step tutorial** — Learn to connect, configure, and acquire EEG data from DSI headsets using the DSI API.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Tutorial 1: Basic Connection](#tutorial-1-basic-connection)
- [Tutorial 2: Channel Configuration](#tutorial-2-channel-configuration)
- [Tutorial 3: Data Acquisition](#tutorial-3-data-acquisition)
- [Tutorial 4: Background Acquisition](#tutorial-4-background-acquisition)
- [Tutorial 5: Real-Time Processing](#tutorial-5-real-time-processing)
- [Next Steps](#next-steps)

---

## Prerequisites

### Hardware
- DSI headset (DSI-7, DSI-24, DSI-Flex, or DSI-VR300)
- USB cable or Bluetooth adapter
- Charged battery

### Software

See the DSI [Downloads](../help/downloads/index.md) page for the latest API release.

- DSI API library (`DSI.dll` / `DSI.so` / `DSI.dylib`)
- Header file (`DSI.h`)
- C/C++ compiler or Python 3.0+

### Platform Support

- **Windows:** Visual Studio 2015+ or MinGW (requires `DSI.dll`)
- **Linux:** GCC 4.8+, GLIBC 2.14+, USB permissions configured (requires `DSI.so`)
- **macOS:** Xcode Command Line Tools (requires `DSI.dylib`)

---

## Quick Start

Get up and running quickly with these minimal examples.

### C Quick Start

```c
#include "DSI.h"
#include <stdio.h>

int main() {
    // Create and connect to headset
    DSI_Headset h = DSI_Headset_New(NULL);
    DSI_Headset_Connect(h, NULL);  // NULL uses default COM port
    if (!h || DSI_Error()) {
        fprintf(stderr, "Error: %s\n", DSI_ClearError());
        return 1;
    }
    printf("Connected to %s\n", DSI_Headset_GetPort(h));
    
    // Configure channels (montage)
    DSI_Headset_ChooseChannels(h, "P3,Pz,P4", "A1+A2", 1);
    
    // Start acquisition
    DSI_Headset_StartDataAcquisition(h);
    
    // Collect data using callback
    DSI_Channel pz = DSI_Headset_GetChannelByName(h, "Pz");
    
    for (int i = 0; i < 10; i++) {
        DSI_Headset_Idle(h, 0.1);  // Process for 100ms
        
        // Read latest value
        double value = DSI_Channel_GetSignal(pz);
        printf("Sample %d: Pz = %.2f µV\n", i, value);
    }
    
    // Cleanup
    DSI_Headset_StopDataAcquisition(h);
    DSI_Headset_Delete(h);
    
    return 0;
}
```

**Compile:**
```bash
# Windows (Visual Studio)
cl quick_start.c DSI.lib

# Linux
gcc quick_start.c -L. -lDSI -o quick_start

# macOS
clang quick_start.c -L. -lDSI -o quick_start
```

### Python Quick Start

```python
from DSI import Headset

# Connect to headset
h = Headset()
h.Connect(None)  # None uses default COM port
print(f"Connected to {h.GetPort()}")

# Configure channels
h.ChooseChannels("P3,Pz,P4", "A1+A2", True)

# Start acquisition
h.StartDataAcquisition()

# Collect data
ch = h.GetChannelByName("Pz")

for i in range(10):
    h.Idle(0.1)  # Process for 100ms
    
    value = ch.GetSignal()
    print(f"Sample {i}: Pz = {value:.2f} µV")

# Cleanup
h.StopDataAcquisition()
```

**Quick Test:**
The `DSI.py` file in the release directory is runnable as-is for quick testing. Simply edit the default port and run:
```bash
# Edit line 296 in DSI.py to set your COM port (default is COM6 for Windows)
python DSI.py

# Or pass port as command-line argument
python DSI.py COM4
python DSI.py /dev/ttyUSB0  # Linux
python DSI.py /dev/cu.DSI24-023-BluetoothSerial  # macOS

# Optional second argument for reference or impedance mode
python DSI.py COM4 A1+A2      # Use A1+A2 reference
python DSI.py COM4 impedances # Run impedance test
```

---

## Tutorial 1: Basic Connection

### Step 1: Include the API

**C:**
```c
#include "DSI.h"
#include <stdio.h>
#include <stdlib.h>
```

**Python:**
```python
from DSI import Headset
```

### Step 2: Specify Port or Use Environment Variable

**Port specification by platform:**
- **Windows:** COM ports (e.g., `COM4`, `COM5`, `COM6`)
- **Linux:** `/dev/ttyUSB0`, `/dev/ttyUSB1`, `/dev/ttyACM0`, `/dev/ttyACM1`
- **macOS:** `/dev/cu.DSI24-xxxxx-BluetoothSerial` or `/dev/tty.usbserial-xxxxx`
- **Environment variable:** Set `DSISerialPort` and pass `NULL` (C) or `None` (Python)

**C example:**
```c
// Option 1: Use environment variable (set DSISerialPort)
const char* port = NULL;  // NULL uses DSISerialPort env variable

// Option 2: Specify port directly
#ifdef _WIN32
    port = "COM4";  // Windows
#elif defined(__APPLE__)
    port = "/dev/cu.DSI24-023-BluetoothSerial";  // macOS
#else
    port = "/dev/ttyUSB0";  // Linux
#endif

printf("Using port: %s\n", port ? port : "from DSISerialPort env var");
```

**Python example:**
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
```

### Step 3: Create and Connect Headset Object

**C example:**
```c
// Create headset object (does not connect yet)
DSI_Headset h = DSI_Headset_New(NULL);
if (!h) {
    fprintf(stderr, "Failed to create headset: %s\n", DSI_ClearError());
    return 1;
}

// Connect to the serial port
DSI_Headset_Connect(h, port);
if (DSI_Error()) {
    fprintf(stderr, "Failed to connect: %s\n", DSI_ClearError());
    DSI_Headset_Delete(h);
    return 1;
}
```

**Python example:**
```python
try:
    # Create and connect in one step
    h = Headset()
    h.Connect(port)  # port can be None for env variable
except Exception as e:
    print(f"Failed to connect: {e}")
    exit(1)
```

**What happens:**
- **C:** `DSI_Headset_New(NULL)` allocates object, then `DSI_Headset_Connect(h, port)` connects
- **Python:** `Headset()` allocates, then `.Connect(port)` connects
- Connection process: Opens serial port → Queries hardware model/firmware → Initializes communication

### Step 4: Verify Connection

**C example:**
```c
if (!DSI_Headset_IsConnected(h)) {
    fprintf(stderr, "Not connected!\n");
    DSI_Headset_Delete(h);
    return 1;
}

// Get device information
const char* model = DSI_Headset_GetHardwareModel(h);
const char* firmware = DSI_Headset_GetFirmwareRevision(h);
unsigned int serial = DSI_Headset_GetSerialNumber(h);

printf("Connected to: %s\n", model);
printf("Firmware: %s\n", firmware);
printf("Serial: %u\n", serial);
```

**Python example:**
```python
if not h.IsConnected():
    print("Not connected!")
    exit(1)

# Get device information
print(f"Connected to: {h.GetHardwareModel()}")
print(f"Firmware: {h.GetFirmwareRevision()}")
print(f"Serial: {h.GetSerialNumber()}")
```

### Step 5: Error Handling

See the [Error Codes](error_codes.md) page for a full list of error messages.

```c
// ALWAYS check for errors after critical operations
DSI_Headset h = DSI_Headset_New(NULL);
if (!h || DSI_Error()) {
    fprintf(stderr, "Failed to create headset: %s\n", DSI_ClearError());
    return 1;
}

DSI_Headset_Connect(h, port);
if (DSI_Error()) {
    fprintf(stderr, "Connection failed: %s\n", DSI_ClearError());
    DSI_Headset_Delete(h);
    return 1;
}

// Optional: Set error callback for automatic logging
int errorCallback(const char* msg, int level) {
    fprintf(stderr, "[Level %d] %s\n", level, msg);
    return 1;  // Continue execution
}

DSI_SetErrorCallback(errorCallback);
```

**Complete connection example:**

```c
int connectToHeadset(DSI_Headset* pHeadset, const char* port) {
    // Create headset object
    DSI_Headset h = DSI_Headset_New(NULL);
    if (!h) {
        fprintf(stderr, "Failed to create headset\n");
        return 0;
    }
    
    // Connect to serial port (NULL uses DSISerialPort env variable)
    DSI_Headset_Connect(h, port);
    if (DSI_Error()) {
        fprintf(stderr, "Connection failed: %s\n", DSI_ClearError());
        DSI_Headset_Delete(h);
        return 0;
    }
    
    // Verify connection
    if (!DSI_Headset_IsConnected(h)) {
        fprintf(stderr, "Connection verification failed\n");
        DSI_Headset_Delete(h);
        return 0;
    }
    
    // Get device info
    printf("Connected to %s (SN: %u)\n",
           DSI_Headset_GetHardwareModel(h),
           DSI_Headset_GetSerialNumber(h));
    
    *pHeadset = h;
    return 1;
}
```

**Python equivalent:**
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
        print(f"Connected to {h.GetHardwareModel()} (SN: {h.GetSerialNumber()})")
        
        return h
    except Exception as e:
        print(f"Connection failed: {e}")
        return None
```

---

## Tutorial 2: Channel Configuration

### Understanding Montages

**montage** defines which electrodes to use and how to reference them.

**Syntax:** `"electrode1,electrode2,electrode3"`

**Common montage examples:**
- `"P3,Pz,P4,O1,O2"` — Five posterior channels
- `"Fp1,Fp2,F3,F4,C3,C4"` — Frontal and central channels  
- `"@1,@2,@3,@4"` — First four sensors (numbered indexing)

### Step 1: List Available Sources

```c
// Get all available electrode names
const char* sources = DSI_Headset_GetSourceNames(h);
printf("Available electrodes:\n%s\n", sources);

// Or iterate programmatically
int nSources = DSI_Headset_GetNumberOfSources(h);
printf("Total sources: %d\n", nSources);

for (int i = 0; i < nSources; i++) {
    DSI_Source src = DSI_Headset_GetSourceByIndex(h, i);
    printf("%d: %s\n", i, DSI_Source_GetName(src));
}
```

### Step 2: Choose Reference

**Common reference options:**
- `"A1+A2"` — Average of both ear sensors (linked ears)
- `"Cz"` — Single electrode reference
- `""` (empty string) — No re-referencing, uses factory reference (typically Pz)

### Step 3: Configure Channels

**C example:**
```c
// ChooseChannels(headset, montage, reference, autoswap)
DSI_Headset_ChooseChannels(h, "P3,Pz,P4,O1,O2", "A1+A2", 1);

if (DSI_Error()) {
    fprintf(stderr, "Montage error: %s\n", DSI_ClearError());
    
    // Troubleshoot: List available sources
    const char* sources = DSI_Headset_GetSourceNames(h);
    fprintf(stderr, "Available: %s\n", sources);
    return 0;
}

// Verify configuration
printf("Configured %d channels\n", DSI_Headset_GetNumberOfChannels(h));
```

**Python example:**
```python
# ChooseChannels(montage, reference, autoswap)
h.ChooseChannels("P3,Pz,P4,O1,O2", "A1+A2", True)

print(f"Configured {h.GetNumberOfChannels()} channels")
```

**Parameters:**
- `montage` — Comma-separated electrode names
- `reference` — Reference electrode(s) specification
- `autoswap` — Automatically swap signal/reference if needed (use `1` or `True`)

### Step 4: Inspect Channels

```c
int nChannels = DSI_Headset_GetNumberOfChannels(h);

for (int i = 0; i < nChannels; i++) {
    DSI_Channel ch = DSI_Headset_GetChannelByIndex(h, i);
    
    printf("Channel %d: %s", i, DSI_Channel_GetName(ch));
    
    if (DSI_Channel_IsReferentialEEG(ch)) {
        printf(" (EEG)");
    }
    if (DSI_Channel_IsTrigger(ch)) {
        printf(" (Trigger)");
    }
    printf("\n");
}
```

### Step 5: Access Channels by Name

```c
// Preferred: Access by name
DSI_Channel pz = DSI_Headset_GetChannelByName(h, "Pz");
if (!pz) {
    fprintf(stderr, "Channel 'Pz' not found\n");
} else {
    printf("Found channel: %s\n", DSI_Channel_GetName(pz));
}

// Alternative: Access by index
DSI_Channel ch0 = DSI_Headset_GetChannelByIndex(h, 0);
```

### Advanced: Bipolar Montages

```c
// Bipolar: Each channel is difference between two electrodes
// Syntax: "electrode1-electrode2"
DSI_Headset_ChooseChannels(h, "Fp1-F3,F3-C3,C3-P3,P3-O1", "", 1);

// This creates 4 channels:
// - Fp1-F3 (voltage at Fp1 minus voltage at F3)
// - F3-C3
// - C3-P3
// - P3-O1
```

**Complete montage example:**

```c
int configureMontage(DSI_Headset h, const char* model) {
    const char* montage;
    const char* reference;
    
    // Choose montage based on headset model
    if (strstr(model, "DSI-7")) {
        // DSI-7: 7 dry electrodes
        montage = "P3,Pz,P4,POz,O1,Oz,O2";
        reference = "Cz";
    } 
    else if (strstr(model, "DSI-24")) {
        // DSI-24: Full 10-20 system
        montage = "Fp1,Fp2,F7,F3,Fz,F4,F8,"
                  "T3,C3,Cz,C4,T4,"
                  "T5,P3,Pz,P4,T6,"
                  "O1,Oz,O2";
        reference = "A1+A2";
    }
    else {
        // Unknown model: use numbered sources
        montage = "@1,@2,@3,@4,@5";
        reference = "";
    }
    
    printf("Montage: %s\n", montage);
    printf("Reference: %s\n", reference);
    
    DSI_Headset_ChooseChannels(h, montage, reference, 1);
    
    if (DSI_Error()) {
        fprintf(stderr, "Montage failed: %s\n", DSI_ClearError());
        return 0;
    }
    
    printf("Configured %d channels\n", 
           DSI_Headset_GetNumberOfChannels(h));
    return 1;
}
```

---

## Tutorial 3: Data Acquisition

### Step 1: Configure Sampling

```c
// Set sampling rate and filter mode
// DSI_Headset_ConfigureADC(h, samplesPerSecond, filterMode)

// NOTE: Configuring non-default sampling rates requires the appropriate feature
// to be unlocked on your headset. Check feature availability first:
if (DSI_Headset_GetFeatureAvailability(h, "SampleRate")) {
    printf("Custom sampling rates are available\n");
} else {
    printf("Using default sampling rate (feature not unlocked)\n");
}

const char* model = DSI_Headset_GetHardwareModel(h);

if (strstr(model, "DSI-7")) {
    // DSI-7 default is 300 Hz
    DSI_Headset_ConfigureADC(h, 300, 0);
}
else if (strstr(model, "DSI-24")) {
    // DSI-24 default is 300 Hz, can configure higher if unlocked
    DSI_Headset_ConfigureADC(h, 300, 0);
}

// Verify actual sampling rate
double fs = DSI_Headset_GetSamplingRate(h);
printf("Sampling rate: %.0f Hz\n", fs);
```

**Filter modes:**
- `0` - No filtering (default)
- `1` - Low-pass filter
- `2` - High-pass filter
- `3` - Band-pass filter

### Step 2: Buffers

```c
// Channel buffers are allocated automatically when you configure channels.
// The default buffer size is sufficient for most real-time applications.

// Manual buffer reallocation is only needed if:
// 1. You need to store more than a few seconds of data
// 2. You're using custom processing stages that require larger lookback windows

// Example: Allocate 10 seconds for signal, 5 seconds for impedance
DSI_Headset_ReallocateBuffers(h, 10.0, 5.0);

// Check buffer status during acquisition
size_t buffered = DSI_Headset_GetNumberOfBufferedSamples(h);
printf("Buffered samples: %zu\n", buffered);
```

### Step 3: Start Acquisition

```c
DSI_Headset_StartDataAcquisition(h);

if (DSI_Error()) {
    fprintf(stderr, "Failed to start acquisition: %s\n", 
            DSI_ClearError());
    return 0;
}

printf("Acquisition started\n");
```

### Step 4: Receive Data

```c
double fs = DSI_Headset_GetSamplingRate(h);
double blockDuration = 0.5;  // 0.5 second blocks

while (acquiring) {
    // Process events and receive data for specified time
    DSI_Headset_Idle(h, blockDuration);
    
    if (DSI_Error()) {
        fprintf(stderr, "Error: %s\n", DSI_ClearError());
    }
    
    // Read buffered data from each channel
    int nChannels = DSI_Headset_GetNumberOfChannels(h);
    for (int i = 0; i < nChannels; i++) {
        DSI_Channel ch = DSI_Headset_GetChannelByIndex(h, i);
        
        // Get number of buffered samples
        size_t buffered = DSI_Channel_GetNumberOfBufferedSamples(ch);
        
        // Read buffered samples one at a time
        for (size_t j = 0; j < buffered; j++) {
            double value = DSI_Channel_ReadBuffered(ch);
            processData(DSI_Channel_GetName(ch), value);
        }
    }
}
```

### Step 5: Stop Acquisition

```c
DSI_Headset_StopDataAcquisition(h);
printf("Acquisition stopped\n");
```

**Complete acquisition example:**

```c
void acquireData(DSI_Headset h, double durationSeconds) {
    double blockDuration = 0.1;  // 100ms blocks
    int numBlocks = (int)(durationSeconds / blockDuration);
    
    printf("Acquiring %.1f seconds of data...\n", durationSeconds);
    
    // Start acquisition
    DSI_Headset_StartDataAcquisition(h);
    if (DSI_Error()) {
        fprintf(stderr, "Start failed: %s\n", DSI_ClearError());
        return;
    }
    
    // Collect data blocks
    for (int block = 0; block < numBlocks; block++) {
        DSI_Headset_Idle(h, blockDuration);
        
        // Show progress
        if (block % 10 == 0) {
            printf("Progress: %.0f%%\r", 
                   100.0 * block / numBlocks);
            fflush(stdout);
        }
        
        // Check for errors/alarms
        if (DSI_Error()) {
            fprintf(stderr, "\nError: %s\n", DSI_ClearError());
        }
        if (DSI_Headset_GetNumberOfAlarms(h) > 0) {
            int alarm = DSI_Headset_GetAlarm(h, 1);  // 1 = remove from queue
            fprintf(stderr, "\nAlarm: %d\n", alarm);
        }
    }
    
    printf("\nAcquisition complete\n");
    DSI_Headset_StopDataAcquisition(h);
}
```

---

## Tutorial 4: Background Acquisition

Background acquisition runs in a separate thread, allowing your application to continue other work.

### Step 1: Set Sample Callback

```c
void mySampleCallback(DSI_Headset h, double packetTime, void* userData) {
    // This function is called automatically when new data arrives
    // userData can be used to pass application-specific data to the callback
    
    // Get first channel
    DSI_Channel ch = DSI_Headset_GetChannelByIndex(h, 0);
    
    // Get latest sample
    double value = DSI_Channel_GetSignal(ch);
    
    printf("New sample: %.2f µV (time: %.3f)\n", value, packetTime);
}

// Register callback (NULL for userData if not needed)
DSI_Headset_SetSampleCallback(h, mySampleCallback, NULL);
```

### Step 2: Start Background Acquisition

```c
if (!DSI_Headset_StartBackgroundAcquisition(h) || DSI_Error()) {
    fprintf(stderr, "Background acquisition failed: %s\n", 
            DSI_ClearError());
    return 0;
}

printf("Background acquisition running...\n");
```

### Step 3: Application Continues

```c
// Your application can continue other work
// Data collection happens in background thread

for (int i = 0; i < 100; i++) {
    // Do other work
    printf("Main loop iteration %d\n", i);
    DSI_Sleep(0.1);
    
    // Check buffer status
    int buffered = DSI_Headset_GetNumberOfBufferedSamples(h);
    printf("  Buffered samples: %d\n", buffered);
}
```

### Step 4: Stop Background Acquisition

```c
DSI_Headset_StopBackgroundAcquisition(h);
printf("Background acquisition stopped\n");
```

**Complete background acquisition example:**

```c
// Global flag to control acquisition
volatile int g_acquiring = 1;

void sampleCallback(DSI_Headset h, double packetTime, void* userData) {
    static int sampleCount = 0;
    sampleCount++;
    
    // Get channel data
    DSI_Channel pz = DSI_Headset_GetChannelByName(h, "Pz");
    if (pz) {
        double value = DSI_Channel_GetSignal(pz);
        
        // Print every 100 samples
        if (sampleCount % 100 == 0) {
            printf("Sample %d: Pz = %.2f µV\n", sampleCount, value);
        }
    }
}

int main() {
    DSI_Headset h = /* ... connect and configure ... */;
    
    // Set callback and start (NULL for userData)
    DSI_Headset_SetSampleCallback(h, sampleCallback, NULL);
    DSI_Headset_StartBackgroundAcquisition(h);
    
    printf("Acquiring... Press Ctrl+C to stop\n");
    
    // Main loop: monitor health
    while (g_acquiring) {
        DSI_Sleep(5.0);
        
        // Check for overflow
        int overflow = DSI_Headset_GetNumberOfOverflowedSamples(h);
        if (overflow > 0) {
            fprintf(stderr, "WARNING: %d samples lost!\n", overflow);
        }
        
        // Check for alarms
        while (DSI_Headset_GetNumberOfAlarms(h) > 0) {
            int alarm = DSI_Headset_GetAlarm(h, 1);  // 1 = remove from queue
            fprintf(stderr, "Alarm: %d\n", alarm);
        }
    }
    
    DSI_Headset_StopBackgroundAcquisition(h);
    DSI_Headset_Delete(h);
    return 0;
}
```

---

## Tutorial 5: Real-Time Processing

### Using Processing Stages

Processing stages allow you to create processing pipelines (filtering, feature extraction, etc.). They process data sample-by-sample through callbacks. The callback is specified when creating the stage.

```c
// Processing callback that applies custom filter
void myFilterCallback(DSI_Headset h, double packetTime, void* userData) {
    DSI_ProcessingStage output = (DSI_ProcessingStage)userData;
    DSI_ProcessingStage input = DSI_ProcessingStage_GetInput(output);
    
    unsigned int nChannels = DSI_ProcessingStage_GetNumberOfChannels(input);
    
    for (unsigned int ch = 0; ch < nChannels; ch++) {
        // Read most recent sample (0 = current, 1 = previous, etc.)
        double value = DSI_ProcessingStage_Read(input, ch, 0);
        
        // Apply simple low-pass filter (example)
        double filtered = value * 0.9;  // Placeholder - use real filter
        
        // Write to output stage
        DSI_ProcessingStage_Write(output, ch, filtered);
    }
}

// Create processing stage with callback
// AddProcessingStage(headset, name, callback, paramData, inputStage)
DSI_ProcessingStage ps = DSI_Headset_AddProcessingStage(h, "MyFilter", 
                                                         myFilterCallback, NULL, NULL);
if (!ps || DSI_Error()) {
    fprintf(stderr, "Failed to add processing stage: %s\n", DSI_ClearError());
    return;
}

// Start acquisition - callback runs automatically
DSI_Headset_StartDataAcquisition(h);
```

### Real-Time Band-Power Analysis

```c
#include <math.h>

typedef struct {
    double alpha_power;   // 8-13 Hz
    double beta_power;    // 13-30 Hz
    double theta_power;   // 4-8 Hz
} BandPowers;

BandPowers computeBandPowers(const double* data, int n, double fs) {
    BandPowers bp = {0};
    
    // Simple FFT-based power calculation
    // (Use FFTW or similar library in production)
    
    // For demo: compute variance in each band (simplified)
    double sum = 0, sum2 = 0;
    for (int i = 0; i < n; i++) {
        sum += data[i];
        sum2 += data[i] * data[i];
    }
    
    double variance = (sum2 / n) - (sum / n) * (sum / n);
    
    // Placeholder: distribute variance to bands
    bp.alpha_power = variance * 0.4;
    bp.beta_power = variance * 0.3;
    bp.theta_power = variance * 0.3;
    
    return bp;
}

void realTimeBandPower(DSI_Headset h) {
    double fs = DSI_Headset_GetSamplingRate(h);
    int windowSize = (int)(fs * 1.0);  // 1-second windows
    double* buffer = malloc(windowSize * sizeof(double));
    
    DSI_Headset_StartDataAcquisition(h);
    DSI_Channel pz = DSI_Headset_GetChannelByName(h, "Pz");
    
    while (acquiring) {
        // Process events for 1 second
        DSI_Headset_Idle(h, 1.0);
        
        // Read buffered samples one at a time
        size_t buffered = DSI_Channel_GetNumberOfBufferedSamples(pz);
        size_t toRead = buffered < windowSize ? buffered : windowSize;
        
        for (size_t i = 0; i < toRead; i++) {
            buffer[i] = DSI_Channel_ReadBuffered(pz);
        }
        
        if (toRead >= windowSize) {
            BandPowers bp = computeBandPowers(buffer, windowSize, fs);
            printf("Alpha: %.2f | Beta: %.2f | Theta: %.2f\n",
                   bp.alpha_power, bp.beta_power, bp.theta_power);
        }
    }
    
    DSI_Headset_StopDataAcquisition(h);
    free(buffer);
}
```

---

## Common Tasks

### Task: Save Data to File

```c
void saveToCSV(DSI_Headset h, const char* filename, double duration) {
    FILE* f = fopen(filename, "w");
    if (!f) {
        fprintf(stderr, "Cannot open %s\n", filename);
        return;
    }
    
    // Write header
    fprintf(f, "Time");
    int nChannels = DSI_Headset_GetNumberOfChannels(h);
    for (int i = 0; i < nChannels; i++) {
        DSI_Channel ch = DSI_Headset_GetChannelByIndex(h, i);
        fprintf(f, ",%s", DSI_Channel_GetName(ch));
    }
    fprintf(f, "\n");
    
    // Acquire and save data
    double fs = DSI_Headset_GetSamplingRate(h);
    int samplesPerBlock = (int)(fs * 0.1);
    int numBlocks = (int)(duration / 0.1);
    
    DSI_Headset_StartDataAcquisition(h);
    
    double startTime = DSI_Headset_SecondsSinceConnection(h);
    
    for (int block = 0; block < numBlocks; block++) {
        DSI_Headset_Idle(h, samplesPerBlock / fs);  // Process one block duration
        
        // Read buffered samples
        for (int ch = 0; ch < nChannels; ch++) {
            DSI_Channel channel = DSI_Headset_GetChannelByIndex(h, ch);
            size_t buffered = DSI_Channel_GetNumberOfBufferedSamples(channel);
            
            for (size_t samp = 0; samp < buffered; samp++) {
                if (ch == 0) {  // Write time only once per row
                    double time = DSI_Headset_SecondsSinceConnection(h) - startTime;
                    fprintf(f, "%.6f", time);
                }
                
                double value = DSI_Channel_ReadBuffered(channel);
                fprintf(f, ",%.6f", value);
                
                if (ch == nChannels - 1) fprintf(f, "\n");
            }
        }
    }
    
    DSI_Headset_StopDataAcquisition(h);
    fclose(f);
    
    printf("Saved %s\n", filename);
}
```

### Task: Check Impedances

```c
void checkImpedances(DSI_Headset h) {
    printf("Starting impedance test...\n");
    
    // Start impedance driver
    DSI_Headset_StartImpedanceDriver(h);
    if (DSI_Error()) {
        fprintf(stderr, "Failed to start impedance driver: %s\n", DSI_ClearError());
        return;
    }
    
    // Wait for readings to stabilize
    DSI_Sleep(2.0);
    
    // Read impedances
    int nSources = DSI_Headset_GetNumberOfSources(h);
    printf("\nImpedance readings:\n");
    printf("%-10s %10s\n", "Electrode", "Impedance");
    printf("------------------------\n");
    
    for (int i = 0; i < nSources; i++) {
        DSI_Source src = DSI_Headset_GetSourceByIndex(h, i);
        
        if (DSI_Source_IsReferentialEEG(src)) {
            const char* name = DSI_Source_GetName(src);
            double impedance = DSI_Source_GetImpedanceEEG(src);
            
            printf("%-10s %8.0f kΩ", name, impedance / 1000.0);
            
            // Quality indicator
            if (impedance < 50000) {
                printf(" ✓ Good\n");
            } else if (impedance < 100000) {
                printf(" ⚠ Fair\n");
            } else {
                printf(" ✗ Poor\n");
            }
        }
    }
    
    // Get common-mode fault metric
    double cmf = DSI_Headset_GetImpedanceCMF(h);
    printf("\nCommon-mode fault: %.1f\n", cmf);
    
    DSI_Headset_StopImpedanceDriver(h);
    printf("Impedance test complete\n");
}
```

### Task: Monitor Battery Level

```c
void monitorBattery(DSI_Headset h) {
    // Send battery query
    DSI_Headset_SendBatteryQuery(h);
    
    // Wait for response
    DSI_Sleep(0.5);
    
    // Read level (0 = main battery)
    double level = DSI_Headset_GetBatteryLevel(h, 0);
    
    printf("Battery: %.1f%%", level);
    
    if (level < 10.0) {
        printf(" CRITICAL - Charge now!\n");
    } else if (level < 20.0) {
        printf(" LOW - Charge soon\n");
    } else {
        printf(" OK\n");
    }
}
```

---

## Next Steps

### Explore Advanced Features

- [quick_reference](quick_reference.md) - Quick lookup guide
- [error_codes](error_codes.md) - Error handling strategies


### Support

- **Sample code:** See `release/demo.c` and Python `DSI.py` examples in the release package.
- **Technical support:** Contact WearableSensing support team via the [contact page](../help/index.md).

---

[Back to API Index](index.md)
