from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.components import ToggleComponent, TransportComponent as TransportComponentBase

def MetronomeButtonViewTransform( value):
    return u'Transport.MetronomeOn' if value else u'Transport.MetronomeOff'

class TransportComponent(TransportComponentBase):
    def __init__(self, *a, **k):
        super(TransportComponent, self).__init__(*a, **k)
        self.play_button.disabled_color='DefaultButton.Off'
        self._metronome_toggle = ToggleComponent(u'metronome', self.song, parent=self, view_transform=MetronomeButtonViewTransform)
        self.tap_tempo_button.pressed_color = u'DefaultButton.Selected'
    
    def _update_stop_button_color(self):
        self.stop_button.color = self.play_button.untoggled_color if self.play_button.is_toggled else self.play_button.toggled_color

    def set_seek_forward_button(self, ffwd_button):
        super(TransportComponent, self).set_seek_forward_button(ffwd_button)
        self._update_seek_button(self._ffwd_button)

    def set_seek_backward_button(self, rwd_button):
        super(TransportComponent, self).set_seek_backward_button(rwd_button)
        self._update_seek_button(self._rwd_button)
    
    def _update_seek_button(self, button):
        if self.is_enabled() and button != None:
            button.set_light(u'Transport.SeekOn' if button.is_pressed() else u'Transport.SeekOff')

    def _ffwd_value(self, value):
        super(TransportComponent, self)._ffwd_value(value)
        self._update_seek_button(self._ffwd_button)

    def _rwd_value(self, value):
        super(TransportComponent, self)._rwd_value(value)
        self._update_seek_button(self._rwd_button)