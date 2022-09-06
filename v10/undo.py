from __future__ import absolute_import, print_function, unicode_literals
from ableton.v2.control_surface.components import UndoRedoComponent as UndoRedoComponentBase
from ableton.v2.control_surface.control.button import ButtonControl
from ableton.v2.control_surface import Component
import logging
logger = logging.getLogger(__name__)
class UndoRedoComponent(UndoRedoComponentBase):
    def __init__(self, *a, **k):
        super(UndoRedoComponent, self).__init__(*a, **k)
    undo_button = ButtonControl(pressed_color=u'Undo.On', color=u'Undo.Off')
    redo_button = ButtonControl(pressed_color=u'Undo.On')

    def _undo(self):
        logger.warn('Here')
        if self.song.can_undo:
            self.song.undo()

class NewUndoComponent(Component):
    undo_button = ButtonControl(pressed_color=u'Undo.On', color=u'Undo.Off')
    redo_button = ButtonControl(pressed_color=u'Undo.On')
    
    @undo_button.pressed
    def undo_button(self, button):
        self._undo()

    @redo_button.pressed
    def redo_button(self, button):
        self._redo()

    def _redo(self):
        if self.song.can_redo:
            self.song.redo()

    def _undo(self):
        if self.song.can_undo:
            self.song.undo()