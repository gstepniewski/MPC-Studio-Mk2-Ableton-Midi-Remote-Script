#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ATOM/view_toggle.py
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import listens
from ableton.v2.control_surface import Component
from ableton.v2.control_surface.control import ToggleButtonControl

class ViewToggleComponent(Component):
    detail_view_toggle_button = ToggleButtonControl()
    main_view_toggle_button = ToggleButtonControl()
    browser_view_toggle_button = ToggleButtonControl()
    clip_detail_view_toggle_button = ToggleButtonControl()

    
    def __init__(self, *a, **k):
        super(ViewToggleComponent, self).__init__(*a, **k)
        self.__on_detail_view_visibility_changed.subject = self.application.view
        self.__on_main_view_visibility_changed.subject = self.application.view
        self.__on_browser_view_visibility_changed.subject = self.application.view
        self.detail_view_toggle_button.untoggled_color = 'ViewToggle.Dim'
        self.detail_view_toggle_button.toggled_color = 'ViewToggle.On'
        self.main_view_toggle_button.untoggled_color = 'ViewToggle.On'
        self.main_view_toggle_button.toggled_color = 'ViewToggle.Off'
        self.browser_view_toggle_button.untoggled_color = 'ViewToggle.On'
        self.browser_view_toggle_button.toggled_color = 'ViewToggle.Off'
        self.clip_detail_view_toggle_button.untoggled_color = 'ViewToggle.On'
        self.clip_detail_view_toggle_button.toggled_color = 'ViewToggle.On'
        self.__on_detail_view_visibility_changed()
        self.__on_main_view_visibility_changed()
        self.__on_browser_view_visibility_changed()

    @detail_view_toggle_button.toggled
    def detail_view_toggle_button(self, is_toggled, _):
        self._show_or_hide_view(is_toggled, u'Detail')

    @main_view_toggle_button.toggled
    def main_view_toggle_button(self, is_toggled, _):
        self._show_or_hide_view(is_toggled, u'Session')

    @browser_view_toggle_button.toggled
    def browser_view_toggle_button(self, is_toggled, _):
        self._show_or_hide_view(is_toggled, u'Browser')

    @clip_detail_view_toggle_button.toggled
    def clip_view_toggle_button(self, is_toggled, _):
        if self.application.view.is_view_visible(u'Detail/Clip'):
            self.application.view.show_view(u'Detail/DeviceChain')
        elif self.application.view.is_view_visible(u'Detail/DeviceChain'):
            self.application.view.show_view(u'Detail/Clip')
        else:
            self.application.view.show_view(u'Detail')

    def _show_or_hide_view(self, show_view, view_name):
        if show_view:
            self.application.view.show_view(view_name)
        else:
            self.application.view.hide_view(view_name)

    @listens(u'is_view_visible', u'Detail')
    def __on_detail_view_visibility_changed(self):
        self.detail_view_toggle_button.is_toggled = self.application.view.is_view_visible(u'Detail')

    @listens(u'is_view_visible', u'Session')
    def __on_main_view_visibility_changed(self):
        self.main_view_toggle_button.is_toggled = self.application.view.is_view_visible(u'Session')
    
    @listens(u'is_view_visible', u'Browser')
    def __on_browser_view_visibility_changed(self):
        self.browser_view_toggle_button.is_toggled = self.application.view.is_view_visible(u'Browser')
