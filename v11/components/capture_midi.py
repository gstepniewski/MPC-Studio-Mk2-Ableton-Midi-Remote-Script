#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ATOM/note_pad.py
import Live
from ableton.v2.base import listens
from ableton.v2.control_surface import Component
from ableton.v2.control_surface.control.button import ButtonControl


class CaptureMidiCompnent(Component):
    capture_midi_button = ButtonControl()

    def __init__(self, *a, **k):
        super(CaptureMidiCompnent, self).__init__(*a, **k)
        self.__on_can_capture_midi_changed.subject = self.song
        self.__on_can_capture_midi_changed()

    @capture_midi_button.pressed
    def capture_midi_button(self, _):
        if self.song.can_capture_midi:
            self.song.capture_midi()

    @listens('can_capture_midi')
    def __on_can_capture_midi_changed(self):
        self.capture_midi_button.color = 'DefaultButton.On' if self.song.can_capture_midi else 'DefaultButton.Disabled'
