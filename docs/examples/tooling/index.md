# Testing Setup

```{toctree}
:hidden:
Photodiode Experiment<photodiode>
Analyzing the Photodiode Experiment <offset>
```

To ensure our real-time data is accurately timed, we can run a test like a photodiode experiment. This test measures the exact delay between when we tell an event to happen and when it actually does. By using many triggers, we can check for consistency. A script for this type of experiment is provided in the [lsl-tools](https://github.com/WearableSensing/lsl-tools) library on GitHub.

```{admonition} Python Version
:class: attention
The following tutorials is ran using python v3.10

```
