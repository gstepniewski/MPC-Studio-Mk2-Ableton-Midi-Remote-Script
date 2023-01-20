---
layout: default
title: Buttons and Jog Wheel
parent: Operation
nav_order: 2
---

# Intro

A lot of the buttons do exactly what they say they do, with a few exceptions where that functionality does not exist in Ableton Live or there is no API for that.
Most of the buttons that toggle things will also synchronize their state with the software.

The **Jog Wheel** can be used to select tracks and pressing it down will toggle the selected track's record arm.

Here's a full list of buttons and their effects, grouped by action type (and if possible ordered the way they appear on the device).

## Transport Control
- **Record**: Toggle Record when in Arrangement View, Session Overdub when in Session View
- **Overdub**: Toggle Arrangement Overdub
- **Play**: Play
- **Stop**: Stop
- **Play Start**: Toggle Arrangement Loop
- **<**/**>**: Punch in/Punch out. These are momentary!
- **<<**/**>>**: Move the playhead
- **Automation R/W**: Toggles automation read/write - currently slightly bugged, see [GitHub Issue](https://github.com/bcrowe306/MPC-Studio-Mk2-Ableton-Midi-Remote-Script/issues/1)

## Tempo Control
- **Tap Tempo**: Tap tempo, with visual feedback of the tempo
- **TC On/Off**: Toggle Record Quantization
- **Quantize**: Quantizes *all* notes in the currently selected Session View clip.
- **Tune**: Toggles Metronome

## Software Control
- **Main**: Toggle Session View / Arrangement View
- **Mode**: Accesses Shortcuts, see below
- **Zoom**: Session overview on pads for quick navigation, see [Pad mode A](../pads/)
- **Undo**: Undo
- **Shift**: Accesses extra functionality of Pad Modes, see [Pad modes](../pads/ )
- **-**/**+**/**Sample Start**/**Sample End**: Move the session view window around, see [Pad mode A](../pads/)
- **Browse**: Toggles the media browser
- **Track select**: Jog Wheel track selection mode (currently the only one)

## Currently unused
- **Locate**
- **Program Select**
- **Sample Select**

## Mode Button Shortcuts
Holding down the **Mode** button allows using one of the 8 shortcuts using the pads.

The bottom row of pads is adds tracks, from left to right
- Audio Track
- MIDI Track
- Drum Rack Track
- Simpler Track

The second to bottom row of pads adds a device to the current track, from left to right 
- Compressor
- EQ Three
- Auto Filter
- Gate
