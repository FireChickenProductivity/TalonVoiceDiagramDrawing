#The display code is heavily based on the mouse grid code in the knausj_talon repository distributed under the following license:
#"MIT License

# Copyright (c) 2021 Jeff Knaus, Ryan Hileman, Zach Dwiel, Michael Arntzenius, and others

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE."



from talon import canvas, ui, actions
from talon.skia import Paint, Rect

class PositionNumberingDisplay:
    def __init__(self):
        self.screen = None
        self.rect = None
        self.mcanvas = None

    def setup(self):
        origin = actions.user.diagram_drawing_get_canvas_origin()
        ending = actions.user.diagram_drawing_get_canvas_ending()
        if self.mcanvas is not None:
            self.mcanvas.close()
        distance_between_points = origin.distance_from(ending)
        self.mcanvas = canvas.Canvas(0, 0, distance_between_points, distance_between_points)
        self.mcanvas.move(origin.get_horizontal(), origin.get_vertical())
        
    def show(self, positions, text_size = 20):
        self.positions = positions
        self.mcanvas.register("draw", self.draw)
        self.mcanvas.freeze()
        self.text_size = text_size
        return


    def draw(self, canvas):
        paint = canvas.paint
        paint.textsize = self.text_size
        canvas.paint.text_align = canvas.paint.TextAlign.CENTER
        paint.color = "FF0000"
        paint.style = Paint.Style.FILL

        for number, position in enumerate(self.positions, 1):
            canvas.draw_text(
                str(number),
                position.get_horizontal(),
                position.get_vertical() + 20,
            )
    
    def hide(self):
        self.mcanvas.close()
