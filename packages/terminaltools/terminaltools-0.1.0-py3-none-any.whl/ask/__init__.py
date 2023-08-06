from os import system
import color_print
import marker

def ask(
  prompt:str,
  reply_filter,

  disallow_null:bool=True,
  clear_console:dict={"on_true": False, "on_false": False},
  colors:dict={"success": "green", "failure": "red"}
):
  """
  ask(prompt, filter, disallow_null, clear_console, colors)
  define a filter, then call ask:
    def myFilter(reply):
      if (reply == "0"):
        return False, 'This value is not allowed.'
      else:
        return True, 'Value accepted.'
    ask("Enter a non-zero character.", myFilter)
  disallow_null is true by default; clear_console on user success and failure are both false by default; success color and failure color are green and red respectively by default
  """
  # until the user enters a permissible answer
  while True:
    # prompt the user
    reply = input(prompt)

    # null catch
    if disallow_null and reply == "":
      if clear_console["on_false"]:
        system("clear")
      color_print("Please enter a value.", colors["failure"])
      continue # go back to the top of the loop
    
    # use the dev-provided filter
    reply_allowed = reply_filter(reply)

    # the dev-provided filter should return a tuple, if not, then log an error
    if type(reply_allowed) != tuple:
      raise ValueError(
        f"""
      
        {marker("yellow")}Developer: When using ask(), please return a two-element tuple of a boolean (for whether the user answer was valid) followed by an error or success message. For example:
        
        if (reply == "0"):
          return False, 'This value is not allowed'{marker()}
          
        User: Please contact this program's developer.""")

    # if the dev's filter returns true for the user's input, then print the dev's provided success statement and return the reply
    if reply_allowed[0]:
      if clear_console["on_true"]:
        system("clear")
      color_print(reply_allowed[1], colors["success"])
      return reply
    else:
      # else try again, return to the top of the loop
      if clear_console["on_false"]:
        system("clear")
      color_print(reply_allowed[1], colors["failure"])
      continue