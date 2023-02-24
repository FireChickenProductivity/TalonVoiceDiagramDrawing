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
    
    def diagram_drawing_compute_application_specific_storage() -> data_storage.Storage:
        '''Returns the diagram drawing storage for a specific application'''
        storage_for_data: data_storage.Storage = actions.user.diagram_drawing_compute_data_storage().get_path()
        application_specific_storage_path = path_utilities.join_path(storage_for_data, actions.user.diagram_drawing_get_drawing_application_name())
        storage = data_storage.Storage(application_specific_storage_path)
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
    
    def diagram_drawing_set_application_specific_data_storage_position_to_current_mouse_position(name: str):
        ''''''
        position_file = get_application_specific_storage_position_file(name)
        position_file.set_to_current_mouse_position()
    
    def diagram_drawing_get_application_specific_data_storage_position(name: str):
        ''''''
        return get_application_specific_storage_position_file(name).get()

def get_data_storage_position_file(name: str) -> data_storage.MousePositionFile:
    storage: data_storage.Storage = actions.user.diagram_drawing_compute_data_storage()
    position_file = storage.get_position_file(name)
    return position_file

def get_application_specific_storage_position_file(name: str) -> data_storage.MousePositionFile:
    storage: data_storage.Storage = actions.user.diagram_drawing_compute_application_specific_storage()
    position_file = storage.get_position_file(name)
    return position_file
