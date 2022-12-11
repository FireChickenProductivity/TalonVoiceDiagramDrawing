from talon import Context, actions, Module
from ....fire_chicken.mouse_position import MousePosition

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

def activate_line_drawing_tool():
    actions.key('v')

def left_click():
    actions.mouse_click(0)
