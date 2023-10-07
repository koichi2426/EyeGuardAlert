import tkinter
from tkinter import font
from tkinter import *
from tkinter import ttk
import sys

def popup():
    root = tkinter.Tk()
    root.title("提案")
    root.geometry("800x500")
    root.configure(bg="white")
    canvas = tkinter.Canvas(root, bg="#CCFFFF", height=400, width=400)
    canvas.place(x=30, y=45)

    image = tkinter.PhotoImage(file="pyoko_coffee_break.png", width=1000, height=1000)
    canvas.create_image(500, 500, image=image)
    button = ttk.Button(root, text="OK")

    font1 = font.Font(family="Times New Roman", size=20, weight="bold")
    label1 = tkinter.Label(root, text="少し休憩しませんか？", fg="white", font=font1)
    label1.pack(side="right")

    root.mainloop()