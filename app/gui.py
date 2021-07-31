from tkinter import *
from tkinter import filedialog
import os
from PIL import Image, ImageTk
import pathlib as pl
from modules import capture, detect, test


def image():
    fln = filedialog.askopenfilename(initialdir = os.getcwd(), title="Select Image file", filetypes=(("JPG File","*.jpg"),("PNG file", "*.png"),("All Files","*.*")))
    img = Image.open(fln)
    img.thumbnail((300,200))
    img = ImageTk.PhotoImage(img)
    lbl.configure(image = img)
    lbl.image = img
    capture(fln)

def function():
    detect()
    test()

root = Tk()
root.title("Lazuli Cross")
root.geometry("300x400")
root.iconbitmap(str(pl.Path(__file__).parent) + "/logo.ico")

f1 = Frame(root, height=400, width=300)
f1.config(background='#32454a')

f1.pack(fill = 'both', expand = True)

f2 = Frame(f1, height = 300, width = 400)
f2.grid()

lbl = Label(f2, padx = 100, pady = 100, bd = 1)
lbl.pack()

f2.pack(expand = True)

f3 = Frame(f1)
f3.config(background = '#32454a')
f3.pack(expand = True)


b1 = Button(f3, text="Insert Image", bg = '#5a7982', fg = 'white', command = image)
b1.grid(row=0, column=1, padx= 10, pady=10)

b2 = Button(f3, text = "Test Image", bg = '#5a7982', fg = 'white', command = function)
b2.grid(row=0, column=2, padx=10, pady=10)
