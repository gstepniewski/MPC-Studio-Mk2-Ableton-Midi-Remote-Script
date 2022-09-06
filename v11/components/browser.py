from __future__ import absolute_import, print_function, unicode_literals
import Live
from ableton.v2.base import liveobj_valid
from ableton.v2.control_surface import Component
from ableton.v2.control_surface.control import control_list, ButtonControl, StepEncoderControl, ToggleButtonControl

class BrowserComponent(Component):
    empty_color = u'Mixer.EmptyTrack'
    up_button = ButtonControl(repeat=True)
    down_button = ButtonControl(repeat=True)
    right_button = ButtonControl(repeat=True)
    left_button = ButtonControl(repeat=True)
    back_button = ButtonControl()
    open_button = ButtonControl()
    load_button = ButtonControl()
    close_button = ButtonControl()

    def __init__(self, *a, **k):
        super(BrowserComponent, self).__init__(*a, **k)
        self._browser = Live.Application.get_application().browser
        self._current_hotswap_target = self._browser.hotswap_target

    # def _load_item(self, item):
    #     self._show_load_notification(item)
    #     if liveobj_valid(self._browser.hotswap_target):
    #         if isinstance(item, PluginPresetBrowserItem):
    #             self._browser.hotswap_target.selected_preset_index = item.preset_index
    #         else:
    #             self._browser.load_item(item)
    #             self._content_hotswap_target = self._browser.hotswap_target
    #     else:
    #         with self._insert_right_of_selected():
    #             self._browser.load_item(item)