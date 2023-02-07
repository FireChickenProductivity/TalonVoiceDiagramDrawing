import math
from talon import actions, Module
from .fire_chicken.mouse_position import MousePosition
from .directions import Direction
from .position_storage import store_line_in_main_storage, main_position_storage
from .position_captures import PositionSpecifier
from math import atan2, pi, cos, sin

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

@module.action_class
class Actions:
    def diagram_drawing_draw_line_from_cursor(horizontal: int, vertical: int):
        ''''''
        current_position: MousePosition = MousePosition.current()
        unit_length: int = line_drawing_unit.get()
        position_difference: MousePosition = MousePosition(unit_length*horizontal, -unit_length*vertical)
        destination: MousePosition = current_position + position_difference
        actions.user.diagram_drawing_draw_line(current_position, destination)
        store_line_in_main_storage(current_position, destination)

    def diagram_drawing_draw_line_from_cursor_using_direction_and_amount(direction: Direction, amount: int):
        ''''''
        horizontal: int = direction.horizontal*amount
        vertical: int = direction.vertical*amount
        actions.user.diagram_drawing_draw_line_from_cursor(horizontal, vertical)
    
    def diagram_drawing_draw_line_from_cursor_using_complex_direction_and_amounts(direction: Direction, horizontal: int, vertical: int):
        ''''''
        direction_adjusted_horizontal: int = direction.horizontal*horizontal
        direction_adjusted_vertical: int = direction.vertical*vertical
        actions.user.diagram_drawing_draw_line_from_cursor(direction_adjusted_horizontal, direction_adjusted_vertical)

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
    
    def diagram_drawing_draw_rectangle_around_cursor(horizontal_amount: int, vertical_amount: int):
        ''''''
        current_position: MousePosition = MousePosition.current()
        upper_left, upper_right, bottom_left, bottom_right = compute_rectangle_positions_around_position(horizontal_amount, vertical_amount, current_position)
        draw_rectangle(upper_left, upper_right, bottom_left, bottom_right)
        current_position.go()

    def diagram_drawing_draw_vertically_consecutive_rectangles(horizontal_amount: int, upper_vertical_amount: int, bottom_vertical_amount: int):
        ''''''
        current_position: MousePosition = MousePosition.current()
        upper_left, upper_right, bottom_left, bottom_right = compute_rectangle_positions_around_position(horizontal_amount, upper_vertical_amount + bottom_vertical_amount, current_position)
        draw_rectangle(upper_left, upper_right, bottom_left, bottom_right)
        scaled_upper_vertical_amount = upper_vertical_amount*line_drawing_unit.get()
        upper_bottom_left = upper_left + MousePosition(0, scaled_upper_vertical_amount)
        upper_bottom_right = upper_right + MousePosition(0, scaled_upper_vertical_amount)
        draw_and_store_line_between_points(upper_bottom_left, upper_bottom_right)


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

def draw_arrow(angleInDegrees: float, size: int, position: MousePosition):
    angleInRadians = angleInDegrees*pi/180
    arrow_length_distance: MousePosition = compute_difference_position_with_angle_and_length(angleInRadians, size)
    arrow_tip_position: MousePosition = position + arrow_length_distance
    arrow_halfs_angles = [angleInRadians + 5*pi/4, angleInRadians - 5*pi/4]
    for arrow_half_angle in arrow_halfs_angles:
        draw_arrow_half(arrow_half_angle, size, arrow_tip_position)
    
def draw_arrow_half(angle: float, size: int, arrow_tip: MousePosition):
    arrow_difference = compute_difference_position_with_angle_and_length(angle, size)
    ending: MousePosition = arrow_tip + arrow_difference
    actions.user.diagram_drawing_draw_line(arrow_tip, ending)

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
