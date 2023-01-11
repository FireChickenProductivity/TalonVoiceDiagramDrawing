# Talon Voice Diagram Drawing
Work in progress diagram drawing talon commands currently compatible with Vectr. Undocumented commands might undergo serious change.

Proper documentation is in progress.

# Canvas
For some functionality to work, you must use commands to specify the upper left and bottom right corners of the canvas you will be drawing on. You specify the upper left corner by moving the mouse to it and saying "update canvas origin". You specify the bottom right corner by moving the mouse to it and saying "update canvas ending".

The canvas is remembered on a per application basis, so you do not have to respecify it every time you switch between supported drawing applications.

The canvas specifying commands can be found in canvas.talon.

# Position Specifiers
Position specifiers are ways to specify positions to commands. Some commands will number positions. Those positions can be specified by number. Locations on the alpha grid (see below) are specified with the phonetic alphabet words corresponding to the letters in horizontal, vertical order. Positions on the current graph are specified by how many tick marks to move along each axis each separated by the word by (for example: minus five by ten means five tick marks to the left and ten tick marks up on a standard two dimensional graph).

 Saying "move" followed by a position specifier moves the cursor to the specified position.
 
 # Alpha Grid
 The alpha grid denotes positions on the canvas by dividing it into a 26 by 26 grid.
 
  Saying "alpha grid show" shows the grid.
  
  Saying "alpha grid hide" hides the grid.
  
  Saying "alpha grid toggle lines" changes whether or not the lines corresponding to the alpha grid positions should be displayed.
  
  The word grid is optional in these commands.
