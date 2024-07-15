# MPC Studio Mk2 Ableton Midi Remote Script

In this repository, you will find the Midi remote script needed to use the MPC Studio Mk2 with Ableton. It is a work in progress, but the functionality so far is on par with the MPC software.

### Documentation
* Installation and operation: [MPC Studio Mk2 Ableton Documentation](https://gstepniewski.github.io/MPC-Studio-Mk2-Ableton-Midi-Remote-Script/)
* Midi/Sysex Data: [MPC Studio Mk2 Midi Sysex Charts](https://github.com/bcrowe306/MPC-Studio-Mk2-Midi-Sysex-Charts)
* Ableton Live LOM(Live Object Model): [PythonLiveAPI](https://structure-void.com/PythonLiveAPI_documentation/Live11.0.xml)
* Ableton Live Midi Remote Repository [Ableton Live 11.1 MIDI Remote Scripts](https://github.com/gluon/AbletonLive11_MIDIRemoteScripts)

My attempts to use this product with other software left me very frustrated. Without the brains of the MPC 2 software, this device on its own is useless. It sends out midi data, but not in a way that is remotely usable. I fault Akai for this. It would have been very easy and simple for them to make a controller mode for this unit, and release MIDI technical specs in a PDF but they refused to so...  I guess they have a history of making money by not listening to their users... I digress.

Through sending and observing MIDI data to and from the device, I have discovered that this is a "dumb" device. There is no logic on the device to perform any of it's functions, it is all controlled by the software(MPC 2) through MIDI. That means if I can figure out what MIDI messages, I can program the device with other software... hint hint.. Ableton Live...

This repository is the results of me doing just that. I have figured out every element of the MPC Studio Mk2 except the LED display. *Any help is appreciated*. Enjoy!
