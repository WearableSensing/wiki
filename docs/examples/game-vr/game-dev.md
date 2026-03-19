# Game Development with DSI

Wearable Sensing EEG headsets open up a range of possibilities for game development — from neurofeedback experiences and educational tools to adaptive gameplay driven by real-time brain signals. EEG data can inform game mechanics whether used offline (e.g., analyzing session data to adjust difficulty) or online (e.g., classifying brain states in real time to drive controls). For full architecture, tooling, and system setup, see {doc}`Best Practices & Tooling <best-practices>`.

## Use Cases

- **Neurofeedback games** — Display a live metric derived from EEG (e.g., alpha power, attention index) that updates game state as the user modulates their brain activity. Requires continuous streaming; no discrete events needed.
- **Adaptive and educational games** — Use offline EEG analysis between sessions or rounds to adjust difficulty, pacing, or content based on cognitive load, engagement, or fatigue.
- **BCI-controlled games** — Classify brain states in real time (motor imagery, P300, SSVEP) and map predictions to game inputs. Requires a processing backend and accurate stimulus-onset markers during calibration.
- **Research-driven game mechanics** — Collect EEG alongside gameplay data for analysis. The game acts as a structured paradigm; EEG is analyzed post-hoc.

---

## Core Integration

The general pipeline connects your DSI headset to your game engine through a processing backend:

1. **Stream EEG data** from your DSI device using {doc}`LSL <../lsl/index>` via the {doc}`dsi2lslGUI <../lsl/gui>`.
2. **Process signals** in a Python backend (filtering, feature extraction, classification or metric computation). See {doc}`Best Practices & Tooling <best-practices>` for the tooling landscape.
3. **Send outputs** to your game engine via LSL — predictions for BCI control, or continuous metrics for neurofeedback.
4. **Handle events** in your game engine and map outputs to game actions:

```csharp
void HandlePrediction(int prediction)
{
    switch (prediction)
    {
        case 0: // e.g., "rest" — no action
            break;
        case 1: // e.g., "left motor imagery"
            player.MoveLeft();
            break;
        case 2: // e.g., "right motor imagery"
            player.MoveRight();
            break;
        case 3: // e.g., "target detected (P300)"
            player.Select();
            break;
    }
}
```

See the {doc}`Unity Integration <unity>` guide for full code examples including LSL marker sending and prediction receiving.

---

## BCI Paradigms

For online BCI control, the following paradigms are most common in game applications:

- **P300 spellers and grid selection** — Flash items in a rapid sequence; classify the P300 response to identify the attended target. Requires precise stimulus-onset markers aligned with EEG.
- **SSVEP selection** — Display items flickering at different frequencies; classify the steady-state frequency response. Requires stable frame-rate rendering for consistent flicker.
- **Motor imagery** — Classify left vs. right motor imagery for directional control. More tolerant of timing offsets but benefits from accurate event markers during calibration.
- **Neurofeedback** — Display a metric (e.g., alpha power) that responds to brain state in real time. Requires continuous streaming rather than discrete event triggering.

The [bci-essentials-python](https://github.com/kirtonBCIlab/bci-essentials-python) package includes example scripts for each paradigm above. These pair directly with [bci-essentials-unity](https://github.com/kirtonBCIlab/bci-essentials-unity) for Unity-side stimulus presentation.

---

## Starting with 2D Games

2D games are a natural starting point for EEG-driven development. Lower performance overhead leaves more headroom for signal processing, and simpler game logic makes it easier to isolate integration issues. Common BCI paradigms (P300 grids, SSVEP selection, motor imagery) map naturally to 2D interfaces; neurofeedback mechanics are also straightforward to prototype in 2D.

**Getting started with Unity 2D:**
1. Create a new Unity project using the **2D (Built-in Render Pipeline)** template.
2. Add sprites and UI elements for your game board or stimulus presentation.
3. Write scripts that respond to EEG outputs from your backend.
4. Use Unity's built-in 2D physics, tilemaps, and animation systems as needed.

For free prototyping assets, [itch.io](https://itch.io/game-assets/free) hosts a large library of sprites, models, audio, and UI kits.

```{admonition} Check the License
:class: warning
Always read the license for any asset you download. Some free assets are restricted to non-commercial or personal use. If you plan to distribute or publish, confirm the license permits your use case.
```

---

## Game Design Considerations

- **Latency tolerance** — Design mechanics that accommodate EEG processing latency (typically 100–500ms depending on the approach). Avoid mechanics requiring split-second reaction to brain signals.
- **Feedback loops** — Provide clear visual or audio feedback when brain state changes are detected. This helps users learn to modulate their activity and makes neurofeedback more effective.
- **Calibration** — For BCI control, plan a calibration phase at the start of each session to adapt classifiers to the individual user. See {doc}`Learning: Triggers & Event Alignment <../../../help/tutorials/learning/triggers>` for guidance on stimulus marker alignment during calibration.
- **Fallback controls** — Consider providing standard input methods alongside EEG-based controls for a better user experience and easier debugging.

---

## Featured

```{card} BCI4Kids
[BCI4Kids](https://github.com/kirtonBCIlab) is a research initiative that uses DSI headsets to build brain-computer interface games for children — demonstrating how EEG-driven games can be both engaging and scientifically rigorous.

**What it uses:**
- [bci-essentials-unity](https://github.com/kirtonBCIlab/bci-essentials-unity) — pre-built BCI paradigms (P300, SSVEP, motor imagery) for Unity
- [bci-essentials-python](https://github.com/kirtonBCIlab/bci-essentials-python) — signal processing and classification backend
```

---

## Resources

- {doc}`Learning: Triggers & Event Alignment <../../../help/tutorials/learning/triggers>`
- {doc}`Unity Integration <unity>`
- {doc}`Best Practices & Tooling <best-practices>`
- {doc}`LSL Integration <../lsl/index>`
- [bci-essentials-unity](https://github.com/kirtonBCIlab/bci-essentials-unity)
- [bci-essentials-python](https://github.com/kirtonBCIlab/bci-essentials-python)
