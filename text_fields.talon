tag: user.diagram_drawing
-
text: user.diagram_drawing_create_text_field_with_position_stored()
label <number>: user.diagram_drawing_label_stored_position(number)
change <number>: 
    user.diagram_drawing_edit_text_at_stored_position(number)
    edit.select_all()
fresh <number>:
    user.diagram_drawing_edit_text_at_stored_position(number)
    edit.line_end()
