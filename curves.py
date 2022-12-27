from talon import Module, actions
from .fire_chicken.mouse_position import MousePosition
from enum import Enum
import math

def draw_points(points, between_point_delay: float = 0.02):
    points[0].go()
    actions.user.diagram_drawing_start_freestyle_drawing()
    for point in points:
        point.go()
        actions.sleep(between_point_delay)
    actions.user.diagram_drawing_stop_freestyle_drawing()
    
def draw_curve_dashed(points):
    dash_size = math.floor(len(points)/9)
    for dash_ending in range(dash_size, len(points), dash_size*2):
        dash_start = dash_ending - dash_size
        draw_points(points[dash_start:dash_ending])

class SwoopingDirection(Enum):
    UP = 1
    RIGHT = 2

class Quadratic:
    def __init__(self, linear_term, quadratic_term):
        self.quadratic_term = quadratic_term
        self.linear_term = linear_term
    
    def compute_value(self, independent_variable) -> float:
        return self.quadratic_term*independent_variable*independent_variable + self.linear_term*independent_variable
    
    def compute_points_between(self, start: MousePosition, ending: MousePosition):
        points = []
        for horizontal in range(start.get_horizontal(), ending.get_horizontal() + 1):
            horizontal_change = horizontal - start.get_horizontal()
            vertical = self.compute_value(horizontal_change) + start.get_vertical()
            point = MousePosition(horizontal, vertical)
            points.append(point)
        return points

    @staticmethod
    def from_positions_and_initial_slope(start: MousePosition, ending: MousePosition, initial_slope: float):
        linear_term = -initial_slope
        change: MousePosition = ending - start
        quadratic_term = (change.get_vertical() - linear_term*change.get_horizontal())/(change.get_horizontal()*change.get_horizontal())
        result = Quadratic(linear_term, quadratic_term)
        return result

def get_horizontal(position: MousePosition):
    return position.get_horizontal()

def get_vertical(position: MousePosition):
    return position.get_vertical()

module = Module()
@module.action_class
class Actions:
    def draw_quadratic_between_points_with_slope(start: MousePosition, ending: MousePosition, initial_slope: float):
        ''''''
        quadratic = Quadratic.from_positions_and_initial_slope(start, ending, initial_slope)
        points = quadratic.compute_points_between(start, ending)
        draw_points(points)
    
    def draw_quadratic_between_stored_positions_with_slope(initial_position_number: int, ending_position_number: int, initial_slope: float):
        ''''''
        start = actions.user.diagram_drawing_get_position(initial_position_number)
        ending = actions.user.diagram_drawing_get_position(ending_position_number)
        actions.user.draw_quadratic_between_points_with_slope(start, ending, initial_slope)
    
    def draw_dashed_quadratic_between_stored_positions_with_slope(initial_position_number: int, ending_position_number: int, initial_slope: float):
        ''''''
        start = actions.user.diagram_drawing_get_position(initial_position_number)
        ending = actions.user.diagram_drawing_get_position(ending_position_number)
        quadratic = Quadratic.from_positions_and_initial_slope(start, ending, initial_slope)
        points = quadratic.compute_points_between(start, ending)
        draw_curve_dashed(points)
