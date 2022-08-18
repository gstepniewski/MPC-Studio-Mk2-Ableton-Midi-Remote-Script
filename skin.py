#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ATOM/skin.py
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface import Skin
from .colors import Mono, Rgb, OneColorButton, TwoColorButtonMap

class Colors:

    class DefaultButton:
        On = OneColorButton.ON
        Off = OneColorButton.OFF
        Disabled = OneColorButton.DISABLED
        Reset = OneColorButton.OFF
        RgbOff = Rgb.BLACK
    
    class UpDownButton:
        On = TwoColorButtonMap.COLOR_2_DIM
        Off = TwoColorButtonMap.COLOR_1_DIM

    class Undo:
        On = TwoColorButtonMap.COLOR_1_FULL
        Off = TwoColorButtonMap.COLOR_1_DIM
        Disabled = TwoColorButtonMap.DISABLED

    class ViewToggle:
        On = TwoColorButtonMap.COLOR_2_DIM
        Off = TwoColorButtonMap.COLOR_1_DIM

    class Transport:
        PlayOn = OneColorButton.ON
        PlayOff = OneColorButton.OFF
        Disabled = OneColorButton.OFF
        SeekOn = OneColorButton.ON
        SeekOff = OneColorButton.OFF
    
    class Automation:
        On = TwoColorButtonMap.COLOR_2_FULL
        Off = TwoColorButtonMap.COLOR_1_FULL

    class Recording:
        On = OneColorButton.ON
        Transition = Mono.ON
        Off = OneColorButton.OFF

    class Mixer:
        ArmOn = Rgb.RED
        ArmOff = Rgb.RED_DIM
        SoloOn = Rgb.BLUE
        SoloOff = Rgb.BLUE_DIM
        Selected = Rgb.WHITE
        EmptyTrack = Rgb.BLACK
        MuteOn = Rgb.YELLOW_LIGHT
        MuteOff = Rgb.YELLOW
        On = TwoColorButtonMap.COLOR_1_DIM
    class Session:
        ClipEmpty = Rgb.BLACK
        ClipTriggeredPlay = Rgb.GREEN_BLINK
        ClipTriggeredRecord = Rgb.RED_BLINK
        ClipStarted = Rgb.GREEN_PULSE
        ClipRecording = Rgb.RED_PULSE
        RecordButton = Rgb.RED_HALF
        Scene = Rgb.GREEN_HALF
        NoScene = Rgb.BLACK
        SceneTriggered = Rgb.GREEN_BLINK
        StopClipTriggered = Rgb.RED_BLINK
        StopClip = Rgb.PURPLE
        StopClipDisabled = Rgb.RED_HALF

    class Zooming:
        Selected = Rgb.WHITE
        Stopped = Rgb.RED
        Playing = Rgb.GREEN
        Empty = Rgb.BLACK

    class NotePad:
        Pressed = Rgb.RED

    class Keyboard:
        Natural = Rgb.YELLOW
        Sharp = Rgb.BLUE

    class DrumGroup:
        Off = Rgb.OFF
        On = Rgb.RED_HALF
        Disabled = Rgb.BLACK
        PadEmpty = Rgb.BLACK
        PadFilled = Rgb.YELLOW
        PadSelected = Rgb.TEAL
        PadSelectedNotSoloed = Rgb.LIGHT_BLUE
        PadMuted = Rgb.ORANGE
        PadMutedSelected = Rgb.LIGHT_BLUE
        PadSoloed = Rgb.BLUE
        PadSoloedSelected = Rgb.LIGHT_BLUE
        PadQuadrant0 = Rgb.BLUE
        PadQuadrant1 = Rgb.GREEN
        PadQuadrant2 = Rgb.YELLOW
        PadQuadrant3 = Rgb.PURPLE
        PadQuadrant4 = Rgb.ORANGE
        PadQuadrant5 = Rgb.LIGHT_BLUE
        PadQuadrant6 = Rgb.PINK
        PadQuadrant7 = Rgb.PEACH

    class Mode:
        class Volume:
            On = Rgb.GREEN
            Off = Rgb.GREEN_HALF
        class Pan:
            On = Rgb.YELLOW
            Off = Rgb.YELLOW_HALF
        class SendA:
            On = Rgb.BLUE
            Off = Rgb.BLUE_HALF
        class SendB:
            On = Rgb.PURPLE
            Off = Rgb.PURPLE_HALF
        
        class Session:
            On = TwoColorButtonMap.COLOR_2_FULL
            Off = TwoColorButtonMap.COLOR_1_DIM
            Disabled = TwoColorButtonMap.COLOR_1_DIM
        class Note:
            On = TwoColorButtonMap.COLOR_2_FULL
            Off = TwoColorButtonMap.COLOR_1_DIM
            Disabled = TwoColorButtonMap.COLOR_1_DIM
        class Channel:
            On = TwoColorButtonMap.COLOR_2_FULL
            Off = TwoColorButtonMap.COLOR_1_DIM
            Disabled = TwoColorButtonMap.COLOR_1_DIM
        class TouchStripModes:
            On = TwoColorButtonMap.COLOR_2_FULL
            Off = TwoColorButtonMap.COLOR_1_DIM
            Disabled = TwoColorButtonMap.COLOR_1_DIM


skin = Skin(Colors)
