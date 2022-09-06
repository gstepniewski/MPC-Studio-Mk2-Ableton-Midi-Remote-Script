from __future__ import division, absolute_import, print_function
from _Framework.ButtonElement import ButtonElement
import colorsys

PAD_MAPPING = {
            37: 0,
            36: 1,
            42:2,
            82: 3,
            40: 4,
            38: 5,
            46: 6,
            44: 7,
            48: 8,
            47: 9,
            45: 10,
            43: 11,
            49: 12,
            55: 13,
            51: 14,
            53: 15,
        }
def rgb_colorconverter(red, green, blue, brightness=0):
    # Convert RGB 255 values into unit values
    red_unit = red / 255
    blue_unit = blue / 255
    green_unit = green / 255

    # Conver rgb to hsv
    hsv = colorsys.rgb_to_hsv(red_unit, green_unit, blue_unit)

    # Set custom value of brightness if supplied
    value = hsv[2]
    if(brightness != 0):
        value = brightness / 127

    # Convert back to RGB
    rgb_with_brightness = colorsys.hsv_to_rgb(hsv[0], hsv[1], value)
    
    # Convert RGB unit values to midi sysex values
    midi_rgb = (
        int(round(rgb_with_brightness[0] * 127)), 
        int(round(rgb_with_brightness[1] * 127)), 
        int(round(rgb_with_brightness[2] * 127))
    )
    return midi_rgb

class TwoColorButton(ButtonElement):
    def __init__(self, is_momentary, msg_type, channel, identifier, _send_midi):
        ButtonElement.__init__(self, is_momentary, msg_type, channel, identifier)
        self.MIDI_TYPE = 176
        self.cc_value = identifier
        self._send_midi = _send_midi
        self.OFF = 0
        self.DIM_1 = 1
        self.DIM_2 = 2
        self.FULL_1 = 3
        self.FULL_2 = 4
    def Initialize(self):
        self._send_midi((self.MIDI_TYPE, self.cc_value, self.DIM_1))

    def Reset(self):
        self._send_midi((self.MIDI_TYPE, self.cc_value, self.OFF))

    def SetLED_Dim1(self):
        self._send_midi((self.MIDI_TYPE, self.cc_value, self.DIM_1))
        
    def SetLED_Dim2(self):
        self._send_midi((self.MIDI_TYPE, self.cc_value, self.DIM_2))

    def SetLED_Full1(self):
        self._send_midi((self.MIDI_TYPE, self.cc_value, self.FULL_1))

    def SetLED_Full2(self):
        self._send_midi((self.MIDI_TYPE, self.cc_value, self.FULL_2))

class NewTwoColorButton(ButtonElement):
    def __init__(self, is_momentary, msg_type, channel, identifier, _send_midi):
        ButtonElement.__init__(self, is_momentary, msg_type, channel, identifier)
        self.MIDI_TYPE = 176
        self.cc_value = identifier
        self._send_midi = _send_midi
        self.OFF = 0
        self.DIM_1 = 1
        self.DIM_2 = 2
        self.FULL_1 = 3
        self.FULL_2 = 4
    def Initialize(self):
        self._send_midi((self.MIDI_TYPE, self.cc_value, self.DIM_1))

    def Reset(self):
        self._send_midi((self.MIDI_TYPE, self.cc_value, self.OFF))

    def SetLED_Dim1(self):
        self._send_midi((self.MIDI_TYPE, self.cc_value, self.DIM_1))
        
    def SetLED_Dim2(self):
        self._send_midi((self.MIDI_TYPE, self.cc_value, self.DIM_2))

    def SetLED_Full1(self):
        self._send_midi((self.MIDI_TYPE, self.cc_value, self.FULL_1))

    def SetLED_Full2(self):
        self._send_midi((self.MIDI_TYPE, self.cc_value, self.FULL_2))

class GreenRedButton(ButtonElement):
    def __init__(self, is_momentary, msg_type, channel, identifier, _send_midi):
        ButtonElement.__init__(self, is_momentary, msg_type, channel, identifier)
        self.MIDI_TYPE = 176
        self.cc_value = identifier
        self._send_midi = _send_midi
        self.OFF = 0
        self.DIM_1 = 1
        self.DIM_2 = 2
        self.FULL_1 = 3
        self.FULL_2 = 4
    def Initialize(self):
        self._send_midi((self.MIDI_TYPE, self.cc_value, self.DIM_2))

    def Reset(self):
        self._send_midi((self.MIDI_TYPE, self.cc_value, self.OFF))

    def SetLED_Dim1(self):
        self._send_midi((self.MIDI_TYPE, self.cc_value, self.DIM_1))
        
    def SetLED_Dim2(self):
        self._send_midi((self.MIDI_TYPE, self.cc_value, self.DIM_2))

    def SetLED_Full1(self):
        self._send_midi((self.MIDI_TYPE, self.cc_value, self.FULL_1))

    def SetLED_Full2(self):
        self._send_midi((self.MIDI_TYPE, self.cc_value, self.FULL_2))

class OneColorButton(ButtonElement):
    def __init__(self, is_momentary, msg_type, channel, identifier, _send_midi):
        ButtonElement.__init__(self, is_momentary, msg_type, channel, identifier)
        self.MIDI_TYPE = 176
        self.cc_value = identifier
        self._send_midi = _send_midi
        self.OFF = 0
        self.DIM = 1
        self.FULL = 2
    def Initialize(self):
        self._send_midi((self.MIDI_TYPE, self.cc_value, self.DIM))
    def Reset(self):
        self._send_midi((self.MIDI_TYPE, self.cc_value, self.OFF))
    def SetLED_Dim(self):
        self._send_midi((self.MIDI_TYPE, self.cc_value, self.DIM))

    def SetLED_Full(self):
        self._send_midi((self.MIDI_TYPE, self.cc_value, self.FULL))

class ControllerPads():

    def __init__(self, send_midi, default_pad_color=(255,0,0), default_pad_brightness=5):
        self._send_midi = send_midi
        self.pad_mapping = PAD_MAPPING
        self.default_pad_color= default_pad_color
        self.default_pad_brightness= default_pad_brightness
    
    def SetPadLEDByNumber(self, pad_number, pad_color=None, brightness=None):
        pad_color = pad_color if pad_color else self.default_pad_color
        brightness = brightness if brightness else self.default_pad_brightness

        midi_color_tuple = rgb_colorconverter(pad_color[0], pad_color[1], pad_color[2], brightness)
        sysex_data = (240, 71, 71, 74, 101, 0, 4, pad_number, midi_color_tuple[0], midi_color_tuple[1], midi_color_tuple[2], 247)
        print(sysex_data)
        self._send_midi(  sysex_data )

    def SetPadLEDByNote(self, midi_note_value, pad_color=None, brightness=None):
        pad_color = pad_color if pad_color else self.default_pad_color
        brightness = brightness if brightness else self.default_pad_brightness

        if midi_note_value in self.pad_mapping.keys():
            pad_number = self.pad_mapping[midi_note_value]
            self.SetPadLEDByNumber(pad_number=pad_number, pad_color=pad_color, brightness=brightness)
    
    def SetAllPadsLED(self, pad_color=None, brightness=None):
        pad_color = pad_color if pad_color else self.default_pad_color
        brightness = brightness if brightness else self.default_pad_brightness
        for pad in range(16):
            self.SetPadLEDByNumber(pad, pad_color, brightness)

