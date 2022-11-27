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
        position = main_position_storage.get_position_indexed_from_one(position_index)
        position.go()
        actions.user.diagram_drawing_create_text_field()
