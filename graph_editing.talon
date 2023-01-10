tag: user.diagram_drawing
and tag: user.diagram_drawing_graphing
-
graphing finish: user.diagram_drawing_finish_graph()

axis new <number_small> and <number_small>: user.diagram_drawing_add_next_axis(number_small_1, number_small_2)

spot <user.diagram_drawing_number_float> by <user.diagram_drawing_number_float>:
    user.diagram_drawing_draw_point_at(diagram_drawing_number_float_1, diagram_drawing_number_float_2)

spot <user.diagram_drawing_number_float> by <user.diagram_drawing_number_float> by <user.diagram_drawing_number_float>:
    user.diagram_drawing_draw_point_at(diagram_drawing_number_float_1, diagram_drawing_number_float_2, diagram_drawing_number_float_3)

open [spot] <user.diagram_drawing_number_float> by <user.diagram_drawing_number_float>:
    user.diagram_drawing_draw_open_point_at(diagram_drawing_number_float_1, diagram_drawing_number_float_2)

open [spot] <user.diagram_drawing_number_float> by <user.diagram_drawing_number_float> by <user.diagram_drawing_number_float>:
    user.diagram_drawing_draw_open_point_at(diagram_drawing_number_float_1, diagram_drawing_number_float_2, diagram_drawing_number_float_3)

axis <number_small>: user.diagram_drawing_edit_axis(number_small)

start tick <user.diagram_drawing_number>: user.diagram_drawing_add_start_tick(diagram_drawing_number)

tail tick <user.diagram_drawing_number>: user.diagram_drawing_add_tail_tick(diagram_drawing_number)
