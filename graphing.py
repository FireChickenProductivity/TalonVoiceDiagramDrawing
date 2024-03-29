from talon import Module, actions, Context, app, settings
from .fire_chicken.mouse_position import MousePosition
from .fire_chicken.data_storage import JSONFile, Storage
import math
from .text_fields import give_active_text_field_text

module = Module()
module.tag('diagram_drawing_graphing', desc = 'Activate diagram drawing graphing commands')
graphing_context = Context()
circle_drawing_delay_setting_name = 'diagram_drawing_circle_drawing_delay'
circle_drawing_delay = 'user.' + circle_drawing_delay_setting_name
module.setting(
    circle_drawing_delay_setting_name,
    type = float,
    default = 0.02,
    desc = 'How much to pause between points when drawing circles through freestyle drawing'
)
dot_radius_setting_name = 'diagram_drawing_dot_radius'
dot_radius = 'user.' + dot_radius_setting_name
module.setting(
    dot_radius_setting_name,
    type = int,
    default = 7,
    desc = 'The radius of dots'
)

tick_half_size_setting_name = 'diagram_drawing_tick_half_size'
tick_half_size = 'user.' + tick_half_size_setting_name
module.setting(
    tick_half_size_setting_name,
    type = int,
    default = 15,
    desc = 'Half the size of tick marks on graphs'
)

default_tick_spacing_setting_name = 'diagram_drawing_default_tick_spacing'
default_tick_spacing = 'user.' + default_tick_spacing_setting_name
module.setting(
    default_tick_spacing_setting_name,
    type = int,
    default = 30,
    desc = 'The default amount of space between ticks in pixels'
)

axis_length_unit_setting_name = 'diagram_drawing_axis_length_unit'
axis_length_unit = 'user.' + axis_length_unit_setting_name
module.setting(
    axis_length_unit_setting_name,
    type = int,
    default = 30,
    desc = 'The unit for determining axis length in pixels'
)

def draw_dot_circle(center: MousePosition, radius: int, delay: float = 0.02):
    positions = compute_circle_points(center, radius)
    positions[0].go()
    for position in positions:
        position.go()
        actions.sleep(delay)
    positions[0].go()

def draw_open_dot_circle(center: MousePosition, radius: int, delay: float = 0.02):
    positions = compute_circle_points(center, radius)
    positions[0].go()
    actions.user.diagram_drawing_start_freestyle_drawing()
    for position in positions:
        position.go()
        actions.sleep(delay)
    positions[0].go()
    actions.user.diagram_drawing_stop_freestyle_drawing()

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
        self.origin = compute_integer_position(origin)
        self.start = compute_integer_position(start)
        self.ending = compute_integer_position(ending)
        self.tick_spacing = tick_spacing
        self.starting_ticks = []
        self.ending_ticks = []

    def to_json(self):
        representation = {}
        representation['origin'] = str(self.origin)
        representation['start'] = str(self.start)
        representation['ending'] = str(self.ending)
        representation['tick_spacing'] = self.tick_spacing
        representation['starting_ticks'] = self.starting_ticks
        representation['ending_ticks'] = self.ending_ticks
        return representation
    
    @classmethod
    def from_json(cls, representation):
        axis = Axis(MousePosition.from_text(representation['origin']), MousePosition.from_text(representation['start']), MousePosition.from_text(representation['ending']), representation['tick_spacing'])
        axis.starting_ticks = representation['starting_ticks']
        axis.ending_ticks = representation['ending_ticks']
        return axis
    
    def __str__(self) -> str:
        dictionary_representation = self.to_json()
        string_representation = str(dictionary_representation)
        return string_representation
    
    def __repr__(self) -> str:
        return self.__str__()
    
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
        tick_direction_vector: MousePosition = MousePosition(tick_direction_unit_vector.get_horizontal()*settings.get(tick_half_size), tick_direction_unit_vector.get_vertical()*settings.get(tick_half_size))
        tick_start: MousePosition = axis_position + tick_direction_vector
        tick_ending: MousePosition = axis_position - tick_direction_vector
        actions.user.diagram_drawing_draw_line(tick_start, tick_ending)
        tick_label_position: MousePosition = tick_ending + 2*tick_direction_vector
        tick_label_position.go()
        actions.user.diagram_drawing_create_text_field()
        give_active_text_field_text(label)

    def _get_tick_list_with_target_direction(self, *, target_direction_toward_ending):
        if target_direction_toward_ending:
            return self.ending_ticks
        return self.starting_ticks
    
class Graph:
    def __init__(self, origin, dimensions: int = 2):
        self.axes = []
        self.origin = origin
        self.dimensions = dimensions
    
    def to_json(self):
        representation = {}
        representation['origin'] = str(self.origin)
        representation['dimensions'] = self.dimensions
        axes_representation = []
        for axis in self.axes:
            axis_representation = axis.to_json()
            axes_representation.append(axis_representation)
        representation['axes'] = axes_representation
        return representation
    
    @classmethod
    def from_json(cls, representation):
        if representation is None:
            return None
        origin = MousePosition.from_text(representation['origin'])
        dimensions = representation['dimensions']
        graph = Graph(origin, dimensions)
        for axis in representation['axes']:
            graph.axes.append(Axis.from_json(axis))
        return graph

    def __str__(self) -> str:
        return str(self.to_json())
    
    def __repr__(self) -> str:
        return str(self)

    def get_position_along_axes(self, primary_amount, secondary_amount = 0, tertiary_amount = 0) -> MousePosition:
        target_position: MousePosition = self.origin
        amounts_list = [primary_amount, secondary_amount, tertiary_amount]
        for index, axis in enumerate(self.axes):
            target_position = axis.get_position_along_axis_by_amount_from(amounts_list[index], target_position)
        return target_position
    
    def move_mouse_along_axes(self, primary_amount, secondary_amount = 0, tertiary_amount = 0):
        position: MousePosition = self.get_position_along_axes(primary_amount, secondary_amount, tertiary_amount)
        position.go()

    def add_next_axis(self, starting_distance, ending_distance):
        if self.dimensions == 2:
            self.add_next_two_dimensional_axis(starting_distance, ending_distance)
        elif self.dimensions == 3:
            self.add_next_three_dimensional_axis(starting_distance, ending_distance)

    def add_next_two_dimensional_axis(self, starting_distance, ending_distance):
        number_of_axes = len(self.axes)
        if number_of_axes == 0:
            self.add_horizontal_axis(starting_distance, ending_distance)
        elif number_of_axes == 1:
            self.add_vertical_axis(starting_distance, ending_distance)

    def add_next_three_dimensional_axis(self, starting_distance, ending_distance):
        number_of_axes = len(self.axes)
        if number_of_axes == 0:
            self.add_three_dimensional_x_axis(starting_distance, ending_distance)
        elif number_of_axes == 1:
            self.add_three_dimensional_y_axis(starting_distance, ending_distance)
        elif number_of_axes == 2:
            self.add_vertical_axis(starting_distance, ending_distance)

    def add_horizontal_axis(self, starting_distance, ending_distance):
        self.add_axis(-1, 0, starting_distance, ending_distance)
    
    def add_vertical_axis(self, starting_distance, ending_distance):
        self.add_axis(0, 1, starting_distance, ending_distance)
    
    def add_three_dimensional_x_axis(self, starting_distance, ending_distance):
       self.add_axis(1, -1, starting_distance, ending_distance)
    
    def add_three_dimensional_y_axis(self, starting_distance, ending_distance):
        self.add_horizontal_axis(starting_distance, ending_distance)
    
    def add_axis(self, direction_horizontal, direction_vertical, starting_distance, ending_distance):
        unit_vector: MousePosition = compute_unit_vector(MousePosition(direction_horizontal, direction_vertical))
        start: MousePosition = self.origin + position_multiplied_by(unit_vector, starting_distance)
        ending: MousePosition = self.origin - position_multiplied_by(unit_vector, ending_distance)
        axis: Axis = Axis(self.origin, start, ending, settings.get(default_tick_spacing))
        axis.draw()
        self.axes.append(axis)
        
    def get_axes(self):
        return self.axes

def compute_unit_vector(position: MousePosition):
    magnitude = position.distance_from(MousePosition(0, 0))
    new_position: MousePosition = MousePosition(position.get_horizontal()/magnitude, position.get_vertical()/magnitude)
    return new_position

def position_multiplied_by(position: MousePosition, factor):
    result = MousePosition(position.get_horizontal()*factor, position.get_vertical()*factor)
    return result

def compute_integer_position(position: MousePosition) -> MousePosition:
    return MousePosition(int(position.get_horizontal()), int(position.get_vertical()))

@module.action_class
class Actions:
    def diagram_drawing_draw_dot():
        ''''''
        actions.user.diagram_drawing_start_freestyle_drawing()
        current_position = MousePosition.current()
        actions.user.diagram_drawing_store_position(current_position)
        for i in range(settings.get(dot_radius)):
            draw_dot_circle(current_position, i, settings.get(circle_drawing_delay))
        actions.user.diagram_drawing_stop_freestyle_drawing()
    
    def diagram_drawing_draw_open_dot():
        ''''''
        current_position = MousePosition.current()
        actions.user.diagram_drawing_store_position(current_position)
        draw_open_dot_circle(current_position, settings.get(dot_radius), settings.get(circle_drawing_delay))

    def diagram_drawing_new_graph():
        ''''''
        make_new_graph(2)
    
    def diagram_drawing_new_three_dimensional_graph():
        ''''''
        make_new_graph(3)

    def diagram_drawing_finish_graph():
        ''''''
        global current_graph
        current_graph = None
        global graphing_context
        graphing_context.tags = []
        update_graph_file()
    
    def diagram_drawing_add_next_axis(starting_distance: int, ending_distance: int):
        ''''''
        global current_graph
        unit = settings.get(axis_length_unit)
        current_graph.add_next_axis(starting_distance*unit, ending_distance*unit)
        update_graph_file()
    
    def diagram_drawing_go_to_position_along_axes(primary_amount: float, secondary_amount: float = 0, tertiary_amount: float = 0):
        ''''''
        global current_graph
        current_graph.move_mouse_along_axes(primary_amount, secondary_amount, tertiary_amount)
    
    def diagram_drawing_get_position_along_axes(primary_amount: float, secondary_amount: float = 0, tertiary_amount: float = 0) -> MousePosition:
        ''''''
        global current_graph
        position = current_graph.get_position_along_axes(primary_amount, secondary_amount, tertiary_amount)
        return position

    def diagram_drawing_draw_point_at(primary_amount: float, secondary_amount: float = 0, tertiary_amount: float = 0):
        ''''''
        global current_graph
        current_graph.move_mouse_along_axes(primary_amount, secondary_amount, tertiary_amount)
        actions.user.diagram_drawing_draw_dot()
    
    def diagram_drawing_draw_open_point_at(primary_amount: float, secondary_amount: float = 0, tertiary_amount: float = 0):
        ''''''
        global current_graph
        current_graph.move_mouse_along_axes(primary_amount, secondary_amount, tertiary_amount)
        actions.user.diagram_drawing_draw_open_dot()
    
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
    update_graph_file()

def make_new_graph(dimensions: int = 2):
    global current_graph
    current_graph = Graph(MousePosition.current(), dimensions)
    activate_graphing_tag()
    update_graph_file()

def activate_graphing_tag():
    global graphing_context
    graphing_context.tags = ['user.diagram_drawing_graphing']

def update_graph_file():
    global graph_file, current_graph
    graph_file.set(current_graph)

def set_up_graphing_system():
    global storage, graph_file, current_graph, graphing_context, current_axis
    storage = actions.user.diagram_drawing_compute_data_storage()
    graph_file = storage.get_json_file('Graph.json', from_json = Graph.from_json)
    current_graph = graph_file.get()
    if current_graph is not None:
        activate_graphing_tag()
    current_axis = 1

app.register('ready', set_up_graphing_system)
