from talon import Module, actions
from .fire_chicken.mouse_position import MousePosition
import math

def draw_dot_circle(center: MousePosition, radius: int, delay: float = 0.02):
    positions = compute_circle_points(center, radius)
    positions[0].go()
    for position in positions:
        position.go()
        actions.sleep(delay)
    positions[0].go()

def compute_circle_points(center: MousePosition, radius: int):
    circle_top_half = compute_circle_top_half_points(center, radius)
    circle_bottom_half = compute_position_array_flipped_around_horizontal(circle_top_half, center.get_vertical())
    circle_bottom_half.reverse()
    result = []
    result.extend(circle_top_half)
    result.extend(circle_bottom_half)
    return result

def compute_circle_top_half_points(center: MousePosition, radius: int):
    points = []
    for horizontal in range(center.get_horizontal() - radius, center.get_horizontal() + radius + 1):
        points.append(compute_semi_circle_point(center, radius, horizontal))
    return points

def compute_semi_circle_point(center: MousePosition, radius: int, horizontal: int):
    vertical = math.sqrt(radius*radius - (horizontal - center.get_horizontal())**2) + center.get_vertical()
    point = MousePosition(horizontal, vertical)
    return point

def compute_position_array_flipped_around_horizontal(positions, horizontal_height: int):
    result = []
    for position in positions:
        flipped_position = MousePosition(position.get_horizontal(), horizontal_height - (position.get_vertical() - horizontal_height))
        result.append(flipped_position)
    return result

module = Module()
@module.action_class
class Actions:
    def diagram_drawing_draw_dot(radius: int = 7):
        ''''''
        actions.user.diagram_drawing_start_freestyle_drawing()
        current_position = MousePosition.current()
        for i in range(radius):
            draw_dot_circle(current_position, i)
        actions.user.diagram_drawing_stop_freestyle_drawing()