tag: user.diagram_drawing
-
line <user.diagram_drawing_direction> <number_small>: 
    user.diagram_drawing_draw_line_from_cursor_using_direction_and_amount(diagram_drawing_direction, number_small)

line <number_small> <user.diagram_drawing_complex_direction> <number_small>:
    user.diagram_drawing_draw_line_from_cursor_using_complex_direction_and_amounts(diagram_drawing_complex_direction, number_small_1, number_small_2)

<user.diagram_drawing_position_specifier> stripe <user.diagram_drawing_position_specifier>:
    user.diagram_drawing_draw_line_between_named_positions(diagram_drawing_position_specifier_1, diagram_drawing_position_specifier_2)

<user.diagram_drawing_position_specifier> stripe <user.diagram_drawing_position_specifier> with <user.diagram_drawing_number>:
    user.diagram_drawing_draw_line_between_named_positions_with_label(diagram_drawing_position_specifier_1, diagram_drawing_position_specifier_2, diagram_drawing_number)

<number> vector <number>:
    user.diagram_drawing_draw_vector_between_stored_positions(number_1, number_2)

<number> vector <number> with <user.diagram_drawing_number>:
    user.diagram_drawing_draw_vector_between_stored_positions_with_label(number_1, number_2, diagram_drawing_number)

cross [out] <number>: user.diagram_drawing_cross_out_stored_position(number)

arrow [new] <number>: user.diagram_drawing_draw_arrowhead_at_cursor(number)

<number> dash stripe <number>:
    user.diagram_drawing_draw_dashed_line_between_stored_positions(number_1, number_2)
