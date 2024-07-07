from ableton.v2.base import listens, liveobj_valid
from ableton.v2.control_surface import Component
from ableton.v2.control_surface.components import ChannelStripComponent
from ableton.v2.control_surface.control.button import ButtonControl

import Live

import logging
logger = logging.getLogger(__name__)

def reset_button(button):
    if button != None:
        button.reset()


class TrackNavigationComponent(Component):
    jog_wheel_button = ButtonControl()
    arm_button = ButtonControl()
    shift_button = ButtonControl()
    tempo_button = ButtonControl()

    def __init__(self, *a, **k):
        super(TrackNavigationComponent, self).__init__(*a, **k)
        self._track = None
        self._arm_pressed = False
        self._shift_pressed = False
        self._arm_button = None
        self.__on_selected_track_changed()
        self.__on_selected_track_changed.subject = self.song.view
        self.__on_selected_chain_changed()
        self.__on_selected_chain_changed.subject = self.song.view
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
        # ChannelStripComponent._active_instances.remove(self)
        reset_button(self._arm_button)
        self._arm_button = None
        super(TrackNavigationComponent, self).disconnect()

    def _arm_value(self, value):
        if self.is_enabled():
            if value and self.shift_button.is_pressed:
                if self._track and self._track.can_show_chains:
                    self._track.is_showing_chains = not self._track.is_showing_chains
                elif self._track and self._track.is_foldable:
                    self._track.fold_state = not self._track.fold_state
            elif liveobj_valid(self._track) and self._track.can_be_armed:
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
    def scroll_wheel(self, x, _):
        if self.tempo_button.is_pressed:
            self._adjust_tempo(x)
        elif self.shift_button.is_pressed:
            if x == 1 and self._can_select_next_scene():
                self._select_next_scene()
            if x == 127 and self._can_select_prev_scene():
                self._select_prev_scene()
        else:
            if x == 1 and self._can_scroll_forward():
                self._move_selection(1)
            if x == 127 and self._can_scroll_back():
                self._move_selection(-1)

    # ################# HORIZONTAL SCROLLING START ################# #
    
    def all_tracks(self):
        return self.tracks_to_use() + (self.song.master_track,)

    def tracks_to_use(self):
        return tuple(self.song.visible_tracks) + tuple(self.song.return_tracks)

    def _move_selection(self, delta):
        if self._chain:
            chain_parent = self._chain.canonical_parent
            if isinstance(chain_parent, Live.RackDevice.RackDevice):
                self._scroll_rack_chain(delta)
            else:
                # Unsupported, fallback to scrolling tracks
                self._scroll_track(delta)
        else:
            self._scroll_track(delta)

    def _can_scroll_back(self):
        return (self.song.view.selected_track != self.song.tracks[0]) or (
                    self.song.view.selected_track == self.song.tracks[0] and self._chain)

    def _can_scroll_forward(self):
        return self.song.view.selected_track != self.song.master_track

    def _scroll_rack_chain(self, delta):
        chain_parent = self._chain.canonical_parent
        chain_index = list(chain_parent.chains).index(self._chain)
        # First chain going left
        if delta == -1 and chain_index == 0 and self._can_scroll_back():
            self._scroll_track(0)
        # Last chain going right
        elif delta == 1 and chain_index == len(chain_parent.chains) - 1 and self._can_scroll_forward():
            self._scroll_track(1)
        # Middle of chain
        else:
            new_chain = chain_parent.chains[chain_index + delta]
            self.song.view.selected_chain = new_chain
            chain_parent.view.selected_chain = new_chain

    def _scroll_track(self, delta):
        all_tracks = self.all_tracks()
        track_index = list(all_tracks).index(self._track)
        target_track = all_tracks[track_index + delta]

        # Scrolling right into an open chain
        if delta == 1 and self._track.can_show_chains and self._track.is_showing_chains and self._chain is None:
            rack_device = self._find_rack_with_chains(self._track.devices)
            if rack_device is not None:
                self.song.view.selected_chain = rack_device.chains[0]
                rack_device.view.selected_chain = rack_device.chains[0]
            else:
                logger.warning("This should not happen, showing chains but can't show chains?")
                self.song.view.selected_track = target_track
        # Scrolling left into an open chain
        elif delta == -1 and target_track.can_show_chains and target_track.is_showing_chains:
            rack_device = self._find_rack_with_chains(target_track.devices)
            if rack_device is not None:
                target_chain = rack_device.chains[len(rack_device.chains) - 1]
                self.song.view.selected_chain = target_chain
                rack_device.view.selected_chain = target_chain
            else:
                logger.warning("This should not happen, showing chains but can't show chains?")
                self.song.view.selected_track = target_track
        # Just scrolling tracks
        else:
            self.song.view.selected_track = target_track

    def _find_rack_with_chains(self, devices):
        for device in devices:
            if isinstance(device, Live.RackDevice.RackDevice) and device.can_show_chains:
                return device
        return None

    @listens(u'selected_chain')
    def __on_selected_chain_changed(self):
        self._chain = self.song.view.selected_chain

    @listens(u'selected_track')
    def __on_selected_track_changed(self):
        self._track = self.song.view.selected_track

    # ################# HORIZONTAL SCROLLING END ################# #

    def selected_scene_index(self):
        def tuple_index(tuple, obj):
            for i in range(0, len(tuple)):
                if tuple[i] == obj:
                    return i

        return tuple_index(self.song.scenes, self.song.view.selected_scene)

    def _can_select_prev_scene(self):
        return self.selected_scene_index() > 0

    def _can_select_next_scene(self):
        return (len(self.song.scenes) - self.selected_scene_index()) > 1

    def _select_prev_scene(self):
        index = self.selected_scene_index() - 1
        self.song.view.selected_scene = self.song.scenes[index]

    def _select_next_scene(self):
        index = self.selected_scene_index() + 1
        self.song.view.selected_scene = self.song.scenes[index]

    def _adjust_tempo(self, x):
        factor = 1 if x == 1 else -1
        self.song.tempo = max(min(int(self.song.tempo) + factor, 999), 20)
