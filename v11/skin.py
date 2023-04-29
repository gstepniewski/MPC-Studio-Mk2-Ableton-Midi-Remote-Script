#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ATOM/skin.py
from __future__ import absolute_import, print_function, unicode_literals
from ast import Delete
from ableton.v2.control_surface import Skin
from .colors import OneColorButton, TwoColorButtonMap, MPCPadColor, RGBColorDef, MPCInterface

class Colors:

    class DefaultButton:
        On = OneColorButton.ON
        Off = OneColorButton.OFF
        Selected = TwoColorButtonMap.COLOR_1_FULL
        Alert = TwoColorButtonMap.COLOR_2_FULL
        Disabled = OneColorButton.DISABLED
        Reset = OneColorButton.OFF
        RgbOff = MPCPadColor(color=RGBColorDef.BLACK, brightness=1)
    
    class DefaultBlinkPad:
        On = MPCPadColor(color=RGBColorDef.RED, brightness=100)
        Off = MPCPadColor(color=RGBColorDef.RED, brightness=5)
    
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
        Dim = TwoColorButtonMap.COLOR_1_DIM

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
        ArmOn = MPCPadColor(color=RGBColorDef.RED, brightness=120)
        ArmOff = MPCPadColor(color=RGBColorDef.RED, brightness=5)
        SoloOn = MPCPadColor(color=RGBColorDef.BLUE, brightness=100)
        SoloOff = MPCPadColor(color=RGBColorDef.BLUE, brightness=5)
        Selected = MPCPadColor(color=RGBColorDef.WHITE, brightness=100)
        EmptyTrack = MPCPadColor(color=RGBColorDef.BLACK, brightness=1)
        MuteOn = MPCPadColor(color=RGBColorDef.YELLOW, brightness=5)
        MuteOff = MPCPadColor(color=RGBColorDef.YELLOW, brightness=100)
        On = TwoColorButtonMap.COLOR_1_DIM

    class Session:
        ClipEmpty = MPCPadColor(color=RGBColorDef.BLACK, brightness=1)
        ClipTriggeredPlay = MPCPadColor(color=RGBColorDef.GREEN, brightness=100, animation_type=MPCInterface.Animation.Blink)
        ClipTriggeredRecord = MPCPadColor(color=RGBColorDef.YELLOW, brightness=127, animation_type=MPCInterface.Animation.Blink)
        ClipStarted = MPCPadColor(color=RGBColorDef.GREEN, brightness=100)
        ClipRecording = MPCPadColor(color=RGBColorDef.RED, brightness=127, animation_type=MPCInterface.Animation.Blink)
        Delete = TwoColorButtonMap.COLOR_2_DIM
        DeletePressed = TwoColorButtonMap.COLOR_2_FULL
        Duplicate = TwoColorButtonMap.COLOR_1_DIM
        DuplicatePressed = TwoColorButtonMap.COLOR_1_FULL
        Select = TwoColorButtonMap.COLOR_1_DIM
        SelectPressed = TwoColorButtonMap.COLOR_1_FULL
        RecordButton = MPCPadColor(color=RGBColorDef.RED, brightness=32)
        Scene = MPCPadColor(color=RGBColorDef.GREEN, brightness=64)
        NoScene = MPCPadColor(color=RGBColorDef.BLACK, brightness=1)
        SceneTriggered = MPCPadColor(color=RGBColorDef.GREEN, brightness=127, animation_type=MPCInterface.Animation.Blink)
        StopClipTriggered = MPCPadColor(color=RGBColorDef.YELLOW, brightness=127, animation_type=MPCInterface.Animation.Blink)
        StopClip = MPCPadColor(color=RGBColorDef.PURPLE, brightness=100)
        StopClipDisabled = MPCPadColor(color=RGBColorDef.YELLOW, brightness=20)

    class Zooming:
        Selected = MPCPadColor(color=RGBColorDef.WHITE, brightness=120)
        Stopped = MPCPadColor(color=RGBColorDef.RED, brightness=120)
        Playing = MPCPadColor(color=RGBColorDef.GREEN, brightness=120)
        Empty = MPCPadColor(color=RGBColorDef.BLACK, brightness=1)

    class NotePad:
        Pressed = MPCPadColor(color=RGBColorDef.RED, brightness=120)

    class Keyboard:
        Natural = MPCPadColor(color=RGBColorDef.YELLOW, brightness=120)
        Sharp = MPCPadColor(color=RGBColorDef.BLUE, brightness=120)
        Off = MPCPadColor(color=RGBColorDef.BLACK, brightness=1)
    class Accent:
        On = TwoColorButtonMap.COLOR_1_FULL
        Off = TwoColorButtonMap.COLOR_1_DIM
    
    class DrumGroup:
        Off = MPCPadColor(color=RGBColorDef.BLACK, brightness=1)
        On = MPCPadColor(color=RGBColorDef.RED, brightness=64)
        Disabled = MPCPadColor(color=RGBColorDef.BLACK, brightness=1)
        PadEmpty = MPCPadColor(color=RGBColorDef.BLACK, brightness=1)
        PadFilled = MPCPadColor(color=RGBColorDef.YELLOW, brightness=100)
        PadSelected = MPCPadColor(color=RGBColorDef.TEAL, brightness=100)
        PadSelectedNotSoloed = MPCPadColor(color=RGBColorDef.LIGHT_BLUE, brightness=100)
        PadMuted = MPCPadColor(color=RGBColorDef.ORANGE, brightness=100)
        PadMutedSelected = MPCPadColor(color=RGBColorDef.LIGHT_BLUE, brightness=100)
        PadSoloed = MPCPadColor(color=RGBColorDef.BLUE, brightness=100)
        PadSoloedSelected = MPCPadColor(color=RGBColorDef.LIGHT_BLUE, brightness=100)
        PadQuadrant0 = MPCPadColor(color=RGBColorDef.INDIGO, brightness=100)
        PadQuadrant1 = MPCPadColor(color=RGBColorDef.GREEN, brightness=100)
        PadQuadrant2 = MPCPadColor(color=RGBColorDef.YELLOW, brightness=100)
        PadQuadrant3 = MPCPadColor(color=RGBColorDef.PURPLE, brightness=100)
        PadQuadrant4 = MPCPadColor(color=RGBColorDef.ORANGE, brightness=100)
        PadQuadrant5 = MPCPadColor(color=RGBColorDef.LIGHT_BLUE, brightness=100)
        PadQuadrant6 = MPCPadColor(color=RGBColorDef.PINK, brightness=100)
        PadQuadrant7 = MPCPadColor(color=RGBColorDef.PEACH, brightness=100)
        PadAction = MPCPadColor(color=RGBColorDef.GREEN, brightness=100)
        
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
        AudioOff = MPCPadColor(color=RGBColorDef.BLUE, brightness=64)
        AudioOn = MPCPadColor(color=RGBColorDef.BLUE, brightness=5)
        MidiOff = MPCPadColor(color=RGBColorDef.ORANGE, brightness=64)
        MidiOn = MPCPadColor(color=RGBColorDef.ORANGE, brightness=5)
        DrumRackOff = MPCPadColor(color=RGBColorDef.YELLOW, brightness=64)
        DrumRackOn = MPCPadColor(color=RGBColorDef.YELLOW, brightness=5)
        SimplerOff = MPCPadColor(color=RGBColorDef.TEAL, brightness=64)
        SimplerOn = MPCPadColor(color=RGBColorDef.TEAL, brightness=1)
        CompressorOff = MPCPadColor(color=RGBColorDef.PURPLE, brightness=5)
        CompressorOn = MPCPadColor(color=RGBColorDef.PURPLE, brightness=64)
        EqOff = MPCPadColor(color=RGBColorDef.GREEN, brightness=5)
        EqOn = MPCPadColor(color=RGBColorDef.GREEN, brightness=64)
        AutofilterOff = MPCPadColor(color=RGBColorDef.RED, brightness=5)
        AutofilterOn = MPCPadColor(color=RGBColorDef.RED, brightness=64)
        GateOff = MPCPadColor(color=RGBColorDef.PEACH, brightness=5)
        GateOn = MPCPadColor(color=RGBColorDef.PEACH, brightness=70)
        LfoOff = MPCPadColor(color=RGBColorDef.YELLOW, brightness=5)
        LfoOn = MPCPadColor(color=RGBColorDef.YELLOW, brightness=64)
        Eq8Off = MPCPadColor(color=RGBColorDef.GREEN, brightness=5)
        Eq8On = MPCPadColor(color=RGBColorDef.GREEN, brightness=64)
        UtilityOff = MPCPadColor(color=RGBColorDef.WHITE, brightness=5)
        UtilityOn = MPCPadColor(color=RGBColorDef.WHITE, brightness=64)
        LimiterOff = MPCPadColor(color=RGBColorDef.PINK, brightness=5)
        LimiterOn = MPCPadColor(color=RGBColorDef.PINK, brightness=64)
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
            AudioOff = MPCPadColor(color=RGBColorDef.BLUE, brightness=64)
            AudioOn = MPCPadColor(color=RGBColorDef.BLUE, brightness=5)
            MidiOff = MPCPadColor(color=RGBColorDef.ORANGE, brightness=64)
            MidiOn = MPCPadColor(color=RGBColorDef.ORANGE, brightness=5)
            DrumRackOff = MPCPadColor(color=RGBColorDef.YELLOW, brightness=64)
            DrumRackOn = MPCPadColor(color=RGBColorDef.YELLOW, brightness=5)
            SimplerOff = MPCPadColor(color=RGBColorDef.TEAL, brightness=64)
            SimplerOn = MPCPadColor(color=RGBColorDef.TEAL, brightness=1)
            CompressorOff = MPCPadColor(color=RGBColorDef.PURPLE, brightness=5)
            CompressorOn = MPCPadColor(color=RGBColorDef.PURPLE, brightness=64)
            EqOff = MPCPadColor(color=RGBColorDef.GREEN, brightness=5)
            EqOn = MPCPadColor(color=RGBColorDef.GREEN, brightness=64)
            AutofilterOff = MPCPadColor(color=RGBColorDef.RED, brightness=5)
            AutofilterOn = MPCPadColor(color=RGBColorDef.RED, brightness=64)
            GateOff = MPCPadColor(color=RGBColorDef.PEACH, brightness=5)
            GateOn = MPCPadColor(color=RGBColorDef.PEACH, brightness=64)
        class Volume:
            On = MPCPadColor(color=RGBColorDef.GREEN, brightness=100)
            Off = MPCPadColor(color=RGBColorDef.GREEN, brightness=5)
        class Pan:
            On = MPCPadColor(color=RGBColorDef.YELLOW, brightness=100)
            Off = MPCPadColor(color=RGBColorDef.YELLOW, brightness=5)
        class SendA:
            On = MPCPadColor(color=RGBColorDef.BLUE, brightness=100)
            Off = MPCPadColor(color=RGBColorDef.BLUE, brightness=5)
        class SendB:
            On = MPCPadColor(color=RGBColorDef.PURPLE, brightness=100)
            Off = MPCPadColor(color=RGBColorDef.PURPLE, brightness=5)
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
