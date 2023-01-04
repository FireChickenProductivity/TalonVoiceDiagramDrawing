tag: user.diagram_drawing
-
text: user.diagram_drawing_create_text_field_with_position_stored()
char <user.letter>: user.diagram_drawing_create_text_field_at_cursor_with_text_uppercase(letter)
label <user.diagram_drawing_position_specifier>: user.diagram_drawing_label_named_position(diagram_drawing_position_specifier)
change <user.diagram_drawing_position_specifier>: 
    user.diagram_drawing_edit_text_at_named_position(diagram_drawing_position_specifier)
    edit.select_all()
fresh <user.diagram_drawing_position_specifier>:
    user.diagram_drawing_edit_text_at_named_position(diagram_drawing_position_specifier)
    edit.line_end()
<user.diagram_drawing_position_specifier> (value|val) <user.diagram_drawing_number>:
    user.diagram_drawing_label_named_position_with_text(diagram_drawing_position_specifier, diagram_drawing_number)
