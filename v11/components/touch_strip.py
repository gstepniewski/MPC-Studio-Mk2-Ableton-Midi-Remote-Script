from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import liveobj_valid, listens
from ableton.v2.control_surface.components import ChannelStripComponent as ChannelStripComponentBase
from ..elements.meter_display_element import MeterDisplayElement
from ..CONST import TC_LIGHT_MAPPING, TOTAL_LEDS

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
