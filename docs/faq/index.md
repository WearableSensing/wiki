# Frequently Asked Questions

This page contains answers to some of the most common questions using Wearable Sensing's technology. If you have a question that is not answered here, please feel free to reach out to us. See {doc}`Contact <../help/index>` for contact information.

## General

```{dropdown} Do these devices support real-time data streaming?
:animate: fade-in
Yes, Wearable Sensing's devices support real-time data streaming. You can stream data directly to your computer or other devices for immediate analysis using TCP/IP, DSI API or Lab Streaming Library (LSL).
```

```{dropdown} How do I get support?
:animate: fade-in
If you need support, please contact our support team through the {doc}`Contact <../help/index>` page. We are here to help you with any issues or questions you may have.
```

```{dropdown} If I purchase a new device, what is the expected delivery time?
:animate: fade-in
The expected delivery time for a new device is typically 4-8 weeks from the date of order confirmation. Please note that this timeline may vary based on product availability, order size and customization options.
```

```{dropdown} Where can you ship to?
:animate: fade-in
We have a distribution network spanning over 40 countries and can ship worldwide, including North America, South America, Europe, and Asia. Please contact us if you would like to know more about our shipping options or to inquire if we have a distribution center in your area.
```

## Software

```{dropdown} Does the DSI-Streamer output raw or filtered data?
:animate: fade-in
The DSI-Streamer outputs both raw and filtered data. You can choose the desired output format in the software settings.
```

```{dropdown} What types of output formats does the DSI-Streamer support?
:animate: fade-in
The DSI-Streamer supports various output formats including CSV, EDF, and our binary format (.DSI). You can select the format that best suits your needs in the settings.
```

## Integrations

```{dropdown} Do the DSI devices work with Eye-Tracking or other hardware systems?
:animate: fade-in
Yes! The system accepts triggers that can be used to synchronize data between different hardware systems. In addition, if using a system supported by Lab Streaming Layer (LSL) the data and triggers can be synchronized using that protocol.

Our system is robust to electronic interference and should not cause interference with other systems. Please ask us about our Wireless Trigger Hub and its functionality. It can support interfacing with other hardware.
```

```{dropdown} Do the DSI devices work with popular Stimulus Presentation Software (Presentation, E-Prime, PsychoPy)?
:animate: fade-in
Yes! The system accepts triggers that can be used to synchronize stimuli with recorded EEG data. Please see our {doc}`Integrations <../examples/index>` page for more information on currently supported software (PsychoPy, BCI2000, etc.) and reach out about your specific interfacing needs if not already covered.
```

```{dropdown} Can data be imported into MATLAB?
:animate: fade-in
Yes, both the .csv and .edf file formats can be imported into MATLAB (and other 3rd party software). Often when using MATLAB for EEG data processing, EEGLab is leveraged. We have a plugin available on our Downloads page to import data from our devices into EEGLab.

Real-time streaming can also be established with other software via the TCP/IP socket or via Lab Streaming Layer (LSL). Please see our {doc}`Integrations <../examples/index>` page for more information on currently supported software and reach out to us about your specific interfacing needs if not already covered.
```

```{dropdown} Do you have a low level API or SDK?
:animate: fade-in
Yes, we provide a low-level API and SDK for developers who want to integrate our devices into their own applications. We also offer these APIs for Android and iOS platforms.
```

## Hardware

```{dropdown} Are your dry electrodes active?
:animate: fade-in
Yes. Our dry sensors are active: there are amplifiers right behind the electrode tips.
```

```{dropdown} How many times can the electrodes be used before they should be replaced?
:animate: fade-in
Our electrodes tips are specified, designed and tested for >100 uses without signal degradation. We recommend monitoring the electrode performance and replacing them when you notice a decline in signal quality.
```

```{dropdown} What is the battery life of the devices?
:animate: fade-in
The DSI-24 has two hot-swappable batteries, meaning that the headset will keep working without interruption if one battery is taken out and replaced. Each battery lasts approximately 8-12 hours on a single charge.

The DSI-7 has one battery that lasts over 12 hours in continuous use. 

The DSI-VR300 has a battery built into the headset that lasts 8-12 hours.

Excluding the DSI-VR300, which has its own charging method, all batteries can be removed and re-charged with the provided charger in a few hours.
```

```{dropdown} How do I clean the devices?
:animate: fade-in
The systems are cleaned with their supplied brushes and 70% isopropanol alcohol. Cleaning takes on average less than 1 minute. Please refer to the device manual for detailed cleaning instructions.
```

## Triggers

```{dropdown} What type of external triggers are supported?
:animate: fade-in
The system accepts TTL-style pulse triggers, as well as parallel or serial outputs from your computer. The voltage output should be between 3 and 12 V. 

The DSI-24 supports 8-bit trigger inputs, and the DSI-7 and DSI-VR300 accept 4-bit trigger inputs. We offer a Trigger Hub with various accessories including: photodetector, audio detector, and push-button triggers. This can be accomplished in a wired and wireless manner.

In addition, we support software triggering via Lab Streaming Library (LSL).
```

## Warranty

```{dropdown} What is offered in terms of warranty and support?
:animate: fade-in
All systems come with a standard 90-day warranty and we offer annual Extended Support packages.
```

```{dropdown} What is the maximum warranty duration available?
:animate: fade-in
The maximum warranty available for purchase is 5 years.
```

```{dropdown} What is covered under the warranty?
:animate: fade-in
Any damage resulting from normal wear and tear of the system is covered under warranty. The warranty also includes advanced technical support.
```

```{dropdown} Are replacement electrodes covered under warranty?
:animate: fade-in
No. It is recommended to purchase replacement electrodes every 100 uses. The cost of replacement electrodes is comparable to the cost of gel for wet EEG systems per use
```




