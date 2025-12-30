# Getting Started

> **API tutorials and guides** — Learn to connect, configure, and acquire EEG data from DSI headsets using the DSI API.

## Overview

This guide will help you get started with the DSI API. Choose your programming language to follow step-by-step tutorials covering connection, configuration, data acquisition, and common tasks.

---

## Prerequisites

### Hardware
- DSI headset (DSI-7, DSI-24, DSI-Flex, or DSI-VR300)
- USB cable or Bluetooth adapter
- Charged battery

### Software

See the DSI [Downloads](../../help/downloads/index.md) page for the latest API release.

- DSI API library (`DSI.dll` / `DSI.so` / `DSI.dylib`)
- Header file (`DSI.h`) for C/C++
- Python wrapper (`DSI.py`) for Python 2.6+

### Platform Support

- **Windows:** Visual Studio 2015+ or MinGW (requires `DSI.dll`)
- **Linux:** GCC 4.8+, GLIBC 2.14+, USB permissions configured (requires `DSI.so`)
- **macOS:** Xcode Command Line Tools (requires `DSI.dylib`)

---

## Language-Specific Guides

### [C/C++ Getting Started](start_c.md)

Complete guide for C/C++ developers covering:
- Basic connection and error handling
- Channel configuration and montages
- Data acquisition (foreground and background)
- Common tasks (save data, check impedances, monitor battery)

**Best for:** Performance-critical applications, embedded systems, and integration with existing C/C++ codebases.

### [Python Getting Started](start_python.md)

Complete guide for Python developers covering:
- Quick setup and connection
- Channel configuration
- Data acquisition and processing
- Common tasks and integration examples

**Best for:** Rapid prototyping, data analysis, research applications, and integration with scientific Python libraries (NumPy, SciPy, MNE-Python).

---

## Port Configuration

All DSI headsets connect via serial port. The port specification varies by platform:

- **Windows:** COM ports (e.g., `COM4`, `COM5`, `COM6`)
- **Linux:** `/dev/ttyUSB0`, `/dev/ttyUSB1`, `/dev/ttyACM0`, `/dev/ttyACM1`
- **macOS:** `/dev/cu.DSI24-xxxxx-BluetoothSerial` or `/dev/tty.usbserial-xxxxx`

**Environment variable:** Set `DSISerialPort` to avoid hardcoding the port in your application. Pass `NULL` (C) or `None` (Python) to use the environment variable.

---

## Next Steps

After completing the getting started guide for your language:

- [Quick Reference](../quick_reference.md) - API function lookup guide
- [Error Codes](../error_codes.md) - Complete error code reference
- [Examples](../../examples/index.md) - Integration examples for various platforms

### Support

- **Sample code:** See `release/demo.c` and `DSI.py` in the release package for runnable examples
- **Technical support:** Contact WearableSensing support team via the [contact page](../../help/index.md)

---

[← Back to API Index](../index.md)

```{toctree}
:hidden:
:maxdepth: 2

Start with Python <start_python>
Start with C <start_c>
```
