import Live
from ableton.v2.control_surface import Component
from ableton.v2.control_surface.control.button import ButtonControl
NavDirection = Live.Application.Application.View.NavDirection

import logging
logger = logging.getLogger(__name__)


class DeviceNavigationComponent(Component):
    jog_wheel_button = ButtonControl()
    jog_wheel_press = ButtonControl()
    shift_button = ButtonControl()

    def __init__(self, *a, **k):
        super(DeviceNavigationComponent, self).__init__(*a, **k)

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
        device = self.song.view.selected_track.view.selected_device
        if device is None:
            return
        if self.shift_button.is_pressed:
            device.view.is_collapsed = not device.view.is_collapsed
        else:
            self.set_device_enabled(device, not self.is_device_enabled(device))

    @jog_wheel_button.value
    def _on_jog_wheel_turn(self, x, _):
        if self.shift_button.is_pressed:
            device = self.song.view.selected_track.view.selected_device
            if device is None:
                return
            if x == 1:
                self.move_device_right(device)
            if x == 127:
                self.move_device_left(device)
        else:
            if x == 1:
                self.application.view.scroll_view(NavDirection.right, 'Detail/DeviceChain', False)
            if x == 127:
                self.application.view.scroll_view(NavDirection.left, 'Detail/DeviceChain', False)
