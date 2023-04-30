#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/ATOM/keyboard.py
from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.components import PlayableComponent, ScrollComponent
from ableton.v2.control_surface.control import ToggleButtonControl, ButtonControl
from .note_pad import NotePadMixin

MAX_START_NOTE = 108
SHARP_INDICES = (1, 3, 4, 6, 10, 13, 15)

ALTERNATE_MODE_COLORS = (
    'Sharp', 'Sharp', 'Sharp', 'Off',
    'Natural', 'Natural', 'Natural', 'Natural',
    'Off', 'Sharp', 'Sharp', 'Off',
    'Natural', 'Natural', 'Natural', 'Natural'
)

ALTERNATE_MODE_MAPPING = (
    0, 2, 4, 5,
    None, 1, 3, None,
    7, 9, 11, 12,
    6, 8, 10, None,
)


class KeyboardComponent(NotePadMixin, PlayableComponent, ScrollComponent):
    alternate_mode_button = ToggleButtonControl(toggled_color='DefaultButton.On', untoggled_color='DefaultButton.Off')
    pad_mute_button = ButtonControl(color = 'DefaultButton.Disabled', pressed_color='Default.Button.Disabled')

    def __init__(self, translation_channel, *a, **k):
        self._translation_channel = translation_channel
        self._alternate_mode = False
        self._start_note = 60
        super(KeyboardComponent, self).__init__(*a, **k)

    @alternate_mode_button.toggled
    def alternate_mode_toggled(self, is_toggled, _):
        self._alternate_mode = is_toggled
        self._update_note_translations()
        self._update_led_feedback()
        self._release_all_pads()

    def can_scroll_up(self):
        return self._start_note < MAX_START_NOTE

    def can_scroll_down(self):
        return self._start_note > 0

    def scroll_up(self):
        if self.can_scroll_up():
            self._move_start_note(12)

    def scroll_down(self):
        if self.can_scroll_down():
            self._move_start_note(-12)

    def _move_start_note(self, factor):
        self._start_note += factor
        self._update_note_translations()
        self._update_led_feedback()
        self._release_all_pads()

    def _update_button_color(self, button):
        if self._alternate_mode:
            button.color = u'Keyboard.{}'.format(ALTERNATE_MODE_COLORS[button.index])
        else:
            button.color = u'Keyboard.{}'.format(u'Sharp' if button.index in SHARP_INDICES else u'Natural')

    def _note_translation_for_button(self, button):
        row, column = button.coordinate
        inverted_row = self.matrix.height - row - 1
        note_index = inverted_row * self.matrix.width + column
        if self._alternate_mode:
            offset = ALTERNATE_MODE_MAPPING[note_index]
            if offset is None:
                return note_index, self._translation_channel
            else:
                return self._start_note + offset, self._translation_channel
        else:
            return note_index + self._start_note, self._translation_channel

    def _release_all_pads(self):
        for pad in self.matrix:
            if pad.is_pressed:
                pad._release_button()
