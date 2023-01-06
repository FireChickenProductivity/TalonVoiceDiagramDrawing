tag: user.diagram_drawing
-
#Saving positions
<user.diagram_drawing_position_specifier> save <user.diagram_drawing_position_specifier>:
    user.diagram_drawing_save_named_position(1, diagram_drawing_position_specifier_1)
    user.diagram_drawing_save_named_position(2, diagram_drawing_position_specifier_2)

#Using saved positions
quad <user.diagram_drawing_number_float>: 
    user.draw_quadratic_between_saved_positions_with_slope(diagram_drawing_number_float)
dash quad <user.diagram_drawing_number_float>: 
    user.draw_dashed_quadratic_between_saved_positions_with_slope(diagram_drawing_number_float)
curve <user.diagram_drawing_number_float> slope <user.diagram_drawing_number_float>: 
    user.diagram_drawing_draw_two_slope_curve_between_saved_positions(diagram_drawing_number_float_1, diagram_drawing_number_float_2)
