import tkinter as tk
from controller import PuzzleController

try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

if __name__ == "__main__":
    root = tk.Tk()
    app = PuzzleController(root)
    root.mainloop()