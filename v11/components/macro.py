import Live
from ableton.v2.control_surface import Component
from ableton.v2.control_surface.control.button import ButtonControl
import logging
logger = logging.getLogger(__name__)


def tuple_index(tuple, obj):
    for i in range(0, len(tuple)):
        if tuple[i] == obj:
            return i

class MacroComponent(Component):
    create_audio_button = ButtonControl(color=u'Macro.AudioOff', pressed_color=u'Macro.AudioOn')
    create_midi_button = ButtonControl(color=u'Macro.MidiOff', pressed_color=u'Macro.MidiOn')
    create_drumrack_button = ButtonControl(color=u'Macro.DrumRackOff', pressed_color=u'Macro.DrumRackOn')
    create_simpler_button = ButtonControl(color=u'Macro.SimplerOff', pressed_color=u'Macro.SimplerOn')
    add_compressor_button = ButtonControl(color=u'Macro.CompressorOff', pressed_color=u'Macro.CompressorOn')
    add_eq_button = ButtonControl(color=u'Macro.EqOff', pressed_color=u'Macro.EqOn')
    add_autofilter_button = ButtonControl(color=u'Macro.AutofilterOff', pressed_color=u'Macro.AutofilterOn')
    add_gate_button = ButtonControl(color=u'Macro.GateOff', pressed_color=u'Macro.GateOn')
    add_lfo_button = ButtonControl(color=u'Macro.LfoOff', pressed_color=u'Macro.LfoOn')
    add_eq8_button = ButtonControl(color=u'Macro.Eq8Off', pressed_color=u'Macro.Eq8On')
    add_utility_button = ButtonControl(color=u'Macro.UtilityOff', pressed_color=u'Macro.UtilityOn')
    add_limiter_button = ButtonControl(color=u'Macro.LimiterOff', pressed_color=u'Macro.LimiterOn')
    delete_track_button = ButtonControl(color=u'Macro.DeleteTrackOff', pressed_color=u'Macro.DeleteTrackOn')
    delete_device_button = ButtonControl(color=u'Macro.DeleteDeviceOff', pressed_color=u'Macro.DeleteDeviceOn')
    duplicate_track_button = ButtonControl(color=u'Macro.DuplicateTrackOff', pressed_color=u'Macro.DuplicateTrackOn')
    duplicate_scene_button = ButtonControl(color=u'Macro.DuplicateSceneOff', pressed_color=u'Macro.DuplicateSceneOn')

    def __init__(self, *a, **k):
        super(MacroComponent, self).__init__(*a, **k)
        self.current_item = None
        self._browser = Live.Application.get_application().browser
    
    def _add_device(self, root_folder, name, create_new=False):
        root = getattr(self._browser, root_folder)
        for device in root.children:
            if device.name == name:
                if create_new:
                    self.song.create_midi_track(-1)
                self._browser.load_item(device)
                
    @create_audio_button.pressed
    def _on_create_audio_button_pressed(self, value):
        self.song.create_audio_track(-1)

    @create_midi_button.pressed
    def _on_create_midi_button_pressed(self, value):
        self.song.create_midi_track(-1)

    @create_drumrack_button.pressed
    def _on_create_drumrack_button_pressed(self, value):
        for ins in self._browser.instruments.children:
            if ins.name == 'Drum Rack':
                self.song.create_midi_track(-1)
                self._browser.load_item(ins)

    @create_simpler_button.pressed
    def _on_create_simpler_button_pressed(self, value):
        for ins in self._browser.instruments.children:
            if ins.name == 'Simpler':
                self.song.create_midi_track(-1)
                self._browser.load_item(ins)
    
    @add_compressor_button.pressed
    def _on_add_compressor_button_pressed(self, value):
        self._add_device('audio_effects', 'Compressor')

    @add_eq_button.pressed
    def _on_add_eq_button_pressed(self, value):
        self._add_device('audio_effects', 'EQ Three')
    
    @add_autofilter_button.pressed
    def _on_add_autofilter_button_pressed(self, value):
        self._add_device('audio_effects', 'Auto Filter')
        
    @add_gate_button.pressed
    def _on_add_gate_button_pressed(self, value):
        self._add_device('audio_effects', 'Gate')

    @add_lfo_button.pressed
    def _on_add_lfo_button_pressed(self, value):
        self._add_device('audio_effects', 'LFO')

    @add_eq8_button.pressed
    def _on_add_eq8_button_pressed(self, value):
        self._add_device('audio_effects', 'EQ Eight')

    @add_utility_button.pressed
    def _on_add_utility_button_pressed(self, value):
        self._add_device('audio_effects', 'Utility')

    @add_limiter_button.pressed
    def _on_add_limiter_button_pressed(self, value):
        self._add_device('audio_effects', 'Limiter')

    @delete_track_button.pressed
    def _on_delete_track_button_pressed(self, value):
        tracks = tuple(self.song.visible_tracks) + tuple(self.song.return_tracks)
        track_index = list(tracks).index(self.song.view.selected_track)
        self.song.delete_track(track_index)

    @delete_device_button.pressed
    def _on_delete_device_button_pressed(self, value):
        device = self.song.view.selected_track.view.selected_device
        device_index = list(device.canonical_parent.devices).index(device)
        self.song.view.selected_track.delete_device(device_index)

    @duplicate_track_button.pressed
    def _on_duplicate_track_button_pressed(self, value):
        tracks = tuple(self.song.visible_tracks) + tuple(self.song.return_tracks)
        track_index = list(tracks).index(self.song.view.selected_track)
        self.song.duplicate_track(track_index)

    @duplicate_scene_button.pressed
    def _on_duplicate_track_button_pressed(self, value):
        scene_index = tuple_index(self.song.scenes, self.song.view.selected_scene)
        self.song.duplicate_scene(scene_index)

