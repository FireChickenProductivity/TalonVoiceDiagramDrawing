from talon import Context, actions, Module, ctrl, settings
from ...fire_chicken.mouse_position import MousePosition
from typing import List
from .application_specific_utilities import fill_in_current_continuous_line_shape
from ...graphing import dot_radius

module = Module()
module.tag('vectr', desc = 'Activates drawing commands for vectr')

context = Context()
context.matches = r'''
tag: user.vectr
'''
@context.action_class('user')
class Actions:
    def diagram_drawing_draw_line(origin: MousePosition, destination: MousePosition):
        ''''''
        actions.user.diagram_drawing_unselect()
        origin.go()
        activate_line_drawing_tool()
        left_click()
        destination.go()
        left_click()
        actions.user.diagram_drawing_unselect()
    
    def diagram_drawing_draw_filled_in_line_shape(positions: List):
        ''''''
        actions.user.diagram_drawing_unselect()
        activate_line_drawing_tool()
        for position in positions:
            position.go()
            left_click()
        positions[0].go()
        left_click()
        fill_in_current_continuous_line_shape()
        actions.user.diagram_drawing_unselect()

    def diagram_drawing_create_text_field():
        ''''''
        actions.user.diagram_drawing_unselect()
        actions.key('t')
        left_click()
    
    def diagram_drawing_unselect():
        ''''''
        actions.key('escape:2')
    
    def diagram_drawing_edit_text_at_cursor():
        ''''''
        left_click()
        left_click()
    
    def diagram_drawing_start_freestyle_drawing():
        ''''''
        actions.user.diagram_drawing_unselect()
        toggle_pencil_tool()
        hold_left_mouse_button_down()
    
    def diagram_drawing_stop_freestyle_drawing():
        ''''''
        release_left_mouse_button()
        toggle_pencil_tool()
        actions.user.diagram_drawing_unselect()
    
    def diagram_drawing_get_drawing_application_name() -> str:
        ''''''
        return 'Vectr'
    
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
        actions.key('shift:up')
        release_left_mouse_button()
        actions.user.diagram_drawing_unselect()

def activate_line_drawing_tool():
    actions.key('v')

def left_click():
    actions.mouse_click(0)

def toggle_pencil_tool():
    actions.key('p')

def activate_ellipse_tool():
    actions.key('e')

def hold_left_mouse_button_down():
    ctrl.mouse_click(button=0, down=True)

def release_left_mouse_button():
    ctrl.mouse_click(button=0, up=True)
