from talon import Module, actions
from .fire_chicken import data_storage
from .fire_chicken import path_utilities

module = Module()
@module.action_class
class Actions:
    def diagram_drawing_compute_data_storage() -> data_storage.Storage:
        '''Returns the storage object for the data directory'''
        current_directory = path_utilities.compute_directory_at_path(__file__)
        data_directory = path_utilities.join_path(current_directory, 'data')
        storage = data_storage.Storage(data_directory)
        return storage
