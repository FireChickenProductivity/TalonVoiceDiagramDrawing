from ...fire_chicken import path_utilities, data_storage
import os
from talon import actions, Module

module = Module()
@module.action_class
class Actions:
    def diagram_drawing_update_stored_vectr_position(name: str):
        '''Updates the stored mouse position for working with vectr with the specified name to be the current mouse position'''
        file = get_storage_position(name)
        file.set_to_current_mouse_position()

def fill_in_current_continuous_line_shape():
    click_storage_position('fill')
    click_storage_position('fill_color')
    click_storage_position('fill_color_black')
    

def click_storage_position(name: str):
    file = get_storage_position(name)
    file.go()
    actions.mouse_click(0)

def get_storage_position(name: str):
    storage = compute_current_storage()
    file = storage.get_position_file(name + '.txt')
    return file

def compute_current_storage() -> data_storage.Storage:
    current_directory = os.path.dirname(os.path.dirname(path_utilities.compute_directory_at_path(__file__)))
    data_directory = os.path.join(current_directory, 'data')
    application_specific_subdirectory = os.path.join(data_directory, actions.user.diagram_drawing_get_drawing_application_name(), 'application_specific')
    storage = data_storage.Storage(application_specific_subdirectory)
    return storage


    