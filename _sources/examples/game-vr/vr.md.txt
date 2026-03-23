# VR Development with DSI devices

Build immersive virtual reality experiences powered by real-time EEG data. Wearable Sensing devices are designed to work alongside consumer VR headsets, either with the compact VR-300 or with other DSI devices using the VR Adapter.

```{figure} ../../_static/images/vr-headset.jpg
:alt: VR-300 worn under a consumer VR headset
:align: center
:width: 320px

The VR-300 worn with a consumer VR headset for EEG in VR development
```

## Device Options for VR

The **VR-300** is the recommended device for VR development. Its low-profile form factor sits comfortably under most consumer headsets (Meta Quest, HTC Vive, Valve Index) without requiring any additional hardware.

Other DSI devices (DSI-24, DSI-7, DSI-Flex) can also be used with VR headsets using the **Wearable Sensing VR Adapter**. The adapter provides mounting clips and a head strap that secure the headset and EEG cap together.

```{figure} ../../_static/images/examples/game-vr/vr-adapter.jpg
:alt: DSI-24 with VR adapter clips attached
:align: center
:width: 200px

DSI-24 with the VR Adapter clips for use with a VR headset
```

The VR Adapter is available as an accessory for most DSI devices. Contact [Wearable Sensing](https://wearablesensing.com) for availability and compatibility with your device.

## Why EEG in VR?

Combining EEG with VR enables brain-computer interface applications in immersive environments — from neurofeedback that adapts the virtual world in real time, to active BCI control using motor imagery or P300 signals.

## Getting Started

### 1. Hardware Setup

- Seat the EEG cap properly before putting on the VR headset.
- Verify signal quality using the DSI software before launching your VR application.
- In electrically noisy environments, use a wired USB connection for more reliable data quality.

### 2. Data Pipeline

See the {doc}`Best Practices & Tooling <best-practices>` page for the full architecture diagram, tooling, and system requirements.

The pipeline:

1. Stream EEG data from the device using {doc}`LSL <../lsl/index>`.
2. A Python backend reads the LSL stream, processes the data, and sends predictions to the game engine.
3. Unity (or your engine of choice) receives predictions and uses them to drive the VR experience.

See the {doc}`Unity Integration <unity>` guide for implementation details.

### 3. LSL Markers in VR

LSL markers are the standard way to synchronize stimulus events between the game engine and the EEG backend. In a VR application, Unity sends an LSL marker at each stimulus onset. The Python backend reads both the EEG LSL stream and the marker stream to extract time-locked epochs for classification.

See the {doc}`Unity Integration <unity>` guide for code examples showing how to send LSL markers from a Unity VR scene.

### 4. VR Platform SDK Setup

The VR headset must be connected to the game engine through a platform-specific SDK before EEG data can be integrated. This is separate from the EEG streaming setup.

#### Unity XR Plugin Framework

| Headset | Plugin / Package |
|---------|-----------------|
| **Meta Quest 2/3/Pro** | [Meta XR SDK](https://developer.oculus.com/downloads/package/meta-xr-all-in-one-upm/) via Unity Package Manager |
| **HTC Vive / Valve Index / SteamVR** | [OpenXR Plugin](https://docs.unity3d.com/Manual/com.unity.xr.openxr.html) (`com.unity.xr.openxr`) |
| **Varjo / Pico / others** | [OpenXR Plugin](https://docs.unity3d.com/Manual/com.unity.xr.openxr.html) |

1. Open **Edit > Project Settings > XR Plug-in Management**.
2. Install the relevant provider plugin for your target headset.
3. Enable the provider under the **PC** or **Android** tab (Quest uses Android; PC headsets use the PC tab).
4. Optionally install the **XR Interaction Toolkit** (`com.unity.xr.interaction.toolkit`) for hand and controller input.

#### Unreal Engine OpenXR

1. Open **Edit > Plugins**, search for **OpenXR**, and enable it.
2. For Meta Quest, also enable the **Meta XR Plugin**.
3. Set the project to target the correct platform (Desktop VR or Android for Quest).

#### Godot OpenXR

1. Download the [GodotOpenXR plugin](https://github.com/GodotVR/godot_openxr) from the Godot Asset Library or GitHub.
2. Enable it in **Project > Project Settings > Plugins**.
3. Add an `XROrigin3D` node and attach an `XRCamera3D` for the player's viewpoint.

The VR SDK and EEG pipeline run independently in parallel. The SDK controls the headset; the EEG pipeline drives in-game events from brain signals.

### 5. VR-Specific Considerations

- **Frame rate:** VR requires a consistent 72-120 Hz frame rate. Offload all EEG processing to the backend so the game engine can focus on rendering.
- **Latency:** Use serial port communication for the lowest latency prediction delivery. See {doc}`Learning: Triggers & Event Alignment <../../../help/tutorials/learning/triggers>` for timing validation.
- **Comfort:** Plan for shorter sessions when combining EEG and VR hardware. Allow users to adjust both devices for a comfortable fit.
- **Motion artifacts:** Head movement in VR introduces EEG artifacts. Include artifact rejection in your processing pipeline.

## Resources

- {doc}`Learning: Triggers & Event Alignment <../../../help/tutorials/learning/triggers>`
- {doc}`Unity Integration <unity>`
- {doc}`Best Practices & Tooling <best-practices>`
- {doc}`LSL Integration <../lsl/index>`
