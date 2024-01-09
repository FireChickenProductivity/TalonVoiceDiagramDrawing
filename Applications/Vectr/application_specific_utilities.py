from ...fire_chicken import path_utilities, data_storage
import os
from talon import actions, Module, settings

module = Module()
vectr_color_interface_click_delay_setting_name = 'diagram_drawing_vectr_color_interface_click_delay'
vectr_color_interface_click_delay = 'user.' + vectr_color_interface_click_delay_setting_name
module.setting(
    vectr_color_interface_click_delay_setting_name,
    type = int,
    default = 100,
    desc = 'How long to pause between clicking on aspects of the vectr color interface'
)

@module.action_class
class Actions:
    def diagram_drawing_update_stored_vectr_position(name: str):
        '''Updates the stored mouse position for working with vectr with the specified name to be the current mouse position'''
        file = get_storage_position(name)
        file.set_to_current_mouse_position()

def fill_in_current_continuous_line_shape():
    wait_for_color_interface_to_process_clicking()
    click_storage_position('fill')
    wait_for_color_interface_to_process_clicking()
    click_storage_position('fill_color')
    wait_for_color_interface_to_process_clicking()
    click_storage_position('fill_color_black')
    wait_for_color_interface_to_process_clicking()
    
def wait_for_color_interface_to_process_clicking():
    actions.sleep(f'{settings.get(vectr_color_interface_click_delay)}ms')

def click_storage_position(name: str):
    file = get_storage_position(name)
    position = file.get()
    position.go()
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


    
