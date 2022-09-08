#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ATOM/colors.py
from __future__ import absolute_import, print_function, unicode_literals
from typing import Type
from ableton.v2.control_surface import MIDI_CC_TYPE, MIDI_NOTE_TYPE
from functools import partial
from ableton.v2.base import task
from ableton.v2.control_surface.elements import Color
from . import midi
from .CONST import PAD_MAPPING
import colorsys
import logging
logger = logging.getLogger(__name__)

BLINK_VALUE = 1
PULSE_VALUE = 2

class RGBColorDef:
    OFF = (0, 0, 0)
    BLACK = (0, 1, 2) 
    WHITE = (109, 80, 27)
    RED = (127, 0, 0)
    ORANGE = (127, 64, 0)
    YELLOW = (127, 100, 0)
    GREEN = (0, 127, 0)
    TEAL = (0, 64, 64)
    BLUE = (0, 10, 127)
    INDIGO = (36, 0, 64)
    PURPLE = (120, 0, 120)
    LIGHT_BLUE = (0, 91, 91)
    PEACH = (127, 51, 6)
    PINK = (127, 0, 30)
def rgb_colorconverter(color, brightness=127, unit=127):

    # Convert RGB 255 values into unit values
    red_unit = int(color[0][0]) / unit
    green_unit = int(color[0][1]) / unit
    blue_unit = int(color[0][2]) / unit

    # Conver rgb to hsv
    hsv = colorsys.rgb_to_hsv(red_unit, green_unit, blue_unit)

    # Set custom value of brightness if supplied
    value = hsv[2]
    if(brightness != 0):
        value = brightness / unit

    # Convert back to RGB
    rgb_with_brightness = colorsys.hsv_to_rgb(hsv[0], hsv[1], value)
    
    # Convert RGB unit values to midi sysex values
    return (
        int(round(rgb_with_brightness[0] * 127)), 
        int(round(rgb_with_brightness[1] * 127)), 
        int(round(rgb_with_brightness[2] * 127))
    )
    

class MPCInterface:
        class Type:
            Button = 0
            Pad = 1
        class Animation:
            Solid = 0
            Blink = 1
            Fade = 2
            Pulse = 3
        class OneColorButton:
            Off = 0
            Dim = 1
            Full = 2
        class TwoColorButton:
            Off = 0
            Dim_1 = 1
            Dim_2 = 2
            Full_1 = 3
            Full_2 = 4

class MPCPadColor(Color):
    
    def __init__(self, interface_type=MPCInterface.Type.Pad, color=RGBColorDef.BLACK, brightness=100, animation_type= MPCInterface.Animation.Solid, blink_off_color=RGBColorDef.BLACK , blink_period=0.1, *a, **k):
        super(MPCPadColor, self).__init__(*a, **k)
        self.interface_type = interface_type
        self._color = color,
        self.brightness = brightness
        self.animation_type = animation_type
        self.blink_off_color = blink_off_color
        self._blink_period = blink_period
        self.blink_off_button_color = MPCInterface.OneColorButton.Off
    
    def _send_color(self, color, identifier, send_midi):
        if self.interface_type == MPCInterface.Type.Button:
            send_midi((midi.MIDI_STATUS.CC_STATUS, identifier, color))

        elif self.interface_type == MPCInterface.Type.Pad:
            send_midi((240, 71, 71, 74, 101, 0, 4, identifier, color[0], color[1], color[2], 247))

    def _kill_all_tasks(self, interface):
        interface._tasks.kill()
        interface._tasks.clear()

    def start_blinking(self):
        self._blink_task.restart()

    def stop_blinking(self):
        self._blink_task.kill()

    def draw(self, interface):
        identifier = interface._original_identifier if self.interface_type == MPCInterface.Type.Button else PAD_MAPPING[interface._original_identifier]
        color = self._color if self.interface_type == MPCInterface.Type.Button else rgb_colorconverter(color=self._color, brightness=self.brightness)

        # Draw color by animation type        
        if self.animation_type == MPCInterface.Animation.Solid:
            if hasattr(interface, '_current_color'):
                if interface._current_color == color:
                    # No need to update the pad color
                    pass
                else:
                    self._do_draw_color(identifier, color, interface)
            else:
                self._do_draw_color(identifier, color, interface)

        elif self.animation_type == MPCInterface.Animation.Blink:
            blink_off_color = rgb_colorconverter(color=self._color, brightness=1) if self.interface_type == MPCInterface.Type.Pad else self.blink_off_button_color
            blink_on = partial(self._send_color, color, identifier, interface.send_midi)
            blink_off = partial(self._send_color, blink_off_color, identifier, interface.send_midi)
            self._kill_all_tasks(interface)
            interface._tasks.add(
                    task.loop(
                        task.sequence(
                        task.run(blink_on), 
                        task.wait(self._blink_period), 
                        task.run(blink_off), 
                        task.wait(self._blink_period), 
                        )
                )
            ) 
        elif self.animation_type == MPCInterface.Animation.Fade:
            def fade_on(x):
                fade_color = rgb_colorconverter(color=self._color, brightness=(x * 127))
                if self.interface_type == MPCInterface.Type.Pad:
                    interface._send_midi((240, 71, 71, 74, 101, 0, 4, identifier, fade_color[0], fade_color[1], fade_color[2], 247))
            self._kill_all_tasks(interface)
            interface._tasks.add(
                    task.loop(
                        task.sequence(
                        task.fade(fade_on), 
                        task.wait(self._blink_period), 
                        )
                )
            ) 
    def _do_draw_color(self, identifier, color, interface):
        new_color_function = partial(self._send_color, color, identifier, interface.send_midi)
        self._kill_all_tasks(interface)
        setattr(interface, '_current_color', color)
        interface._tasks.add(task.run(new_color_function))

class MPCButtonColor(Color):
    def __init__(self, midi_cc_value, *a, **k):
        super(MPCButtonColor, self).__init__(*a, **k)
        self.midi_cc_value = midi_cc_value
    
    def _kill_all_tasks(self, interface):
        interface._tasks.kill()
        interface._tasks.clear()
    
    def draw(self, interface):
        self._kill_all_tasks(interface)
        interface.send_midi((midi.MIDI_STATUS.CC_STATUS, interface._original_identifier, self.midi_cc_value))

class MPCButtonColorBlink(Color):

    def __init__(self, blink_on_color= 2, blink_off_color=1, blink_period=0.1, *a, **k):
        super(MPCButtonColorBlink, self).__init__(*a, **k)
        self.blink_on_color = blink_on_color
        self.blink_off_color = blink_off_color
        self._blink_period = blink_period

    def start_blinking(self):
        self._blink_task.restart()

    def stop_blinking(self):
        self._blink_task.kill()

    def _set_blinking_color(self, color, identifier, send_midi):
        send_midi((midi.MIDI_STATUS.CC_STATUS, identifier, color))

    def _kill_all_tasks(self, interface):
        interface._tasks.kill()
        interface._tasks.clear()
    
    def draw(self, interface):
        blink_on = partial(self._set_blinking_color, self.blink_on_color, interface._original_identifier, interface.send_midi)
        blink_off = partial(self._set_blinking_color, self.blink_off_color, interface._original_identifier, interface.send_midi)
        self._kill_all_tasks(interface)
        interface._tasks.add(
                task.loop(
                    task.sequence(
                    task.run(blink_on), 
                    task.wait(self._blink_period), 
                    task.run(blink_off), 
                    task.wait(self._blink_period), 
                    )
            )
        ) 
        
class Mono:
    OFF = Color(1)
    ON = Color(2)

class OneColorButton:
    DISABLED = MPCButtonColor(0)
    OFF = MPCButtonColor(1)
    ON = MPCButtonColor(2)
    BLINK= MPCButtonColorBlink(2, 1)


class TwoColorButtonMap:
    DISABLED = MPCButtonColor(0)
    COLOR_1_DIM = MPCButtonColor(1)
    COLOR_2_DIM = MPCButtonColor(2)
    COLOR_1_FULL = MPCButtonColor(3)
    COLOR_2_FULL = MPCButtonColor(4)
    COLOR_1_BLINK = MPCButtonColorBlink(3,1)
    COLOR_2_BLINK = MPCButtonColorBlink(4,2)

def color_generator(red, green, blue):
    color_tuple = (red, green, blue)
    return MPCPadColor(color=color_tuple)
LIVE_COLOR_INDEX_TO_RGB = {
 0: color_generator(102, 46, 46),
 1: color_generator(127, 34, 0),
 2: color_generator(51, 51, 0),
 3: color_generator(123, 122, 57),
 4: color_generator(95, 125, 0),
 5: color_generator(0, 39, 0),
 6: color_generator(25, 127, 25),
 7: color_generator(46, 127, 116),
 8: color_generator(0, 76, 76),
 9: color_generator(0, 51, 102),
 10: color_generator(16, 89, 85),
 11: color_generator(69, 21, 113),
 12: color_generator(110, 10, 30),
 13: color_generator(127, 127, 127),
 14: color_generator(127, 0, 0),
 15: color_generator(127, 32, 0),
 16: color_generator(51, 51, 0),
 17: color_generator(127, 82, 0),
 18: color_generator(17, 69, 17),
 19: color_generator(0, 31, 0),
 20: color_generator(0, 76, 38),
 21: color_generator(0, 127, 127),
 22: color_generator(0, 51, 102),
 23: color_generator(0, 0, 51),
 24: color_generator(38, 0, 76),
 25: color_generator(51, 0, 51),
 26: color_generator(110, 10, 30),
 27: color_generator(104, 104, 104),
 28: color_generator(89, 17, 17),
 29: color_generator(127, 49, 35),
 30: color_generator(105, 86, 56),
 31: color_generator(118, 127, 87),
 32: color_generator(86, 127, 23),
 33: color_generator(86, 127, 23),
 34: color_generator(86, 127, 23),
 35: color_generator(106, 126, 112),
 36: color_generator(102, 120, 124),
 37: color_generator(127, 76, 127),
 38: color_generator(127, 76, 127),
 39: color_generator(127, 25, 127),
 40: color_generator(114, 110, 112),
 41: color_generator(84, 84, 84),
 42: color_generator(127, 49, 35),
 43: color_generator(51, 51, 0),
 44: color_generator(51, 51, 0),
 45: color_generator(77, 102, 25),
 46: color_generator(86, 127, 23),
 47: color_generator(38, 76, 0),
 48: color_generator(30, 89, 56),
 49: color_generator(23, 69, 43),
 50: color_generator(23, 69, 43),
 51: color_generator(23, 69, 43),
 52: color_generator(119, 65, 119),
 53: color_generator(119, 65, 119),
 54: color_generator(89, 17, 17),
 55: color_generator(61, 61, 61),
 56: color_generator(69, 0, 0),
 57: color_generator(82, 21, 21),
 58: color_generator(51, 51, 0),
 59: color_generator(127, 82, 0),
 60: color_generator(0, 50, 0),
 61: color_generator(0, 50, 0),
 62: color_generator(5, 78, 71),
 63: color_generator(17, 49, 66),
 64: color_generator(0, 0, 127),
 65: color_generator(0, 51, 102),
 66: color_generator(38, 0, 76),
 67: color_generator(51, 0, 51),
 68: color_generator(102, 23, 55),
 69: color_generator(30, 30, 30)}
