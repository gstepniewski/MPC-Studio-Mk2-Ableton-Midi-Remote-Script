import Live

from ableton.v2.base import listens
from ableton.v2.control_surface import Component
from ableton.v2.control_surface.control import control_matrix
from ableton.v2.control_surface.control.button import ButtonControl
NavDirection = Live.Application.Application.View.NavDirection

import logging
logger = logging.getLogger(__name__)


def clamp(val, minv, maxv):
    return max(minv, min(val, maxv))


def _adjust_parameter(parameter, offset, fine_tune):
    if parameter.is_quantized:
        parameter.value = clamp(parameter.value + offset, parameter.min, parameter.max)
    else:
        range = abs(parameter.max - parameter.min)
        step = (range / 100) * fine_tune
        delta = step * offset
        parameter.value = clamp(parameter.value + delta, parameter.min, parameter.max)


class ParameterNavigationComponent(Component):
    jog_wheel_button = ButtonControl()
    jog_wheel_press = ButtonControl()
    shift_button = ButtonControl()
    tempo_button = ButtonControl()

    # TODO This is so ugly it hurts :(
    param_1_button = ButtonControl()
    param_2_button = ButtonControl()
    param_3_button = ButtonControl()
    param_4_button = ButtonControl()
    param_5_button = ButtonControl()
    param_6_button = ButtonControl()
    param_7_button = ButtonControl()
    param_8_button = ButtonControl()
    param_9_button = ButtonControl()
    param_10_button = ButtonControl()
    param_11_button = ButtonControl()
    param_12_button = ButtonControl()
    param_13_button = ButtonControl()
    param_14_button = ButtonControl()
    param_15_button = ButtonControl()
    param_16_button = ButtonControl()

    def __init__(self, *a, **k):
        super(ParameterNavigationComponent, self).__init__(*a, **k)
        self.selected_param_index = 1
        self._update_button_colors()
        self._on_selected_track_changed.subject = self.song.view
        self._on_device_selection_changed.subject = self.song.view.selected_track.view

    @listens('selected_track')
    def _on_selected_track_changed(self):
        self._set_selected_param(1)
        self._on_device_selection_changed.subject = self.song.view.selected_track.view

    @listens('selected_device')
    def _on_device_selection_changed(self):
        self._set_selected_param(1)

    @jog_wheel_press.pressed
    def _on_jog_wheel_pressed(self, value):
        device = self.song.view.selected_track.view.selected_device
        parameter = device.parameters[self.selected_param_index]
        if not parameter.is_quantized:
            parameter.value = parameter.default_value

    @jog_wheel_button.value
    def _on_jog_wheel_turn(self, x, _):
        device = self.song.view.selected_track.view.selected_device
        parameter = device.parameters[self.selected_param_index]
        if self.tempo_button.is_pressed:
            self._adjust_tempo(x)
        elif parameter is not None:
            fine_tune = 1
            if self.shift_button.is_pressed:
                fine_tune = 0.1
            if x == 1:
                _adjust_parameter(parameter, 1, fine_tune)
            if x == 127:
                _adjust_parameter(parameter, -1, fine_tune)

    def _adjust_tempo(self, x):
        factor = 1 if x == 1 else -1
        self.song.tempo = max(min(int(self.song.tempo) + factor, 999), 20)

    def _set_selected_param(self, index):
        device = self.song.view.selected_track.view.selected_device
        if index < len(device.parameters):
            self.selected_param_index = index
            self._update_button_colors()

    def _set_button_color(self, button, button_index):
        device = self.song.view.selected_track.view.selected_device
        if button_index >= len(device.parameters):
            button.color = 'Parameter.Off'
        elif self.selected_param_index == button_index:
            button.color = 'Parameter.Selected'
        else:
            button.color = 'Parameter.On'

    @param_1_button.pressed
    def _param_1_selected(self, _):
        self._set_selected_param(1)

    @param_2_button.pressed
    def _param_2_selected(self, _):
        self._set_selected_param(2)

    @param_3_button.pressed
    def _param_3_selected(self, _):
        self._set_selected_param(3)

    @param_4_button.pressed
    def _param_4_selected(self, _):
        self._set_selected_param(4)

    @param_5_button.pressed
    def _param_5_selected(self, _):
        self._set_selected_param(5)

    @param_6_button.pressed
    def _param_6_selected(self, _):
        self._set_selected_param(6)

    @param_7_button.pressed
    def _param_7_selected(self, _):
        self._set_selected_param(7)

    @param_8_button.pressed
    def _param_8_selected(self, _):
        self._set_selected_param(8)

    @param_9_button.pressed
    def _param_9_selected(self, _):
        self._set_selected_param(9)

    @param_10_button.pressed
    def _param_10_selected(self, _):
        self._set_selected_param(10)

    @param_11_button.pressed
    def _param_11_selected(self, _):
        self._set_selected_param(11)

    @param_12_button.pressed
    def _param_12_selected(self, _):
        self._set_selected_param(12)

    @param_13_button.pressed
    def _param_13_selected(self, _):
        self._set_selected_param(13)

    @param_14_button.pressed
    def _param_14_selected(self, _):
        self._set_selected_param(14)

    @param_15_button.pressed
    def _param_15_selected(self, _):
        self._set_selected_param(15)

    @param_16_button.pressed
    def _param_16_selected(self, _):
        self._set_selected_param(16)

    def _update_button_colors(self):
        self._set_button_color(self.param_1_button, 1)
        self._set_button_color(self.param_2_button, 2)
        self._set_button_color(self.param_3_button, 3)
        self._set_button_color(self.param_4_button, 4)
        self._set_button_color(self.param_5_button, 5)
        self._set_button_color(self.param_6_button, 6)
        self._set_button_color(self.param_7_button, 7)
        self._set_button_color(self.param_8_button, 8)
        self._set_button_color(self.param_9_button, 9)
        self._set_button_color(self.param_10_button, 10)
        self._set_button_color(self.param_11_button, 11)
        self._set_button_color(self.param_12_button, 12)
        self._set_button_color(self.param_13_button, 13)
        self._set_button_color(self.param_14_button, 14)
        self._set_button_color(self.param_15_button, 15)
        self._set_button_color(self.param_16_button, 16)


