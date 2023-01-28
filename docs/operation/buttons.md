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
Holding **SHIFT** while turning the jog wheel will instead select scenes in Session view.

Here's a full list of buttons and their effects, grouped by action type (and if possible ordered the way they appear on the device).

## Jog Wheel
There are currently 2 ways that the Jog Wheel can be used - Track Navigation and Device Navigation. They can be selected by using the **Track Select** and **Program Select** buttons respectively.

### Track Navigation
In this mode you can turn the wheel to scroll through tracks. This works both in Session and Arrangement views. If implicit record arm is enabled, it will follow the selection so that the selected track will be armed if possible.

Pressing the Jog Wheel button will toggle the recording arm on the selected track.

Turning the Jog Wheel while holding **SHIFT** will scroll around scenes in Session View.

### Device Navigation
In this mode you can browse and modify the devices on the currently selected track. Turning the Jog Wheel will scroll around the devices, selecting each device (so that parameters can be controlled via MIDI - this is coming soon to the Touch Strip).

Pressing the Jog Wheel will turn the device on/off, and pressing it while holding **SHIFT** will collapse the device view.

Turning the Jog Wheel while holding **SHIFT** will move the selected device to the left or right.


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
- **Tap Tempo**: Tap tempo, with visual feedback of the tempo. To adjust tempo manually, hold **SHIFT**, **Quantize** and turn the Jog Wheel.
- **TC On/Off**: Toggle Record Quantization
- **Quantize**: Quantizes *all* notes in the currently selected Session View clip. Hold **SHIFT** and **Quantize**, then use the Jog Wheel to adjust tempo manually.
- **Tune**: Toggles Metronome

## Software Control
- **Main**: Toggle Session View / Arrangement View
- **Mode**: Accesses Shortcuts, see below
- **Zoom**: Session overview on pads for quick navigation, see [Pad mode A](../pads/). **SHIFT** to reset the session ring to currently selected track and scene.
- **Undo**: Undo
- **Shift**: Accesses extra functionality of Pad Modes, see [Pad modes](../pads/ )
- **-**/**+**/**Sample Start**/**Sample End**: Move the session view window around, **SHIFT** for paged navigation, see [Pad mode A](../pads/)
- **Browse**: Toggles the media browser
- **Track select**: Jog Wheel track selection mode (currently the only one) **SHIFT** to select scenes

## Currently unused
- **Locate**
- **Program Select**

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
