#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ATOM/session.py
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import liveobj_valid, duplicate_clip_loop, depends, const
from ableton.v2.control_surface.components import ClipSlotComponent as ClipSlotComponentBase, SceneComponent as SceneComponentBase, SessionComponent as SessionComponentBase
from ableton.v2.control_surface import ClipCreator
from ableton.v2.control_surface.control import ButtonControl
from ableton.v2.control_surface import Component

from ..colors import LIVE_COLOR_INDEX_TO_RGB

def is_button_pressed(button):
    if button:
        return button.is_pressed()
    return False

class ClipSlotComponent(ClipSlotComponentBase):

    @depends(fixed_length_recording=(const(None)))
    def __init__(self, fixed_length_recording, *a, **k):
        super(ClipSlotComponent, self).__init__(*a, **k)
        self._create_button = None
        self._double_button = None
        self._fixed_length_recording = fixed_length_recording

    def _color_value(self, slot_or_clip):
        return LIVE_COLOR_INDEX_TO_RGB.get(slot_or_clip.color_index, 0)

    def set_create_button(self, button):
        self._create_button = button

    def set_double_button(self, button):
        self._double_button = button

    def _on_launch_button_pressed(self):
        if is_button_pressed(self._select_button):
            self._do_select_clip(self._clip_slot)
        elif liveobj_valid(self._clip_slot):
            if is_button_pressed(self._duplicate_button):
                self._do_duplicate_clip()
            elif is_button_pressed(self._create_button):
                self._do_create_clip()
            elif is_button_pressed(self._double_button):
                self._do_double_clip()
            elif is_button_pressed(self._delete_button):
                self._do_delete_clip()
            elif self._fixed_length_recording.should_start_recording_in_slot(self._clip_slot):
                self._fixed_length_recording.start_recording_in_slot(self._clip_slot)
            else:
                self._do_launch_clip(True)
                self._show_launched_clip_as_highlighted_clip()
    
    def _do_create_clip(self):
        if self._clip_slot and not self._clip_slot.has_clip:
            ClipCreator().create(self._clip_slot, 8)

    def _do_double_clip(self):
        if self._clip_slot and self._clip_slot.has_clip:
            duplicate_clip_loop(self._clip_slot.clip)

class SceneComponent(SceneComponentBase):
    clip_slot_component_type = ClipSlotComponent

    def _color_value(self, color):
        if liveobj_valid(self._scene):
            return LIVE_COLOR_INDEX_TO_RGB.get(self._scene.color_index, 0)
        return 0

class SessionComponent(SessionComponentBase):
    scene_component_type = SceneComponent
    managed_create_button = ButtonControl(color=u'Session.Duplicate', pressed_color=u'Session.DuplicatePressed')
    managed_double_button = ButtonControl(color=u'Session.Duplicate', pressed_color=u'Session.DuplicatePressed')

    def set_managed_create_button(self, button):
        self.managed_create_button.set_control_element(button)
        self.set_modifier_button(button, u'create', True)
        
    def set_managed_double_button(self, button):
        self.managed_double_button.set_control_element(button)
        self.set_modifier_button(button, u'double', True)

class SessionResetComponent(Component):
    reset_session_ring_button = ButtonControl()

    def __init__(self, session_ring=None, *a, **k):
        super(SessionResetComponent, self).__init__(*a, **k)
        self._session_ring = session_ring

    @reset_session_ring_button.pressed
    def reset_session_ring(self, button):
        track_offset = self._session_ring.track_offset
        scene_offset = self._session_ring.scene_offset

        try:
            selected_track_index = list(self.song.tracks).index(self.song.view.selected_track)
        except ValueError:
            # If this happened then we are probably in a send or master track.
            # Fallback to the last proper track.
            selected_track_index = len(list(self.song.tracks)) - 1

        selected_scene_index = list(self.song.scenes).index(self.song.view.selected_scene)

        self._session_ring.move(selected_track_index - track_offset, selected_scene_index - scene_offset)


