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
There are currently 4 navigation modes that the Jog Wheel can be in:
1. Track Navigation (**Track Select**)
2. Device Navigation (**Program Select**)
3. Parameter Navigation (**Sample Select**)
4. Browser Navigation (**Browse**)

### Track Navigation
In this mode you can turn the wheel to scroll through tracks. This works both in Session and Arrangement views. If implicit record arm is enabled, it will follow the selection so that the selected track will be armed if possible.

Pressing the Jog Wheel button will toggle the recording arm on the selected track.

Turning the Jog Wheel while holding **SHIFT** will scroll around scenes in Session View.

### Device Navigation
In this mode you can browse and modify the devices on the currently selected track. Turning the Jog Wheel will scroll around the devices, selecting each device (so that parameters can be controlled via MIDI - this is coming soon to the Touch Strip).

Pressing the Jog Wheel will turn the device on/off, and pressing it while holding **SHIFT** will collapse the device view.

Turning the Jog Wheel while holding **SHIFT** will move the selected device to the left or right.

### Parameter Navigation
In this mode you can use the jog wheel to control a selected parameter. First select the parameter using your mouse (most parameters will respond to being selected with little brackets in the corners), then turn the jog wheel to adjust the parameter value.

For quantized, i.e. discrete parameters each step of the Jog Wheel will switch to the next value.

For continuous parameters, the available range of values is mapped to 100 steps and each step of the Jog Wheel adjusts the value by one step - so if a parameter goes from 0% to 100%, the Jog Wheel will adjust it by 1% at a time. The number of steps can be increased to 1000 by holding the **SHIFT** button, allowing for finer tuning. Pressing the Jog Wheel returns the parameter to its default value, if it has one.

### Browser Navigation
In this mode you can use the Jog Wheel to browse the Ableton library. By default, turning the browser mode on will show the library window, and switching to any other mode will hide it. You can still show/hide the window at any time by using **SHIFT** + **Browse**.

Turning the Jog Wheel will travel across the library vertically. Turning it while holding **SHIFT** will travel it horizontally (i.e. right for enter and left for back).

Pressing it is equivalent to left arrow (i.e. enter) and pressing it while holding **SHIFT** is pressing the right arrow (i.e. back). Note that this is the same as turning the Jog Wheel with shift, since actually loading something from the library is currently unsupported - you still have to hit Enter.

If the Jog Wheel is not doing anything, try selecting something in the browser with the mouse first. This is usually only needed once after starting Ableton.

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
- **Zoom**: Session overview on pads for quick navigation, see [Pad mode A](../pads/). Also while pressed paged session view movement. **SHIFT** to reset the session ring to currently selected track and scene.
- **Undo**: Undo
- **Shift**: Accesses extra functionality of Pad Modes, see [Pad modes](../pads/ )
- **-**/**+**/**Sample Start**/**Sample End**: Move the session view window around, **Zoom** for paged navigation, see [Pad mode A](../pads/)
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

The second and third to bottom rows of pads add a device to the current track, from left to right and bottom to top: 
- Compressor
- EQ Three
- Auto Filter
- Gate
- LFO
- EQ Eight
- Utility
- Limiter
