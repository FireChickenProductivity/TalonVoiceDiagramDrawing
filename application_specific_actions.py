from talon import Module
from ..fire_chicken.mouse_position import MousePosition
module = Module()

@module.action_class
class Actions:
    def diagram_drawing_draw_line(origin: MousePosition, destination: MousePosition):
        ''''''
        pass
    
    def diagram_drawing_activate_text_tool():
        ''''''
        pass

    def diagram_drawing_create_text_field():
        ''''''
        pass

    def diagram_drawing_unselect():
        ''''''
        pass

    def diagram_drawing_edit_text_at_cursor():
        ''''''
        pass

    def diagram_drawing_start_free_style_drawing():
        '''Starts freestyle drawing where moving the cursor draws'''
        pass

    def diagram_drawing_stop_freestyle_drawing():
        '''Stops freestyle drawing where moving the cursor draws'''
        pass
