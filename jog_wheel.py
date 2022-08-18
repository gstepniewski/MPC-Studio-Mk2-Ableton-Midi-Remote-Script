from ableton.v2.control_surface import Component, InputControlElement
from ableton.v2.control_surface.control.button import ButtonControl

import logging
logger = logging.getLogger(__name__)

class JogWheelElement(InputControlElement):
    def __init__(self, inc_value, dec_value, *a, **k):
        super(JogWheelElement, self).__init__(*a, **k)
        self._inc_value = inc_value
        self._dec_value = dec_value

class TrackSelectComponent(Component):
    jog_wheel_button = ButtonControl()
    jog_wheel_press = ButtonControl()

    @jog_wheel_press.pressed
    def arm_selected_track(self):
        pass
    
    @jog_wheel_button.value
    def undo_button(self, x, _):
        if x == 1:
            self._select_next_track()
        if x == 127:
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
        selected_track = self.song.view.selected_track
        all_tracks = self.all_tracks()
        assert selected_track in all_tracks
        index = list(all_tracks).index(selected_track)
        self.song.view.selected_track = all_tracks[index - 1]

    def _select_next_track(self):
        selected_track = self.song.view.selected_track
        all_tracks = self.all_tracks()
        assert selected_track in all_tracks
        index = list(all_tracks).index(selected_track)
        self.song.view.selected_track = all_tracks[index + 1]