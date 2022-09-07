import Live
from ableton.v2.control_surface import Component
from ableton.v2.control_surface.control.button import ButtonControl
import logging
logger = logging.getLogger(__name__)

class MacroComponent(Component):
    create_audio_button = ButtonControl(color=u'Macro.AudioOff', pressed_color=u'Macro.AudioOn')
    create_midi_button = ButtonControl(color=u'Macro.MidiOff', pressed_color=u'Macro.MidiOn')
    create_drumrack_button = ButtonControl(color=u'Macro.DrumRackOff', pressed_color=u'Macro.DrumRackOn')
    create_simpler_button = ButtonControl(color=u'Macro.SimplerOff', pressed_color=u'Macro.SimplerOn')
    add_compressor_button = ButtonControl(color=u'Macro.CompressorOff', pressed_color=u'Macro.CompressorOn')
    add_eq_button = ButtonControl(color=u'Macro.EqOff', pressed_color=u'Macro.EqOn')
    add_autofilter_button = ButtonControl(color=u'Macro.AutofilterOff', pressed_color=u'Macro.AutofilterOn')
    add_gate_button = ButtonControl(color=u'Macro.GateOff', pressed_color=u'Macro.GateOn')

    def __init__(self, *a, **k):
        super(MacroComponent, self).__init__(*a, **k)
        self.current_item = None
        self._browser = Live.Application.get_application().browser
    
    def _add_device(self, root_folder, sub_category, name, create_new=False):
        root = getattr(self._browser, root_folder)
        logger.warning(type(root.children))
        for folder in root.children:
            if folder.name == sub_category:
                for device in folder.children:
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
        self._add_device('audio_effects', 'Dynamics', 'Compressor')

    @add_eq_button.pressed
    def _on_add_eq_button_pressed(self, value):
        self._add_device('audio_effects', 'EQ & Filters', 'EQ Three')
    
    @add_autofilter_button.pressed
    def _on_add_autofilter_button_pressed(self, value):
        self._add_device('audio_effects', 'EQ & Filters', 'Auto Filter')
        
    
    @add_gate_button.pressed
    def _on_add_gate_button_pressed(self, value):
        self._add_device('audio_effects', 'Dynamics', 'Gate')
    