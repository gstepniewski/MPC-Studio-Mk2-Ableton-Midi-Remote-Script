#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ATOM/skin.py
from __future__ import absolute_import, print_function, unicode_literals
from ast import Delete
from ableton.v2.control_surface import Skin
from .colors import Mono, Rgb, OneColorButton, TwoColorButtonMap, RgbColorBlink

class Colors:

    class DefaultButton:
        On = OneColorButton.ON
        Off = OneColorButton.OFF
        Selected = TwoColorButtonMap.COLOR_1_FULL
        Alert = TwoColorButtonMap.COLOR_2_FULL
        Disabled = OneColorButton.DISABLED
        Reset = OneColorButton.OFF
        RgbOff = Rgb.BLACK
    
    class DefaultBlinkPad:
        On = Rgb.RED
        Off = Rgb.RED_DIM
    
    class UpDownButton:
        On = TwoColorButtonMap.COLOR_2_DIM
        Off = TwoColorButtonMap.COLOR_1_DIM

    class Undo:
        On = TwoColorButtonMap.COLOR_1_FULL
        Off = TwoColorButtonMap.COLOR_1_DIM
        Disabled = TwoColorButtonMap.DISABLED

    class ViewToggle:
        On = TwoColorButtonMap.COLOR_2_FULL
        Off = TwoColorButtonMap.COLOR_1_FULL

    class Transport:
        PlayOn = OneColorButton.ON
        PlayOff = OneColorButton.OFF
        Disabled = OneColorButton.OFF
        SeekOn = OneColorButton.ON
        SeekOff = OneColorButton.OFF
        MetronomeOn = TwoColorButtonMap.COLOR_1_FULL
        MetronomeOff = TwoColorButtonMap.COLOR_1_DIM
    
    class Automation:
        On = TwoColorButtonMap.COLOR_2_FULL
        Off = TwoColorButtonMap.COLOR_1_FULL

    class Recording:
        On = OneColorButton.ON
        Transition = OneColorButton.BLINK
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
    class NoteRepeat:
        RateUnselected= Rgb.BLACK
        RateSelected= Rgb.RED
    class Session:
        ClipEmpty = Rgb.BLACK
        ClipTriggeredPlay = RgbColorBlink(Rgb.GREEN_HALF, Rgb.BLACK)
        ClipTriggeredRecord = RgbColorBlink(Rgb.YELLOW_HALF, Rgb.BLACK)
        ClipStarted = Rgb.GREEN_PULSE
        ClipRecording = RgbColorBlink(Rgb.RED_HALF, Rgb.BLACK)
        Delete = TwoColorButtonMap.COLOR_2_DIM
        DeletePressed = TwoColorButtonMap.COLOR_2_FULL
        Duplicate = TwoColorButtonMap.COLOR_1_DIM
        DuplicatePressed = TwoColorButtonMap.COLOR_1_FULL
        Select = TwoColorButtonMap.COLOR_1_DIM
        SelectPressed = TwoColorButtonMap.COLOR_1_FULL
        RecordButton = Rgb.RED_DIM
        Scene = Rgb.GREEN_HALF
        NoScene = Rgb.BLACK
        SceneTriggered = RgbColorBlink(Rgb.GREEN, Rgb.BLACK)
        StopClipTriggered = RgbColorBlink(Rgb.YELLOW, Rgb.BLACK)
        StopClip = Rgb.PURPLE
        StopClipDisabled = Rgb.YELLOW_LIGHT

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
    class Accent:
        On = TwoColorButtonMap.COLOR_1_FULL
        Off = TwoColorButtonMap.COLOR_1_DIM
    
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
        PadAction = Rgb.GREEN
        
        class DeleteButton:
            Off = TwoColorButtonMap.COLOR_2_DIM
            On = TwoColorButtonMap.COLOR_2_FULL
        class MuteButton:
            Off = TwoColorButtonMap.COLOR_1_DIM
            On = TwoColorButtonMap.COLOR_1_FULL
        class SoloButton:
            Off = TwoColorButtonMap.COLOR_1_DIM
            On = TwoColorButtonMap.COLOR_1_FULL

    class Action:
        QuantizeOff = TwoColorButtonMap.COLOR_1_DIM
        QuantizeOn = TwoColorButtonMap.COLOR_1_FULL
        On = TwoColorButtonMap.COLOR_1_DIM
        Off = TwoColorButtonMap.COLOR_1_FULL
    class Macro:
        AudioOff = Rgb.BLUE_HALF
        AudioOn = Rgb.BLUE
        MidiOff = Rgb.ORANGE_HALF
        MidiOn = Rgb.ORANGE
        DrumRackOff = Rgb.YELLOW_HALF
        DrumRackOn = Rgb.YELLOW
        SimplerOff = Rgb.TEAL_DIM
        SimplerOn = Rgb.TEAL
        CompressorOff = Rgb.PURPLE_DIM
        CompressorOn = Rgb.PURPLE
        EqOff = Rgb.GREEN_HALF
        EqOn = Rgb.GREEN
        AutofilterOn = Rgb.RED_HALF
        AutofilterOff = Rgb.RED
        GateOn = Rgb.PEACH
        GateOff = Rgb.PEACH_DIM
    class Quantization:
        On = TwoColorButtonMap.COLOR_1_FULL
        Off  = TwoColorButtonMap.COLOR_2_BLINK
    class Mode:
        class Stopclip:
            On = TwoColorButtonMap.COLOR_2_FULL
            Off = TwoColorButtonMap.COLOR_1_DIM
        class Macro:
            Off = OneColorButton.OFF
            On = OneColorButton.ON
            AudioOff = Rgb.BLUE_HALF
            AudioOn = Rgb.BLUE
            MidiOff = Rgb.ORANGE_HALF
            MidiOn = Rgb.ORANGE
            DrumRackOff = Rgb.YELLOW_HALF
            DrumRackOn = Rgb.YELLOW
            SimplerOff = Rgb.TEAL_DIM
            SimplerOn = Rgb.TEAL
            CompressorOff = Rgb.PURPLE_DIM
            CompressorOn = Rgb.PURPLE
            EqOff = Rgb.GREEN_HALF
            EqOn = Rgb.GREEN
            AutofilterOn = Rgb.RED_HALF
            AutofilterOff = Rgb.RED
            GateOn = Rgb.PEACH
            GateOff = Rgb.PEACH_DIM
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
        class Stopclip:
            On = TwoColorButtonMap.COLOR_2_FULL
            Off = TwoColorButtonMap.COLOR_1_DIM
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
