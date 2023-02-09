# Talon Voice Diagram Drawing
Work in progress diagram drawing talon commands currently compatible with Vectr. Undocumented commands might undergo serious change.

Proper documentation is in progress.

Note that this command set is very large and can take a while to load on some computers when you first open Vectr and when you first open the "are you sure" menu on each talon session. Attempts will be made to reduce the command set size without meaningfully reducing functionality. The current command set size may prevent these commands from working with dragon.

# Canvas
For some functionality to work, you must use commands to specify the upper left and bottom right corners of the canvas you will be drawing on. You specify the upper left corner by moving the mouse to it and saying "update canvas origin". You specify the bottom right corner by moving the mouse to it and saying "update canvas ending".

The canvas is remembered on a per application basis, so you do not have to respecify it every time you switch between supported drawing applications.

The canvas specifying commands can be found in canvas.talon.

# Position Specifiers
Position specifiers are ways to specify positions to commands. Some commands will number positions. Those positions can be specified by number. Locations on the alpha grid (see below) are specified with the phonetic alphabet words corresponding to the letters in vertical, horizontal order. Positions on the current graph are specified by how many tick marks to move along each axis each separated by the word by (for example: minus five by ten means five tick marks to the left and ten tick marks up on a standard two dimensional graph).

 Saying "move" followed by a position specifier moves the cursor to the specified position.
 
 # Alpha Grid
 The alpha grid denotes positions on the canvas by dividing it into a 26 by 26 grid.
 
  Saying "alpha grid show" shows the grid.
  
  Saying "alpha grid hide" hides the grid.
  
  Saying "alpha grid toggle lines" changes whether or not the lines corresponding to the alpha grid positions should be displayed.
  
  The word grid is optional in these commands.

# Numbered Positions
Some commands will automatically number positions so that they can be referred to by number.

Saying "numbering show" shows the numbering. Note that only numbers within the canvas as specified with the above canvas commands will be shown.

Saying "numbering hide" hides the numbering.

Saying "numbering clear" opens up an are you sure dialog. Saying "yes I am sure" will clear the current numbering. Saying "no" closes the dialogue without clearing the numbering.

Saying "number this", "number here", or "number that" manually numbers the current mouse position.

The numbering is stored in a file and should be preserved across sessions.

# Line Drawing
Saying "line (up, down, left, right, peft (up and left), pight (up and right), neft (down and left), or night (down and right)) (an integer between 1 and 99)" will draw a line from the cursor's current position to a position in the direction specified by the specified integer amount. Saying "line up five" draws a line up from the cursor by five units.

Saying "(position specifier) stripe (position specifier)" will draw a line between the position specifiers.

Saying "(position specifier) stripe (position specifier) with (number)" will draw a line between the specified positions labeled in the middle with the number.

Saying "(position specifier) vector (position specifier)" will draw an arrow from the first specified position to the second.

Saying "(position specifier) vector (position specifier) with (number)" will draw an arrow from the first specified position to the second labeled in the middle with the number.

Saying "(position specifier) dash stripe (position specifier)" will draw a dashed line in between the specified positions.

Saying "cross out (position specifier)" draws an x at the specified position. The word out is optional.

# Text
Saying "text" creates a text field at the cursor's location.

Saying "char (phonetic alphabet word for a letter)" creates a text field at the cursor with the specified letter in upper case.

Saying "label (position specifier)" creates a text field at the specified position.

Saying "change (position specifier)" edits the text field at the specified location and selects all its text.

Saying "fresh (position specifier)" edits the text field at the specified location and moves the text cursor to the end of the text field's first line.

Saying "(position specifier) (value or val) (number)" creates a text field with the specified number as its text at the specified position.

# Selection
Saying "done" or "finish" unselects.
