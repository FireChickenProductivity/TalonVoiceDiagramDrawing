from talon import Module, actions
from .fire_chicken import data_storage
from .fire_chicken import path_utilities
from .fire_chicken.mouse_position import MousePosition

module = Module()
@module.action_class
class Actions:
    def diagram_drawing_compute_data_storage() -> data_storage.Storage:
        '''Returns the storage object for the data directory'''
        current_directory = path_utilities.compute_directory_at_path(__file__)
        data_directory = path_utilities.join_path(current_directory, 'data')
        storage = data_storage.Storage(data_directory)
        return storage
    
    def diagram_drawing_get_data_storage_position(name: str) -> MousePosition:
        ''''''
        position_file = get_data_storage_position_file(name)
        position = position_file.get()
        return position
    
    def diagram_drawing_set_data_storage_position_to_current_mouse_position(name: str):
        ''''''
        position_file = get_data_storage_position_file(name)
        position_file.set_to_current_mouse_position()
    
    def diagram_drawing_set_data_storage_position(name: str, position: MousePosition):
        ''''''
        position_file = get_data_storage_position_file(name)
        position_file.set(position)

def get_data_storage_position_file(name: str) -> data_storage.MousePositionFile:
    storage: data_storage.Storage = actions.user.diagram_drawing_compute_data_storage()
    position_file = storage.get_position_file(name)
    return position_file
