from __future__ import absolute_import, print_function, unicode_literals
import re
import Live
from ableton.v2.base import liveobj_valid, listens, task
from ableton.v2.control_surface.components import ChannelStripComponent as ChannelStripComponentBase
from ableton.v2.control_surface import ControlElement
import logging
logger = logging.getLogger(__name__)

TOTAL_LEDS = 9
TC_LIGHT_MAPPING = {
    0: 57,
    1: 58,
    2: 59,
    3: 60,
    4: 61,
    5: 62,
    6: 63,
    7: 64,
    8: 65
}

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
        self._meter_values = list(self._clear_values)
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

class TouchStrip(ChannelStripComponentBase):
    def __init__(self, *a, **k):
        self.touch_strip_button = None
        super(TouchStrip, self).__init__(*a, **k)
        self.meter_display = MeterDisplayElement(TC_LIGHT_MAPPING, TOTAL_LEDS)
        self._update_listeners()
    
    def set_track(self, track):
        super(TouchStrip, self).set_track(track)
        self._update_volume_listener()
        self._update_pan_listener()
        self._update_output_meter_listeners()
        self._update_track_devices_listeners(track)
    

    def _update_track_devices_listeners(self, track):
        self.__on_devices_changed.subject = self.song.view

    def _update_output_meter_listeners(self):
        track = self._track
        subject = track if liveobj_valid(track) and track.has_audio_output else None
        self.__on_output_meter_left_changed.subject = subject
        if liveobj_valid(subject):
            self.__on_output_meter_left_changed()

    def _update_listeners(self):
        self._update_volume_listener()
        self._update_pan_listener()
        self.__on_selected_track_changed.subject = self.song.view
        self.__on_selected_track_changed()
        self.__on_volume_changed()
        self._update_output_meter_listeners()

    def _update_volume_listener(self):
        track = self._track
        self.__on_volume_changed.subject = track.mixer_device.volume if liveobj_valid(track) else None
        self.__on_volume_changed()
    
    def _update_pan_listener(self):
        track = self._track
        self.__on_pan_changed.subject = track.mixer_device.panning if liveobj_valid(track) else None
        self.__on_pan_changed()
    
    def _update_vol_meter(self, volume=None):
        track = self._track
        if liveobj_valid(track) and track.has_audio_output:
            if volume is None:
                volume_value = str(track.mixer_device.volume.value)
                self.meter_display.update_volume_meter_display(volume=volume_value)
            else:
                self.meter_display.update_volume_meter_display(volume=volume)
        else:
            self.meter_display.update_volume_meter_display(0)
    
    @listens(u'selected_track')
    def __on_selected_track_changed(self):
        selected_track = self.song.view.selected_track
        if selected_track != self.song.master_track:
            self.set_track(selected_track)
        else:
            self.set_track(None)

    @listens(u'output_meter_left')
    def __on_output_meter_left_changed(self):
        volume_level =  self.track.output_meter_left
        if self._volume_control is None and self._pan_control is None:
            if float(volume_level) >= float(.01):
                self._update_vol_meter(volume=volume_level)
            else:
                self._update_vol_meter()

    @listens(u'value')
    def __on_volume_changed(self):
        self._update_vol_meter()
            
    
    @listens(u'value')
    def __on_pan_changed(self):
        track = self._track
        if liveobj_valid(track) and track.has_audio_output:
            panning_value = str(track.mixer_device.panning.value)
            self.meter_display.update_pan_meter_display(panning_value)

    @listens(u'selected_track.devices')
    def __on_devices_changed(self):
        self._update_volume_listener()
        self._update_pan_listener()
        self._update_output_meter_listeners()
    
    def disconnect(self):
        self._update_vol_meter(0)
        super(TouchStrip, self).disconnect()
    
    def set_send_a_control(self, control):
        self._set_send_control(control, 0)

    def set_send_b_control(self, control):
        self._set_send_control(control, 1)

    def _set_send_control(self, control, send_index):
        if control:
            self.set_send_controls((None,) * send_index + (control,))
        else:
            self.set_send_controls(None)
