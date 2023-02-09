tag: user.diagram_drawing
-
line <user.diagram_drawing_direction> <number_small>: 
    user.diagram_drawing_draw_line_from_cursor_using_direction_and_amount(diagram_drawing_direction, number_small)

line <number_small> <user.diagram_drawing_complex_direction> <number_small>:
    user.diagram_drawing_draw_line_from_cursor_using_complex_direction_and_amounts(diagram_drawing_complex_direction, number_small_1, number_small_2)

dash [line] <user.diagram_drawing_direction> <number_small>:
    user.diagram_drawing_draw_dashed_line_from_cursor_using_direction_and_amount(diagram_drawing_direction, number_small)

dash [line] <number_small> <user.diagram_drawing_complex_direction> <number_small>:
    user.diagram_drawing_draw_dashed_line_from_cursor_using_complex_direction_and_amounts(diagram_drawing_complex_direction, number_small_1, number_small_2)

<user.diagram_drawing_position_specifier> stripe <user.diagram_drawing_position_specifier>:
    user.diagram_drawing_draw_line_between_named_positions(diagram_drawing_position_specifier_1, diagram_drawing_position_specifier_2)

<user.diagram_drawing_position_specifier> stripe <user.diagram_drawing_position_specifier> with <user.diagram_drawing_number>:
    user.diagram_drawing_draw_line_between_named_positions_with_label(diagram_drawing_position_specifier_1, diagram_drawing_position_specifier_2, diagram_drawing_number)

<user.diagram_drawing_position_specifier> vector <user.diagram_drawing_position_specifier>:
    user.diagram_drawing_draw_vector_between_named_positions(diagram_drawing_position_specifier_1, diagram_drawing_position_specifier_2)

<user.diagram_drawing_position_specifier> vector <user.diagram_drawing_position_specifier> with <user.diagram_drawing_number>:
    user.diagram_drawing_draw_vector_between_named_positions_with_label(diagram_drawing_position_specifier_1, diagram_drawing_position_specifier_2, diagram_drawing_number)

cross [out] <user.diagram_drawing_position_specifier>: user.diagram_drawing_cross_out_named_position(diagram_drawing_position_specifier)

arrow [new] <number>: user.diagram_drawing_draw_arrowhead_at_cursor(number)
arrowhead [new] <number>: user.diagram_drawing_draw_triangle_arrowhead_at_cursor(number)

<user.diagram_drawing_position_specifier> dash stripe <user.diagram_drawing_position_specifier>:
    user.diagram_drawing_draw_dashed_line_between_named_positions(diagram_drawing_position_specifier_1, diagram_drawing_position_specifier_2)

lines <number_small> by <number_small>: user.diagram_drawing_draw_rectangle_around_cursor(number_small_1, number_small_2)
lines <number_small> by <number_small> by <number_small>: user.diagram_drawing_draw_vertically_consecutive_rectangles(number_small_1, number_small_2, number_small_3)
diamond <number_small> by <number_small>: user.diagram_drawing_draw_diamond_around_cursor(number_small_1, number_small_2)
(dub|double) diamond <number_small> by <number_small>:
    user.diagram_drawing_draw_double_diamond_around_cursor(number_small_1, number_small_2)

<user.diagram_drawing_position_specifier> (pair|parallel) [lines] <user.diagram_drawing_position_specifier> gap <number_small>:
    user.draw_parallel_lines_around_named_positions_with_gap(diagram_drawing_position_specifier_1, diagram_drawing_position_specifier_2, number_small)
