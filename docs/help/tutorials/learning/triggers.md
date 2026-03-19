# Triggers and Event Alignment

A **trigger** (also called an **event marker** or **stim marker**) is a signal that marks the exact moment something happens in an experiment or application: a stimulus appears, a user responds, or a game event fires. Different fields and software packages use different terms for the same concept, but they all refer to the same thing. This marker is recorded alongside the EEG data so you can extract brain activity time-locked to each event, whether you are analyzing data offline or processing it in real time.

Accurate trigger alignment matters in both workflows:

- **Offline / ERP analysis:** Event markers define the epochs cut from a continuous recording. A timing error shifts every epoch by the same amount, distorting ERP waveforms and reducing statistical power.
- **Real-time BCI:** Markers during calibration define the training windows for your classifier. Inaccurate markers directly degrade classification accuracy before a single prediction is made.

For supported trigger types and device-specific bit depths, see {doc}`What type of external triggers are supported? <../../../faq/triggers/questions/trigger-types>`.

## Trigger Methods

Three approaches are commonly used, each with different trade-offs for timing accuracy and setup complexity.

### Hardware Triggers (MMBT-S / Trigger Hub)

Send TTL-style electrical pulses directly into the DSI trigger input at the moment of stimulus onset via the **MMBT-S** device or Wearable Sensing Trigger Hub.

- Most accurate and consistent timing; signal lands directly on the EEG trigger channel
- No network or OS scheduling latency
- Requires additional hardware and a serial port connection from your stimulus computer (or USB-to-serial adapter in the case of the MMBT-S)

```{figure} ../../../_static/images/triggerhub.jpg
:alt: Wearable Sensing Trigger Hub
:align: center
:width: 320px

Wearable Sensing Trigger Hub
```

Parallel port output from a stimulus computer is another hardware option, but parallel ports are a legacy interface not present on most modern computers. The MMBT-S via serial port is the recommended hardware trigger method.

**Guides:** {doc}`Hardware Triggers with PsychoPy <../../../examples/psychopy/hardware>`

### Software Triggers (LSL Markers)

Send marker events over a **Lab Streaming Layer (LSL)** stream from your stimulus application. LSL time-synchronizes the marker stream with the EEG stream at the recording level.

- No additional hardware needed; works across the network
- Compatible with any LSL-enabled application (PsychoPy, Unity, custom scripts)
- Introduces a small, measurable timing offset relative to actual stimulus onset with some variability based on hardware and OS scheduling. This offset must be measured and corrected for accurate epoching and analysis.

**Guides:** {doc}`Software Triggers with PsychoPy <../../../examples/psychopy/software>`

### Serial Port

Send data over a **serial port** connection. This is commonly used to pass trigger codes from a front end application to a backend application or recording system, but it can also be used in any local setup where low-latency, deterministic communication is needed.

- Lowest and most consistent latency (~1 ms); no network jitter

**Guides:** {doc}`Unity Integration <../../../examples/game-vr/unity>`, {doc}`Best Practices & Tooling <../../../examples/game-vr/best-practices>`

## Measuring and Correcting Trigger Offset

All trigger methods introduce a delay between when a trigger is sent and when the stimulus actually occurs. This offset depends on your specific setup: the stimulus presentation software, the stimuli type, the hardware, and the operating system. There is no universal value you can assume. You need to measure it for your setup, and remeasure any time the setup changes (new computer, new presentation software, new stimuli type, or significant hardware changes).

The measurement method also depends on the type of stimulus:

**Visual stimuli:** Attach a photodiode to the screen. The photodiode detects the physical light change and records it on the DSI trigger channel, giving you the true onset time to compare against your software or hardware trigger signal. We provide a complete example of this approach in the {doc}`Photodiode Experiment <../../../examples/tooling/diode/photodiode>` guide using PsychoPy.

**Audio stimuli:** Split the audio signal from your presentation computer using a Y-splitter. Send one output to your speakers or headphones as normal, and route the other into the Trigger Hub audio input. The Trigger Hub records the audio onset on the EEG trigger channel, which you can then compare against your trigger signal to measure the offset.

The {doc}`Offset Analysis <../../../examples/tooling/diode/offset>` tool visualizes timing differences and reports mean offset, standard deviation, and drift across trials for either method.

These are examples only. Your values will differ. Once measured, apply the offset as a fixed correction to your event timestamps during epoching or real-time processing.

## Offline Use: ERP and Epoch-Based Analysis

In offline ERP workflows, triggers are the anchors around which you cut epochs from a continuous recording.

- Each trigger value identifies a condition (e.g., `1` = target, `2` = non-target). Consistent, accurate coding here is what makes it possible to average across trials and recover condition-specific ERP components.
- After measuring your system's trigger offset, apply that correction when epoching so that time-zero in each epoch corresponds to true stimulus onset, not the moment the trigger was sent.


## Real-Time Use: BCI and Game Development

In real-time applications, triggers serve two roles:

1. **Stimulus markers during calibration:** Your application marks each stimulus onset so the backend can extract time-locked windows and train a classifier. The quality of these markers directly determines classifier performance.
2. **Prediction delivery:** Once trained, the backend sends classification results to the game engine over serial port or TCP to drive in-game events.

For low-latency prediction delivery, how you handle data on the backend matters as much as the communication method. Buffer incoming EEG data into fixed-size windows, process each window as it fills, and send the result immediately. Avoid blocking I/O on the main processing thread. Keeping the processing loop tight and predictable minimizes the delay between when data arrives and when a prediction is sent.

See the {doc}`Best Practices & Tooling <../../../examples/game-vr/best-practices>` page for the recommended pipeline architecture.

## Resources

- {doc}`Triggers and Timing FAQ <../../../faq/triggers/index>` — Supported trigger types and device specs
- {doc}`Software Triggers (PsychoPy) <../../../examples/psychopy/software>` — Send LSL markers from a stimulus application
- {doc}`Hardware Triggers (PsychoPy) <../../../examples/psychopy/hardware>` — Send serial port triggers via MMBT-S
- {doc}`Photodiode Experiment <../../../examples/tooling/diode/photodiode>` — Measure your system's trigger offset
- {doc}`Offset Analysis <../../../examples/tooling/diode/offset>` — Visualize and quantify timing accuracy
- {doc}`MNE-LSL Epoching <../../../examples/mne/lsl/processing/epochs>` — Epoch continuous data around event markers
- {doc}`Best Practices & Tooling <../../../examples/game-vr/best-practices>` — Real-time pipeline architecture
