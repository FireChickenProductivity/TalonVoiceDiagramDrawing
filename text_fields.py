from talon import Module, actions
from .position_storage import store_current_position_in_main_storage
from .position_captures import PositionSpecifier

module = Module()
@module.action_class
class Actions:
    def diagram_drawing_create_text_field_with_position_stored():
        '''Create a text field at the current mouse position and store its location in the main storage'''
        actions.user.diagram_drawing_create_text_field()
        store_current_position_in_main_storage()

    def diagram_drawing_label_named_position(position_specifier: PositionSpecifier):
        '''Creates a text field at the specified stored mouse position'''
        actions.user.diagram_drawing_move_mouse_to_position(position_specifier)
        actions.user.diagram_drawing_create_text_field()
    
    def diagram_drawing_edit_text_at_named_position(position_specifier: PositionSpecifier):
        '''Edits the text field at the stored position'''
        actions.user.diagram_drawing_move_mouse_to_position(position_specifier)
        actions.user.diagram_drawing_edit_text_at_cursor()
    
    def diagram_drawing_label_named_position_with_text(position_specifier: PositionSpecifier, text: str):
        '''Labels the stored position with the specified text'''
        actions.user.diagram_drawing_label_named_position(position_specifier)
        give_active_text_field_text(text)
    
    def diagram_drawing_label_named_position_with_positive_number(position_specifier: PositionSpecifier, number: int):
        '''Labels the stored position with the specified positive number'''
        actions.user.diagram_drawing_label_named_position_with_text(position_specifier, str(number))
    
    def diagram_drawing_label_named_position_with_negative_number(position_specifier: PositionSpecifier, magnitude: int):
        '''Labels the stored position with the negative number with specified magnitude'''
        actions.user.diagram_drawing_label_named_position_with_text(position_specifier, '-' + str(magnitude))
    
    def diagram_drawing_create_text_field_at_cursor_with_text_uppercase(text: str):
        ''''''
        actions.user.diagram_drawing_create_text_field_at_cursor_with_text(text.upper())
    
    def diagram_drawing_create_text_field_at_cursor_with_text(text: str):
        ''''''
        actions.user.diagram_drawing_create_text_field_with_position_stored()
        give_active_text_field_text(text)

def give_active_text_field_text(text: str):
    actions.insert(text)
    actions.user.diagram_drawing_unselect()
