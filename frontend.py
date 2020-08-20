"""
Created by researches to researches
"""

from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import ImageTk,Image
import os
from howardnator import main
import pandas as pd

# Define window
window = Tk()
window.resizable(False,False)
# Call window
window.tk.call('wm', 'iconphoto', window._w, PhotoImage(file='howardnator.PNG'))

# Define the title of the window
window.title('Howardnator - Bibliometric Analysis')

# Define the size of the window
window.geometry('1000x500')

img = Image.open("howardnator.PNG")
image = ImageTk.PhotoImage(img)
panel = Label(window,image=image)
panel.grid(row=0,column=0,rowspan=10,columnspan=10)

def choose_file():
    global filename
    file = askopenfilename(filetypes=[('Database Files','*.csv')])
    if file!='':
        filename = file
        name = filename.split('/')[-1]
        label_1.config(text="File: " + name)

def analyze(filename):
    if filename is not None:
        Authors_final, Countries_final, Institutions_final = main(filename)
        label_2.config(text="Analysis success!")

btn = Button(window,text="Choose .csv to analyze", width=40, command = lambda:choose_file())
btn.grid(row=2, column=11,sticky=W)

try: filename
except NameError: filename=None

label_1 = Label(window,text='No File Selected',width=40)
label_1.grid(row=3,column=11,sticky=W)

btn = Button(window,text="Analyze .csv file", width=40, command = lambda:analyze(filename))
btn.grid(row=4, column=11,sticky=W)

label_2 = Label(window,text='',width=40)
label_2.grid(row=5,column=11,sticky=W)


window.mainloop()
