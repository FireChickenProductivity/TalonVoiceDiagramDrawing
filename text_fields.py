from talon import Module, actions
from .position_storage import store_current_position_in_main_storage, main_position_storage

module = Module()
@module.action_class
class Actions:
    def diagram_drawing_create_text_field_with_position_stored():
        '''Create a text field at the current mouse position and store its location in the main storage'''
        actions.user.diagram_drawing_create_text_field()
        store_current_position_in_main_storage()

    def diagram_drawing_label_stored_position(position_index: int):
        '''Creates a text field at the specified stored mouse position'''
        move_mouse_to_position_in_storage_indexed_from_one(position_index)
        actions.user.diagram_drawing_create_text_field()
    
    def diagram_drawing_edit_text_at_stored_position(position_index: int):
        '''Edits the text field at the stored position'''
        move_mouse_to_position_in_storage_indexed_from_one(position_index)
        actions.user.diagram_drawing_edit_text_at_cursor()
    
    def diagram_drawing_label_stored_position_with_text(position_index: int, text: str):
        '''Labels the stored position with the specified text'''
        actions.user.diagram_drawing_label_stored_position(position_index)
        actions.insert(text)
        actions.user.user.diagram_drawing_unselect()
    
    def diagram_drawing_label_stored_position_with_positive_number(position_index: int, number: int):
        '''Labels the stored position with the specified positive number'''
        actions.user.diagram_drawing_label_stored_position_with_text(position_index, str(number))
    
    def diagram_drawing_label_stored_position_with_negative_number(position_index: int, magnitude: int):
        '''Labels the stored position with the negative number with specified magnitude'''
        actions.user.diagram_drawing_label_stored_position_with_text(position_index, '-' + str(magnitude))

def move_mouse_to_position_in_storage_indexed_from_one(position_index: int):
    position = main_position_storage.get_position_indexed_from_one(position_index)
    position.go()

