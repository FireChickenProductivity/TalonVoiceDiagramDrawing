from talon import Module, actions, Context
from .fire_chicken.mouse_position import MousePosition
import math
from .text_fields import give_active_text_field_text

module = Module()
circle_drawing_delay = module.setting(
    'diagram_drawing_circle_drawing_delay',
    type = float,
    default = 0.02,
    desc = 'How much to pause between points when drawing circles through freestyle drawing'
)
dot_radius = module.setting(
    'diagram_drawing_dot_radius',
    type = int,
    default = 7,
    desc = 'The radius of dots'
)

tick_half_size = module.setting(
    'diagram_drawing_tick_half_size',
    type = int,
    default = 15,
    desc = 'Half the size of tick marks on graphs'
)

default_tick_spacing = module.setting(
    'diagram_drawing_default_tick_spacing',
    type = int,
    default = 20,
    desc = 'The default amount of space between ticks in pixels'
)

axis_length_unit = module.setting(
    'diagram_drawing_axis_lengthy_unit',
    type = int,
    default = 20,
    desc = 'The unit for determining axis length in pixels'
)

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

class Axis:
    def __init__(self, origin: MousePosition, start: MousePosition, ending: MousePosition, tick_spacing: int):
        self.origin = origin
        self.start = start
        self.ending = ending
        self.tick_spacing = tick_spacing
        self.starting_ticks = []
        self.ending_ticks = []
    
    def draw(self):
        actions.user.diagram_drawing_draw_line(self.start, self.ending)
    
    def move_mouse_along(self, amount: int):
        target_position = self.get_position_along_axis_by_amount_from(amount, MousePosition.current())
        target_position.go()
    
    def get_position_along_axis_by_amount_from(self, amount, starting_position: MousePosition):
        direction_unit_vector: MousePosition = self.compute_direction_unit_vector()
        change_to_final_position: MousePosition = MousePosition(direction_unit_vector.get_horizontal()*amount*self.tick_spacing, direction_unit_vector.get_vertical()*amount*self.tick_spacing)
        final_position: MousePosition = change_to_final_position + starting_position
        return final_position

    def compute_direction_unit_vector(self):
        direction: MousePosition = self.ending - self.origin
        direction_position_magnitude = direction.distance_from(MousePosition(0, 0))
        direction_unit_vector: MousePosition = MousePosition(direction.get_horizontal()/direction_position_magnitude, direction.get_vertical()/direction_position_magnitude)
        return direction_unit_vector
    
    def add_tick(self, label: str, *, target_direction_toward_ending):
        target_list = self._get_tick_list_with_target_direction(target_direction_toward_ending = target_direction_toward_ending)
        target_list.append(label)
        self._draw_tick(label, target_direction_toward_ending = target_direction_toward_ending)
    
    def _draw_tick(self, label: str, *, target_direction_toward_ending):
        target_list = self._get_tick_list_with_target_direction(target_direction_toward_ending = target_direction_toward_ending)
        ticks_along_axis = len(target_list)
        axis_position_signed_distance = ticks_along_axis
        if target_direction_toward_ending:
            axis_position_signed_distance *= -1
        axis_position: MousePosition = self.get_position_along_axis_by_amount_from(axis_position_signed_distance, self.origin)
        direction_unit_vector: MousePosition = self.compute_direction_unit_vector()
        tick_direction_unit_vector: MousePosition = MousePosition(direction_unit_vector.get_vertical(), -direction_unit_vector.get_horizontal())
        tick_direction_vector: MousePosition = MousePosition(tick_direction_unit_vector.get_horizontal()*tick_half_size.get(), tick_direction_unit_vector.get_vertical()*tick_half_size.get())
        tick_start: MousePosition = axis_position + tick_direction_vector
        tick_ending: MousePosition = axis_position - tick_direction_vector
        actions.user.diagram_drawing_draw_line(tick_start, tick_ending)
        tick_label_position: MousePosition = tick_ending + tick_direction_vector
        tick_label_position.go()
        actions.user.diagram_drawing_create_text_field()
        give_active_text_field_text(label)

    def _get_tick_list_with_target_direction(self, *, target_direction_toward_ending):
        if target_direction_toward_ending:
            return self.ending_ticks
        return self.starting_ticks
    
class Graph:
    def __init__(self, origin):
        self.axes = []
        self.origin = origin
    
    def get_position_along_axes(self, primary_amount, secondary_amount = 0, tertiary_amount = 0) -> MousePosition:
        target_position: MousePosition = self.origin
        amounts_list = [primary_amount, secondary_amount, tertiary_amount]
        for index, axis in enumerate(self.axes):
            target_position = axis.get_position_along_axis_by_amount_from(amounts_list[index], target_position)
        return target_position
    
    def move_mouse_along_axes(self, primary_amount, secondary_amount = 0, tertiary_amount = 0):
        position: MousePosition = self.get_position_along_axes(primary_amount, secondary_amount, tertiary_amount)
        position.go()
    
    def add_axis(self, direction_horizontal, direction_vertical, starting_distance, ending_distance):
        unit_vector: MousePosition = compute_unit_vector(MousePosition(direction_horizontal, direction_vertical))
        start: MousePosition = self.origin + position_multiplied_by(unit_vector, starting_distance)
        ending: MousePosition = self.origin - position_multiplied_by(unit_vector, ending_distance)
        axis: Axis = Axis(self.origin, start, ending, default_tick_spacing.get())
        axis.draw()
        self.axes.append(axis)
    
    def add_horizontal_axis(self, starting_distance, ending_distance):
        self.add_axis(-1, 0, starting_distance, ending_distance)
    
    def add_vertical_axis(self, starting_distance, ending_distance):
        self.add_axis(0, 1, starting_distance, ending_distance)
    
    def add_axis_coming_out(self, starting_distance, ending_distance):
        self.add_axis(1, -1, starting_distance, ending_distance)
    
    def add_next_axis(self, starting_distance, ending_distance):
        number_of_axes = len(self.axes)
        if number_of_axes == 0:
            self.add_horizontal_axis(starting_distance, ending_distance)
        elif number_of_axes == 1:
            self.add_vertical_axis(starting_distance, ending_distance)
        elif number_of_axes == 2:
            self.add_axis_coming_out(starting_distance, ending_distance)
        
    def get_axes(self):
        return self.axes

def compute_unit_vector(position: MousePosition):
    magnitude = position.distance_from(MousePosition(0, 0))
    new_position: MousePosition = MousePosition(position.get_horizontal()/magnitude, position.get_vertical()/magnitude)
    return new_position

def position_multiplied_by(position: MousePosition, factor):
    result = MousePosition(position.get_horizontal()*factor, position.get_vertical()*factor)
    return result

current_graph = None
graphing_context = Context()
module.tag('diagram_drawing_graphing', desc = 'Activate diagram drawing graphing commands')
current_axis = 1
@module.action_class
class Actions:
    def diagram_drawing_draw_dot():
        ''''''
        actions.user.diagram_drawing_start_freestyle_drawing()
        current_position = MousePosition.current()
        for i in range(dot_radius.get()):
            draw_dot_circle(current_position, i, circle_drawing_delay.get())
        actions.user.diagram_drawing_stop_freestyle_drawing()
    
    def diagram_drawing_new_graph():
        ''''''
        global current_graph
        current_graph = Graph(MousePosition.current())
        global graphing_context
        graphing_context.tags = ['user.diagram_drawing_graphing']
    
    def diagram_drawing_finish_graph():
        ''''''
        global current_graph
        current_graph = []
        global graphing_context
        graphing_context.tags = []
    
    def diagram_drawing_add_next_axis(starting_distance: int, ending_distance: int):
        ''''''
        global current_graph
        unit = axis_length_unit.get()
        current_graph.add_next_axis(starting_distance*unit, ending_distance*unit)
    
    def diagram_drawing_go_to_position_along_axes(primary_amount: float, secondary_amount: float = 0, tertiary_amount: float = 0):
        ''''''
        global current_graph
        current_graph.move_mouse_along_axes(primary_amount, secondary_amount, tertiary_amount)

    def diagram_drawing_draw_point_at(primary_amount: float, secondary_amount: float = 0, tertiary_amount: float = 0):
        ''''''
        global current_graph
        current_graph.move_mouse_along_axes(primary_amount, secondary_amount, tertiary_amount)
        actions.user.diagram_drawing_draw_dot()
    
    def diagram_drawing_edit_axis(number: int):
        ''''''
        global current_axis
        if number > 0 and number < 4:
            current_axis = number
    
    def diagram_drawing_add_start_tick(label: str):
        ''''''
        global current_axis
        add_tick(current_axis, label, target_direction_toward_ending = False)
    
    def diagram_drawing_add_tail_tick(label: str):
        ''''''
        global current_axis
        add_tick(current_axis, label, target_direction_toward_ending = True)

def add_tick(axis_number, label, *, target_direction_toward_ending):
    global current_graph
    axis = current_graph.get_axes()[axis_number - 1]
    axis.add_tick(label, target_direction_toward_ending = target_direction_toward_ending)
