import math
from talon import ctrl, actions

class MousePosition:
    STRING_START = '('
    STRING_ENDING = ')'
    COORDINATE_SEPARATOR = ', '
    def __init__(self, horizontal: int, vertical: int):
        self.horizontal = horizontal
        self.vertical = vertical
    
    def get_horizontal(self):
        return self.horizontal
    def get_vertical(self):
        return self.vertical
    
    def __add__(self, other):
        result = MousePosition(0, 0)
        result += self
        result += other
        return result
    def __iadd__(self, other):
        self.horizontal += other.horizontal
        self.vertical += other.vertical
        return self
    def __sub__(self, other):
        result = MousePosition(0, 0)
        result += self
        result -= other
        return result
    def __isub__(self, other):
        self.horizontal -= other.horizontal
        self.vertical -= other.vertical
        return self

    def go(self):
        actions.mouse_move(self.horizontal, self.vertical)

    def __str__(self) -> str:
        return MousePosition.STRING_START + str(self.horizontal) + MousePosition.COORDINATE_SEPARATOR \
        + str(self.vertical) + MousePosition.STRING_ENDING

    #assumes that the text properly represents a mouse position object
    @staticmethod
    def from_text(text: str):
        horizontal_start = text.index(MousePosition.STRING_START) + 1
        horizontal_ending = text.index(MousePosition.COORDINATE_SEPARATOR)
        horizontal = int(text[horizontal_start : horizontal_ending])
        vertical_start = horizontal_ending + 1
        vertical_ending = text.index(MousePosition.STRING_ENDING)
        vertical = int(text[vertical_start : vertical_ending])
        return MousePosition(horizontal, vertical)

    @staticmethod
    def current():
        horizontal, vertical = ctrl.mouse_pos()
        current_mouse_position = MousePosition(horizontal, vertical)
        return current_mouse_position
    
    def __eq__(self, other):
        return self.horizontal == other.horizontal and self.vertical == other.vertical

    def distance_from(self, other):
        return math.sqrt((self.horizontal - other.horizontal)**2 + (self.vertical - other.vertical)**2)

