from talon import Module, actions
from .position_captures import PositionSpecifier
from .fire_chicken.mouse_position import MousePosition

module = Module()
@module.action_class
class Actions:
    def diagram_drawing_save_position(number: int, position: MousePosition):
        ''''''
        set_position_with_number(number, position)

    def diagram_drawing_save_named_position(number: int, specifier: PositionSpecifier):
        ''''''
        position = actions.user.diagram_drawing_get_position_from_specifier(specifier)
        actions.user.diagram_drawing_save_position(number, position)
    
    def diagram_drawing_save_current_position(number: int):
        ''''''
        actions.user.diagram_drawing_save_position(number, MousePosition.current())

    def diagram_drawing_get_saved_position(number: int) -> MousePosition:
        ''''''
        position = get_position_from_number(number)
        return position

def get_position_from_number(number: int):
    filename = compute_position_filename_from_number(number)
    position = actions.user.diagram_drawing_get_data_storage_position(filename)
    return position

def set_position_with_number(number: int, position: MousePosition):
    filename = compute_position_filename_from_number(number)
    actions.user.diagram_drawing_set_data_storage_position(filename, position)

def compute_position_filename_from_number(number: int):
    filename =  f'SavedPosition{number}.txt'
    return filename
