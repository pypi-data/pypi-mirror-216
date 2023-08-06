def marker(color:str='white'):
  """
  marker(color)
  allowed colors include:
  BLACK, RED, GREEN, YELLOW, BLUE, PURPLE, CYAN, WHITE

  Returns the escape sequence for a given color.
  """
  # available colors
  colors = {'black': 30, 'red': 31, 'green': 32, 'yellow': 33, 'blue': 34, 'purple': 35, 'cyan': 36, 'white': 37}
  # if the requested color exists
  if colors.get(color.lower()):
    # just return the tag
    return f"\033[1;{colors[color]};40m"
  else:
    # color not found
    raise ValueError("Invalid color: " + color)