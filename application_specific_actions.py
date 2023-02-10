from talon import Module
from .fire_chicken.mouse_position import MousePosition
from typing import List
module = Module()

@module.action_class
class Actions:
    def diagram_drawing_draw_line(origin: MousePosition, destination: MousePosition):
        '''Draws a line between these specified mouse positions.'''
        pass

    def diagram_drawing_draw_filled_in_line_shape(positions: List):
        '''Draws the shape fill in. This shape is specified by a list of mouse positions. Lines are consecutively drawn between them.'''
        pass
    
    def diagram_drawing_activate_text_tool():
        '''Activate the tool for adding text fields.'''
        pass

    def diagram_drawing_create_text_field():
        '''Creates a text field at the current mouse position.'''
        pass

    def diagram_drawing_unselect():
        '''Unselects the current diagram part.'''
        pass

    def diagram_drawing_edit_text_at_cursor():
        '''Edits the text field at the current mouse position.'''
        pass

    def diagram_drawing_start_freestyle_drawing():
        '''Starts freestyle drawing where moving the cursor draws.'''
        pass

    def diagram_drawing_stop_freestyle_drawing():
        '''Stops freestyle drawing where moving the cursor draws.'''
        pass

    def diagram_drawing_get_drawing_application_name() -> str:
        '''Gives the name of the current drawing application. This is used by some file storage code.'''
        return ''
