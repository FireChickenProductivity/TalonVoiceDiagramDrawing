from talon import Module, actions
from typing import Union, List
from .fire_chicken.mouse_position import MousePosition

module = Module()
@module.capture(rule = '<number>|<user.diagram_drawing_number_float> by <user.diagram_drawing_number_float> [by <user.diagram_drawing_number_float>]')
def diagram_drawing_position_specifier(m) -> Union[int, List]:
    ''''''
    try:
        return m.number
    except:
        pass
    
    result = []
    for i in range(0, len(m), 2):
        result.append(m[i])
    return result
    
@module.action_class
class Actions:
    def diagram_drawing_get_position_from_specifier(specifier: Union[int, List]) -> MousePosition:
        ''''''
        if type(specifier) == int:
            return actions.user.diagram_drawing_get_position(specifier)
        elif type(specifier) == List:
            return actions.user.get_position_along_axes(*specifier)
        
    def diagram_drawing_move_mouse_to_position(specifier: Union[int, List]):
        ''''''
        position = actions.user.diagram_drawing_get_position_from_specifier(specifier)
        position.go()
