# Game Development & VR Integration

```{figure} ../../_static/images/examples/game-vr/dsi24-vr.jpg
:alt: DSI-24 in a VR development setup
:align: center
:width: 150px

DSI-24 with VR Adapter clips
```

Use Wearable Sensing EEG devices with game engines and VR platforms to create brain-computer interface experiences. Stream real-time neural data into your engine of choice, trigger in-game events from brain signals, and build immersive neurofeedback applications.

The concepts and architecture described here apply to any game engine. Unity, Unreal Engine, Godot, and others can all consume LSL streams and communicate with a Python backend. The documentation focuses on Unity as the primary example, but the same approaches work across platforms.

## What Are You Looking For?

````{grid} 2
:gutter: 3

```{grid-item-card} How do I align triggers and events?
:link: ../../../help/tutorials/learning/triggers
:link-type: doc
:text-align: center
```

```{grid-item-card} How do I get EEG data into my engine?
:link: best-practices
:link-type: doc
:text-align: center
```

```{grid-item-card} How do I build a real-time BCI game?
:link: game-dev
:link-type: doc
:text-align: center
```

```{grid-item-card} How do I develop for VR with EEG?
:link: vr
:link-type: doc
:text-align: center
```

````

## Tutorials

```{toctree}
:maxdepth: 1
:hidden:

Best Practices & Tooling <best-practices>
Unity Integration <unity>
Game Development <game-dev>
VR Development <vr>
```

- **{doc}`Best Practices & Tooling <best-practices>`** — Recommended architecture, triggering methods, tooling overview, and system requirements. Start here before anything else.
- **{doc}`Unity Integration <unity>`** — How to receive LSL markers and EEG data in Unity, with Python backend examples and communication code.
- **{doc}`Game Development <game-dev>`** — BCI paradigms, game design considerations, and an overview of the bci-essentials framework for building BCI games.
- **{doc}`VR Development <vr>`** — Device selection, VR adapter setup, platform SDK configuration, and EEG-VR integration patterns.

## Additional Resources

- {doc}`Learning: Triggers & Event Alignment <../../../help/tutorials/learning/triggers>`
- {doc}`LSL Integration <../lsl/index>`
- {doc}`DSI-API <../../api/index>`
- [bci-essentials-unity](https://github.com/kirtonBCIlab/bci-essentials-unity)
- [bci-essentials-python](https://github.com/kirtonBCIlab/bci-essentials-python)
