from ableton.v2.control_surface import Component, InputControlElement
from ableton.v2.control_surface.control.button import ButtonControl

import logging
logger = logging.getLogger(__name__)



class DeviceNavigationComponent(Component):
    jog_wheel_button = ButtonControl()
    jog_wheel_press = ButtonControl()
    def __init__(self, *a, **k):
        super(DeviceNavigationComponent, self).__init__(*a, **k)

    @jog_wheel_press.pressed
    def _on_jog_wheel_pressed(self, value):
        logger.warn('device')