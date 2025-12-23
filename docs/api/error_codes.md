# Error Codes

> **Complete error catalog** — All error messages, causes, and recovery strategies.

## Table of Contents

- [Error System Overview](#error-system-overview)
- [Error Categories](#error-categories)
  - [Connection Errors](#connection-errors)
  - [Configuration Errors](#configuration-errors)
  - [Runtime Errors](#runtime-errors)
  - [Resource Errors](#resource-errors)
  - [File I/O Errors](#file-io-errors)
  - [Index/Range Errors](#indexrange-errors)
- [Error Detection Patterns](#error-detection-patterns)
- [Best Practices](#best-practices)
- [Common Error Scenarios](#common-error-scenarios)

---

## Error System Overview

The DSI API uses a global error string system for error reporting:

### Error Propagation Flow

1. **Setting Errors:** Internal functions set a global error string when errors occur
2. **Checking Errors:** Call `DSI_Error()` to check if an error occurred (non-destructive)
3. **Clearing Errors:** Call `DSI_ClearError()` to retrieve and clear the error state
4. **Callbacks:** Set `DSI_SetErrorCallback()` for automatic error notifications

### Key Functions

```c
const char* DSI_Error(void)                        // Check error (non-destructive)
const char* DSI_ClearError(void)                   // Retrieve and clear error
void DSI_SetErrorCallback(DSI_MessageCallback func) // Register error callback
```

### Error Callback Signature

```c
typedef int (*DSI_MessageCallback)(const char* msg, int debugLevel);

// debugLevel values:
// 0 = Critical
// 1 = Error
// 2 = Warning
// 3 = Info
// 4 = Debug
```

---

## Error Categories

### Connection Errors

| Error Message | Cause | Recovery |
|---------------|-------|----------|
| `"Port not found"` | Serial port doesn't exist | Verify port name, check device connection |
| `"Port in use"` | Port already opened by another process | Close other applications, use different port |
| `"Communication timeout"` | No response from headset within timeout period | Check cables, power, try reconnecting |
| `"Device not responding"` | Headset connected but not communicating | Power cycle headset, check battery |
| `"Invalid device"` | Connected device is not a DSI headset | Verify correct device, check firmware |
| `"Bluetooth initialization failed"` | Cannot initialize Bluetooth subsystem | Check Bluetooth drivers, permissions |
| `"the serial port name must be given explicitly, because the DSISerialPort environment variable is empty"` | No default port configured | Provide explicit port name or set DSISerialPort |
| `"Cannot resynchronize: serial connection is not open"` | Attempted operation on closed port | Connect first using `DSI_Headset_Connect()` |
| `"Cannot send commands to headset: serial-port connection not yet established"` | Commands sent before connection | Wait for connection to complete |
| `"Cannot read from headset: serial-port connection not yet established"` | Read attempted before connection | Ensure `DSI_Headset_IsConnected()` returns true |

**Detection Pattern:**
```c
DSI_Headset h = DSI_Headset_New(NULL);
DSI_Headset_Connect(h, "COM3");
if (DSI_Error()) {
    fprintf(stderr, "Connection failed: %s\n", DSI_ClearError());
    // Try alternative port or auto-detection
    const char* port = DSI_GetDefaultPort();
    if (port) DSI_Headset_Connect(h, port);
}
```

---

### Configuration Errors

| Error Message | Cause | Recovery |
|---------------|-------|----------|
| `"Invalid sampling rate"` | Requested rate not supported by hardware | Use model-appropriate rate (DSI-7: 300Hz, DSI-24: up to 1200Hz) |
| `"Invalid filter mode"` | Filter mode not recognized | Use valid filter mode (0-3) |
| `"Unsupported feature"` | Feature not available on this model | Check `DSI_Headset_GetFeatureAvailability()` |
| `"Invalid montage specification"` | Malformed channel specification | Check syntax: "Ch1,Ch2,Ch3" or "Ch1-Ch2" |
| `"could not interpret \"...\" as a valid channel specification"` | Parsing error in montage string | Verify electrode names, check separator usage |
| `"Source name not found"` | Electrode name doesn't exist | Use `DSI_Headset_GetSourceNames()` to list valid names |
| `"Failed to match desired source \"...\""` | Name doesn't match any known sensors | Check spelling, verify source is active |
| `"The name \"...\" matches more than one source"` | Ambiguous electrode specification | Use full unique name or index |
| `"Invalid source number ..."` | Source index out of range | Use index 1 to N (not 0-based) |
| `"Cannot construct channel"` | Invalid bipolar/reference combination | Verify both sources exist and are compatible |
| `"cannot rename Source ... because there is another Source already called ..."` | Naming conflict | Choose different name or rename conflicting source |
| `"\"...\" matches more than one Source, and hence cannot be set as a list of aliases"` | Ambiguous alias specification | Use unique identifiers |
| `"Unrecognized electrode naming scheme \"...\""` | Invalid naming scheme | Use "10-20", "BIOSEMI", "NUMBERED", or "FACTORY" |
| `"cannot set code ... as the common mode position"` | Invalid common mode reference selection | Use valid sensor index for reference |
| `"must read calibration memory completely before attempting to write it"` | Incomplete calibration read | Read all pages before writing |
| `"cannot write to page number ...: must be in range 0 to ..."` | Calibration page out of range | Use valid page index |
| `"failed to change accelerometer rate to ..."` | Headset rejected accelerometer configuration | Use supported rate (0, 10, 50, 100 Hz) |

**Detection Pattern:**
```c
DSI_Headset_ChooseChannels(h, "P3,Pz,P4", "A1+A2", 1);
if (DSI_Error()) {
    fprintf(stderr, "Montage error: %s\n", DSI_ClearError());
    
    // List available sources
    const char* sources = DSI_Headset_GetSourceNames(h);
    fprintf(stderr, "Available: %s\n", sources);
    
    // Try simpler montage
    DSI_Headset_ChooseChannels(h, "@1,@2,@3,@4", "@A1+@A2", 1);
}
```

---

### Runtime Errors

| Error Message | Cause | Recovery |
|---------------|-------|----------|
| `"Buffer overflow"` | Data arriving faster than being read | Increase buffer size, optimize processing |
| `"buffer underflow"` | Attempted to read from empty buffer | Wait for samples, check acquisition status |
| `"cannot read from unallocated buffer"` | Buffer not initialized | Call `DSI_Headset_ReallocateBuffers()` |
| `"cannot look back N steps: buffer size is M"` | LookBack exceeds buffer capacity | Increase buffer size or reduce lookback |
| `"cannot look back N steps: M samples available"` | Not enough samples buffered yet | Wait for more samples to accumulate |
| `"Data corruption (CRC failure)"` | Packet checksum failed | Check cables, reduce EMI, replace cable |
| `"Block failed consistency check"` | Data packet corrupted | Verify signal integrity, check grounding |
| `"Packet size mismatch"` | Unexpected packet length | May indicate firmware/API mismatch |
| `"Command failed"` | Headset rejected command | Check command validity for this model |
| `"Command failed too many times"` | Exceeded retry limit (20 attempts) | Power cycle headset, check communication |
| `"Write to serial port failed with errno ..."` | Low-level write failure | Check USB connection, drivers, permissions |
| `"Could not send complete command (sent X of Y bytes)"` | Partial transmission | Retry command, check port stability |
| `"Serial port read error"` | USB communication failure | Reconnect cable, check USB hub/port |

**Detection Pattern:**
```c
// Monitor buffer health
size_t overflow = DSI_Headset_GetNumberOfOverflowedSamples(h);
if (overflow > 0) {
    fprintf(stderr, "WARNING: Lost %zu samples!\n", overflow);
    
    // Increase buffer
    DSI_Headset_StopBackgroundAcquisition(h);
    DSI_Headset_ReallocateBuffers(h, 20.0, 0.0); // 20 seconds
    DSI_Headset_FlushBuffers(h);
    DSI_Headset_StartBackgroundAcquisition(h);
}

// Check for data corruption
const char* err = DSI_Error();
if (err && strstr(err, "CRC")) {
    fprintf(stderr, "Data corruption detected: %s\n", err);
    DSI_ClearError();
    // Log incident, continue acquisition
}
```

---

### Resource Errors

| Error Message | Cause | Recovery |
|---------------|-------|----------|
| `"Memory allocation failure"` | Out of memory | Reduce buffer sizes, close other applications |
| `"Thread creation failure"` | Cannot create background thread | Check system resources, thread limits |
| `"Buffer reallocation failed"` | Insufficient memory for buffers | Use smaller buffer sizes |
| `"CreateWaitableTimer failed with error code ..."` | Windows timer creation failed | Check system resources, restart application |
| `"SetWaitableTimer failed with error code ..."` | Windows timer configuration failed | Verify timer parameters, check permissions |
| `"WaitForSingleObject failed with error code ..."` | Windows synchronization primitive failed | Check system state, restart application |
| `"NULL <type> pointer"` | NULL pointer passed to C interface | Verify handle validity before function calls |

**Detection Pattern:**
```c
int allocateBuffers(DSI_Headset h, double seconds) {
    DSI_Headset_ReallocateBuffers(h, seconds, 0.0);
    if (DSI_Error()) {
        fprintf(stderr, "Buffer allocation failed: %s\n", DSI_ClearError());
        
        // Try smaller buffer
        double reduced = seconds / 2.0;
        fprintf(stderr, "Trying smaller buffer: %.1f seconds\n", reduced);
        DSI_Headset_ReallocateBuffers(h, reduced, 0.0);
        
        if (DSI_Error()) {
            fprintf(stderr, "Cannot allocate even minimal buffer\n");
            return 0;
        }
    }
    return 1;
}
```

---

### File I/O Errors

| Error Message | Cause | Recovery |
|---------------|-------|----------|
| `"failed to open \"...\" to dump calibration memory"` | Cannot write calibration file | Check permissions, disk space, path validity |
| `"failed to open \"...\" to read calibration memory"` | Cannot read calibration file | Verify file exists, check permissions |
| `"failed to read N 8-bit decimal-formatted values from ..."` | Calibration file read error | Verify file format, check for corruption |
| `"failed to read N 8-bit hex-formatted values from ..."` | Calibration file format error | Re-export calibration from headset |
| `"failed to read N raw bytes (after 'BIN\n' header) from ..."` | Binary calibration file corrupted | Use backup calibration file |
| `"file \"...\" has unexpected format - expected it to begin with 'DEC\n', 'HEX\n' or 'BIN\n'"` | Invalid calibration file format | Check file header, use correct format |
| `"unrecognized dump file format \"...\""` | Invalid format specifier | Use "DEC", "HEX", or "BIN" |

**Detection Pattern:**
```c
const char* calFile = "calibration.bin";
if (!readCalibration(h, calFile)) {
    fprintf(stderr, "Calibration read failed: %s\n", DSI_ClearError());
    
    // Try alternative formats
    const char* formats[] = {"calibration.dec", "calibration.hex", NULL};
    for (int i = 0; formats[i]; i++) {
        if (readCalibration(h, formats[i])) {
            fprintf(stderr, "Loaded from %s\n", formats[i]);
            break;
        }
        DSI_ClearError();
    }
}
```

---

### Index/Range Errors

| Error Message | Cause | Recovery |
|---------------|-------|----------|
| `"Channel index N is out of range (M channels available)"` | Channel index exceeds count | Use valid index 0 to M-1 |
| `"Source index N is out of range (M sources available)"` | Source index exceeds count | Use valid index 0 to M-1 |
| `"ProcessingStage index N is out of range (M stages available)"` | Stage index exceeds count | Verify stage count before access |
| `"Channel index N is out of range (M channels available in ProcessingStage \"...\")"` | Stage-specific channel index error | Check channel count for specific stage |
| `"failed to match processing stage \"...\""` | Stage name not found | Use correct stage name from creation |
| `"cannot add ProcessingStage \"...\" because this name already exists in the cascade"` | Duplicate stage name | Use unique stage names |

**Detection Pattern:**
```c
int nChannels = DSI_Headset_GetNumberOfChannels(h);
printf("Available channels: %d\n", nChannels);

for (int i = 0; i < nChannels; i++) {
    DSI_Channel ch = DSI_Headset_GetChannelByIndex(h, i);
    if (!ch) {
        fprintf(stderr, "Invalid channel index %d: %s\n", 
                i, DSI_ClearError());
        break;
    }
    printf("Channel %d: %s\n", i, DSI_Channel_GetName(ch));
}
```

---

## Error Detection Patterns

### Pattern 1: Check After Critical Operations

```c
DSI_Headset h = DSI_Headset_New(NULL);
if (!h) {
    fprintf(stderr, "Failed to create headset: %s\n", DSI_ClearError());
    return -1;
}

DSI_Headset_Connect(h, "COM3");
if (DSI_Error()) {
    fprintf(stderr, "Connection failed: %s\n", DSI_ClearError());
    DSI_Headset_Delete(h);
    return -1;
}

DSI_Headset_ChooseChannels(h, "P3,Pz,P4,O1,O2", "A1+A2", 1);
if (DSI_Error()) {
    fprintf(stderr, "Montage error: %s\n", DSI_ClearError());
    // Try alternative montage
}
```

### Pattern 2: Callback for Automatic Logging

```c
int errorLogger(const char* msg, int level) {
    const char* levelStr[] = {"CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"};
    fprintf(stderr, "[%s] %s\n", 
            level < 5 ? levelStr[level] : "UNKNOWN", 
            msg);
    
    // Log to file
    FILE* f = fopen("dsi_errors.log", "a");
    if (f) {
        time_t now = time(NULL);
        fprintf(f, "%s [%s] %s\n", 
                ctime(&now), 
                levelStr[level], 
                msg);
        fclose(f);
    }
    
    return 1; // Continue execution
}

DSI_SetErrorCallback(errorLogger);
```

### Pattern 3: Validate Return Values

```c
DSI_Channel ch = DSI_Headset_GetChannelByName(h, "Pz");
if (!ch) {
    const char* err = DSI_Error();
    if (err) {
        fprintf(stderr, "Channel error: %s\n", err);
        DSI_ClearError();
    } else {
        fprintf(stderr, "Channel 'Pz' not found (no error set)\n");
    }
}
```

### Pattern 4: Monitor Buffer Overflow

```c
void monitorBuffers(DSI_Headset h) {
    size_t overflow = DSI_Headset_GetNumberOfOverflowedSamples(h);
    if (overflow > 0) {
        fprintf(stderr, "WARNING: Lost %zu samples!\n", overflow);
        
        // Calculate time lost
        double fs = DSI_Headset_GetSamplingRate(h);
        double timeLost = overflow / fs;
        fprintf(stderr, "Time lost: %.3f seconds\n", timeLost);
        
        // Increase buffer size
        DSI_Headset_StopBackgroundAcquisition(h);
        DSI_Headset_ReallocateBuffers(h, 20.0, 0.0); // 20 seconds
        DSI_Headset_FlushBuffers(h);
        DSI_Headset_StartBackgroundAcquisition(h);
        
        fprintf(stderr, "Buffer increased to 20 seconds\n");
    }
}

// Call periodically during acquisition
while (acquiring) {
    DSI_Sleep(5.0);
    monitorBuffers(h);
}
```

### Pattern 5: Combined Error and Alarm Monitoring

```c
void checkForProblems(DSI_Headset h) {
    // Check for API errors
    const char* err = DSI_Error();
    if (err) {
        fprintf(stderr, "API Error: %s\n", err);
        DSI_ClearError();
    }
    
    // Check for hardware alarms
    size_t nAlarms = DSI_Headset_GetNumberOfAlarms(h);
    if (nAlarms > 0) {
        fprintf(stderr, "Headset alarms: %zu\n", nAlarms);
        
        for (size_t i = 0; i < nAlarms; i++) {
            int alarm = DSI_Headset_GetAlarm(h, 1);  // 1 = remove from queue
            handleAlarm(alarm);
        }
    }
    
    // Check for buffer overflow
    size_t overflow = DSI_Headset_GetNumberOfOverflowedSamples(h);
    if (overflow > 0) {
        fprintf(stderr, "Buffer overflow: %zu samples lost\n", overflow);
    }
}
```

---

## Best Practices

### 1. Always Check Critical Operations

```c
// BAD - No error checking
DSI_Headset h = DSI_Headset_New(NULL);
DSI_Headset_Connect(h, "COM3");
DSI_Headset_ChooseChannels(h, "P3,Pz,P4", "A1+A2", 1);

// GOOD - Comprehensive error checking
DSI_Headset h = DSI_Headset_New(NULL);
if (!h) {
    fprintf(stderr, "Failed: %s\n", DSI_ClearError());
    return -1;
}

DSI_Headset_Connect(h, "COM3");
if (DSI_Error()) {
    fprintf(stderr, "Connection failed: %s\n", DSI_ClearError());
    DSI_Headset_Delete(h);
    return -1;
}

DSI_Headset_ChooseChannels(h, "P3,Pz,P4", "A1+A2", 1);
if (DSI_Error()) {
    fprintf(stderr, "Montage error: %s\n", DSI_ClearError());
    DSI_Headset_Delete(h);
    return -1;
}
```

### 2. Use Error Callback for Real-Time Monitoring

```c
int errorHandler(const char* msg, int level) {
    if (level <= 1) { // Critical and errors only
        fprintf(stderr, "[ERROR] %s\n", msg);
        
        // Set flag for main loop to check
        extern volatile int errorOccurred;
        errorOccurred = 1;
    }
    return 1; // Continue execution
}

DSI_SetErrorCallback(errorHandler);
```

### 3. Validate Pointers Before Use

```c
DSI_Channel ch = DSI_Headset_GetChannelByName(h, "Pz");
if (ch) {
    double val = DSI_Channel_GetSignal(ch);
    // Use val safely
} else {
    fprintf(stderr, "Channel 'Pz' not found\n");
}
```

### 4. Monitor System Health

```c
typedef struct {
    size_t samplesReceived;
    size_t samplesLost;
    size_t alarmsReceived;
    time_t lastCheck;
} HealthStats;

void updateHealth(DSI_Headset h, HealthStats* stats) {
    size_t buffered = DSI_Headset_GetNumberOfBufferedSamples(h);
    size_t overflow = DSI_Headset_GetNumberOfOverflowedSamples(h);
    size_t alarms = DSI_Headset_GetNumberOfAlarms(h);
    
    stats->samplesReceived = buffered;
    stats->samplesLost += overflow;
    stats->alarmsReceived += alarms;
    stats->lastCheck = time(NULL);
    
    // Log if problems detected
    if (overflow > 0) {
        fprintf(stderr, "Health: Lost %zu samples (total: %zu)\n",
                overflow, stats->samplesLost);
    }
    if (alarms > 0) {
        fprintf(stderr, "Health: %zu new alarms (total: %zu)\n",
                alarms, stats->alarmsReceived);
    }
}
```

### 5. Implement Graceful Degradation

```c
int connectWithRetry(DSI_Headset h, const char* port, int maxRetries) {
    for (int i = 0; i < maxRetries; i++) {
        DSI_Headset_Connect(h, port);
        
        if (!DSI_Error()) {
            printf("Connected successfully\n");
            return 1;
        }
        
        fprintf(stderr, "Attempt %d failed: %s\n", 
                i + 1, DSI_ClearError());
        
        if (i < maxRetries - 1) {
            fprintf(stderr, "Retrying in 2 seconds...\n");
            DSI_Sleep(2.0);
        }
    }
    
    fprintf(stderr, "Failed to connect after %d attempts\n", maxRetries);
    return 0;
}
```

---

## Common Error Scenarios

### Scenario 1: Port Already in Use

**Error:** `"Port in use"`

**Cause:** Another application is using the serial port

**Solution:**
```c
// Try auto-detection first
const char* port = DSI_GetDefaultPort();
if (port) {
    DSI_Headset_Connect(h, port);
    if (!DSI_Error()) {
        printf("Connected to %s\n", port);
        return;
    }
    DSI_ClearError();
}

// Try specific ports
const char* ports[] = {"COM3", "COM4", "COM5", "COM6", NULL};
for (int i = 0; ports[i]; i++) {
    printf("Trying %s...\n", ports[i]);
    DSI_Headset_Connect(h, ports[i]);
    if (!DSI_Error()) {
        printf("Connected to %s\n", ports[i]);
        return;
    }
    DSI_ClearError();
}

fprintf(stderr, "No available ports found\n");
```

### Scenario 2: Unsupported Sampling Rate

**Error:** `"Invalid sampling rate"`

**Cause:** Requested sampling rate not supported by hardware model, or feature not unlocked

**Solution:**
```c
// Check if custom sampling rates are available
if (!DSI_Headset_GetFeatureAvailability(h, "SampleRate")) {
    fprintf(stderr, "Custom sampling rates not available (feature locked)\n");
    // Use default rate (300 Hz)
    DSI_Headset_ConfigureADC(h, 300, 0);
    return;
}

const char* model = DSI_Headset_GetHardwareModel(h);

if (strstr(model, "DSI-7")) {
    // DSI-7 supports 300 Hz only
    DSI_Headset_ConfigureADC(h, 300, 0);
} else if (strstr(model, "DSI-24")) {
    // DSI-24 supports up to 1200 Hz
    DSI_Headset_ConfigureADC(h, 600, 0);
} else if (strstr(model, "VR300")) {
    // VR300 supports 300 Hz
    DSI_Headset_ConfigureADC(h, 300, 0);
}

if (DSI_Error()) {
    fprintf(stderr, "ADC config failed: %s\n", DSI_ClearError());
}
```

### Scenario 3: Invalid Montage

**Error:** `"Cannot construct channel"` or `"Source name not found"`

**Cause:** Electrode names don't match available sources

**Solution:**
```c
// List available sources first
const char* sources = DSI_Headset_GetSourceNames(h);
printf("Available sources: %s\n", sources);

// Try requested montage
DSI_Headset_ChooseChannels(h, "P3,Pz,P4", "A1+A2", 1);
if (DSI_Error()) {
    fprintf(stderr, "Montage error: %s\n", DSI_ClearError());
    
    // Use numbered sources as fallback
    DSI_Headset_ChooseChannels(h, "@1,@2,@3", "@A1+@A2", 1);
    if (!DSI_Error()) {
        printf("Using numbered source montage\n");
    }
}
```

### Scenario 4: Buffer Overflow

**Alarm:** `OverrunInFIFO` (alarm code 14)

**Cause:** Data arriving faster than application can process

**Solution:**
```c
void handleBufferOverflow(DSI_Headset h) {
    size_t overflow = DSI_Headset_GetNumberOfOverflowedSamples(h);
    if (overflow == 0) return;
    
    fprintf(stderr, "Buffer overflow: %zu samples lost\n", overflow);
    
    // Stop acquisition temporarily
    DSI_Headset_StopBackgroundAcquisition(h);
    
    // Double buffer size
    double currentSize = DSI_Headset_GetNumberOfBufferedSamples(h) / 
                        DSI_Headset_GetSamplingRate(h);
    double newSize = currentSize * 2.0;
    
    fprintf(stderr, "Increasing buffer: %.1f → %.1f seconds\n", 
            currentSize, newSize);
    
    DSI_Headset_ReallocateBuffers(h, newSize, 0.0);
    DSI_Headset_FlushBuffers(h);
    DSI_Headset_ClearAlarms(h);
    
    // Resume acquisition
    DSI_Headset_StartBackgroundAcquisition(h);
    printf("Acquisition resumed with larger buffer\n");
}
```

### Scenario 5: Data Corruption

**Error:** `"Data corruption (CRC failure)"` or `"Block failed consistency check"`

**Cause:** EMI, poor cable connection, or hardware issues

**Solution:**
```c
int corruptionCount = 0;

void monitorDataQuality(DSI_Headset h) {
    const char* err = DSI_Error();
    if (err && (strstr(err, "CRC") || strstr(err, "consistency"))) {
        corruptionCount++;
        fprintf(stderr, "Data corruption #%d: %s\n", corruptionCount, err);
        DSI_ClearError();
        
        if (corruptionCount > 10) {
            fprintf(stderr, "Excessive corruption detected!\n");
            fprintf(stderr, "Check: cables, grounding, EMI sources\n");
            
            // Consider stopping acquisition for inspection
            DSI_Headset_StopDataAcquisition(h);
        }
    }
}
```

---

## Related Documentation

- [quick_reference](quick_reference.md) - Quick function lookup
- [getting_started](getting_started.md) - Tutorial guide

---

[Back to API Index](index.md)
