# Integrations
---
See our {doc}`Integrations <../../examples/index>` page for more information.


## Do the DSI devices work with Eye-Tracking or other hardware systems?

Yes! The system accepts triggers that can be used to synchronize data between different hardware systems. In addition, if using a system supported by Lab Streaming Layer (LSL) the data and triggers can be synchronized using that protocol.

Our system is robust to electronic interference and should not cause interference with other systems. Please ask us about our Wireless Trigger Hub and its functionality. It can support interfacing with other hardware.

## Do the DSI devices work with popular Stimulus Presentation Software (Presentation, E-Prime, PsychoPy)?

Yes! The system accepts triggers that can be used to synchronize stimuli with recorded EEG data. Please see our {doc}`Integrations <../../examples/index>` page for more information on currently supported software (PsychoPy, BCI2000, etc.) and reach out about your specific interfacing needs if not already covered.

## Can data be imported into MATLAB?

Yes, both the .csv and .edf file formats can be imported into MATLAB (and other 3rd party software). Often when using MATLAB for EEG data processing, EEGLab is leveraged. We have a plugin available on our Downloads page to import data from our devices into EEGLab.

Real-time streaming can also be established with other software via the TCP/IP socket or via Lab Streaming Layer (LSL). Please see our {doc}`Integrations <../../examples/index>` page for more information on currently supported software and reach out to us about your specific interfacing needs if not already covered.
