import colored

def color_print(text:str, color:str, is_input=False, insert_end='\n'):
  """
  color_print(text, color, is_input, insert_end)
  allowed colors include:
  BLACK, RED, GREEN, YELLOW, BLUE, PURPLE, CYAN, WHITE

  Prints the text parameter as a given color.
  insert_end is used for the 'end' parameter in print statements; is_input will allow an input to be created instead."""
  # if using input
  if is_input:
    input(colored(text, color))
  else:
    # else just print, but also add the insert_end
    print(colored(text, color), end=insert_end)