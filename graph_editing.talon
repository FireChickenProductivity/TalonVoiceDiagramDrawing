tag: user.diagram_drawing
and tag: user.diagram_drawing_graphing
-
graphing finish: user.diagram_drawing_finish_graph()

axis new <number_small> and <number_small>: user.diagram_drawing_add_next_axis(number_small_1, number_small_2)

move <user.diagram_drawing_number_float> by <user.diagram_drawing_number_float>: user.diagram_drawing_go_to_position_along_axes(diagram_drawing_number_float_1, diagram_drawing_number_float_2)

move <user.diagram_drawing_number_float> by <user.diagram_drawing_number_float> by <user.diagram_drawing_number_float>: 
    user.diagram_drawing_go_to_position_along_axes(diagram_drawing_number_float_1, diagram_drawing_number_float_2, diagram_drawing_number_float_3)

spot <user.diagram_drawing_number_float> by <user.diagram_drawing_number_float>:
    user.diagram_drawing_draw_point_at(diagram_drawing_number_float_1, diagram_drawing_number_float_2)

spot <user.diagram_drawing_number_float> by <user.diagram_drawing_number_float> by <user.diagram_drawing_number_float>:
    user.diagram_drawing_draw_point_at(diagram_drawing_number_float_1, diagram_drawing_number_float_2, diagram_drawing_number_float_3)