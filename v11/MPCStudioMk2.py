from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.base import const, inject, listens, liveobj_valid, task, lazy_attribute, depends
from ableton.v2.control_surface import ControlSurface, Layer, PercussionInstrumentFinder
from ableton.v2.control_surface.components import ArmedTargetTrackComponent, BackgroundComponent, AccentComponent, SessionNavigationComponent, SessionOverviewComponent, SessionRingComponent, SimpleTrackAssigner, AutoArmComponent
from ableton.v2.control_surface.mode import AddLayerMode, LayerMode, ModesComponent, MomentaryBehaviour
from ableton.v2.control_surface.control.button import ButtonControl
from .elements.mpc_elements import MPCButtonElement
from . import midi
from .components.channel_strip import ChannelStripComponent
from .components.drum_group import DrumGroupComponent
from .elements.elements import Elements, SESSION_HEIGHT, SESSION_WIDTH
from .components.keyboard import KeyboardComponent
from .components.lighting import LightingComponent
from .components.mixer import MixerComponent
from .components.session import SessionComponent, SessionResetComponent
from .skin import skin
from .components.view_toggle import ViewToggleComponent
from .components.undo import  NewUndoComponent
from .components.jog_wheel import TrackSelectComponent
from .components.transport import TransportComponent
from .components.touch_strip import TouchStrip
from .components.session_recording import SessionRecordingComponent
from .components.clip_actions import ClipActionsComponent
from .components.quantization import QuantizationComponent
from .components.browser import BrowserComponent
from .components.note_repeat import NoteRepeatEnabler
from .components.track_navigation import TrackNavigationComponent
from .components.macro import MacroComponent
from .components.device_navigation import DeviceNavigationComponent
from .elements.repeat_display_element import RepeatDisplayElement
from .components.routing_component import RoutingComponent

import logging
logger = logging.getLogger(__name__)

class MPCStudioMk2(ControlSurface):

    def __init__(self, *a, **k):
        (super(MPCStudioMk2, self).__init__)(*a, **k)
            
        with self.component_guard():
            with inject(skin=(const(skin))).everywhere():
                self._elements = Elements()
        with self.component_guard():
            with inject(element_container=(const(self._elements))).everywhere():
                self._repeat_display_element = RepeatDisplayElement()
                self._create_note_repeat()
                self._set_button_colors()
                self._create_lighting()
                self._create_undo()
                self._create_view_toggle()
                self._create_background()
                self._create_navigation_modes()
                self._create_auto_arm()
                self._create_session()
                self._create_session_ring_reset()
                self._create_touch_strip()
                self._create_touch_strip_modes()
                self._create_mixer()
                self._create_session_navigation_modes()
                self._create_keyboard()
                self._create_drum_group()
                self._create_note_modes()
                self._create_routing_component()
                self._create_channel_modes()
                self._create_macro()
                self._create_pad_modes()
                self._create_transport()
                self._create_record_modes()
                self._create_clip_actions()
                self._create_quantization()
                self._target_track = ArmedTargetTrackComponent(name='Target_Track')
                self.__on_target_track_changed.subject = self._target_track
        self._drum_group_finder = self.register_disconnectable(PercussionInstrumentFinder(device_parent=(self._target_track.target_track)))
        self.set_feedback_channels([9])

        # Setup Listens 
        # self.__on_session_record_changed.subject = self.song
        # self._set_feedback_velocity()
        # self.__on_armed_tracks_changed.subject = self._target_track
        self.__on_drum_group_changed.subject = self._drum_group_finder
        self.__on_drum_group_changed()
        self.__on_main_view_changed.subject = self.application.view
        self._enable_session_ring()
        self.__on_selected_mode_change.subject = self._pad_modes
        self.show_message('---MPC Studio Mk2: Active')

    def _set_button_colors(self):
        self._elements.sample_start_button.color = 'UpDownButton.Off'

    def disconnect(self):
        super(MPCStudioMk2, self).disconnect()
        self._set_pad_led_disabled()
        self._touch_strip.meter_display.reset()
        self._repeat_display_element.blackout()
        for e in dir(self._elements):
            if isinstance(e, MPCButtonElement):
                e.blackout()
        logger.warning('Goodbye')
    
    def _create_note_repeat(self):
        self._note_repeat_enabler = NoteRepeatEnabler(note_repeat=(self._c_instance.note_repeat))
        self._note_repeat_enabler.set_enabled(False)
        self._note_repeat_enabler.layer = Layer(repeat_button='note_repeat_button')
        self._note_repeat_enabler.note_repeat_component.layer = self._create_note_repeat_layer()

    def _create_note_repeat_layer(self):
        return Layer(
            # aftertouch_control='aftertouch_control',
            select_buttons='pads_with_zoom',
            rate_control='touch_strip_control',
            priority=2)

    def _create_auto_arm(self):
        self._auto_arm = AutoArmComponent(is_enabled=False)
        self._auto_arm.set_enabled(True)

    def _create_macro(self):
        self._macro = MacroComponent(name='Macro', is_enabled=False)
        self._macro.set_enabled(True)

    def _create_routing_component(self):
        self._routing_component = RoutingComponent(name='routing', is_enabled=False)
        self._routing_component.set_enabled(True)

    def _create_lighting(self):
        self._lighting = LightingComponent(name='Lighting',
          is_enabled=False,
          layer=Layer(shift_button='shift_button', zoom_button='zoom_button'))
        self._lighting.set_enabled(True)

    def _create_transport(self):
        self._transport = TransportComponent(name='Transport',
          is_enabled=False,
          layer=Layer(priority=5, 
          play_button='play_button',
          loop_button='play_start_button',
          stop_button='stop_button',
          metronome_button='tune_button',
          tap_tempo_button='tap_tempo_button'))
        self._transport.set_enabled(True)
        self._transport.set_seek_forward_button(self._elements.seek_forward_button)
        self._transport.set_seek_backward_button(self._elements.seek_back_button)
        self._transport.set_arrangement_overdub_button(self._elements.overdub_button)
        self._transport.set_punch_in_button(self._elements.nudge_left_button)
        self._transport.set_punch_out_button(self._elements.nudge_right_button)

    def _create_record_modes(self):
        self._session_record = SessionRecordingComponent(name='Session_Record',
          is_enabled=False,
          layer=Layer(record_button='record_button',
          automation_button='automation_rw_button'))
        self._record_modes = ModesComponent(name='Record_Modes')
        self._record_modes.add_mode('session', self._session_record)
        self._record_modes.add_mode('arrange', AddLayerMode((self._transport), layer=Layer(record_button='record_button')))
        self.__on_main_view_changed()

    def _create_undo(self):
        self._undo = NewUndoComponent(name='Undo',
          is_enabled=False,
          layer=Layer(undo_button='undo_button', redo_button='undo_button_with_shift'))
        self._undo.set_enabled(True)

    def _create_clip_actions(self):
        self._clip_actions = ClipActionsComponent(name=u'Clip_Actions', is_enabled=False, layer=Layer(quantize_button=u'quantize_button'))
        self._clip_actions.set_enabled(True)

    def _create_quantization(self):
        self._quantize_toggle = QuantizationComponent(name=u'Quantization_Component', is_enabled=False, layer=Layer(quantization_toggle_button=u'tc_on_off_Button'))
        self._quantize_toggle.set_enabled(True)

    def _create_view_toggle(self):
        self._view_toggle = ViewToggleComponent(name='View_Toggle',
          is_enabled=False,
          layer=Layer(
            detail_view_toggle_button='locate_button',
            main_view_toggle_button='main_button',
            browser_view_toggle_button='browse_button',
            clip_detail_view_toggle_button='locate_button_with_shift'
          ))
        self._view_toggle.set_enabled(True)

    def _create_background(self):
        self._background = BackgroundComponent(name='Background',
          is_enabled=False,
          add_nop_listeners=True,
          layer=Layer(
            set_note_repeat_button='note_repeat_button',
            set_pad_bank_dh_button='pad_bank_dh_button',
            set_full_level_button='full_level_button',
            set_level_16_button='level_16_button',
            set_erase_button='erase_button',
            set_copy_button='copy_button'
          ))
        self._background.set_enabled(True)

    def _create_session(self):
        self._session_ring = SessionRingComponent(name='Session_Ring',
          is_enabled=False,
          num_tracks=SESSION_WIDTH,
          num_scenes=SESSION_HEIGHT)
        self._session = SessionComponent(name='Session', session_ring=self._session_ring)

        self._session_navigation = SessionNavigationComponent(name='Session_Navigation',
          is_enabled=False,
          session_ring=self._session_ring,
          layer=Layer(left_button='minus_button', right_button='plus_button', up_button='sample_start_button', down_button='sample_end_button'))

        self._session_navigation.set_enabled(True)

        self._session_overview = SessionOverviewComponent(name='Session_Overview',
          is_enabled=False,
          session_ring=self._session_ring,
          enable_skinning=True,
          layer=Layer(button_matrix='pads_with_zoom'))

    def _create_session_ring_reset(self):
        self._session_ring_reset = SessionResetComponent(
            name='SessionRingReset',
            session_ring=self._session_ring,
            is_enabled=False,
            layer=Layer(reset_session_ring_button='zoom_button_with_shift')
        )
        self._session_ring_reset.set_enabled(True)

    def _create_touch_strip(self):
        self._touch_strip = TouchStrip(is_enabled=True)

    def _create_mixer(self):
        self._mixer = MixerComponent(name='Mixer',
          auto_name=True,
          tracks_provider=(self._session_ring),
          track_assigner=(SimpleTrackAssigner()),
          invert_mute_feedback=True,
          channel_strip_component_type=ChannelStripComponent)

    def _create_touch_strip_modes(self):
        self._touch_strip_modes = ModesComponent(name='touch_strip_modes', enable_skinning=True)
        self._touch_strip_modes.add_mode('volume', AddLayerMode(self._touch_strip, Layer(volume_control='touch_strip_control')))
        self._touch_strip_modes.add_mode('pan', AddLayerMode(self._touch_strip, Layer(pan_control='touch_strip_control')))
        self._touch_strip_modes.add_mode('send_a', AddLayerMode(self._touch_strip, Layer(send_a_control='touch_strip_control')))
        self._touch_strip_modes.add_mode('send_b', AddLayerMode(self._touch_strip, Layer(send_b_control='touch_strip_control')))
        self._touch_strip_modes.selected_mode = 'volume'
    
    def _create_navigation_modes(self):
        self._navigation_modes = ModesComponent(name='Navigation_Modes', is_enabled=False, layer=Layer(
            track_button='track_select_button',
            device_button='program_select_button'
        ))
        self._navigation_modes.add_mode('track', AddLayerMode(TrackNavigationComponent(), Layer(
                jog_wheel_button='jog_wheel',
                arm_button='jog_wheel_button',
                shift_button='shift_button')))
        self._navigation_modes.add_mode('device', AddLayerMode(DeviceNavigationComponent(), Layer(
                jog_wheel_button='jog_wheel',
                jog_wheel_press='jog_wheel_button',
                shift_button='shift_button')))
        self._navigation_modes.selected_mode = 'track'
        self._navigation_modes.set_enabled(True)
        self._on__navigation_modes_changed.subject = self._navigation_modes
    
    @listens(u'selected_mode')
    def _on__navigation_modes_changed(self, mode):
        if mode == 'track':
            self.application.view.focus_view(u'Session')
        if mode == 'device':
            self.application.view.focus_view(u'Detail')

    def _create_session_navigation_modes(self):
        self._session_navigation_modes = ModesComponent(name='Session_Navigation_Modes',
          is_enabled=False,
          layer=Layer(cycle_mode_button='sample_select_button'))

        self._session_navigation_modes.add_mode('default',
            AddLayerMode((self._session_navigation),
                layer=Layer(up_button='sample_start_button', down_button='sample_end_button')),
                cycle_mode_button_color='DefaultButton.Off')

        self._session_navigation_modes.add_mode('paged',
            AddLayerMode((self._session_navigation),
                layer=Layer(page_up_button='sample_start_button',
                page_down_button='sample_end_button',
                page_left_button='minus_button',
                page_right_button='plus_button')),
                cycle_mode_button_color='DefaultButton.On')
        self._session_navigation_modes.selected_mode = 'default'

    def _create_keyboard(self):
        self._keyboard = KeyboardComponent((midi.KEYBOARD_CHANNEL),
          name='Keyboard',
          is_enabled=False,
          layer=Layer(matrix='pads',
          scroll_up_button='full_level_button',
          scroll_down_button='copy_button'))

    def _create_drum_group(self):
        self._drum_group = DrumGroupComponent(name='Drum_Group',
          is_enabled=False,
          translation_channel=(midi.DRUM_CHANNEL),
          layer=Layer(matrix='pads',
            scroll_page_up_button='full_level_button',
            scroll_page_down_button='copy_button',
            mute_button='pad_mute_button',
            solo_button='level_16_button',
            delete_button='erase_button'
        #   accent_button='full_level_button'
          ),
        )

    def _create_note_modes(self):
        self._note_modes = ModesComponent(name='Note_Modes', is_enabled=False, layer=Layer(session_button='shift_button'))
        self._note_modes.add_mode('keyboard', self._keyboard)
        self._note_modes.add_mode('drum', self._drum_group)
        self._note_modes.add_mode('session', AddLayerMode(self._session, Layer(clip_launch_buttons='pads_with_shift')), behaviour=(MomentaryBehaviour() ))
        self._note_modes.selected_mode = 'keyboard'

    def _create_channel_modes(self):
        self._channel_modes = ModesComponent(name='Channel_Mode', is_enabled=False, layer=Layer(session_button='shift_button'))
        self._channel_modes.add_mode('channel', 
            (
                self._elements.pads.reset, 
                AddLayerMode(self._mixer, Layer(
                    track_select_buttons=( self._elements.pads.submatrix[:, :1] ),
                    arm_buttons=( self._elements.pads.submatrix[:, 3:] ),
                    solo_buttons=( self._elements.pads.submatrix[:, 2:3] ),
                    mute_buttons=( self._elements.pads.submatrix[:, 1:2] )
                    )
                ),
                AddLayerMode(self._routing_component, Layer(
                    input_type_button='full_level_button',
                    input_channel_button='copy_button',
                    output_type_button='pad_mute_button',
                    output_channel_button='level_16_button',
                    monitor_cycle_button='erase_button',
                )) 
            ),
            self._session_navigation_modes,
        )
        self._channel_modes.add_mode('session', AddLayerMode(self._session, Layer(clip_launch_buttons='pads_with_shift')), behaviour=(MomentaryBehaviour() ))
        self._channel_modes.selected_mode = 'channel'
            
    def _create_pad_modes(self):
        self._pad_modes = ModesComponent(name='Pad_Modes',
            enable_skinning=True,
            is_enabled=False,
            layer=Layer(
                session_button='pad_bank_ae_button',
                note_button='pad_bank_bf_button',
                channel_button='pad_bank_cg_button',
                touch_strip_modes_button='touch_strip_button',
                stopclip_button='pad_bank_dh_button',
                macro_button='mode_button'))

        self._pad_modes.add_mode('session', (
            AddLayerMode(self._background, Layer(unused_pads='pads_with_shift')),
            AddLayerMode(self._session, Layer(
                clip_launch_buttons='pads',
                scene_launch_buttons=self._elements.pads_with_shift.submatrix[3:, :],
                managed_select_button='level_16_button',
                managed_delete_button='erase_button',
                managed_duplicate_button='copy_button',
                managed_create_button='full_level_button',
                managed_double_button='pad_mute_button'
                ),
            ),
            self._session_overview,
            self._session_navigation_modes))
        self._pad_modes.add_mode('note', [self._note_modes, self._note_repeat_enabler])
        self._pad_modes.add_mode('channel', self._channel_modes)

        self._pad_modes.add_mode('stopclip',
            AddLayerMode(
                self._session, 
                Layer(stop_track_clip_buttons=(self._elements.pads.submatrix[:, 3:] ) ) ),
            behaviour=(MomentaryBehaviour() )
        )

        self._pad_modes.add_mode('touch_strip_modes',
          (LayerMode(self._touch_strip_modes, Layer(
            volume_button=(self._elements.pads_raw[0][0]),
            pan_button=(self._elements.pads_raw[0][1]),
            send_a_button=(self._elements.pads_raw[0][2]),
            send_b_button=(self._elements.pads_raw[0][3]))),
         AddLayerMode(self._background, Layer(unused_pads=(self._elements.pads.submatrix[:, 1:])))),
          behaviour=MomentaryBehaviour()  )

        self._pad_modes.add_mode('macro', 
            (
                AddLayerMode(self._background, Layer(unused_pads='pads_with_shift')),
                AddLayerMode( 
                self._macro, 
                    Layer(
                    create_audio_button=self._elements.pads_raw[3][0],
                    create_midi_button=self._elements.pads_raw[3][1],
                    create_drumrack_button=self._elements.pads_raw[3][2],
                    create_simpler_button=self._elements.pads_raw[3][3],
                    add_compressor_button=self._elements.pads_raw[2][0],
                    add_eq_button=self._elements.pads_raw[2][1],
                    add_autofilter_button=self._elements.pads_raw[2][2],
                    add_gate_button=self._elements.pads_raw[2][3],
                    )
                )
            ),
            behaviour=MomentaryBehaviour()
        )

        self._pad_modes.selected_mode = 'session'
        self._pad_modes.set_enabled(True)

    def _set_pad_led_disabled(self):
        # Set all pads to black rgb color:
        self._send_midi( (240, 71, 71, 74, 101, 0, 64, 
        0, 0, 0, 0,
        1, 0, 0, 0,
        2, 0, 0, 0,
        3, 0, 0, 0,
        4, 0, 0, 0,
        5, 0, 0, 0,
        6, 0, 0, 0,
        7, 0, 0, 0,
        8, 0, 0, 0,
        9, 0, 0, 0,
        10, 0, 0, 0,
        11, 0, 0, 0,
        12, 0, 0, 0,
        13, 0, 0, 0,
        14, 0, 0, 0,
        15, 0, 0, 0,
        247) )

    @listens('is_view_visible', 'Session')
    def __on_main_view_changed(self):
        if self.application.view.is_view_visible('Session'):
            self._record_modes.selected_mode = 'session'
        else:
            self._record_modes.selected_mode = 'arrange'
    
    @listens('selected_mode')
    def __on_selected_mode_change(self, value):
        pass
        # logger.warn(value)
        # logger.warn(self._pad_modes.get_mode(value)._modes[1]._layer._element_to_names)

    @listens('target_track')
    def __on_target_track_changed(self):
        self._drum_group_finder.device_parent = self._target_track.target_track

    @listens('instrument')
    def __on_drum_group_changed(self):
        drum_group = self._drum_group_finder.drum_group
        self._drum_group.set_drum_group_device(drum_group)
        self._note_modes.selected_mode = 'drum' if liveobj_valid(drum_group) else 'keyboard'
        self.set_controlled_track(self._target_track.target_track)

    def _enable_session_ring(self):
        self._session_ring.set_enabled(True)