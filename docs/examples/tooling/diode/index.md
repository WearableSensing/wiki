# Photodiode Experiment
--------------------------------------------------------------------------------------

To ensure our data is accurately timed with stimuli, we can run a test like a photodiode experiment. 

This test measures the exact delay between when we tell an event to happen on a display and when it actually occurs. The goal is to determine any offsets or timing inaccuracies with the system. The introduction of delays can come from a variety of sources. 

A tool such as this is useful to test the timing of a system for visual stimuli presentation without the overhead of other stimuli and experiment protocols that may introduce their own delays to the system. Our tool for this type of experiment is provided in the [lsl-tools](https://github.com/WearableSensing/lsl-tools) library on GitHub.

## Installation
--------------------------------------------------------------------------------------

```{admonition} Python Version
:class: note
The following tutorials are run using Python v3.10. A virtual environment is recommended.
```

```bash
# Clone the library
git clone https://github.com/WearableSensing/lsl-tools.git

# Change directory to project root
cd lsl-tools

# Create and activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate

# Install the library
pip install -e .[dev]
```

After successful installation, you can follow the walkthroughs to set up the hardware and run the analysis.


```{toctree}
:hidden:
Run the experiment <photodiode>
Determine offset and timing accuracy <offset>
```