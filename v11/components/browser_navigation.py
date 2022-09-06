import Live
from ableton.v2.control_surface import Component
from ableton.v2.control_surface.control.button import ButtonControl
NavDirection = Live.Application.Application.View.NavDirection
import logging
logger = logging.getLogger(__name__)

# COde snippet to listen to mode changes
# self.__on_selected_mode_changed.subject = self
# @listens(u'selected_mode')

# Potential Browser Navigation commands
# self.application().view.scroll_view(nav.up, u'', self.alt_is_pressed())
# nav = Live.Application.Application.View.NavDirection


class BrowserNavigationComponent(Component):
    jog_wheel_button = ButtonControl()
    jog_wheel_press = ButtonControl()
    def __init__(self, *a, **k):
        super(BrowserNavigationComponent, self).__init__(*a, **k)
        self.current_item = None
        self._browser = Live.Application.get_application().browser
    
    @jog_wheel_press.pressed
    def _on_jog_wheel_pressed(self, value):
        # self.application.view.focus_view(u'Browser')
        logger.warn('browser')

    @jog_wheel_button.value
    def scroll_direction(self, x, _):
        self.application.view.focus_view(u'Browser')
        if x == 1:
            # self.application.view.scroll_view(NavDirection.down, u'', False)
            self._browser.drums.iter_children.next().is_selected = True
            logger.warn('test')

        if x == 127:
            pass
            # self.application.view.scroll_view(NavDirection.up, u'', False)
    