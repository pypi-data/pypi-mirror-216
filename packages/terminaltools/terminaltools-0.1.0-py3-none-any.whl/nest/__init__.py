def nest(
  text:str,
  top_icon:str="=",
  side_icon:str="",
  corner_icon:str="",
  left_right_padding:int=0,
  up_down_padding:int=0
):
  """
  text, top_icon, side_icon, corner_icon, left_right_padding, up_down_padding
  DEFAULTS TO: None, '=', '', '', 0, 0
  Nests 'text' in a box with 'top_icon' on the top and bottom, 'side_icon' on the left and right, and 'corner_icon' on the corners; can also add interior padding via left_right_padding and up_down_padding
  Returns a string.
  Try nesting nests in nests!
  """
  # ensuring that padding is not affected if corner is empty, or if side is empty, etc.
  if side_icon != "" and corner_icon == "":
    corner_icon = " "
  elif corner_icon != "" and side_icon == "":
    side_icon = " "
  if corner_icon != "" and top_icon == "":
    top_icon = " "

  # split text into an array of lines to figure out the longest line
  line_by_line_text = text.split("\n")
  longest_line_length = 0
  for line in line_by_line_text:
    if len(line) > longest_line_length:
      longest_line_length = len(line)
  
  # insert more lines based on up-down padding
  for new_line in range(up_down_padding):
    line_by_line_text.insert(0, "")
    line_by_line_text.append("")

  # make all lines equal length by appending spaces to the ends
  # then, surround them with left-right padding and side-icons
  for i, line in enumerate(line_by_line_text):
    line_by_line_text[i] = (
      side_icon + (
        " " * left_right_padding + (
          line + (
            " " * (
              longest_line_length - len(line)
            )
          )
        ) + " " * left_right_padding
      ) + side_icon
    )
  
  # if theres a top row
  if top_icon != "" or corner_icon != "":
    # create a row of top=icons until it equals the length of all the other lines in line_by_line_text, then add corner icons to either side
    icon_row = (
      corner_icon + (
        top_icon * (
          left_right_padding + (
            longest_line_length
          ) + left_right_padding
        )
      ) + corner_icon
    )
    # append this to the top and bottom of line_by_line_text
    line_by_line_text.insert(0, icon_row)
    line_by_line_text.append(icon_row)

  # join line_by_line text together using line breaks and return
  return (
    "\n".join(line_by_line_text)
  )