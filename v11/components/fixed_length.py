#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ATOM/note_pad.py
from __future__ import absolute_import, print_function, unicode_literals
from __future__ import absolute_import, print_function, unicode_literals

from builtins import map, object, range
from ableton.v2.base import listens, task
from ableton.v2.control_surface import Component
from ableton.v2.control_surface.control import ButtonControl, InputControl
from .action_with_options_component import OptionsComponent
from ..elements.repeat_display_element import RepeatDisplayElement

import logging
logger = logging.getLogger(__name__)


def track_can_record(track):
    return track.can_be_armed and (track.arm or track.implicit_arm)


class FixedLengthSetting(object):

    def __init__(self, *a, **k):
        super(FixedLengthSetting, self).__init__(*a, **k)
        self._selected_beats = 16
        self._enabled = False

    @property
    def selected_beats(self):
        return self._selected_beats

    @selected_beats.setter
    def selected_beats(self, value):
        self._selected_beats = value

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        self._enabled = value


class FixedLengthRecording(object):

    def __init__(self, fixed_length_setting=None, *a, **k):
        super(FixedLengthRecording, self).__init__(*a, **k)
        self._fixed_length_setting = fixed_length_setting

    def should_start_recording_in_slot(self, clip_slot):
        return track_can_record(clip_slot.canonical_parent) and not clip_slot.is_recording and not clip_slot.has_clip and self._fixed_length_setting.enabled

    def start_recording_in_slot(self, clip_slot):
        clip_slot.fire(record_length=self._fixed_length_setting.selected_beats)


class FixedLengthEnabler(Component):
    fixed_length_button = ButtonControl()

    def __init__(self, fixed_length_setting=None, *a, **k):
        super(FixedLengthEnabler, self).__init__(*a, **k)
        self.fixed_length_component = FixedLengthComponent(name='Fixed Length',
               fixed_length_setting=fixed_length_setting,
               parent=self,
               is_enabled=False)
        self._fixed_length_setting = fixed_length_setting
        self._restore_fixed_length_enabled()

    @fixed_length_button.pressed
    def fixed_length_button(self, button):
        self._toggle_fixed_length()

    @fixed_length_button.released_delayed
    def fixed_length_button(self, button):
        self._togggle_fixed_length()

    def _toggle_fixed_length(self):
        is_enabled = not self._fixed_length_setting.enabled
        self._set_fixed_length_enabled(is_enabled)

    def _set_fixed_length_enabled(self, is_enabled):
        self._fixed_length_setting.enabled = is_enabled
        self.fixed_length_component.set_enabled(is_enabled)
        self.fixed_length_button.color = 'DefaultButton.Selected' if is_enabled else 'DefaultButton.Off'

    def _restore_fixed_length_enabled(self):
        self._set_fixed_length_enabled(self._fixed_length_setting.enabled)


FIXED_LENGTHS = [32, 32, 16, 16, 8, 8, 4, 4]
DEFAULT_INDEX = 4


class FixedLengthComponent(Component):
    length_control = InputControl()

    def __init__(self, fixed_length_setting=None, *a, **k):
        super(FixedLengthComponent, self).__init__(*a, **k)
        self._fixed_length_display = RepeatDisplayElement()
        self._fixed_length_setting=fixed_length_setting
        self._current_cc_index = None
        self._last_record_quantization = None
        self._options = OptionsComponent(parent=self)
        self._options.option_names = list(map(str, list(range(8))))
        self._options.selected_option = DEFAULT_INDEX
        self._on_selected_option_changed.subject = self._options

    @length_control.value
    def rate_control_slider(self, value, _):
        cc_index = int(value) // 16
        if self._current_cc_index != cc_index:
            repeat_rate_index = 7 - cc_index
            self._on_selected_option_changed(repeat_rate_index)
            self._current_cc_index = cc_index

    def disconnect(self):
        self._fixed_length_display.reset()
        super(FixedLengthComponent, self).disconnect()

    def update(self):
        super(FixedLengthComponent, self).update()
        self._update_fixed_length()

    def set_select_buttons(self, buttons):
        self._options.select_buttons.set_control_element(buttons)

    def _get_fixed_length_index(self):
        fixed_length = self._fixed_length_setting.selected_beats
        if fixed_length in FIXED_LENGTHS:
            return FIXED_LENGTHS.index(fixed_length)
        return DEFAULT_INDEX

    @listens('selected_option')
    def _on_selected_option_changed(self, option):
        self._fixed_length_setting.selected_beats = FIXED_LENGTHS[option]
        self._set_length_display(option)
        self._options.selected_option = option

    def _update_fixed_length(self):
        length_index = self._get_fixed_length_index()
        self._on_selected_option_changed(length_index)
        # self._fixed_length_setting.enabled = self.is_enabled()

    def _set_length_display(self, index):
        if self.is_enabled():
            self._fixed_length_display.update_repeat_display_index(7 - int(index))
        else:
            self._fixed_length_display.reset()


