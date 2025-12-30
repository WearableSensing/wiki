# Quick Reference

> **Fast lookup guide** — Function signatures organized by category for experienced developers.

This page provides a complete function reference organized by task. Each section groups related functions together, making it easy to find what you need. For detailed tutorials and examples, see [Getting Started](getting_started/index.md).

## Table of Contents

- [General Purpose Functions](#general-purpose-functions)
- [Headset Lifecycle](#headset-lifecycle)
- [Connection Management](#connection-management)
- [Device Configuration](#device-configuration)
- [Montage Configuration](#montage-configuration)
- [Data Acquisition](#data-acquisition)
- [Buffer Management](#buffer-management)
- [Device Information](#device-information)
- [Feature Queries](#feature-queries)
- [Impedance Testing](#impedance-testing)
- [Alarm System](#alarm-system)
- [Source Naming](#source-naming)
- [Hardware Control](#hardware-control)
- [Processing Stages](#processing-stages)
- [Channel Functions](#channel-functions)
- [Source Functions](#source-functions)

---

## General Purpose Functions

Core utilities and error handling used throughout the API.

### Error Handling
```c
const char* DSI_Error(void)
const char* DSI_ClearError(void)
void DSI_SetErrorCallback(DSI_MessageCallback func)
```

### Utilities
```c
const char* DSI_GetAPIVersion(void)
const char* DSI_GetDefaultPort(void)
void DSI_Sleep(double seconds)
```

---

## Headset Lifecycle

Fundamental headset object creation and cleanup. Always use `DSI_Headset_New(NULL)` followed by `DSI_Headset_Connect(h, port)` for connection.

```c
DSI_Headset DSI_Headset_New(const char* port)
void DSI_Headset_Delete(DSI_Headset h)
```

---

## Connection Management

```c
void DSI_Headset_Connect(DSI_Headset h, const char* port)
int DSI_Headset_IsConnected(DSI_Headset h)
double DSI_Headset_SecondsSinceConnection(DSI_Headset h)
const char* DSI_Headset_GetPort(DSI_Headset h)
void DSI_Headset_Disconnect(DSI_Headset h)
```

---

## Device Configuration

### Core Configuration
```c
void DSI_Headset_ConfigureADC(DSI_Headset h, unsigned int samplesPerSecond, unsigned int filterMode)
void DSI_Headset_SetAccelerometerRate(DSI_Headset h, unsigned int rate)
void DSI_Headset_SetVerbosity(DSI_Headset h, int level)
```

**Note:** Configuring non-default sampling rates requires the appropriate feature to be unlocked on your headset. Check `DSI_Headset_GetFeatureAvailability(h, "SampleRate")` before attempting to configure custom rates.

### Callbacks
```c
void DSI_Headset_SetMessageCallback(DSI_Headset h, DSI_MessageCallback func)
void DSI_Headset_SetSampleCallback(DSI_Headset h, DSI_SampleCallback func, void* userData)
```

---

## Montage Configuration

Define which electrodes to use and how to reference them. A **montage** is a specification like `"P3,Pz,P4"` that defines your channel layout.

```c
void DSI_Headset_ChooseChannels(DSI_Headset h, const char* montage, const char* reference, int autoswap)
void DSI_Headset_AddChannelToMontage_FromSource(DSI_Headset h, DSI_Source s)
void DSI_Headset_AddChannelToMontage_FromString(DSI_Headset h, const char* spec, int autoswap)
void DSI_Headset_SetDefaultReference(DSI_Headset h, const char* spec, int autoswap)
const char* DSI_Headset_SetTraditionalReference(DSI_Headset h, int autoswap)
const char* DSI_Headset_GetFactoryReferenceString(DSI_Headset h)
const char* DSI_Headset_GetReferenceString(DSI_Headset h)
void DSI_Headset_ForgetMontage(DSI_Headset h)
int DSI_Headset_GetNumberOfChannels(DSI_Headset h)
DSI_Channel DSI_Headset_GetChannelByIndex(DSI_Headset h, unsigned int index)
DSI_Channel DSI_Headset_GetChannelByName(DSI_Headset h, const char* name)
int DSI_Headset_GetNumberOfSources(DSI_Headset h)
DSI_Source DSI_Headset_GetSourceByIndex(DSI_Headset h, unsigned int index)
DSI_Source DSI_Headset_GetSourceByName(DSI_Headset h, const char* name)
const char* DSI_Headset_GetMontageString(DSI_Headset h)
```

---

## Data Acquisition

Control when and how data is collected from the headset. Choose foreground (you control the loop) or background (automatic callback) acquisition.

### Foreground Acquisition
```c
void DSI_Headset_StartDataAcquisition(DSI_Headset h)
void DSI_Headset_StopDataAcquisition(DSI_Headset h)
void DSI_Headset_Receive(DSI_Headset h, double seconds, double idleAfter)
size_t DSI_Headset_WaitForSamples(DSI_Headset h, size_t target)
void DSI_Headset_Idle(DSI_Headset h, double seconds)
```

### Background Acquisition
```c
int DSI_Headset_StartBackgroundAcquisition(DSI_Headset h)
void DSI_Headset_StopBackgroundAcquisition(DSI_Headset h)
```

---

## Buffer Management

Manage internal sample buffers. Buffers are allocated automatically when you configure channels, but you can adjust sizes and monitor status.

### Buffer Control
```c
void DSI_Headset_ReallocateBuffers(DSI_Headset h, double secondsForSignal, double secondsForImpedance)
void DSI_Headset_FlushBuffers(DSI_Headset h)
size_t DSI_Headset_GetNumberOfBufferedSamples(DSI_Headset h)
size_t DSI_Headset_GetNumberOfOverflowedSamples(DSI_Headset h)
```

### Buffering Controller
```c
void DSI_Headset_ConfigureBufferingController(DSI_Headset h, 
    double secondsBetweenUpdates, double smoothing, double P, double I, double D)
void DSI_Headset_ConfigureBatch(DSI_Headset h, unsigned int nSamples, double targetDelaySeconds)
double DSI_Headset_WaitForBatch(DSI_Headset h)
```

---

## Device Information

```c
const char* DSI_Headset_GetHardwareModel(DSI_Headset h)
const char* DSI_Headset_GetHardwareRevision(DSI_Headset h)
const char* DSI_Headset_GetFirmwareRevision(DSI_Headset h)
unsigned int DSI_Headset_GetSerialNumber(DSI_Headset h)
unsigned int DSI_Headset_GetSensorCount(DSI_Headset h)
double DSI_Headset_GetSamplingRate(DSI_Headset h)
double DSI_Headset_GetAccelerometerRate(DSI_Headset h)
int DSI_Headset_GetFilterMode(DSI_Headset h)
int DSI_Headset_GetDataAcquisitionMode(DSI_Headset h)
int DSI_Headset_GetImpedanceDriverMode(DSI_Headset h)
int DSI_Headset_GetAnalogResetMode(DSI_Headset h)
double DSI_Headset_GetBatteryLevel(DSI_Headset h, int whichBattery)
const char* DSI_Headset_GetBatteryLevelString(DSI_Headset h)
const char* DSI_Headset_GetInfoString(DSI_Headset h)
```

---

## Feature Queries

```c
void DSI_Headset_QueryUnlockedFeatures(DSI_Headset h)
int DSI_Headset_GetFeatureAvailability(DSI_Headset h, const char* featureName)
```

### Hardware State
```c
void DSI_Headset_SendBatteryQuery(DSI_Headset h)
int DSI_Headset_IsBlueToothInitialized(DSI_Headset h)
```

---

## Impedance Testing

Measure electrode contact quality. Start the impedance driver, wait ~2 seconds for stabilization, then read values from individual sources using `DSI_Source_GetImpedanceEEG()`.

```c
void DSI_Headset_StartImpedanceDriver(DSI_Headset h)
void DSI_Headset_StopImpedanceDriver(DSI_Headset h)
double DSI_Headset_GetImpedanceCMF(DSI_Headset h)
```

---

## Alarm System

```c
int DSI_Headset_GetAlarm(DSI_Headset h, int remove)
size_t DSI_Headset_GetNumberOfAlarms(DSI_Headset h)
void DSI_Headset_ClearAlarms(DSI_Headset h)
```


---

## Source Naming

```c
void DSI_Headset_UseNamingScheme(DSI_Headset h, const char* schemeName)
int DSI_Headset_RenameSource(DSI_Headset h, const char* oldName, const char* newName)
int DSI_Headset_AddSourceAliases(DSI_Headset h, const char* aliasString)
const char* DSI_Headset_GetSourceNames(DSI_Headset h, DSI_SourceSelection selection)
```

---

## Hardware Control

### Analog Reset
```c
void DSI_Headset_StartAnalogReset(DSI_Headset h)
void DSI_Headset_LockAnalogReset(DSI_Headset h)
void DSI_Headset_ReleaseAnalogReset(DSI_Headset h)
```

### Low-Level Control
```c
void DSI_Headset_Shutdown(DSI_Headset h)
void DSI_Headset_KillDataStream(DSI_Headset h, int expectReply)
void DSI_Headset_UseOptionalCommandPrefix(DSI_Headset h, int enable)
void DSI_Headset_ChangeLEDs(DSI_Headset h, int setAndSelect)
```

---

## Processing Stages

Create custom data processing pipelines. Processing stages work sample-by-sample through callbacks.

```c
DSI_ProcessingStage DSI_Headset_AddProcessingStage(DSI_Headset h, const char* name, 
    DSI_SampleCallback func, void* paramData, DSI_ProcessingStage input)
unsigned int DSI_Headset_GetNumberOfProcessingStages(DSI_Headset h)
DSI_ProcessingStage DSI_Headset_GetProcessingStageByIndex(DSI_Headset h, unsigned int index)
DSI_ProcessingStage DSI_Headset_GetProcessingStageByName(DSI_Headset h, const char* name)
void DSI_Headset_ReallocateStageBuffers(DSI_Headset h, DSI_ProcessingStage stage, double seconds)
void DSI_ProcessingStage_ClearChannels(DSI_ProcessingStage p)
DSI_Channel DSI_ProcessingStage_AddChannel(DSI_ProcessingStage p, const char* name, size_t bufferSamples)
DSI_Channel DSI_ProcessingStage_GetChannelByIndex(DSI_ProcessingStage p, unsigned int index)
DSI_Channel DSI_ProcessingStage_GetChannelByName(DSI_ProcessingStage p, const char* name)
DSI_ProcessingStage DSI_ProcessingStage_GetInput(DSI_ProcessingStage p)
const char* DSI_ProcessingStage_GetName(DSI_ProcessingStage p)
void* DSI_ProcessingStage_ParamData(DSI_ProcessingStage p)
unsigned int DSI_ProcessingStage_GetNumberOfChannels(DSI_ProcessingStage p)
double DSI_ProcessingStage_Read(DSI_ProcessingStage p, unsigned int channel, size_t lookbackSteps)
void DSI_ProcessingStage_Write(DSI_ProcessingStage p, unsigned int channel, double value)
```

---

## Channel Functions

Access data from individual channels. `ReadBuffered()` returns one sample at a time; call it in a loop to read multiple samples.

### Data Access
```c
double DSI_Channel_GetSignal(DSI_Channel ch)
double DSI_Channel_ReadBuffered(DSI_Channel ch)
double DSI_Channel_LookBack(DSI_Channel ch, size_t nSteps)
size_t DSI_Channel_GetNumberOfBufferedSamples(DSI_Channel ch)
size_t DSI_Channel_GetNumberOfOverflowedSamples(DSI_Channel ch)
size_t DSI_Channel_GetBufferCapacity(DSI_Channel ch)
void DSI_Channel_FlushOutputBuffer(DSI_Channel ch)
```

### Channel Properties
```c
const char* DSI_Channel_GetName(DSI_Channel ch)
const char* DSI_Channel_GetString(DSI_Channel ch)
void DSI_Channel_SetName(DSI_Channel ch, const char* name)
double DSI_Channel_CalculateRawSignal(DSI_Channel ch)
int DSI_Channel_IsReferentialEEG(DSI_Channel ch)
int DSI_Channel_IsTrigger(DSI_Channel ch)
```

---

## Source Functions

### Source Properties
```c
const char* DSI_Source_GetName(DSI_Source s)
void DSI_Source_SetName(DSI_Source s, const char* name)
double DSI_Source_GetSignal(DSI_Source s)
double DSI_Source_GetImpedanceEEG(DSI_Source s)
double DSI_Source_GetGain(DSI_Source s)
double DSI_Source_GetDCOffset(DSI_Source s)
```

### Source Type Queries
```c
int DSI_Source_IsReferentialEEG(DSI_Source s)
int DSI_Source_IsFactoryReference(DSI_Source s)
int DSI_Source_IsTrigger(DSI_Source s)
int DSI_Source_IsSensor(DSI_Source s)
int DSI_Source_IsCommonModeSignal(DSI_Source s)
```

---

## Type Definitions

### Callback Types
```c
typedef int (*DSI_MessageCallback)(const char* msg, int debugLevel);
typedef void (*DSI_SampleCallback)(DSI_Headset h, double packetTime, void* userData);
```

### Handle Types
```c
typedef char* DSI_Headset;
typedef short* DSI_Channel;
typedef long* DSI_Source;
typedef double* DSI_ProcessingStage;
```

### Source Selection Flags
```c
typedef enum {
    ActiveSensors       =   1,
    IgnoredSensors      =   2,
    UnconnectedSensors  =   4,
    Reference           =   8,
    Triggers            =  16,
    Clocks              =  32,
    CommonModeSignal    =  64,
    NullSignal          = 128,
    TriggerBits         = 256,
    ConnectedSensors    = (ActiveSensors + IgnoredSensors),
    AllSensors          = (ConnectedSensors + UnconnectedSensors),
    Default             = (AllSensors + Triggers),
    Everything          = 0xffff
} DSI_SourceSelection;
```

---

## Common Return Values

### Boolean Returns
- `1` = true/success
- `0` = false/failure

### Pointer Returns
- Valid pointer = success
- `NULL` = failure (check `DSI_Error()`)

### Double Returns
- Valid value or special indicators:
  - `-1.0` = invalid/not available
  - `0.0` = timeout (for `WaitFor*` functions)

---

## Error Handling Pattern

```c
// Check errors after critical operations
DSI_Headset h = DSI_Headset_New(NULL);
if (!h || DSI_Error()) {
    fprintf(stderr, "Error: %s\n", DSI_ClearError());
    return -1;
}

DSI_Headset_Connect(h, "COM3");
if (DSI_Error()) {
    fprintf(stderr, "Connection failed: %s\n", DSI_ClearError());
    DSI_Headset_Delete(h);
    return -1;
}

DSI_Headset_ChooseChannels(h, "P3,Pz,P4", "@P3,P4", 1);
if (DSI_Error()) {
    fprintf(stderr, "Montage failed: %s\n", DSI_ClearError());
    DSI_Headset_Delete(h);
    return -1;
}

DSI_Headset_StartDataAcquisition(h);
if (DSI_Error()) {
    fprintf(stderr, "Acquisition failed: %s\n", DSI_ClearError());
    DSI_Headset_Delete(h);
    return -1;
}
```

**See:** [error_codes](error_codes.md) for complete error reference

---

## Common Workflows

Typical sequences for common tasks. These show the correct order of operations for different acquisition modes.

### Basic Acquisition
```c
1. DSI_Headset_New(NULL)
2. DSI_Headset_Connect(h, port)
3. DSI_Headset_ChooseChannels(h, montage, reference, autoswap)
4. DSI_Headset_StartDataAcquisition(h)
5. Loop: DSI_Headset_Idle(h, seconds)
6. Read: for each buffered sample, call DSI_Channel_ReadBuffered(ch)
7. DSI_Headset_StopDataAcquisition(h)
8. DSI_Headset_Delete(h)
```

### Background Acquisition
```c
1. DSI_Headset_New(NULL)
2. DSI_Headset_Connect(h, port)
3. DSI_Headset_ChooseChannels(h, montage, reference, autoswap)
4. DSI_Headset_SetSampleCallback(h, callback, userData)
5. DSI_Headset_StartBackgroundAcquisition(h)
6. ... application continues ...
7. DSI_Headset_StopBackgroundAcquisition(h)
8. DSI_Headset_Delete(h)
```

---

## Platform Differences

| Feature | Windows | Linux | macOS |
|---------|---------|-------|-------|
| Default ports | COM1-COM256 | /dev/ttyUSB*, /dev/ttyACM* | /dev/tty.usb*, /dev/cu.usb* |
| Bluetooth | Full support | Full support | Limited (see docs) |
| LED control | Supported | Supported | Model-dependent |

---

## Related Documentation

- [getting_started](getting_started/index.md) - Comprehensive tutorials
- [error_codes](error_codes.md) - Error handling reference

---

[← Back to API Index](index.md)
