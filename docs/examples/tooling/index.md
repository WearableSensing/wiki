# Testing Setup

```{toctree}
:hidden:
Photodiode Experiment<photodiode>
Analyzing the Photodiode Experiment <offset>
```

To ensure our real-time data is accurately timed, we can run a test like a photodiode experiment. This test measures the exact delay between when we tell an event to happen and when it actually does. By using many triggers, we can check for consistency. A tool for this type of experiment is provided in the [lsl-tools](https://github.com/WearableSensing/lsl-tools) library on GitHub.

## Installation

Install the required packages using pip.

```bash
pip install -e .[dev]
```

After installation, you can follow the walkthroughs to set up the hardware and run the analysis.

```{admonition} Python Version
:class: attention
The following tutorials is ran using python v3.10
```
