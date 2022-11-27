from talon import Module, Context, imgui

module = Module()
module.tag('diagram_drawing_confirmation', desc = 'Activates are you sure commands')

class ConfirmationState:
    def __init__(self):
        self.context = SingleTagContext('user.diagram_drawing_confirmation')
    
    def request_confirmation(self, message: str, on_confirmation, on_disconfirmation):
        self.on_confirmation = on_confirmation
        self.on_disconfirmation = on_disconfirmation
        self.message = message
        self.context.on()
        gui.show()
    
    def confirm(self):
        self.on_confirmation()
        self.cleanup()
    
    def disconfirm(self):
        self.on_disconfirmation()
        self.cleanup()

    def cleanup(self):
        self.context.off()
        self.on_confirmation = None
        self.on_disconfirmation = None
        self.message = None
        gui.hide()

    def get_message(self) -> str:
        return self.message

class SingleTagContext:
    def __init__(self, tag_name: str):
        self.tag_name = tag_name
        self.context = Context()
    
    def on(self):
        self.context.tags = [self.tag_name]
    
    def off(self):
        self.context.tags = []
    
confirmation = ConfirmationState()

@imgui.open(y=0)
def gui(gui: imgui.GUI):
    gui.text(confirmation.get_message())
    gui.line()
    gui.text('Yes I am sure')
    gui.text('No')

@module.action_class
class Actions:
    def diagram_drawing_confirm():
        ''''''
        confirmation.confirm()
    
    def diagram_drawing_disconfirm():
        ''''''
        confirmation.disconfirm()
