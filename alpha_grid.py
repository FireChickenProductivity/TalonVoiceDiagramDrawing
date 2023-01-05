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



#The original alpha grid for the diagram drawing commands was written by whatIV

from talon import canvas, ui, Module, actions
from talon.skia import Paint, Rect
from .fire_chicken.mouse_position import MousePosition
from .fire_chicken.data_storage import RelativeStorage

class AlphaGrid:
    def __init__(self):
        self.screen = None
        self.rect = None
        self.mcanvas = None
        self.grid_labels = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        self.showing = False

    def setup(self, text_size):
        # draw_grid_lines - if true draw grid lines
        # upper left corner position1
        self.position1 = actions.user.diagram_drawing_get_canvas_origin()
        self.position2 = actions.user.diagram_drawing_get_canvas_ending()
        if self.mcanvas is not None:
            self.mcanvas.close()
        distance_between_points = self.position1.distance_from(self.position2)
        distance_away_from_canvas_for_text = text_size*20
        self.mcanvas = canvas.Canvas(-distance_away_from_canvas_for_text, -distance_away_from_canvas_for_text, distance_between_points + distance_away_from_canvas_for_text, distance_between_points + distance_away_from_canvas_for_text)
        self.mcanvas.move(self.position1.get_horizontal() - distance_away_from_canvas_for_text, self.position1.get_vertical() - distance_away_from_canvas_for_text)
       
    def show(self, text_size = 20):
        self.setup(text_size)
        self.showing = True
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
        num_chars = len(self.grid_labels)
        delta_vertical = (self.position2.vertical - self.position1.vertical)/(num_chars + 1)
        delta_horizontal = (self.position2.horizontal - self.position1.horizontal)/(num_chars + 1)

        for i in range(num_chars):
            x = self.position1.horizontal + int((i + 1) * delta_horizontal)
            y = self.position1.vertical + int((i + 1) * delta_vertical)
            # top label
            canvas.draw_text(
                self.grid_labels[i],
                x,
                self.position1.vertical,
            )
            # bottom label
            canvas.draw_text(
                self.grid_labels[i],
                x,
                self.position2.vertical,
            )
            # left label
            canvas.draw_text(
                self.grid_labels[i],
                self.position1.horizontal,
                y,
            )
            canvas.draw_text(
                self.grid_labels[i],
                self.position2.horizontal,
                y,
            )
            if show_grid_lines_file.get():
                # Draw horizontal lines
                canvas.draw_line(
                    self.position1.horizontal,
                    y,
                    self.position2.horizontal,
                    y,
                )
                # Draw vertical lines
                canvas.draw_line(
                    x,
                    self.position1.vertical,
                    x,
                    self.position2.vertical,
                )
           
    def get_position(self, ychar: str, xchar: str):
        num_chars = len(self.grid_labels)
        x_pos = self.position1.horizontal + int((self.grid_labels.index(xchar)+1)*(self.position2.horizontal - self.position1.horizontal)/(num_chars + 1))
        y_pos = self.position1.vertical + int((self.grid_labels.index(ychar)+1)*(self.position2.vertical - self.position1.vertical)/(num_chars + 1))
        pos = MousePosition(x_pos,y_pos)
        return pos

    def hide(self):
        self.showing = False
        self.mcanvas.close()

    def is_showing(self):
        return self.showing
    
    def refresh(self):
        if self.is_showing():
            self.hide()
            self.show()

grid = AlphaGrid()

storage = RelativeStorage(__file__, 'data')
show_grid_lines_file = storage.get_boolean_file('ShowAlphaGridLines.txt')

module = Module()
@module.action_class
class Actions:
    def diagram_drawing_show_alpha_grid():
        ''''''
        grid.show()
    
    def diagram_drawing_hide_alpha_grid():
        ''''''
        grid.hide()
    
    def diagram_drawing_get_alpha_grid_position(position: str) -> MousePosition:
        ''''''
        vertical = position[0]
        horizontal = position[1]
        position = grid.get_position(vertical, horizontal)
        return position
    
    def diagram_drawing_go_to_alpha_grid_position(position: str):
        ''''''
        position = actions.user.diagram_drawing_get_alpha_grid_position(position)
        position.go()
    
    def diagram_drawing_toggle_alpha_grid_lines():
        ''''''
        current_value = show_grid_lines_file.get()
        show_grid_lines_file.set(not current_value)
        grid.refresh()
