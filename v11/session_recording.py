from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import liveobj_valid
from ableton.v2.control_surface.components import SessionRecordingComponent as SessionRecordingComponentBase


class SessionRecordingComponent(SessionRecordingComponentBase):
    def __init__(self, *a, **k):
        super(SessionRecordingComponent, self).__init__(*a, **k)
    def _update_generic_new_button(self, new_button):
        if new_button and self.is_enabled():
            song = self.song
            selected_track = song.view.selected_track
            clip_slot = song.view.highlighted_clip_slot
            can_new = liveobj_valid(clip_slot) and clip_slot.clip or selected_track.can_be_armed and selected_track.playing_slot_index >= 0
            new_button.set_light(u'DefaultButton.On' if can_new else u'DefaultButton.Off')

    def _update_new_scene_button(self):
        if self._new_scene_button and self.is_enabled():
            song = self.song
            track_is_playing = find_if(lambda x: x.playing_slot_index >= 0, song.tracks)
            can_new = not song.view.selected_scene.is_empty or track_is_playing
            self._new_scene_button.set_light(u'DefaultButton.On' if can_new else u'DefaultButton.Off')
    