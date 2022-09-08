from ableton.v2.base import task
from ableton.v2.control_surface import ControlElement
from ..CONST import REPEAT_LIGHT_MAPPING

class RepeatDisplayElement(ControlElement):

    def __init__(self, repeat_light_mapping=REPEAT_LIGHT_MAPPING, unselected_value=8, selected_value=127, off_value=0, *a, **k):
        super(RepeatDisplayElement, self).__init__(*a, **k)
        self._repeat_light_mapping = repeat_light_mapping
        self.unselected_value = unselected_value
        self.selected_value = selected_value
        self.off_value = off_value
        self.led_values = None
        self._last_sent_message = None
        self._send_message_task = self._tasks.add(task.run(self._send_message))
        self._send_message_task.kill()

    def generate_repeat_display_values(self, value):
        value = int(value) if value != '' else None
        selected_index = value // 16 if value else None
        light_cc_mapping = []
        for light in self._repeat_light_mapping:
            if value:
                cc_value = self.selected_value if light == selected_index else self.unselected_value
                light_cc_mapping.append((light, cc_value))
            else:
                light_cc_mapping.append((light, self.off_value))
        return light_cc_mapping

    def generate_repeat_display_values_by_index(self, index):
        light_cc_mapping = []
        for light in self._repeat_light_mapping:
            cc_value = self.selected_value if light == int(index) else self.unselected_value
            light_cc_mapping.append((light, cc_value))
        return light_cc_mapping

    def update_repeat_display_cc(self, cc_value):
        self.led_values = self.generate_repeat_display_values(cc_value)
        self._request_send_message()

    def update_repeat_display_index(self, index):
        self.led_values = self.generate_repeat_display_values_by_index(index)
        self._request_send_message()

    def reset(self):
        self.led_values = self.generate_repeat_display_values('')
        self._request_send_message()

    def send_midi(self, midi_bytes):
        if midi_bytes != self._last_sent_message:
            super(RepeatDisplayElement, self).send_midi(midi_bytes)
            self._last_sent_message = midi_bytes

    def _request_send_message(self):
        self._send_message_task.restart()

    def _send_message(self, *a):
        for led in self.led_values:
            self.send_midi( ( 176, self._repeat_light_mapping[led[0]], led[1] ) )