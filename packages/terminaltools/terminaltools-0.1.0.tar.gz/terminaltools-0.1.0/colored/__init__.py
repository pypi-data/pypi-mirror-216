import marker

def colored(text:str, color:str):
  """
  colored(text, color)
  allowed colors include:
  BLACK, RED, GREEN, YELLOW, BLUE, PURPLE, CYAN, WHITE

  Returns the text parameter as a given color.
  """
  # put tags around it
  return f"{marker(color)}{text}{marker()}"