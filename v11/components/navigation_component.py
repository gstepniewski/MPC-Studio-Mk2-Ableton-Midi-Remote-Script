from ableton.v2.base import listens
from ableton.v2.control_surface.mode import ModesComponent

from ..lcd import show_lcd_message_2, show_lcd_message

import logging
logger = logging.getLogger(__name__)


class NavigationModesComponent(ModesComponent):
    def __init__(self, enable_skinning=False, support_momentary_mode_cycling=True, *a, **k):
        super(NavigationModesComponent, self).__init__(*a, **k)
        self.__on_selected_mode_changed.subject = self
        self._hotswap_cycled = False

    @listens(u'selected_mode')
    def __on_selected_mode_changed(self, mode):
        if mode == 'browser':
            show_lcd_message("BROWSER")
            self.application.view.show_view(u'Browser')
            if not self._hotswap_cycled:
                # Toggle hot swap on and off to force browser focus
                self.application.view.toggle_browse()
                self.application.view.toggle_browse()
                # But only once because it resets location to current device
                self._hotswap_cycled = True
        else:
            self.application.view.hide_view(u'Browser')
            if mode == 'track':
                show_lcd_message_2("TRACK", self.song.view.selected_track.name)
            if mode == 'device':
                show_lcd_message_2("DEVICE", self.song.view.selected_track.view.selected_device.name)
            if mode == 'parameter':
                show_lcd_message_2("PARAM", "--selected--")
            logger.info(f'Selected mode {mode}')
