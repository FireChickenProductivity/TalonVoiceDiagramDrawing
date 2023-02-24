from talon import Context, actions, Module, ctrl
from ...fire_chicken.mouse_position import MousePosition
from typing import List

module = Module()
module.tag('inkscape', desc = 'Activates drawing commands for inkscape')

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
        pass

    def diagram_drawing_create_text_field():
        ''''''
        actions.user.diagram_drawing_unselect()
        actions.key('t')
        left_click()
    
    def diagram_drawing_unselect():
        ''''''
        actions.key('escape')
    
    def diagram_drawing_edit_text_at_cursor():
        ''''''
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

def left_click():
    actions.mouse_click(0)

def right_click():
    actions.mouse_click(1)

def activate_pencil_tool():
    actions.key('p')

def hold_left_mouse_button_down():
    ctrl.mouse_click(button=0, down=True)

def release_left_mouse_button():
    ctrl.mouse_click(button=0, up=True)
