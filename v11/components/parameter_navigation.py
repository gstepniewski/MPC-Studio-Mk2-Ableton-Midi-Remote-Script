import Live
from ableton.v2.control_surface import Component
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

    def __init__(self, *a, **k):
        super(ParameterNavigationComponent, self).__init__(*a, **k)

    @staticmethod
    def is_device_enabled(device):
        return bool(device.parameters[0].value)

    @staticmethod
    def set_device_enabled(device, enabled):
        device.parameters[0].value = int(enabled)

    def move_device_left(self, device):
        parent = device.canonical_parent
        device_index = list(parent.devices).index(device)
        if device_index > 0:
            self.song.move_device(device, parent, device_index - 1)

    def move_device_right(self, device):
        parent = device.canonical_parent
        device_index = list(parent.devices).index(device)
        if device_index < len(parent.devices) - 1:
            self.song.move_device(device, parent, device_index + 2)

    @jog_wheel_press.pressed
    def _on_jog_wheel_pressed(self, value):
        parameter = self.song.view.selected_parameter
        if not parameter.is_quantized:
            parameter.value = parameter.default_value


    @jog_wheel_button.value
    def _on_jog_wheel_turn(self, x, _):
        parameter = self.song.view.selected_parameter
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

