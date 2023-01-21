---
layout: default
title: Pads and Pad modes
parent: Operation
nav_order: 1
---

# Intro

There are 4 different pad modes, accessed by the Pad Bank buttons A-D.
Here's a summary of all the modes and a full description follows below.

# Pad Modes Summary

## A - Session View

In this mode, the MPC Studio Mk2 functions similar to a Launchpad, where each pad represents a clip in the Session view of Ableton Live.
If there is no clip in the corresponding slot, the pad light is off. Otherwise, it matches the colour of the clip.
Playing or queued up clips blink with a green colour. Clips about to start recording blink yellow and then pulse red while recording.

You can navigate around your session in two ways:
1. Using the **+**/**-** and **Sample Start**/**Sample End** buttons (next to the Jog Wheel) will move the selection window around. You can move the window by one clip or by its dimension - this behaviour is toggled with the **Sample Select** button.
2. Holding the **Zoom** button shows an overview of your entire session and you can use the pads to select a 4x4 block to view.

Holding **SHIFT** allows you to launch scenes by using the rightmost column of pads.

The bottom left buttons can be used to perform operations on clips. You need to hold a button and then select a target clip using pads.
- **Full Level**: Create a new empty clip with a default length of 2 bars.
- **Copy**: Create a copy of a clip, paste it directly below. This will overwrite any existing clips!
- **Pad Mute**: Duplicate a clip length. This will also duplicate the notes in the clip.
- **16 Level**: Select a clip without playing it.
- **Erase**: Delete a clip.

## B - Notes

In this mode you can enter trigger notes in the currently armed MIDI tracks. The mode will automatically recognize the type of track and display a drumkit or a piano layout.
In drumkit mode, only the pads that have samples assigned will be lit up. The currently selected pad is marked and pads will present a visual feedback when pressed.
In piano mode there are different colours for black and white keys.

Holding **SHIFT** displays a Session Overview (like mode A) so you can quickly launch clips or start/stop recording. 

The **Full Level**/**Copy** buttons can be used to switch drumkit banks or piano octaves up and down. 
In drumkit mode you can also hold the bottom 3 buttons and select a pad to access extra operations:
- **Pad mute**: mutes a pad
- **16 level**: solos a pad
- **Erase**: deletes a sample from a pad

This mode can also use the **Note Repeat** button to keep entering the selected note, synchronized with the tempo. Hold down the **Note Repeat** button, the pad you want to trigger and use the Touch Strip to select the repeat interval.

## C - Mixer

In this mode each column is a track, and each row is:
- Select a track
- Toggle track mute
- Toggle track solo
- Toggle track record arm

There is visual feedback for each operation, and it is always synchronized with the software. The range of tracks works just like in mode A, and can be moved around the same way (**+**/**-** and **Sample Start**/**Sample End** or **Zoom**).

Holding **SHIFT** displays a Session Overview (like mode A) so you can quickly launch clips or start/stop recording. 

The buttons below the pad banks allow controlling the track routing and monitoring options:
- **Full Level** and **Copy** toggle the values in the Audio/MIDI From combo boxes. You can use them to toggle the input device and channel or track.
- **Pad Mude** and **16 Level** toggle the values in the Audio/MIDI To combo boxes. You can use them to toggle the output device and channel or track.
- **Erase** toggles between the available monitoring options (In/Auto/Off)

## D - Clip stop

This mode is momentary, i.e. it is only active as long as you hold the **Pad bank D** button. It allows you to use the bottom row of pads to stop any clips playing in that track.

**Shift** and the lower left buttons are not used in this mode.