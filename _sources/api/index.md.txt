# DSI API Documentation

The DSI API provides programmatic control of Wearable Sensing DSI headsets for real-time EEG data acquisition, impedance testing, and signal processing. Available for **C/C++** and **Python** across Windows, Linux, and macOS. Other platforms or language extensions may be supported via request, please visit our [contact page](../help/index.md).

```{admonition} API Version
:class: tip
**Version:** 1.20.3  
**Last Updated:** June, 6 2025  
**Platforms:** Windows, Linux, macOS  
**Languages:** C/C++, Python
```

---

## Key Capabilities

- **Connect & Configure**: Serial connections via USB or Bluetooth with flexible channel setups.
- **Acquire EEG Data**: Real-time streaming at 300 Hz with configurable filtering
- **Test Impedance**: Measure electrode contact quality
- **Process Signals**: Custom real-time processing with sample-by-sample callbacks
- **Control Hardware**: Analog reset, LED indicators, and low-level features

---

## DSI-API Sections

### [Getting Started](getting_started/index.md)
**Best for:** First-time users, tutorial-based learning

Step-by-step tutorials with C and Python examples covering:
- Quick start guide to streaming data
- Four detailed tutorials: connection, data acquisition, impedance testing, and background acquisition
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

**Need examples?** Check `demo.c` and `DSI.py` included with your DSI-API download.

---


```{toctree}
:maxdepth: 4
:hidden:

Getting Started <getting_started/index>
Quick Reference <quick_reference>
Error Codes <error_codes>

```

---

[← Back to Home](../index.md)
