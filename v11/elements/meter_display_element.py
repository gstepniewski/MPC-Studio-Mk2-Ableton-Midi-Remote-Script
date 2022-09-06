from ableton.v2.base import task
from ableton.v2.control_surface import ControlElement

class MeterDisplayElement(ControlElement):

    def __init__(self, segment_cc_map, num_segments, *a, **k):
        super(MeterDisplayElement, self).__init__(*a, **k)
        self._segment_cc_map = segment_cc_map
        self.num_segments = num_segments
        self.led_values = None
        self._last_sent_message = None
        self._send_message_task = self._tasks.add(task.run(self._send_message))
        self._send_message_task.kill()

    # This function generates the necessary cc values for the 9 touch_strip_leds.
    # It is specific for pan values from -1.0 - 1.0 and will generate a List of tuples with the first item
    # in the tuple being the led index and the second being the CC value.
    def generate_pan_meter_led_values(self, volume):
        volume = float(volume) if volume != None else float(0)
        is_positive = False if float(volume) < 0 else True
        vector = 1 if is_positive else -1
        half = self.num_segments // 2
        has_middle = True if self.num_segments % 2 != 0 else False
        led_unit_value = float( round( ( float(1) / float(half) ) , 4) )
        full_led = abs(int( volume // led_unit_value ))
        partial_led_unit_value = round( volume % led_unit_value, 4 ) 
        partial_led = int(round( 127 * (partial_led_unit_value / led_unit_value)) )
        shift = half
        if is_positive and has_middle:
            shift +=1
        if not is_positive:
            shift -= 1
        leds = {}
        for x in range(full_led + 1):
            if x < (full_led):
                leds[x*vector + shift] = 127
            if x == full_led-1 and partial_led != 0 :
                leds[x*vector + shift]=  partial_led
        led_cc_values = []
        for y in range(self.num_segments):
            if y in leds:
                led_cc_values.append((y, leds[y]))
            else:
                if y == half and has_middle:
                    led_cc_values.append((y, 127))
                else:
                    led_cc_values.append((y, 0))
        return led_cc_values

    # This function generates the necessary cc values for the 9 touch_strip_leds.
    # It accepts a float from 0.0 - 1.0 and will generate a List of tuples with the first item
    # in the tuple being the led index and the second being the CC value
    def generate_led_meter_values(self, volume):

        # Filter out bad input for volume. Volume show be between 0 and 1
        if float(volume) > 1 or float(volume) < 0:
            led_cc_values = []
            for led in range(self.num_segments):
                led_cc_values.append( (led, 0) )
            return led_cc_values
        else:
            volume = float(volume) if volume != None else float(0)
            led_unit_value = float( round( ( float(1) / float(self.num_segments) ) , 4) )
            full_led_number = int( volume // led_unit_value )
            partial_led_unit_value = round( volume % led_unit_value, 4 )
            led_cc_values = []
            for led in range(self.num_segments):
                if led < full_led_number:
                    led_cc_values.append( (led, 127) )
                if led == full_led_number:
                    cc_value = round( 127 * (partial_led_unit_value / led_unit_value) )
                    led_cc_values.append( (led, int(cc_value)) )
                if led > full_led_number:
                    led_cc_values.append(( led, 0) )
            return led_cc_values
    
    def update_volume_meter_display(self, volume):
        self.led_values = self.generate_led_meter_values(volume)
        self._request_send_message()

    def update_pan_meter_display(self, pan):
        self.led_values = self.generate_pan_meter_led_values(pan)
        self._request_send_message()

    def reset(self):
        self.led_values = self.generate_led_meter_values(0)
        self._request_send_message()

    def send_midi(self, midi_bytes):
        if midi_bytes != self._last_sent_message:
            super(MeterDisplayElement, self).send_midi(midi_bytes)
            self._last_sent_message = midi_bytes

    def _request_send_message(self):
        self._send_message_task.restart()

    def _send_message(self, *a):
        for led in self.led_values:
            self.send_midi( ( 176, self._segment_cc_map[led[0]], led[1] ) )
    def reset(self):
        for key in self._segment_cc_map:
            self.send_midi( ( 176, self._segment_cc_map[key], 0 ) )