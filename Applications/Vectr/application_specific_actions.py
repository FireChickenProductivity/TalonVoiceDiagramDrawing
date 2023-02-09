from talon import Context, actions, Module, ctrl
from ...fire_chicken.mouse_position import MousePosition

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

def activate_line_drawing_tool():
    actions.key('v')

def left_click():
    actions.mouse_click(0)

def toggle_pencil_tool():
    actions.key('p')

def hold_left_mouse_button_down():
    ctrl.mouse_click(button=0, down=True)

def release_left_mouse_button():
    ctrl.mouse_click(button=0, up=True)
