from ableton.v2.base import listens
from ableton.v2.control_surface.mode import ModesComponent

import logging
logger = logging.getLogger(__name__)


class NavigationModesComponent(ModesComponent):
    def __init__(self, enable_skinning=False, support_momentary_mode_cycling=True, *a, **k):
        super(NavigationModesComponent, self).__init__(*a, **k)
        self.__on_selected_mode_changed.subject = self

    @listens(u'selected_mode')
    def __on_selected_mode_changed(self, mode):
        if mode == 'browser':
            self.application.view.show_view(u'Browser')
        else:
            self.application.view.hide_view(u'Browser')
