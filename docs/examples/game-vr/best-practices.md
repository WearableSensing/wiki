# Best Practices & Tooling

Architecture recommendations, triggering strategy, tooling, and system requirements for running EEG-driven games and VR applications with Wearable Sensing devices.

## Recommended Architecture

Use a separate backend to handle all EEG signal processing. The game engine should only receive final predictions or send/receive event markers. This keeps rendering performance stable and the two concerns cleanly separated.

```
┌──────────────────────┐
│      DSI Headset     │  VR-300 / DSI-24
└──────────┬───────────┘
           │  EEG data  (USB / Bluetooth)
           ▼
┌───────────────────────────────────────────────────────┐
│                    LSL Stream                         │
│  ─────────────────────────────────────────────────── │
│  EEG data channels   (dsi2lslGUI)                     │
│  Trigger channel     (hardware events embedded here)  │
└──────────┬────────────────────────────────────────────┘
           │  pylsl              LSL markers (stim events)
           │          ┌─────────────────────────────────────────┐
           ▼          ▼                                          │
┌──────────────────────────────────┐     ┌──────────────────────┴─────┐
│         Python Backend           │     │  Game Engine or            │
│  ──────────────────────────────  │     │  Presentation Software     │
│  Reads EEG data stream           │     │                            │
│  Reads event markers             │     │  Sends stim markers (LSL)  │
│  Parses trigger channel          │     │  Receives predictions to   │
│  Filter → Feature Ext. → Classify│     │  drive game events         │
└────────────────┬─────────────────┘     └────────────────────────────┘
                 │  predictions  (LSL)                 ▲
                 └─────────────────────────────────────┘
```

The game engine (or presentation software) sends event markers via LSL to the backend during calibration so the backend can extract time-locked EEG windows. The DSI trigger channel in the LSL stream also carries hardware triggers sent from the game engine via serial/MMBT-S. Once the classifier is trained, the backend sends predictions back to the game engine via LSL, which uses them to drive game events.

## Triggering

There are two distinct trigger flows in the pipeline, each serving a different purpose.

**Stimulus markers (game engine → backend):** During calibration, the game engine marks each stimulus onset so the backend can extract time-locked EEG windows. Two methods are available:

| Method | Latency | Notes |
|--------|---------|-------|
| **LSL Markers** | Low | Standard software approach; no extra hardware needed |
| **MMBT-S (Serial)** | Lowest (~1ms) | Hardware trigger embedded directly in EEG trigger channel |

**Predictions (backend → game engine):** Once the classifier is trained, the backend sends classification results back to the game engine via LSL. The game engine reads these using LSL4Unity (or equivalent) and maps them to game events.

See the {doc}`Unity Integration <unity>` guide for code examples, and the {doc}`Learning: Triggers & Event Alignment <../../../help/tutorials/learning/triggers>` page for a complete guide on trigger methods, timing offsets, and validation.

## Tooling

Key tools and libraries organized by their role in the pipeline.

### Data Streaming

| Tool | Description | Link |
|------|-------------|------|
| **dsi2lslGUI** | Stream DSI headset data (EEG + trigger channel) over LSL | {doc}`Guide <../lsl/gui>` |
| **pylsl** | Python library for reading LSL streams in the backend | [GitHub](https://github.com/labstreaminglayer/pylsl) |
| **LSL4Unity** | Unity plugin for sending and receiving LSL streams | [GitHub](https://github.com/labstreaminglayer/LSL4Unity) |

### Signal Processing & Classification

| Tool | Description | Link |
|------|-------------|------|
| **bci-essentials-python** | Python BCI signal processing and classification | [GitHub](https://github.com/kirtonBCIlab/bci-essentials-python) |
| **MNE-Python** | Comprehensive EEG analysis library | [Docs](https://mne.tools/stable/index.html) |
| **NumPy / SciPy** | Numerical computing and signal processing | [NumPy](https://numpy.org/) / [SciPy](https://scipy.org/) |

### Game Engine Integration

| Tool | Description | Link |
|------|-------------|------|
| **bci-essentials-unity** | Pre-built BCI paradigms and game components for Unity | [GitHub](https://github.com/kirtonBCIlab/bci-essentials-unity) |
| **Unity** | Primary documented game engine | [unity.com](https://unity.com/) |
| **Unreal Engine** | Supported via LSL backend architecture | [unrealengine.com](https://www.unrealengine.com/) |
| **Godot** | Supported via LSL backend architecture | [godotengine.org](https://godotengine.org/) |

## System Requirements

Running EEG acquisition alongside a game engine or VR application is demanding. A machine dedicated to this purpose is strongly recommended: sharing the machine with other software introduces timing variability that can affect both EEG data quality and rendering performance.

### Desktop Game Development

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **OS** | Windows 10 | Windows 11 |
| **CPU** | Intel i5 / AMD Ryzen 5 | Intel i7 / AMD Ryzen 7 or better |
| **RAM** | 16 GB | 32 GB |
| **GPU** | NVIDIA GTX 1060 / AMD RX 580 | NVIDIA RTX 3060 or better |
| **Storage** | SSD with 10 GB free | NVMe SSD |

### VR Development

VR applications are significantly more demanding. The system must render at high frame rates (72-120 Hz) while simultaneously handling EEG data acquisition.

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **OS** | Windows 10 | Windows 11 |
| **CPU** | Intel i7 / AMD Ryzen 7 | Intel i9 / AMD Ryzen 9 |
| **RAM** | 32 GB | 64 GB |
| **GPU** | NVIDIA RTX 2070 / AMD RX 6700 XT | NVIDIA RTX 4070 or better |
| **Storage** | SSD with 20 GB free | NVMe SSD |

```{admonition} VR Headset Requirements
:class: warning
Ensure your system meets the VR headset manufacturer's recommended specifications in addition to the requirements above. Running EEG acquisition and processing alongside VR adds overhead that the headset specs alone do not account for.
```

## Performance Optimization

### Engine

- Minimize garbage collection: avoid allocating new objects in the main loop. Pre-allocate buffers for incoming data.
- Use asynchronous I/O: read LSL streams on a background thread and pass results to the main thread via a thread-safe queue.
- Profile regularly: use the engine's built-in profiler to identify frame rate drops and ensure EEG data handling is not a bottleneck.
- Reduce draw calls: batch materials, use LOD groups, and optimize shaders, especially for VR.

### Backend

- Buffer data: process EEG data in fixed-size windows rather than sample-by-sample.
- Use efficient libraries: NumPy, SciPy, and MNE-Python are optimized for EEG signal processing.
- Limit output rate: send predictions at a reasonable rate (e.g., 10-30 Hz), not at the EEG sampling rate.
- Profile memory: long-running backends can accumulate memory usage. Monitor and manage data buffers.

### DSI Device Tips

- Check impedance before each session. Poor electrode contact leads to noisy data and unreliable predictions.
- Secure cables to reduce motion artifacts, particularly in VR where head movement is frequent.

## Resources

- {doc}`Unity Integration <unity>`
- {doc}`VR Development <vr>`
- {doc}`Game Development <game-dev>`
- {doc}`LSL Integration <../lsl/index>`
- {doc}`Learning: Triggers & Event Alignment <../../../help/tutorials/learning/triggers>`
