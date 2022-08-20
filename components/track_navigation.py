from ableton.v2.base import listens, liveobj_valid
from ableton.v2.control_surface import Component, InputControlElement
from ableton.v2.control_surface.components import ChannelStripComponent
from ableton.v2.control_surface.control.button import ButtonControl

import logging
logger = logging.getLogger(__name__)
def reset_button(button):
    if button != None:
        button.reset()


class TrackNavigationComponent(Component):
    jog_wheel_button = ButtonControl()
    arm_button = ButtonControl()
    def __init__(self, *a, **k):
        super(TrackNavigationComponent, self).__init__(*a, **k)
        self._track = None
        self._arm_pressed = False
        self._shift_pressed = False
        self._arm_button = None
        self.__on_selected_track_changed()
        self.__on_selected_track_changed.subject = self.song.view
        self._arm_button_slot = self.register_slot(None, getattr(self, u'_%s_value' % u'arm'), u'value')
    
    def set_arm_button(self, button):
        if button != self._arm_button:
            self.reset_button_on_exchange(self._arm_button)
            self._arm_pressed = False
            self._arm_button = button
            self._arm_button_slot.subject = button
            self.update()

    def reset_button_on_exchange(self, button):
        reset_button(button)

    def arm_button_pressed(self):
        return self._arm_pressed

    def disconnect(self):
        u""" releasing references and removing listeners"""
        ChannelStripComponent._active_instances.remove(self)
        reset_button(self._arm_button)
        self._arm_button = None
        super(ChannelStripComponent, self).disconnect()


    def _arm_value(self, value):
        if self.is_enabled():
            if liveobj_valid(self._track) and self._track.can_be_armed:
                self._arm_pressed = value != 0 and self._arm_button.is_momentary()
                if not self._arm_button.is_momentary() or value != 0:
                    expected_arms_pressed = 1 if self._arm_pressed else 0
                    arm_exclusive = self.song.exclusive_arm != self._shift_pressed and (not self._arm_button.is_momentary() or ChannelStripComponent.number_of_arms_pressed() == expected_arms_pressed)
                    new_value = not self._track.arm
                    respect_multi_selection = self._track.is_part_of_selection
                    for track in self.song.tracks:
                        if track.can_be_armed:
                            if track == self._track or respect_multi_selection and track.is_part_of_selection:
                                track.arm = new_value
                            elif arm_exclusive and track.arm:
                                track.arm = False
    
    @jog_wheel_button.value
    def undo_button(self, x, _):
        if x == 1 and self._can_select_next_track():
            self._select_next_track()
        if x == 127 and self._can_select_prev_track():
            self._select_prev_track()
    
    def all_tracks(self):
        return self.tracks_to_use() + (self.song.master_track,)

    def tracks_to_use(self):
        return tuple(self.song.visible_tracks) + tuple(self.song.return_tracks)

    def _can_select_prev_track(self):
        return self.song.view.selected_track != self.song.tracks[0]

    def _can_select_next_track(self):
        return self.song.view.selected_track != self.song.master_track

    def _select_prev_track(self):
        all_tracks = self.all_tracks()
        assert self._track in all_tracks
        index = list(all_tracks).index(self._track)
        self.song.view.selected_track = all_tracks[index - 1]

    def _select_next_track(self):
        all_tracks = self.all_tracks()
        assert self._track in all_tracks
        index = list(all_tracks).index(self._track)
        self.song.view.selected_track = all_tracks[index + 1]
    
    @listens(u'selected_track')
    def __on_selected_track_changed(self):
        self._track = self.song.view.selected_track