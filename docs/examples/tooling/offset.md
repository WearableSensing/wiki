# Analyzing the Photodiode Experiment

The photodiode experiment quantifies the precise temporal offset between the software-generated trigger and the physical event's onset. This calculated latency can then be systematically applied to correct the event timestamps in the dataset, ensuring accurate alignment with the ground truth.

For easier interpretation, we provide a tool in [lsl-tools](https://github.com/WearableSensing/lsl-tools) that creates a visual plot of the experiment's results.

## Generate the Visualization

1. First, locate the results file created by the photodiode experiment.

2. Then, execute the command below with that file:

```bash
python tools/display/offset.py --filepath="yourfile.csv"
```

Executing this command will generate two plots like this ones below and a statistical summary. The first plot displays the trigger events by sample number, while the second illustrates the distribution of the measured timing offsets. The accompanying table provides key descriptive statistics for these offset values, such as the mean, standard deviation, and min/max.

```{image} ../../_static/images/photodiode-exp.png
:width: 100%
```
