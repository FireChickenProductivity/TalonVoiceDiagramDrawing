from talon import Context, actions, Module, ctrl, settings
from ...fire_chicken.mouse_position import MousePosition
from typing import List
from ...graphing import dot_radius

module = Module()
module.tag('inkscape', desc = 'Activates drawing commands for inkscape')

inkscape_filled_in_shape_drawing_delay_setting_name = 'diagram_drawing_inkscape_filled_in_shape_drawing_delay'
inkscape_filled_in_shape_drawing_delay = 'user.' + inkscape_filled_in_shape_drawing_delay_setting_name
module.setting(
    inkscape_filled_in_shape_drawing_delay_setting_name,
    type = int,
    default = 100,
    desc = 'How long to pause in milliseconds at various points of drawing a filled in shape in inkscape. Consider making this longer if drawing filled in shapes in inkscape is not working.'
)

inkscape_dot_drawing_delay_setting_name = 'diagram_drawing_inkscape_dot_drawing_delay'
inkscape_dot_drawing_delay = 'user.' + inkscape_dot_drawing_delay_setting_name
module.setting(
    inkscape_dot_drawing_delay_setting_name,
    type = int,
    default = 500,
    desc = 'How long to pause in milliseconds when drawing a dot in inkscape. '
)

context = Context()
context.matches = r'''
tag: user.inkscape
'''
@context.action_class('user')
class Actions:
    def diagram_drawing_draw_line(origin: MousePosition, destination: MousePosition):
        ''''''
        actions.user.diagram_drawing_unselect()
        origin.go()
        activate_pencil_tool()
        left_click()
        destination.go()
        left_click()
        actions.user.diagram_drawing_unselect()

    def diagram_drawing_draw_filled_in_line_shape(positions: List):
        ''''''
        actions.user.diagram_drawing_unselect()
        activate_straight_line_tool()
        for position in positions:
            position.go()
            wait_filled_in_shape_drawing_delay()
            left_click()
        positions[0].go()
        wait_filled_in_shape_drawing_delay()
        left_click()
        wait_filled_in_shape_drawing_delay()
        fill_position = actions.user.diagram_drawing_get_application_specific_data_storage_position('fill')
        fill_position.go()
        left_click()
        actions.user.diagram_drawing_unselect()

    def diagram_drawing_create_text_field():
        ''''''
        actions.user.diagram_drawing_unselect()
        activate_text_tool()
        left_click()
    
    def diagram_drawing_unselect():
        ''''''
        actions.key('escape')
        activate_selection_tool()
    
    def diagram_drawing_edit_text_at_cursor():
        ''''''
        actions.user.diagram_drawing_unselect()
        activate_text_tool()
        left_click()
    
    def diagram_drawing_start_freestyle_drawing():
        ''''''
        actions.user.diagram_drawing_unselect()
        activate_pencil_tool()
        hold_left_mouse_button_down()
    
    def diagram_drawing_stop_freestyle_drawing():
        ''''''
        release_left_mouse_button()
        actions.user.diagram_drawing_unselect()
    
    def diagram_drawing_get_drawing_application_name() -> str:
        ''''''
        return 'inkscape'
    
        #overrides
    def diagram_drawing_draw_dot():
        ''''''
        actions.user.diagram_drawing_unselect()
        activate_ellipse_tool()
        actions.key('shift:down')
        hold_left_mouse_button_down()
        original_mouse_position = MousePosition.current()
        target_mouse_position = original_mouse_position + MousePosition(settings.get(dot_radius), settings.get(dot_radius))
        target_mouse_position.go()
        wait_setting_delay(inkscape_dot_drawing_delay)
        actions.key('shift:up')
        release_left_mouse_button()
        actions.user.diagram_drawing_unselect()
        original_mouse_position.go()

def left_click():
    actions.mouse_click(0)

def activate_pencil_tool():
    actions.key('p')

def activate_text_tool():
    actions.key('t')

def activate_selection_tool():
    actions.key('s')

def activate_straight_line_tool():
    actions.key('b')

def activate_ellipse_tool():
    actions.key('e')

def hold_left_mouse_button_down():
    ctrl.mouse_click(button=0, down=True)

def release_left_mouse_button():
    ctrl.mouse_click(button=0, up=True)

def wait_filled_in_shape_drawing_delay():
    wait_setting_delay(inkscape_filled_in_shape_drawing_delay)

def wait_setting_delay(setting):
    actions.sleep(f'{settings.get(setting)}ms')
