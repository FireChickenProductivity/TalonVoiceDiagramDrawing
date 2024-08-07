from talon import Module, actions
from .fire_chicken.mouse_position import MousePosition
from .position_storage import main_position_storage
from .position_captures import PositionSpecifier
from enum import Enum
import math

class Boundary:
    def __init__(self, start: MousePosition, ending: MousePosition):
        self.lower_vertical_boundary = min(start.get_vertical(), ending.get_vertical())
        self.upper_vertical_boundary = max(start.get_vertical(), ending.get_vertical())
        self.lower_horizontal_boundary = min(start.get_horizontal(), ending.get_horizontal())
        self.upper_horizontal_boundary = max(start.get_horizontal(), ending.get_horizontal())

    def get_top(self):
        return self.upper_vertical_boundary
    
    def get_bottom(self):
        return self.lower_vertical_boundary
    
    def get_right(self):
        return self.upper_horizontal_boundary
    
    def get_left(self):
        return self.lower_horizontal_boundary

    def compute_vertical_within_boundary(self, vertical: int):
        return self._compute_coordinate_within_boundary(vertical, self.lower_vertical_boundary, self.upper_vertical_boundary)
    
    def compute_horizontal_within_boundary(self, horizontal: int):
        return self._compute_coordinate_within_boundary(horizontal, self.lower_horizontal_boundary, self.upper_horizontal_boundary)
    
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

def draw_points(points, between_point_delay: float = 0.02):
    points[0].go()
    actions.user.diagram_drawing_start_freestyle_drawing()
    for point in points:
        point.go()
        actions.sleep(between_point_delay)
    actions.user.diagram_drawing_stop_freestyle_drawing()

#whatIV coded this
def draw_curve_dashed(points):
    gap_size = 10
    dash_multiple_of_gap = 2
    # dash size an integer multiple of gap size
   
    num_dashes = math.floor((len(points)/gap_size + 1)/(dash_multiple_of_gap + 1))

    minimum_number_dashes = 2
    if num_dashes < minimum_number_dashes:
        num_dashes = minimum_number_dashes
        gap_size = math.floor(len(points)/(minimum_number_dashes*dash_multiple_of_gap + 1))
    dash_size = dash_multiple_of_gap*gap_size

    left_over = len(points) - (num_dashes*(dash_multiple_of_gap + 1) -1)*gap_size
    add_to_first_dash = math.floor(left_over/2)
   
    # draw first dash
    dash_ending = dash_size + add_to_first_dash
    draw_points(points[0:dash_ending])

    # draw middle dashes - all but first and last
    for i in range(num_dashes - 2):
        dash_ending += dash_size + gap_size
        dash_start = dash_ending - dash_size
        draw_points(points[dash_start:dash_ending])

    # draw last dash
   
    draw_points(points[dash_ending + gap_size:])

def compute_shifted_curve_points(points, shift_function):
    if len(points) <= 2:
        return points
    start: MousePosition = points[0]
    ending: MousePosition = points[-1]
    boundary = Boundary(start, ending)
    in_between_points = points[1: -1]
    result = []
    result.append(start)
    for point in in_between_points:
        horizontal, vertical = shift_function(point, boundary, points)
        new_position = boundary.compute_position_within_boundaries(horizontal, vertical)
        result.append(new_position)
    result.append(ending)
    return result

def compute_curved_points_shifted_fractionally(points, fractional_factor: int, divisor: int):
    def shift_function(point: MousePosition, boundary: Boundary, points):
        horizontal = point.get_horizontal()
        for i in range(fractional_factor):
            boundary_distance = boundary.get_right() - horizontal
            shift_amount = boundary_distance/divisor
            horizontal += shift_amount
        return horizontal, point.get_vertical()
    return compute_shifted_curve_points(points, shift_function)

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

def compute_two_slope_curve_points(start: MousePosition, ending: MousePosition, starting_slope: float, ending_slope: float):
    horizontal_distance = abs(start.get_horizontal() - ending.get_horizontal())
    slope_change = ending_slope - starting_slope
    average_slope_change = slope_change/horizontal_distance
    slope = starting_slope
    vertical = start.get_vertical()
    range_object = compute_range(start.get_horizontal(), ending.get_horizontal())
    points = []
    for horizontal in range_object:
        points.append(MousePosition(horizontal, vertical))
        vertical -= slope
        slope += average_slope_change
    return points

def compute_range(start: int, inclusive_ending: int):
    start = int(start)
    inclusive_ending = int(inclusive_ending)
    increment = 1
    if start > inclusive_ending:
        increment = -1
    range_result = range(start, inclusive_ending + 1, increment)
    return range_result

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

class InvalidBezierQuadratic(Exception):
    pass

class BezierQuadratic:
    def __init__(self, start: MousePosition, ending: MousePosition, control_point: MousePosition):
        self.start = start
        self.ending = ending
        self.control_point = control_point
    
    def compute_position_given_parametric_independent_variable(self, independent_variable: float):
        if independent_variable < 0 or independent_variable > 1:
            raise ValueError(f'The independent variable for a Bézier Quadratic must be between 0 and 1 but instead received {independent_variable}')
        position: MousePosition = self.control_point + ((1 - independent_variable)**2)*(self.start - self.control_point) + (independent_variable**2)*(self.ending - self.control_point)
        return position
    
    def compute_points(self, change_in_independent_variable: float = 0.01):
        points = []
        t = 0
        while t < 1:
            point: MousePosition = self.compute_position_given_parametric_independent_variable(t)
            points.append(point)
            t += change_in_independent_variable
        last_point: MousePosition = self.compute_position_given_parametric_independent_variable(1)
        points.append(last_point)
        return points
    
    #Currently fails to take into account the possibilities of infinite slope and same slopes
    @staticmethod
    def compute_from_start_ending_and_slopes(start: MousePosition, ending: MousePosition, initial_slope: float, final_slope: float):
        horizontal = (-ending.get_vertical() + start.get_vertical() + initial_slope*start.get_horizontal() - final_slope*ending.get_horizontal())/(initial_slope - final_slope)
        vertical = -initial_slope*(horizontal - start.get_horizontal()) + start.get_vertical()
        control_point = MousePosition(horizontal, vertical)
        return BezierQuadratic(start, ending, control_point)

class Line:
    def __init__(self, start: MousePosition, ending: MousePosition):
        self.start = start
        self.ending = ending
    
    def compute_position_at_distance_from_start(self, distance: float) -> MousePosition:
        if 0 > distance > self.start.distance_from(self.ending):
            raise ValueError(f'The specified position with distance {distance} from the starting position of the line is not on the line!')
        change: MousePosition = self.ending - self.start
        direction_change: MousePosition = change*1/(change.compute_magnitude())
        result: MousePosition = self.start + distance*direction_change
        return result
    
    def compute_position_at_fraction_of_distance_between_points(self, fraction: float) -> MousePosition:
        distance: float = self.compute_fraction_of_distance_between_points(fraction)
        position: MousePosition = self.compute_position_at_distance_from_start(distance)
        return position

    def compute_fraction_of_distance_between_points(self, fraction: float) -> float:
        distance: float = fraction*self.start.distance_from(self.ending)
        return distance
    
module = Module()
@module.action_class
class Actions:
    def draw_quadratic_between_points_with_slope(start: MousePosition, ending: MousePosition, initial_slope: float):
        ''''''
        quadratic = Quadratic.from_positions_and_initial_slope(start, ending, initial_slope)
        points = quadratic.compute_points_between(start, ending)
        draw_points(points)
    
    def draw_quadratic_between_named_positions_with_slope(initial_position_specifier: PositionSpecifier, ending_position_specifier: PositionSpecifier, initial_slope: float):
        ''''''
        start = actions.user.diagram_drawing_get_position_from_specifier(initial_position_specifier)
        ending = actions.user.diagram_drawing_get_position_from_specifier(ending_position_specifier)
        actions.user.draw_quadratic_between_points_with_slope(start, ending, initial_slope)
    
    def draw_quadratic_between_saved_positions_with_slope(initial_slope: float):
        ''''''
        start = actions.user.diagram_drawing_get_saved_position(1)
        ending = actions.user.diagram_drawing_get_saved_position(2)
        actions.user.draw_quadratic_between_points_with_slope(start, ending, initial_slope)

    def draw_dashed_quadratic_between_points_with_slope(start: MousePosition, ending: MousePosition, initial_slope: float):
        ''''''
        quadratic = Quadratic.from_positions_and_initial_slope(start, ending, initial_slope)
        points = quadratic.compute_points_between(start, ending)
        draw_curve_dashed(points)

    def draw_dashed_quadratic_between_named_positions_with_slope(initial_position_specifier: PositionSpecifier, ending_position_specifier: PositionSpecifier, initial_slope: float):
        ''''''
        start = actions.user.diagram_drawing_get_position_from_specifier(initial_position_specifier)
        ending = actions.user.diagram_drawing_get_position_from_specifier(ending_position_specifier)
        actions.user.draw_dashed_quadratic_between_points_with_slope(start, ending, initial_slope)

    def draw_dashed_quadratic_between_saved_positions_with_slope(initial_slope: float):
        ''''''
        start = actions.user.diagram_drawing_get_saved_position(1)
        ending = actions.user.diagram_drawing_get_saved_position(2)
        actions.user.draw_dashed_quadratic_between_points_with_slope(start, ending, initial_slope)
    
    def diagram_drawing_draw_dashed_line_between_named_positions(initial_position_specifier: PositionSpecifier, ending_position_specifier: PositionSpecifier):
        ''''''
        origin = actions.user.diagram_drawing_get_position_from_specifier(initial_position_specifier)
        destination = actions.user.diagram_drawing_get_position_from_specifier(ending_position_specifier)
        line_positions = compute_line_points(origin, destination)
        draw_curve_dashed(line_positions)
    
    #not an effective way to draw curves
    def diagram_drawing_draw_shifted_line_between_stored_positions(origin_position_number: int, destination_position_number: int, shift_factor: int, divisor: int):
        ''''''
        origin = main_position_storage.get_position_indexed_from_one(origin_position_number)
        destination = main_position_storage.get_position_indexed_from_one(destination_position_number)
        line_positions = compute_line_points(origin, destination)
        curve_positions = compute_curved_points_shifted_fractionally(line_positions, shift_factor, divisor)
        draw_points(curve_positions)
    
    def diagram_drawing_draw_two_slope_curve_between_points(starting_slope: float, ending_slope: float, start: MousePosition, ending: MousePosition):
        ''''''
        curve = BezierQuadratic.compute_from_start_ending_and_slopes(start, ending, starting_slope, ending_slope)
        points = curve.compute_points()
        draw_points(points)
    
    def diagram_drawing_draw_two_slope_curve(initial_position_specifier: PositionSpecifier, ending_position_specifier: PositionSpecifier, starting_slope: float, ending_slope: float):
        ''''''
        origin = actions.user.diagram_drawing_get_position_from_specifier(initial_position_specifier)
        destination = actions.user.diagram_drawing_get_position_from_specifier(ending_position_specifier)
        actions.user.diagram_drawing_draw_two_slope_curve_between_points(starting_slope, ending_slope, origin, destination)
    
    def diagram_drawing_draw_two_slope_curve_between_saved_positions(starting_slope: float, ending_slope: float):
        ''''''
        origin = actions.user.diagram_drawing_get_saved_position(1)
        destination = actions.user.diagram_drawing_get_saved_position(2)
        actions.user.diagram_drawing_draw_two_slope_curve_between_points(starting_slope, ending_slope, origin, destination)
