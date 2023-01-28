import Live

from ableton.v2.control_surface import Component
from ableton.v2.control_surface.control.button import ButtonControl
NavDirection = Live.Application.Application.View.NavDirection
import logging
logger = logging.getLogger(__name__)


class BrowserNavigationComponent(Component):
    jog_wheel_button = ButtonControl()
    jog_wheel_press = ButtonControl()
    shift_button = ButtonControl()
    tempo_button = ButtonControl()

    def __init__(self, *a, **k):
        super(BrowserNavigationComponent, self).__init__(*a, **k)

    @jog_wheel_press.pressed
    def _on_jog_wheel_pressed(self, value):
        self.application.view.focus_view(u'Browser')
        if self.shift_button.is_pressed:
            self.application.view.scroll_view(NavDirection.left, u'Browser', False)
        else:
            self.application.view.scroll_view(NavDirection.right, u'Browser', False)

    @jog_wheel_button.value
    def scroll_direction(self, x, _):
        self.application.view.focus_view(u'Browser')
        if self.tempo_button.is_pressed:
            self._adjust_tempo(x)
        elif self.shift_button.is_pressed:
            if x == 1:
                self.application.view.scroll_view(NavDirection.right, u'Browser', False)
            if x == 127:
                self.application.view.scroll_view(NavDirection.left, u'Browser', False)
        else:
            if x == 1:
                self.application.view.scroll_view(NavDirection.down, u'Browser', False)
            if x == 127:
                self.application.view.scroll_view(NavDirection.up, u'Browser', False)

    def _adjust_tempo(self, x):
        factor = 1 if x == 1 else -1
        self.song.tempo = max(min(int(self.song.tempo) + factor, 999), 20)
