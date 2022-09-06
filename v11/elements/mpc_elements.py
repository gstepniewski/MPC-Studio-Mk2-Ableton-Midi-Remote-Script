from ableton.v2.control_surface.elements import ButtonElement
from past.builtins import long
from ableton.v2.base import BooleanContext, const, has_event, in_range, listens, old_hasattr

class MPCButtonElement(ButtonElement):
    def __init__(self, *a, **k):
        super(MPCButtonElement, self).__init__(*a, **k)
        self.blink_task = 'Test'
    
    def reset(self):
        self.set_light(u'DefaultButton.Disabled')
        self.use_default_message()
        self.suppress_script_forwarding = False

    def blackout(self):
        self.set_light(u'DefaultButton.Disabled')
        self.use_default_message()
        self.suppress_script_forwarding = False

class MPCPadElement(ButtonElement):
    def __init__(self, *a, **k):
        super(MPCPadElement, self).__init__(*a, **k)
        self._default_button_on = u'DrumGroup.On'
        self._default_button_off = u'DrumGroup.Disabled'
        self._default_button_disabled = u'DrumGroup.Off'
    
    def reset(self):
        self.set_light(self._default_button_off)
        self.use_default_message()
        self.suppress_script_forwarding = False

    def blackout(self):
        self.set_light(self._default_button_disabled)
        self.use_default_message()
        self.suppress_script_forwarding = False
    
    # def set_light(self, value):
    #     # logger.warn('{}, {}, {}'.format(self.name, self._original_identifier, value))
        
    #     if value == u'DefaultButton.On':
    #         value = self._default_button_on 
    #     elif value == u'DefaultButton.Of':
    #         value == self._default_button_off
        
    #     if hasattr(value, u'draw'):
    #         value.draw(self)
    #     elif type(value) in (int, long) and in_range(value, 0, 128):
    #         self.send_value(value)
    #     elif isinstance(value, bool):
    #         self._set_skin_light(self._default_button_on if value else self._default_button_off)
    #     else:
    #         self._set_skin_light(value)
