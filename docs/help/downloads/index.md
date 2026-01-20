# Downloads

Access essential drivers, software tools, user guides, and third-party plugins to get the most out of your Wearable Sensing devices.

---

<div id="password-gate-container">
<p>
      Please provide the password to unlock DSI-Streamer, QStates, DSI-API, TCP/IP code and user manuals.
    </p>
  <div class="input-group">
    <input type="password" id="password-input" placeholder="---">
    <button onclick="checkPassword()">Unlock</button>
  </div>
  <p id="error-message" style="color:red; height: 1em;"> </p>
</div>
<div id="protected-content">
</div>

---

## Data Transmission Drivers

Drivers required for connecting your headset to your computer. Install the appropriate driver based on your connection method.

````{grid} 2

```{grid-item-card}  USB Wired Mode Driver
:link: https://www.dropbox.com/s/01vaox1fk93t5do/CP210x_VCP_Windows.zip?dl=0

*Updated: March 27, 2020*
```

```{grid-item-card}  Bluetooth Dongle Driver
:link: https://www.dropbox.com/scl/fi/mxh8bikmpscuyjdq5xen6/EDUP-Bluetooth-Support.pdf?rlkey=lirw261dakdj8t25pbd2c1qp5&dl=0

*Updated: April 16, 2025*
```
````



---

## Third-Party Integration Plugins

Connect your Wearable Sensing headset to popular neuroscience analysis platforms. These community-developed plugins enable seamless data streaming and import into your preferred software environment.

````{grid} 1

```{grid-item-card}  🌐 Lab Streaming Layer (LSL)
:link: https://github.com/labstreaminglayer/App-WearableSensing/releases/

**Use for:** Real-time data streaming to Python, MATLAB, Unity, and other applications.

**Features:**
- Stream live EEG data over network
- Synchronize with other LSL devices
- Compatible with DSI-Streamer's LSL output

*Released: September 16, 2020*
```

````

**Learn more:** {doc}`LSL Setup Guide <../../examples/lsl/index>` | {doc}`MNE-LSL Tutorials <../../examples/mne/lsl/index>`

````{grid} 3

```{grid-item-card}  📊 EEGLAB Built-in Plugin
:link: ../../examples/eeglab/index

**For:** Latest EEGLAB versions (2024+)

The Wearable Sensing plugin is now **included** in EEGLAB Plugin Manager - no separate download needed!

*Integrated: 2025*
```

```{grid-item-card}  📊 EEGLAB Extension v1.14
:link: https://wearablesensing.com/wp-content/uploads/2023/12/WearableSensing_1.14.zip

**For:** DSI-Streamer 1.08.90 or newer (older EEGLAB versions)

*Released: December 18, 2023*
```

```{grid-item-card}  📊 EEGLAB Extension v1.13
:link: https://wearablesensing.com/wp-content/uploads/2023/12/WearableSensing_1.13.zip

**For:** Older DSI-Streamer versions (pre-1.08.90) with older EEGLAB

*Released: March 12, 2022*
```
````

**Learn more:** {doc}`EEGLAB Tutorial <../../examples/eeglab/index>`

---

## Need Help?

- **Driver Issues?** {doc}`Contact support <../index>`
- **Plugin Questions?** Check our {doc}`tutorials <../tutorials/index>` and {doc}`FAQ <../../faq/index>`
- **Software Access?** {doc}`Contact support <../index>`
