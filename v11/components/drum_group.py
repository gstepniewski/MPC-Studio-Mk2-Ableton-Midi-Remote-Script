#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ATOM/drum_group.py
from __future__ import absolute_import, print_function, unicode_literals
import Live
from ableton.v2.base import liveobj_valid
from past.utils import old_div
from ableton.v2.control_surface.components import DrumGroupComponent as DrumGroupComponentBase, PlayableComponent
from .note_pad import NotePadMixin
import logging
logger = logging.getLogger(__name__)

COMPLETE_QUADRANTS_RANGE = list(range(4, 116))
MAX_QUADRANT_INDEX = 7
NUM_PADS = 16
PADS_PER_ROW = 4

class DrumGroupComponent(NotePadMixin, DrumGroupComponentBase):
    def __init__(self, *a, **k):
        super(DrumGroupComponent, self).__init__(*a, **k)
        self.delete_button.color=u'DrumGroup.DeleteButton.Off'
        self.delete_button.pressed_color=u'DrumGroup.DeleteButton.On'
        self.mute_button.color=u'DrumGroup.MuteButton.Off'
        self.mute_button.pressed_color=u'DrumGroup.MuteButton.On'
        self.solo_button.color=u'DrumGroup.SoloButton.Off'
        self.solo_button.pressed_color=u'DrumGroup.SoloButton.On'

    def set_drum_group_device(self, drum_group_device, *a, **k):
        super(DrumGroupComponent, self).set_drum_group_device(drum_group_device, *a, **k)
    def _update_led_feedback(self):
        PlayableComponent._update_led_feedback(self)

    def _on_matrix_pressed(self, button):
        selected_drum_pad = self._pad_for_button(button)
        if self.mute_button.is_pressed:
            selected_drum_pad.mute = not selected_drum_pad.mute
        if self.solo_button.is_pressed:
            selected_drum_pad.solo = not selected_drum_pad.solo
        if self.delete_button.is_pressed:
            button.color = u'DrumGroup.PadAction'
            self.delete_pitch(selected_drum_pad)
        if self.mute_button.is_pressed or self.solo_button.is_pressed:
            self._update_led_feedback()

    def delete_pitch(self, drum_pad):
        # super(DrumGroupComponent, self).delete_pitch(drum_pad)
        if liveobj_valid(drum_pad):
            Live.DrumPad.DrumPad.delete_all_chains(drum_pad)
    
    def delete_pitch(self, drum_pad):
        # super(DrumGroupComponent, self).delete_pitch(drum_pad)
        if liveobj_valid(drum_pad):
            Live.DrumPad.DrumPad.delete_all_chains(drum_pad)

    def _update_button_color(self, button):
        pad = self._pad_for_button(button)
        color = self._color_for_pad(pad) if liveobj_valid(pad) else 'DrumGroup.PadEmpty'
        if liveobj_valid(self._drum_group_device):
            if color == 'DrumGroup.PadFilled':
                button_row, _ = button.coordinate
                button_index = (self.matrix.height - button_row - 1) * PADS_PER_ROW
                pad_row_start_note = self._drum_group_device.visible_drum_pads[button_index].note
                pad_quadrant = MAX_QUADRANT_INDEX
                if pad_row_start_note in COMPLETE_QUADRANTS_RANGE:
                    pad_quadrant = old_div(pad_row_start_note - 1, NUM_PADS)
                color = 'DrumGroup.PadQuadrant{}'.format(pad_quadrant)
        button.color = color
