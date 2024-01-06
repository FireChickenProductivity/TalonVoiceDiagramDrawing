tag: user.diagram_drawing
-
draw (dot|point): 
    user.diagram_drawing_draw_dot()
    user.diagram_drawing_store_current_position()

graph new: user.diagram_drawing_new_graph()

three graph new: user.diagram_drawing_new_three_dimensional_graph()
