---
layout: default
title: Installation
nav_order: 2
---

# Installation
To install the Midi Remote Script, follow the steps listed below:

* Download the latest release of the script from the Github repository. There will be a `.zip` file located in the releases section.    
    * [
MPC-Studio-Mk2-Ableton-Midi-Remote-Script](https://github.com/bcrowe306/MPC-Studio-Mk2-Ableton-Midi-Remote-Script/releases)
* Extract the zip file to your `Ableton \ User Library\ Remote Scripts` folder. This will be different for MAC and Windows users but is normally found in the `Documents` folder on Windows, and the Music folder on MAC.
    * **Mac:** `/Users/[username]/Music/Ableton/User LIbrary/Remote Scripts`
    * **Win:** `C:\Users\brand\Documents\Ableton\User Library\Remote Scripts`
    * When extracting this, make sure to place it in a top level folder with the name `MPC_Studio_Mk2`. This will be the name that appears inside Ableton live when we select the control surface.
* This is the directory structure that should be in place after unzipping:
```
Ableton/
  |- User Library/
       |- Remote Scripts/
            |- MPC_Studio_Mk2/
                |- __init__.py
                |- v10/
                |- v11/
``` 
![User Library Screenshot](/assets/ableton_live_user_library.jpg)
* After extracting the zip file, open Ableton Live to connect the Script to the controller
    * Navigation to the following menu location.
        * Windows: `Options -> Preferences -> Midi`
        * Mac: `Live -> Preferences -> Midi`
    * On the Midi Tab, you will see dropdown boxes with various control surfaces listed. You can have more than one control surface operating Live at any given time.
        * On the first empty dropdown box, select the `MPC Studio Mk2` option. If you do not see it listed here, verify that you complete the previous steps correctly.
        * For the adjacent input and output dropdown boxes, select the public MIDI port for your MPC Studio Mk2. The Private port will not work 
    * Below the dropdown boxes, you will see all midi ports listed with `Track, Sync, Remote` options.
        * Find the public IN and OUT midi ports for the MPC Studio MK2.
        * Make sure that Track and Sync is selected for both In and Out.
    * Close the preferences.
    
![Midi Settings](/assets/ableton_live_midi_settings.jpg)

* Once the connection has been made, you should see the buttons and pads on the controller light up. If this is the case, you are finished, Enjoy! If not, repeat the above steps again to make sure it is installed correctly.


For information about getting the LCD Display to work, look [here](../lcd-display/).
