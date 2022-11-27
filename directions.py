from talon import Module, actions, Context
from typing import List

module = Module()
module.list('diagram_drawing_direction', desc = 'Words used to indicate directions')
module.list('diagram_drawing_complex_direction', desc = 'Words used to indicate more complex directions than up down left or right')

class InvalidDirectionException(Exception):
    pass

class Direction:
    def __init__(self, horizontal: int, vertical: int):
        self.horizontal = horizontal
        self.vertical = vertical
    
    def validate_format(self):
        def validate_coordinate_format(coordinate: int):
            if coordinate not in [0, 1, -1]:
                raise Direction(f'Direction received invalid coordinate {coordinate}!')
        validate_coordinate_format(self.horizontal)
        validate_coordinate_format(self.vertical)
    


context = Context()
context.lists['user.diagram_drawing_direction'] = {
    'up': '0 1',
    'down': '0 -1',
    'left': '-1 0',
    'right': '1 0',
}
context.lists['user.diagram_drawing_complex_direction'] = {
    'peft': '-1 1',
    'pight': '1 1',
    'neft': '-1 -1',
    'night': '1 -1',
}

@module.capture(rule = '{user.diagram_drawing_direction}|{user.diagram_drawing_complex_direction}')
def diagram_drawing_direction(m) -> Direction:
    direction: Direction = get_direction_from_capture(m)
    return direction

@module.capture(rule = '{user.diagram_drawing_complex_direction}')
def diagram_drawing_complex_direction(m) -> Direction:
    direction: Direction = get_direction_from_capture(m)
    return direction

def get_direction_from_capture(capture) -> Direction:
    direction_string: str = capture[0]
    coordinates: List = direction_string.split(' ')
    horizontal: int = int(coordinates[0])
    vertical: int = int(coordinates[1])
    direction = Direction(horizontal, vertical)
    return direction