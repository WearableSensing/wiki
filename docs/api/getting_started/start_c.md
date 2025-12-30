# Getting Started with C/C++

> **C/C++ tutorial** — Learn to connect, configure, and acquire EEG data using the DSI API in C/C++.

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

- DSI API library (`DSI.dll` / `DSI.so` / `DSI.dylib`)
- Header file (`DSI.h`)
- API loader (`DSI_API_Loader.c`)
- C/C++ compiler

**Important:** Before using any DSI API functions, you must:
1. Add `DSI_API_Loader.c` to your project
2. Call `Load_DSI_API(NULL)` at program startup
3. Check the return value (0 = success, non-zero = error)

### Platform-Specific Requirements

**Windows:**
- Visual Studio 2015+ or MinGW
- `DSI.dll` and `DSI.lib`

**Linux:**
- GCC 4.8+, GLIBC 2.14+
- USB permissions configured
- `DSI.so`

**macOS:**
- Xcode Command Line Tools
- `DSI.dylib`

---

## Quick Start

This minimal example demonstrates the essential steps to connect to a headset, configure channels, and acquire data. Copy this code to get started quickly, then explore the detailed tutorials below for more information.

```c
#include "DSI.h"
#include <stdio.h>

int main() {
    // Load the API (must be first!)
    if (Load_DSI_API(NULL) != 0) {
        fprintf(stderr, "Failed to load DSI API\n");
        return 1;
    }
    
    // Create and connect to headset
    DSI_Headset h = DSI_Headset_New(NULL);
    DSI_Headset_Connect(h, NULL);  // NULL uses DSISerialPort env variable
    if (!h || DSI_Error()) {
        fprintf(stderr, "Error: %s\n", DSI_ClearError());
        return 1;
    }
    printf("Connected!\n");
    
    // Configure channels (montage)
    // Using "" for reference uses the default linked ears reference
    DSI_Headset_ChooseChannels(h, "P3,Pz,P4", "", 1);
    
    // Start acquisition
    DSI_Headset_StartDataAcquisition(h);
    
    // Collect data
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

### Compiling

**Windows (Visual Studio):**
```bash
cl quick_start.c DSI_API_Loader.c DSI.lib
```

**Linux:**
```bash
gcc quick_start.c DSI_API_Loader.c -L. -lDSI -ldl -o quick_start
```

**macOS:**
```bash
clang quick_start.c DSI_API_Loader.c -L. -lDSI -o quick_start
```

---

## Tutorial 1: Basic Connection

This tutorial walks through establishing a connection to your DSI headset. You'll learn how to properly initialize the API, specify serial ports, create headset objects, and handle errors.

### Step 0: Load the API

Before calling any DSI functions, you must load the dynamic library. This step locates the platform-specific library file and imports all API functions into your program's memory space.

```c
#include "DSI.h"

int main() {
    // Load the DSI API library
    if (Load_DSI_API(NULL) != 0) {
        fprintf(stderr, "Failed to load DSI API\n");
        return 1;
    }
    
    // Now you can use DSI functions...
}
```

**What `Load_DSI_API` does:**
- Locates and loads the platform-specific dynamic library (`DSI.dll`, `DSI.so`, or `DSI.dylib`)
- Imports all DSI API functions
- Returns 0 on success, negative if library not found, positive if function import failed

**Note:** You must add `DSI_API_Loader.c` to your project for this function to be available.

### Step 1: Include the API

Include the DSI header file and standard C libraries needed for your application. The DSI.h header defines all API functions and data types.

```c
#include "DSI.h"
#include <stdio.h>
#include <stdlib.h>
```

### Step 2: Specify Port or Use Environment Variable

The serial port identifier varies by platform and connection method. You can specify it directly or use an environment variable for flexibility across different systems.

**Port specification by platform:**
- **Windows:** COM ports (e.g., `COM4`, `COM5`, `COM6`)
- **Linux:** `/dev/ttyUSB0`, `/dev/ttyUSB1`, `/dev/ttyACM0`, `/dev/ttyACM1`
- **macOS:** `/dev/cu.DSI24-xxxxx-BluetoothSerial` or `/dev/tty.usbserial-xxxxx`
- **Environment variable:** Set `DSISerialPort` and pass `NULL`

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

### Step 3: Create and Connect Headset Object

Creating and connecting involves two separate steps: first allocate the headset object, then establish the serial connection. Always check for errors after each step.

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

**What happens during connection:**
1. `DSI_Headset_New(NULL)` allocates the headset object
2. `DSI_Headset_Connect(h, port)` opens serial port
3. Queries hardware model and firmware
4. Initializes communication

### Step 4: Verify Connection

```c
if (!DSI_Headset_IsConnected(h)) {
    fprintf(stderr, "Not connected!\n");
    DSI_Headset_Delete(h);
    return 1;
}

// Get device information
printf("%s\n", DSI_Headset_GetInfoString(h));
```

### Step 5: Error Handling

Always check for errors after critical operations. See [Error Codes](../error_codes.md) for a complete reference.

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

### Complete Connection Example

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
    printf("%s\n", DSI_Headset_GetInfoString(h));
    
    *pHeadset = h;
    return 1;
}
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

Before configuring channels, it's helpful to see which electrodes are available on your headset. Sources represent individual sensors that can be combined into channels.

```c
// Iterate through all sources to see what's available
int nSources = DSI_Headset_GetNumberOfSources(h);
printf("Total sources: %d\n", nSources);

for (int i = 0; i < nSources; i++) {
    DSI_Source src = DSI_Headset_GetSourceByIndex(h, i);
    printf("%d: %s\n", i, DSI_Source_GetName(src));
}
```

### Step 2: Choose Reference

The reference electrode determines the baseline for measuring voltage. **By default, the API automatically uses linked ears (A1+A2 on DSI-24, LE on DSI-7/VR300) as the reference.** You only need to call reference functions if you want to change from this default.

#### Default Reference (Automatic)

No API calls needed - just pass empty string `""` or `NULL` to `ChooseChannels()`:

```c
// Uses default linked ears automatically
DSI_Headset_ChooseChannels(h, "P3,Pz,P4", "", 1);
```

**Default reference by model:**
- **DSI-24:** `A1+A2` (average of A1 and A2 channels)
- **DSI-7:** `LE` (pre-averaged linked ear channel)
- **DSI-VR300:** `LE` (pre-averaged linked ear channel)

#### Change to Hardware Reference

To use the hardware/factory reference instead of linked ears:

```c
// Option 1: Use "FACTORY" keyword
DSI_Headset_SetDefaultReference(h, "FACTORY", 1);
DSI_Headset_ChooseChannels(h, "P3,Pz,P4", "", 1);

// Option 2: Specify hardware reference electrode directly
DSI_Headset_ChooseChannels(h, "P3,Pz,P4", "Pz", 1);  // DSI-24/DSI-7
DSI_Headset_ChooseChannels(h, "P3,Pz,P4", "P4", 1);  // VR300
```

**Hardware reference by model:**
- **DSI-24:** `Pz`
- **DSI-7:** `Pz`
- **DSI-VR300:** `P4`

#### Change to Custom Reference

To use any electrode as reference (e.g., P3, Cz):

```c
// Option 1: Set default reference, then configure channels
DSI_Headset_SetDefaultReference(h, "P3", 1);
DSI_Headset_ChooseChannels(h, "Pz,P4,O1,O2", "", 1);

// Option 2: Specify directly in ChooseChannels
DSI_Headset_ChooseChannels(h, "Pz,P4,O1,O2", "P3", 1);
```

**To check which reference is active:**
```c
const char* ref = DSI_Headset_GetReferenceString(h);
printf("Current reference: %s\n", ref);
```

### Step 3: Configure Channels

After choosing your montage and reference, configure the channels using `ChooseChannels()`. This function validates electrode names and sets up the signal processing pipeline.

```c
// ChooseChannels(headset, montage, reference, autoswap)

// Recommended: Use empty string for default linked ear reference
DSI_Headset_ChooseChannels(h, "P3,Pz,P4,O1,O2", "", 1);

// To use hardware reference instead, specify electrode explicitly:
// DSI_Headset_ChooseChannels(h, "P3,Pz,P4,O1,O2", "Pz", 1);  // DSI-24/DSI-7
// DSI_Headset_ChooseChannels(h, "P3,Pz,P4,O1,O2", "P4", 1);  // VR300

if (DSI_Error()) {
    fprintf(stderr, "Montage error: %s\n", DSI_ClearError());
    
    // Troubleshoot: List available sources
    fprintf(stderr, "Available sources:\n");
    int nSources = DSI_Headset_GetNumberOfSources(h);
    for (int i = 0; i < nSources; i++) {
        DSI_Source src = DSI_Headset_GetSourceByIndex(h, i);
        fprintf(stderr, "  %s\n", DSI_Source_GetName(src));
    }
    return 0;
}

// Verify configuration
printf("Configured %d channels\n", DSI_Headset_GetNumberOfChannels(h));
```

**Parameters:**
- `montage` — Comma-separated electrode names
- `reference` — Reference electrode(s) specification
- `autoswap` — Automatically swap signal/reference if needed (use `1`)

### Step 4: Inspect Channels

After configuration, iterate through channels to verify your montage. Channel properties help you distinguish EEG signals from triggers and auxiliary inputs.

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

Accessing channels by name makes code more readable and maintainable than using indices. The function returns `NULL` if the channel doesn't exist.

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

### Complete Montage Example

```c
int configureMontage(DSI_Headset h) {
    // Configure a standard posterior montage
    const char* montage = "P3,Pz,P4,O1,O2";
    const char* reference = "";  // Default linked ears
    
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

Once your headset is connected and channels are configured, you can start acquiring EEG data. This tutorial covers sampling rate configuration, buffer management, starting/stopping acquisition, and reading data from channels.

### Step 1: Configure Sampling

```c
// Set sampling rate and filter mode
// DSI_Headset_ConfigureADC(h, samplesPerSecond, filterMode)

// NOTE: The default sampling rate is 300 Hz. If the SampleRate feature is unlocked,
// all DSI headsets can configure rates up to 600 Hz. Check feature availability first:
if (DSI_Headset_GetFeatureAvailability(h, "SampleRate")) {
    printf("Custom sampling rates are available (up to 600 Hz)\n");
    DSI_Headset_ConfigureADC(h, 600, 0);  // Use 600 Hz when unlocked
} else {
    printf("Using default sampling rate of 300 Hz (feature not unlocked)\n");
    DSI_Headset_ConfigureADC(h, 300, 0);  // Default 300 Hz
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

### Step 2: Understanding Buffers

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

### Complete Acquisition Example

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

Background acquisition runs data collection in a separate thread, freeing your main application to perform other tasks (UI updates, analysis, etc.). This tutorial shows how to set up callbacks that execute automatically when new data arrives.

### Step 1: Set Sample Callback

```c
void mySampleCallback(DSI_Headset h, double packetTime, void* userData) {
    // This function is called automatically when new data arrives
    // userData can be used to pass application-specific data to the callback
    
    // Get first channel
    DSI_Channel ch = DSI_Headset_GetChannelByIndex(h, 0);
    
    // Read buffered sample (callback context - samples are buffered)
    double value = DSI_Channel_ReadBuffered(ch);
    
    printf("New sample: %.2f µV (time: %.3f)\n", value, packetTime);
}
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
    DSI_Headset_Idle(h, 0.1);  // Process events for 100ms
    
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

### Complete Background Acquisition Example

```c
// Global flag to control acquisition
volatile int g_acquiring = 1;

void sampleCallback(DSI_Headset h, double packetTime, void* userData) {
    static int sampleCount = 0;
    sampleCount++;
    
    // Get channel data
    DSI_Channel pz = DSI_Headset_GetChannelByName(h, "Pz");
    if (pz) {
        double value = DSI_Channel_ReadBuffered(pz);
        
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
        DSI_Headset_Idle(h, 5.0);  // Process events for 5 seconds
        
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

## Common Tasks

These practical examples demonstrate frequently needed operations: saving data to files, checking electrode impedances, and monitoring battery levels.

### Task: Save Data to CSV File

Exporting EEG data to CSV format enables analysis in tools like MATLAB, Python, or Excel. This example writes time-synchronized samples with proper column headers.

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

Impedance testing measures electrode-skin contact quality. Good impedances (below 1MΩ) are critical for clean recordings. Run this before each session to verify sensor placement.

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
    DSI_Headset_Idle(h, 2.0);
    
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
            if (impedance < 1000000) {
                printf(" ✓ Good\n");
            } else if (impedance < 2000000) {
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

Monitoring battery prevents unexpected disconnections. Query battery status periodically during long recordings to ensure data integrity.

```c
void monitorBattery(DSI_Headset h) {
    // Send battery query
    DSI_Headset_SendBatteryQuery(h);
    
    // Wait for response
    DSI_Headset_Idle(h, 0.5);
    
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

- [Quick Reference](../quick_reference.md) - Quick lookup guide for all API functions
- [Error Codes](../error_codes.md) - Complete error code reference
- [Python Getting Started](start_python.md) - Python version of this guide

### Sample Code

Check the `release/demo.c` file in the release package for a complete working example.

### Support

**Technical support:** Contact WearableSensing support team via the [contact page](../../help/index.md).

---

[Back to Getting Started](index.md) | [Back to API Index](../index.md)