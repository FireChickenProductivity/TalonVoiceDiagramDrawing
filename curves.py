from talon import Module, actions
from .fire_chicken.mouse_position import MousePosition
from .position_storage import main_position_storage
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

def compute_shifted_curve_points(points, horizontal_shift: int, vertical_shift: int):
    if len(points) <= 2:
        return points
    start: MousePosition = points[0]
    ending: MousePosition = points[-1]
    boundary = Boundary(start, ending)
    in_between_points = points[1: -1]
    result = []
    result.append(start)
    for point in in_between_points:
        horizontal = point.get_horizontal() + horizontal_shift
        vertical = point.get_vertical() + vertical_shift
        new_position = boundary.compute_position_within_boundaries(horizontal, vertical)
        result.append(new_position)
    result.append(ending)
    return result

def compute_line_points(start: MousePosition, ending: MousePosition):
    if start.get_horizontal() != ending.get_horizontal():
        return compute_none_vertical_line_points(start, ending)
    return compute_vertical_line_points(start, ending)

def compute_none_vertical_line_points(start: MousePosition, ending: MousePosition):
    slope = (ending.get_vertical() - start.get_vertical())/(ending.get_horizontal() - start.get_horizontal())
    range_object = compute_range(start.get_horizontal(), ending.get_horizontal())
    points = []
    for horizontal in range_object:
        relative_horizontal = horizontal - start.get_horizontal()
        relative_position: MousePosition = MousePosition(relative_horizontal, relative_horizontal*slope)
        point_position = relative_position + start
        points.append(point_position)
    return points

def compute_vertical_line_points(start: MousePosition, ending: MousePosition):
    range_object = compute_range(start.get_vertical(), ending.get_vertical())
    horizontal = start.get_horizontal()
    points = []
    for vertical in range_object:
        position = MousePosition(horizontal, vertical)
        points.append(position)
    return points

def compute_range(start: int, inclusive_ending: int):
    increment = 1
    if start > inclusive_ending:
        increment = -1
    range_result = range(start, inclusive_ending + 1, increment)
    return range_result

class Boundary:
    def __init__(self, start: MousePosition, ending: MousePosition):
        self.lower_vertical_boundary = min(start.get_vertical(), ending.get_vertical())
        self.upper_vertical_boundary = max(start.get_vertical(), ending.get_vertical())
        self.lower_horizontal_boundary = min(start.get_horizontal(), ending.get_horizontal())
        self.upper_horizontal_boundary = max(start.get_horizontal(), ending.get_horizontal())

    def compute_vertical_within_boundary(self, vertical: int):
        return self._compute_coordinate_within_boundary(vertical, self.lower_vertical_boundary, self.upper_vertical_boundary)
    
    def compute_horizontal_within_boundary(self, horizontal: int):
        return self._compute_coordinate_within_boundary(horizontal, self.lower_vertical_boundary, self.upper_horizontal_boundary)
    
    def _compute_coordinate_within_boundary(self, coordinate: int, minimum: int, maximum: int):
        result = coordinate
        if coordinate < minimum:
            result = minimum
        elif coordinate > maximum:
            result = maximum
        return result

    def compute_position_within_boundaries(self, horizontal: int, vertical: int) -> MousePosition:
        position = MousePosition(self.compute_horizontal_within_boundary(horizontal), self.compute_vertical_within_boundary((vertical)))
        return position

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
    
    def diagram_drawing_draw_dashed_line_between_stored_positions(origin_position_number: int, destination_position_number: int):
        ''''''
        origin = main_position_storage.get_position_indexed_from_one(origin_position_number)
        destination = main_position_storage.get_position_indexed_from_one(destination_position_number)
        line_positions = compute_line_points(origin, destination)
        draw_curve_dashed(line_positions)
        
