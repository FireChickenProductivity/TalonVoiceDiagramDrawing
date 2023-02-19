import math
from talon import actions, Module
from .fire_chicken.mouse_position import MousePosition
from .directions import Direction
from .position_storage import store_line_in_main_storage
from .position_captures import PositionSpecifier
from .curves import compute_line_points, draw_curve_dashed, draw_points
from math import atan2, pi, cos, sin
from typing import Union

module = Module()
line_drawing_unit = module.setting(
    'diagram_drawing_line_drawing_unit',
    type = int,
    default = 20,
    desc = 'The unit length for line drawing'
)
cross_out_size = module.setting(
    'diagram_drawing_cross_out_size',
    type = int,
    default = 80,
    desc = 'The size of the cross out lines'
)
double_rectangle_thickness = module.setting(
    'diagram_drawing_double_rectangle_thickness',
    type = int,
    default = 6,
    desc = 'The distance between double rectangles'
)

@module.action_class
class Actions:
    def diagram_drawing_draw_line_from_cursor(horizontal: int, vertical: int):
        ''''''
        current_position: MousePosition = MousePosition.current()
        destination: MousePosition = current_position + compute_scaled_position_difference(horizontal, -vertical)
        actions.user.diagram_drawing_draw_line(current_position, destination)
        store_line_in_main_storage(current_position, destination)
    
    def diagram_drawing_draw_dashed_line_from_cursor(horizontal: int, vertical: int):
        ''''''
        current_position: MousePosition = MousePosition.current()  
        destination: MousePosition = current_position + compute_scaled_position_difference(horizontal, -vertical)
        line_points = compute_line_points(current_position, destination)
        draw_curve_dashed(line_points)
        store_line_in_main_storage(current_position, destination)
    
    def diagram_drawing_draw_line_from_cursor_using_direction_and_amount(direction: Direction, amount: int):
        ''''''
        draw_line_with_direction_and_amount(direction, amount, line_drawing_from_cursor_function = actions.user.diagram_drawing_draw_line_from_cursor)
    
    def diagram_drawing_draw_dashed_line_from_cursor_using_direction_and_amount(direction: Direction, amount: int):
        ''''''
        draw_line_with_direction_and_amount(direction, amount, line_drawing_from_cursor_function = actions.user.diagram_drawing_draw_dashed_line_from_cursor)

    def diagram_drawing_draw_line_from_cursor_using_complex_direction_and_amounts(direction: Direction, horizontal: int, vertical: int):
        ''''''
        draw_line_from_cursor_using_complex_direction_and_amounts(direction, horizontal, vertical, actions.user.diagram_drawing_draw_line_from_cursor)
    
    def diagram_drawing_draw_dashed_line_from_cursor_using_complex_direction_and_amounts(direction: Direction, horizontal: int, vertical: int):
        ''''''
        draw_line_from_cursor_using_complex_direction_and_amounts(direction, horizontal, vertical, actions.user.diagram_drawing_draw_dashed_line_from_cursor)

    def diagram_drawing_draw_line_between_named_positions(origin_position_specifier: PositionSpecifier, destination_position_specifier: PositionSpecifier):
        ''''''
        origin = actions.user.diagram_drawing_get_position_from_specifier(origin_position_specifier)
        destination = actions.user.diagram_drawing_get_position_from_specifier(destination_position_specifier)
        actions.user.diagram_drawing_draw_line(origin, destination)
        store_line_in_main_storage(origin, destination)
    
    def diagram_drawing_draw_line_between_named_positions_with_label(origin_position_specifier: PositionSpecifier, destination_position_specifier: PositionSpecifier, label: str):
        ''''''
        actions.user.diagram_drawing_draw_line_between_named_positions(origin_position_specifier, destination_position_specifier)
        label_average_named_position_with(origin_position_specifier, destination_position_specifier, label)
    
    def draw_parallel_lines_around_named_positions_with_gap(origin_position_specifier: PositionSpecifier, destination_position_specifier: PositionSpecifier, gap: int):
        ''''''
        origin: MousePosition = actions.user.diagram_drawing_get_position_from_specifier(origin_position_specifier)
        destination: MousePosition = actions.user.diagram_drawing_get_position_from_specifier(destination_position_specifier)
        direction_vector: MousePosition = destination - origin
        direction_angle = atan2(direction_vector.get_vertical(), direction_vector.get_horizontal())
        first_line_offset = compute_difference_position_with_angle_and_length(direction_angle + pi/2, gap)
        second_line_offset = compute_difference_position_with_angle_and_length(direction_angle - pi/2, gap)
        for offset in [first_line_offset, second_line_offset]:
            draw_and_store_line_between_points(origin + offset, destination + offset)

    def diagram_drawing_draw_vector(origin: MousePosition, destination: MousePosition):
        ''''''
        draw_and_store_line_between_points(origin, destination)
        draw_arrow_after_line(origin, destination)

    def diagram_drawing_draw_vector_between_named_positions(origin_position_specifier: PositionSpecifier, destination_position_specifier: PositionSpecifier):
        ''''''
        origin = actions.user.diagram_drawing_get_position_from_specifier(origin_position_specifier)
        destination = actions.user.diagram_drawing_get_position_from_specifier(destination_position_specifier)
        draw_and_store_line_between_points(origin, destination)
        draw_arrow_after_line(origin, destination)

    def diagram_drawing_draw_vector_between_named_positions_with_label(origin_position_specifier: PositionSpecifier, destination_position_specifier: PositionSpecifier, label: str):
        ''''''
        actions.user.diagram_drawing_draw_vector_between_named_positions(origin_position_specifier, destination_position_specifier)
        label_average_named_position_with(origin_position_specifier, destination_position_specifier, label)
    
    def diagram_drawing_cross_out_named_position(position_specifier: PositionSpecifier):
        ''''''
        position = actions.user.diagram_drawing_get_position_from_specifier(position_specifier)
        cross_out_at_position(position)

    def diagram_drawing_draw_arrowhead_at_cursor(angleInDegrees: float, length: int = 10):
        ''''''
        draw_arrow(angleInDegrees, length, MousePosition.current())
    
    def diagram_drawing_draw_triangle_arrowhead_at_cursor(angleInDegrees: float, length: int = 30):
        ''''''
        draw_triangle_arrowhead(angleInDegrees, length, MousePosition.current(), 190)
    
    def diagram_drawing_draw_filled_in_triangle_arrowhead_with_tail(angle_in_degrees: float, length: int = 15, tail_length: int = 10):
        ''''''
        draw_filled_in_triangle_arrowhead_with_tail(angle_in_degrees, length, tail_length, MousePosition.current(), 190)
    
    def diagram_drawing_draw_rectangle_around_cursor(horizontal_amount: Union[int, float], vertical_amount: Union[int, float]):
        ''''''
        current_position: MousePosition = MousePosition.current()
        upper_left, upper_right, bottom_left, bottom_right = compute_rectangle_positions_around_position(horizontal_amount, vertical_amount, current_position)
        draw_rectangle(upper_left, upper_right, bottom_left, bottom_right)
        current_position.go()
    
    def diagram_drawing_draw_double_rectangle_around_cursor(horizontal_amount: int, vertical_amount: int):
        ''''''
        actions.user.diagram_drawing_draw_rectangle_around_cursor(horizontal_amount, vertical_amount)
        scaled_thickness = double_rectangle_thickness.get()/line_drawing_unit.get()
        actions.user.diagram_drawing_draw_rectangle_around_cursor(horizontal_amount + scaled_thickness, vertical_amount + scaled_thickness)

    def diagram_drawing_draw_vertically_consecutive_rectangles(horizontal_amount: int, upper_vertical_amount: int, bottom_vertical_amount: int):
        ''''''
        current_position: MousePosition = MousePosition.current()
        upper_left, upper_right, bottom_left, bottom_right = compute_rectangle_positions_around_position(horizontal_amount, upper_vertical_amount + bottom_vertical_amount, current_position)
        draw_rectangle(upper_left, upper_right, bottom_left, bottom_right)
        scaled_upper_vertical_amount = upper_vertical_amount*line_drawing_unit.get()
        upper_bottom_left = upper_left + MousePosition(0, scaled_upper_vertical_amount)
        upper_bottom_right = upper_right + MousePosition(0, scaled_upper_vertical_amount)
        draw_and_store_line_between_points(upper_bottom_left, upper_bottom_right)

    def diagram_drawing_draw_vertically_consecutive_rectangles_within_rectangle(horizontal_amount: int, upper_vertical_amount: int, bottom_vertical_amount: int):
        ''''''
        scaled_thickness = double_rectangle_thickness.get()/line_drawing_unit.get()
        actions.user.diagram_drawing_draw_rectangle_around_cursor(horizontal_amount + scaled_thickness, upper_vertical_amount + bottom_vertical_amount + scaled_thickness)
        actions.user.diagram_drawing_draw_vertically_consecutive_rectangles(horizontal_amount, upper_vertical_amount, bottom_vertical_amount)

    def diagram_drawing_draw_diamond_around_cursor(horizontal_amount: float, vertical_amount: float):
        ''''''
        scaled_horizontal = horizontal_amount*line_drawing_unit.get()
        scaled_vertical = vertical_amount*line_drawing_unit.get()
        current_position: MousePosition = MousePosition.current()
        left = current_position + MousePosition(-scaled_horizontal, 0)
        right = current_position + MousePosition(scaled_horizontal, 0)
        top = current_position + MousePosition(0, -scaled_vertical)
        bottom = current_position + MousePosition(0, scaled_vertical)
        draw_and_store_line_between_points(left, top)
        draw_and_store_line_between_points(top, right)
        draw_and_store_line_between_points(right, bottom)
        draw_and_store_line_between_points(bottom, left)
        current_position.go()
    
    def diagram_drawing_draw_double_diamond_around_cursor(horizontal_amount: int, vertical_amount: int):
        ''''''
        actions.user.diagram_drawing_draw_diamond_around_cursor(horizontal_amount, vertical_amount)
        actions.user.diagram_drawing_draw_diamond_around_cursor(horizontal_amount + 0.5, vertical_amount + 0.5*vertical_amount/horizontal_amount)

def compute_scaled_position_difference(horizontal: int, vertical: int):
    return MousePosition(horizontal, vertical)*line_drawing_unit.get()

def draw_line_with_direction_and_amount(direction: Direction, amount: int, line_drawing_from_cursor_function):
    horizontal: int = direction.horizontal*amount
    vertical: int = direction.vertical*amount
    line_drawing_from_cursor_function(horizontal, vertical)

def draw_line_from_cursor_using_complex_direction_and_amounts(direction: Direction, horizontal: int, vertical: int, line_drawing_from_cursor_function):
        ''''''
        direction_adjusted_horizontal: int = direction.horizontal*horizontal
        direction_adjusted_vertical: int = direction.vertical*vertical
        line_drawing_from_cursor_function(direction_adjusted_horizontal, direction_adjusted_vertical)

def compute_rectangle_positions_around_position(horizontal_amount: int, vertical_amount: int, position: MousePosition):
    scaled_horizontal = horizontal_amount*line_drawing_unit.get()
    scaled_vertical = vertical_amount*line_drawing_unit.get()
    upper_left: MousePosition = MousePosition(-scaled_horizontal, -scaled_vertical) + position
    upper_right: MousePosition = MousePosition(scaled_horizontal, -scaled_vertical) + position
    bottom_left: MousePosition = MousePosition(-scaled_horizontal, scaled_vertical) + position
    bottom_right: MousePosition = MousePosition(scaled_horizontal, scaled_vertical) + position
    return upper_left, upper_right, bottom_left, bottom_right

def draw_rectangle(upper_left, upper_right, bottom_left, bottom_right):
    draw_and_store_line_between_points(upper_left, upper_right)
    draw_and_store_line_between_points(upper_right, bottom_right)
    draw_and_store_line_between_points(bottom_right, bottom_left)
    draw_and_store_line_between_points(bottom_left, upper_left)

def draw_and_store_line_between_points(origin: MousePosition, destination: MousePosition):
    actions.user.diagram_drawing_draw_line(origin, destination)
    store_line_in_main_storage(origin, destination)

def draw_arrow_after_line(origin: MousePosition, destination: MousePosition):
    draw_arrow_half_after_line(origin, destination, 5*pi/4)
    draw_arrow_half_after_line(origin, destination, -5*pi/4)

def draw_arrow_half_after_line(origin: MousePosition, destination: MousePosition, angle_addition: float):
    position_difference = destination - origin
    position_difference_angle = atan2(-position_difference.get_vertical(), position_difference.get_horizontal())
    arrow_part_angle = position_difference_angle + angle_addition
    arrow_part_length = position_difference.distance_from(MousePosition(0, 0))//8 + 3
    arrow_difference = compute_difference_position_with_angle_and_length(arrow_part_angle, arrow_part_length)
    actions.user.diagram_drawing_draw_line(destination, destination + arrow_difference)

def draw_arrow(angle_in_degrees: float, size: int, position: MousePosition, angle_difference: float = 225):
    angle_in_radians = math.radians(angle_in_degrees)
    angle_difference_in_radians = math.radians(angle_difference)
    arrow_tip_position: MousePosition = compute_arrow_tip_position(angle_in_radians, size, position)
    for arrow_half_angle in compute_arrow_half_angles(angle_in_radians, angle_difference_in_radians):
        draw_arrow_half(arrow_half_angle, size, arrow_tip_position)

def draw_triangle_arrowhead(angle_in_degrees: float, size: int, position: MousePosition, angle_difference: float = 225):
    angle_in_radians = math.radians(angle_in_degrees)
    angle_difference_in_radians = math.radians(angle_difference)
    arrow_tip_position: MousePosition = compute_arrow_tip_position(angle_in_radians, size, position)
    arrow_half_angles = compute_arrow_half_angles(angle_in_radians, angle_difference_in_radians)
    first_arrow_half_ending = compute_arrow_half_ending(arrow_half_angles[0], size, arrow_tip_position)
    second_arrow_half_ending = compute_arrow_half_ending(arrow_half_angles[1], size, arrow_tip_position)
    draw_consecutive_lines([arrow_tip_position, first_arrow_half_ending, second_arrow_half_ending])

def draw_filled_in_triangle_arrowhead_with_tail(angle_in_degrees: float, arrowhead_size: int, tail_size: int, position: MousePosition, angle_difference: float):
    original_position = MousePosition.current()
    angle_in_radians = math.radians(angle_in_degrees)
    angle_difference_in_radians = math.radians(angle_difference)
    arrow_tip_position: MousePosition = compute_arrow_tip_position(angle_in_radians, arrowhead_size, position)
    arrow_half_angles = compute_arrow_half_angles(angle_in_radians, angle_difference_in_radians)
    arrow_half_size = arrowhead_size + tail_size
    first_arrowhead_ending = compute_arrow_half_ending(arrow_half_angles[0], arrow_half_size, arrow_tip_position)
    second_arrowhead_ending = compute_arrow_half_ending(arrow_half_angles[1], arrow_half_size, arrow_tip_position)
    actions.user.diagram_drawing_draw_filled_in_line_shape([arrow_tip_position, first_arrowhead_ending, position, second_arrowhead_ending])
    original_position.go()
    
def compute_angle_between_positions(start: MousePosition, destination: MousePosition):
    change = destination - start
    angle = math.atan2(change.get_vertical(), change.get_horizontal())
    return angle

def compute_arrow_tip_position(angle: float, size: int, starting_position: MousePosition):
    arrow_length_difference: MousePosition = compute_difference_position_with_angle_and_length(angle, size)
    arrow_tip_position: MousePosition = starting_position + arrow_length_difference
    return arrow_tip_position

def compute_arrow_half_angles(arrow_angle: float, angle_difference: float):
    return [arrow_angle + angle_difference, arrow_angle - angle_difference]

def draw_arrow_half(angle: float, size: int, arrow_tip: MousePosition):
    ending: MousePosition = compute_arrow_half_ending(angle, size, arrow_tip)
    actions.user.diagram_drawing_draw_line(arrow_tip, ending)

def compute_arrow_half_ending(angle: float, size: int, arrow_tip: MousePosition):
    arrow_difference = compute_difference_position_with_angle_and_length(angle, size)
    ending: MousePosition = arrow_tip + arrow_difference
    return ending

def compute_difference_position_with_angle_and_length(angle: float, length: int):
    horizontal = int(cos(angle)*length)
    vertical = int(-sin(angle)*length )
    position = MousePosition(horizontal, vertical)
    return position

def cross_out_at_position(position: MousePosition):
    half_cross_out_size = cross_out_size.get()/2
    first_line_start = MousePosition(-half_cross_out_size, -half_cross_out_size) + position
    first_line_ending = MousePosition(half_cross_out_size, half_cross_out_size) + position
    second_line_start = MousePosition(half_cross_out_size, -half_cross_out_size) + position
    second_line_ending = MousePosition(-half_cross_out_size, half_cross_out_size) + position
    actions.user.diagram_drawing_draw_line(first_line_start, first_line_ending)
    actions.user.diagram_drawing_draw_line(second_line_start, second_line_ending)

def compute_position_average(position1: MousePosition, position2: MousePosition):
    average = MousePosition(computer_average(position1.get_horizontal(), position2.get_horizontal()), computer_average(position1.get_vertical(), position2.get_vertical()))
    return average

def computer_average(number1, number2):
    average = (number1 + number2)/2
    return average

def label_average_named_position_with(origin_position_specifier: PositionSpecifier, destination_position_specifier: PositionSpecifier, label: str):
    origin = actions.user.diagram_drawing_get_position_from_specifier(origin_position_specifier)
    destination = actions.user.diagram_drawing_get_position_from_specifier(destination_position_specifier)
    middle_position = compute_position_average(origin, destination)
    middle_position.go()
    actions.user.diagram_drawing_create_text_field()
    actions.insert(label)
    actions.user.diagram_drawing_unselect()

def draw_consecutive_lines(positions, *, store_positions = True):
    starting_position = positions[-1]
    for position in positions:
        ending_position = position
        actions.user.diagram_drawing_draw_line(starting_position, ending_position)
        if store_positions:
            store_line_in_main_storage(starting_position, ending_position)
        starting_position = ending_position
