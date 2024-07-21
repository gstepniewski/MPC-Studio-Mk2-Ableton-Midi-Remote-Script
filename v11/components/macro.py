import Live
from ableton.v2.control_surface import Component
from ableton.v2.control_surface.control.button import ButtonControl
import logging
logger = logging.getLogger(__name__)

from ..lcd import show_lcd_message_2

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
    add_delay_button = ButtonControl(color=u'Macro.DelayOff', pressed_color=u'Macro.DelayOn')
    add_autofilter_button = ButtonControl(color=u'Macro.AutofilterOff', pressed_color=u'Macro.AutofilterOn')
    add_tuner_button = ButtonControl(color=u'Macro.TunerOff', pressed_color=u'Macro.TunerOn')
    add_reverb_button = ButtonControl(color=u'Macro.ReverbOff', pressed_color=u'Macro.ReverbOn')
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
        show_lcd_message_2("MACRO", "Audio Track")

    @create_midi_button.pressed
    def _on_create_midi_button_pressed(self, value):
        self.song.create_midi_track(-1)
        show_lcd_message_2("MACRO", "Midi Track")

    @create_drumrack_button.pressed
    def _on_create_drumrack_button_pressed(self, value):
        for ins in self._browser.instruments.children:
            if ins.name == 'Drum Rack':
                self.song.create_midi_track(-1)
                self._browser.load_item(ins)
        show_lcd_message_2("MACRO", "Drum Track")

    @create_simpler_button.pressed
    def _on_create_simpler_button_pressed(self, value):
        for ins in self._browser.instruments.children:
            if ins.name == 'Simpler':
                self.song.create_midi_track(-1)
                self._browser.load_item(ins)
        show_lcd_message_2("MACRO", "Simpler Track")
    
    @add_compressor_button.pressed
    def _on_add_compressor_button_pressed(self, value):
        self._add_device('audio_effects', 'Compressor')
        show_lcd_message_2("MACRO", "Compressor")

    @add_delay_button.pressed
    def _on_add_delay_button_pressed(self, value):
        self._add_device('audio_effects', 'Delay')
        show_lcd_message_2("MACRO", "Delay")

    @add_autofilter_button.pressed
    def _on_add_autofilter_button_pressed(self, value):
        self._add_device('audio_effects', 'Auto Filter')
        show_lcd_message_2("MACRO", "Auto Filter")
        
    @add_tuner_button.pressed
    def _on_add_tuner_button_pressed(self, value):
        self._add_device('audio_effects', 'Tuner')
        show_lcd_message_2("MACRO", "Tuner")

    @add_reverb_button.pressed
    def _on_add_reverb_button_pressed(self, value):
        self._add_device('audio_effects', 'Reverb')
        show_lcd_message_2("MACRO", "Reverb")

    @add_eq8_button.pressed
    def _on_add_eq8_button_pressed(self, value):
        self._add_device('audio_effects', 'EQ Eight')
        show_lcd_message_2("MACRO", "EQ Eight")

    @add_utility_button.pressed
    def _on_add_utility_button_pressed(self, value):
        self._add_device('audio_effects', 'Utility')
        show_lcd_message_2("MACRO", "Utility")

    @add_limiter_button.pressed
    def _on_add_limiter_button_pressed(self, value):
        self._add_device('audio_effects', 'Limiter')
        show_lcd_message_2("MACRO", "Limiter")

    @delete_track_button.pressed
    def _on_delete_track_button_pressed(self, value):
        tracks = tuple(self.song.visible_tracks) + tuple(self.song.return_tracks)
        track_index = list(tracks).index(self.song.view.selected_track)
        self.song.delete_track(track_index)
        show_lcd_message_2("MACRO", "Delete Track")

    @delete_device_button.pressed
    def _on_delete_device_button_pressed(self, value):
        device = self.song.view.selected_track.view.selected_device
        device_index = list(device.canonical_parent.devices).index(device)
        self.song.view.selected_track.delete_device(device_index)
        show_lcd_message_2("MACRO", "Delete Device")

    @duplicate_track_button.pressed
    def _on_duplicate_track_button_pressed(self, value):
        tracks = tuple(self.song.visible_tracks) + tuple(self.song.return_tracks)
        track_index = list(tracks).index(self.song.view.selected_track)
        self.song.duplicate_track(track_index)
        show_lcd_message_2("MACRO", "Dup Track")

    @duplicate_scene_button.pressed
    def _on_duplicate_track_button_pressed(self, value):
        scene_index = tuple_index(self.song.scenes, self.song.view.selected_scene)
        self.song.duplicate_scene(scene_index)
        show_lcd_message_2("MACRO", "Dup Scene")

