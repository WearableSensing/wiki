# DSI API Documentation

The DSI API provides programmatic control of Wearable Sensing DSI headsets for real-time EEG data acquisition, impedance testing, and signal processing. Available for **C/C++** and **Python** across Windows, Linux, and macOS.

```{admonition} API Version
:class: tip
**Version:** 1.20.4  
**Last Updated:** November 2025  
**Platforms:** Windows, Linux, macOS  
**Languages:** C/C++, Python
```

---

## Key Capabilities

- **Connect & Configure**: Serial connections via USB, Bluetooth, or COM ports
- **Acquire EEG Data**: Real-time streaming at up to 300 Hz with configurable filtering
- **Test Impedance**: Measure electrode contact quality
- **Process Signals**: Custom real-time processing with sample-by-sample callbacks
- **Control Hardware**: Analog reset, LED indicators, and low-level features

---

## DSI-API Sections

### [Getting Started](getting_started.md)
**Best for:** First-time users, tutorial-based learning

Step-by-step tutorials with C and Python examples covering:
- Quick start guide to streaming data
- Five detailed tutorials: connection, data acquisition, impedance testing, real-time processing, and background acquisition
- Prerequisites, common tasks, and troubleshooting

---

### [Quick Reference](quick_reference.md)
**Best for:** Experienced developers, fast lookup

Complete function reference with:
- All function signatures and parameter types
- Common workflows and code patterns
- Error handling best practices
- Type definitions and enums

---

### [Error Codes](error_codes.md)
**Best for:** Troubleshooting and debugging

Comprehensive error reference with:
- Connection, configuration, and acquisition errors
- Hardware state errors
- Detailed causes and solutions

---

## Common Tasks

- [Connect to a headset](getting_started.md#tutorial-1-basic-connection) • [Configure channels](getting_started.md#tutorial-2-channel-configuration) • [Stream EEG data](getting_started.md#tutorial-3-data-acquisition)
- [Check impedances](getting_started.md#task-check-impedances) • [Background acquisition](getting_started.md#tutorial-4-background-acquisition) • [Real-time processing](getting_started.md#tutorial-5-real-time-processing)

**Need examples?** Check `demo.c` and `DSI.py` included with your API.

---


```{toctree}
:maxdepth: 3
:hidden:

getting_started
quick_reference
error_codes

```

---

[← Back to Home](../index.md)
