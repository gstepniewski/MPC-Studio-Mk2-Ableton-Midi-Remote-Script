from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import liveobj_valid, listens
from ableton.v2.control_surface.control import ButtonControl
from ableton.v2.control_surface import Component

import logging
logger = logging.getLogger(__name__)

class RoutingComponent(Component):
    input_type_button = ButtonControl(color=u'DefaultButton.Off', pressed_color=u'DefaultButton.Selected')
    input_channel_button = ButtonControl(color=u'DefaultButton.Off', pressed_color=u'DefaultButton.Selected')
    output_type_button = ButtonControl(color=u'DefaultButton.Off', pressed_color=u'DefaultButton.Selected')
    output_channel_button = ButtonControl(color=u'DefaultButton.Off', pressed_color=u'DefaultButton.Selected')
    monitor_cycle_button = ButtonControl(color=u'DefaultButton.Off')


    def __init__(self, *a, **k) -> None:
        super(RoutingComponent, self).__init__(*a, **k)
        self._track = None
        self._on_selected_track_changed.subject = self.song.view
        self._on_selected_track_changed()
        self.__on_current_monitoring_state_changed.subject = self.song.view
        self.__on_current_monitoring_state_changed()

    def _list_cycle(self, list, current_item):
        current_index = 0
        for i, item in enumerate(list):
            if item == current_item:
                current_index = i
        new_index = current_index + 1 if current_index + 1 < len(list) else 0
        return new_index
    
    @listens('selected_track')
    def _on_selected_track_changed(self):
        self._track = self.song.view.selected_track
        self.__on_current_monitoring_state_changed()

    @input_type_button.pressed
    def _on_input_type_button_button_pressed(self, _):
        input_types = self._track.available_input_routing_types
        new_index = self._list_cycle(input_types, self._track.input_routing_type)
        self._track.input_routing_type = input_types[new_index]
    
    @input_channel_button.pressed
    def _on_input_channel_button_pressed(self, _):
        channels = self._track.available_input_routing_channels
        new_index = self._list_cycle(channels, self._track.input_routing_channel)
        self._track.input_routing_channel = channels[new_index]

    @output_type_button.pressed
    def _on_output_type_button_pressed(self, _):
        output_types = self._track.available_output_routing_types
        new_index = self._list_cycle(output_types, self._track.output_routing_type)
        self._track.output_routing_type = output_types[new_index] 

    @output_channel_button.pressed
    def _on_output_channel_button_pressed(self, _):
        channels = self._track.available_output_routing_channels
        new_index = self._list_cycle(channels, self._track.output_routing_channel)
        self._track.output_routing_channel = channels[new_index]   

    @monitor_cycle_button.pressed
    def _on_monitor_cycle_button_pressed(self, _):
        monitor_states = [0,1,2]
        new_index = self._list_cycle(monitor_states, self._track.current_monitoring_state)
        self._track.current_monitoring_state = monitor_states[new_index]

    @listens('selected_track.current_monitoring_state')
    def __on_current_monitoring_state_changed(self):
        if self._track in self.song.tracks:
        # if self._track != self.song.master_track:
            state = self._track.current_monitoring_state
            if state == 0:
                self.monitor_cycle_button.color = u'DefaultButton.Selected'
            elif state == 1:
                self.monitor_cycle_button.color = u'DefaultButton.Off'
            elif state == 2:
                self.monitor_cycle_button.color = u'DefaultButton.On'