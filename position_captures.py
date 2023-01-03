from talon import Module, actions
from typing import Union, List
from .fire_chicken.mouse_position import MousePosition
PositionSpecifier = Union[int, List]

module = Module()
@module.capture(rule = '<number>|<user.diagram_drawing_number_float> by <user.diagram_drawing_number_float> [by <user.diagram_drawing_number_float>]')
def diagram_drawing_position_specifier(m) -> PositionSpecifier:
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
    def diagram_drawing_get_position_from_specifier(specifier: PositionSpecifier) -> MousePosition:
        ''''''
        if type(specifier) == int:
            return actions.user.diagram_drawing_get_position(specifier)
        elif type(specifier) == list:
            return actions.user.diagram_drawing_go_to_position_along_axes(*specifier)
        print('specifier', specifier)
        
    def diagram_drawing_move_mouse_to_position(specifier: PositionSpecifier):
        ''''''
        position = actions.user.diagram_drawing_get_position_from_specifier(specifier)
        position.go()
