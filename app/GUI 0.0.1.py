from tkinter import *
from tkinter import filedialog
import os
from PIL import Image, ImageTk

def image():
    fln = filedialog.askopenfilename(initialdir = os.getcwd(), title="Select Image file", filetypes=(("JPG File","*.jpg"),("PNG file", "*.png"),("All Files","*.*")))
    img = Image.open(fln)
    img.thumbnail((300,200))
    img = ImageTk.PhotoImage(img)
    lbl.configure(image = img)
    lbl.image = img

root = Tk()
root.title("Lazuli Cross")
root.geometry("300x400")

f1 = Frame(root, height=400, width=300)
f1.config(background='#32454a')

f2 = Frame(f1)
f2.config(background = '#32454a')
lbl = Label(f2, padx = 80, pady = 80, bd = 1)

f3 = Frame(f1)
f3.config(background = '#32454a')
b1 = Button(f3, text="Insert Image", bg = '#5a7982', fg = 'white', command = image)
b1.pack(side = LEFT)
b2 = Button(f3, text = "Test Image", bg = '#5a7982', fg = 'white')
b2.pack(side = RIGHT)

lbl.pack(side = TOP)
f1.pack(fill='both', expand=True)
f2.pack(expand=True)
f3.pack(expand=True, side = BOTTOM)
root.mainloop()