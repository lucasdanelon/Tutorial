"""
Created by researches to researches
"""

from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import ImageTk,Image
import os
from howardnator import main

window = Tk()

window.tk.call('wm', 'iconphoto', window._w, PhotoImage(file='howardnator.PNG'))
window.title('Howardnator - Bibliometric Analysis')
window.geometry('500x500')
img = Image.open("howardnator.PNG")

window.mainloop()
