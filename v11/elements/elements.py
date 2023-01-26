from __future__ import absolute_import, print_function, unicode_literals
from functools import partial
from ableton.v2.base import depends, recursive_map
from ableton.v2.control_surface import MIDI_CC_TYPE, MIDI_NOTE_TYPE, PrioritizedResource
from ableton.v2.control_surface.elements import ButtonElement, ButtonMatrixElement, ComboElement, SliderElement
from .mpc_elements import MPCButtonElement, MPCPadElement
from ..CONST import PADS_ARRANGEMENT
SESSION_WIDTH = 4
SESSION_HEIGHT = 4

@depends(skin=None)
def create_button(identifier, name, msg_type=MIDI_NOTE_TYPE, **k):
    return MPCButtonElement(True, msg_type, 0, identifier, name=name, **k)

# @depends(skin=None)
# def create_button(identifier, name, msg_type=MIDI_NOTE_TYPE, **k):
#     return ButtonElement(True, msg_type, 0, identifier, name=name, **k)

def create_cc_button(identifier, name, msg_type=MIDI_CC_TYPE, **k):
    return ButtonElement(True, msg_type, 0, identifier, name=name, **k)


@depends(skin=None)
def create_transport_button(identifier, name, msg_type=MIDI_NOTE_TYPE, **k):
    return ButtonElement(True, msg_type, 0, identifier, name=name, **k)

@depends(skin=None)
def create_pad(identifier, name, msg_type=MIDI_NOTE_TYPE, **k):
    return MPCPadElement(True, msg_type, 9, identifier, name=name, **k)

def with_modifier(modifier_button, button):
    return ComboElement(control=button,
        modifier=modifier_button,
        name=('{}_With_{}'.format(button.name, modifier_button.name.split('_')[0])))

class Elements(object):

    def __init__(self, *a, **k):
        (super(Elements, self).__init__)(*a, **k)
        self.touch_strip_button = create_button(0	, 'Touch_Strip_Button')
        self.pad_mute_button = create_button(4	, 'Pad_Mute_Button')
        self.erase_button = create_button(9	, 'Erase_Button')
        self.note_repeat_button = create_button(11, 'Note_Repeat_Button')
        self.quantize_button = create_button(12, 'Quantize_Button')
        self.track_select_button = create_button(13, 'Track_Select_Button')
        self.program_select_button = create_button(14, 'Program_Select_Button')
        self.tc_on_off_Button = create_button(15, 'TC_On_Off_Button')
        self.sample_start_button = create_button(33, 'Sample_Start_Button')
        self.sample_end_button = create_button(34, 'Sample_End_Button')
        self.pad_bank_ae_button = create_button(35, 'Pad_Bank_AE_Button')
        self.pad_bank_bf_button = create_button(36, 'Pad_Bank_BF_Button')
        self.pad_bank_cg_button = create_button(37, 'Pad_Bank_CG_Button')
        self.pad_bank_dh_button = create_button(38, 'Pad_Bank_DH_Button')
        self.full_level_button = create_button(39, 'Full_Level_Button')
        self.level_16_button = create_button(40, 'Level_16_Button')
        self.sample_select_button = create_button(42, 'Sample_Select_Button')
        self.shift_button = create_button(49, 'Shift_Button', resource_type=PrioritizedResource)
        self.browse_button = create_button(50, 'Browse_Button')
        self.main_button = create_button(52, 'Main_Button')
        self.tap_tempo_button = create_button(53, 'Tap_Tempo_Button')
        self.plus_button = create_button(54, 'Plus_Button')
        self.minus_button = create_button(55, 'Minus_Button')
        self.zoom_button = create_button(66, 'Zoom_Button', resource_type=PrioritizedResource)
        self.undo_button = create_button(67, 'Undo_Button')
        self.nudge_left_button = create_button(68, 'Nudge_Left_Button')
        self.nudge_right_button = create_button(69, 'Nudge_Right_Button')
        self.locate_button = create_button(70, 'Locate_Button')
        self.seek_back_button = create_button(71, 'Seek_Back_Button')
        self.seek_forward_button = create_button(72, 'Seek_Forward_Button')
        self.record_button = create_transport_button(73, 'Record_Button')
        self.automation_rw_button = create_button(75, 'Automation_RW_Button')
        self.tune_button = create_button(79, 'Tune_Button')
        self.overdub_button = create_transport_button(80, 'Overdub_Button')
        self.stop_button = create_transport_button(81, 'Stop_Button')
        self.play_button = create_transport_button(82, 'Play_Button')
        self.play_start_button = create_transport_button(83, 'Play_Start_Button')
        self.jog_wheel_button = create_button(111, 'Jog_Wheel_Button')
        self.jog_wheel = create_cc_button(100, 'Jog_Wheel')
        self.mode_button = create_button(114, 'Mode_Button')
        self.copy_button = create_button(122, 'Copy_Button')
        self.pads_raw = []
        for row_index, r in enumerate(PADS_ARRANGEMENT):
            row = []
            for col_index, p in enumerate(r):
                row.append(create_pad(int(p), '{}_Pad_{}'.format(col_index, row_index) ) )
            self.pads_raw.append(row)
        self.pads = ButtonMatrixElement(rows=(self.pads_raw), name='Pads')

        self.undo_button_with_shift = with_modifier(self.shift_button, self.undo_button)
        self.locate_button_with_shift = with_modifier(self.shift_button, self.locate_button)
        self.zoom_button_with_shift = with_modifier(self.shift_button, self.zoom_button)

        self.pads_with_shift = ButtonMatrixElement(name='Pads_With_Shift',rows=(recursive_map(partial(with_modifier, self.shift_button), self.pads_raw)))
        self.pads_with_zoom = ButtonMatrixElement(name='Pads_With_Zoom',rows=(recursive_map(partial(with_modifier, self.zoom_button), self.pads_raw)))
        self.pads_with_pad_mute = ButtonMatrixElement(name='Pads_With_Pad_Mute',rows=(recursive_map(partial(with_modifier, self.pad_mute_button), self.pads_raw)))
        self.pads_with_mode = ButtonMatrixElement(name='Pads_With_Mode',rows=(recursive_map(partial(with_modifier, self.mode_button), self.pads_raw)))
        self.touch_strip_press_button = create_button(78, 'Touch_Strip_Press_Button')
        self.touch_strip_slider = SliderElement(MIDI_CC_TYPE, 0, 33, name='touch_strip_slider')
        self.touch_strip_control = ComboElement(control=self.touch_strip_slider, modifier=self.touch_strip_press_button, name='touch_strip_control')