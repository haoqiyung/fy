import tkinter as tk
from gui import Translator

if __name__ == '__main__':
    root = tk.Tk()
    app = Translator(master=root)
    app.mainloop()