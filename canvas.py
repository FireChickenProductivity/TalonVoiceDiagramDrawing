from talon import Module, actions
from .fire_chicken import data_storage
from .fire_chicken import path_utilities
from .fire_chicken.mouse_position import MousePosition



module = Module()
@module.action_class
class Actions:
    def diagram_drawing_get_canvas_origin() -> MousePosition:
        ''''''
        position = get_canvas_position_with_name('Origin')
        return position
    
    def diagram_drawing_get_canvas_ending() -> MousePosition:
        ''''''
        position = get_canvas_position_with_name('Ending')
        return position
    
    def diagram_drawing_update_canvas_origin_to_current_mouse_position():
        ''''''
        update_canvas_position_with_name_to_current_mouse_position('Origin')
        
    
    def diagram_drawing_update_canvas_ending_to_current_mouse_position():
        ''''''
        update_canvas_position_with_name_to_current_mouse_position('Ending')

def get_canvas_position_with_name(name: str) -> MousePosition:
    position_file = get_canvas_position_file_with_name(name)
    position = position_file.get()
    return position

def update_canvas_position_with_name_to_current_mouse_position(name: str):
    position_file = get_canvas_position_file_with_name(name)
    position_file.set_to_current_mouse_position()

def get_canvas_position_file_with_name(name: str) -> data_storage.MousePositionFile:
    storage = compute_current_storage()
    position_file = storage.get_position_file(f'Canvas{name}.txt')
    return position_file

def compute_current_storage():
    current_directory = path_utilities.compute_directory_at_path(__file__)
    data_directory = path_utilities.join_path(current_directory, 'data')
    application_specific_subdirectory = path_utilities.join_path(data_directory, actions.user.diagram_drawing_get_drawing_application_name())
    storage = data_storage.Storage(application_specific_subdirectory)
    return storage
