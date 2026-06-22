import platform
from ui import gui_03, gui_07_win

def ChooseGui():
  try:
    if platform.system() == "Windows":
        return gui_07_win
    elif platform.system() == "Darwin":
        return gui_07_win
    else:
        return gui_03
  except Exception as e:
    print(f"Error check platform: {e}")
    return False
