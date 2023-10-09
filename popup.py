import tkinter as tk
from tkinter import ttk
import winsound

def popup():
    root = tk.Tk()
    root.title("提案")
    window_width = 500
    window_height = 250
    root.geometry(f"{window_width}x{window_height}")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width - window_width) //2
    y = (screen_height - window_height) //2
    root.geometry(f"{window_width}x{window_height}+{x}+{y-100}")

    canvas = tk.Canvas(root, width = 500, height = 250)
    canvas.create_rectangle(0, 0, 600, 400, fill = "white")
    canvas.place(x=0, y=0)

    img = tk.PhotoImage(file = "exclamation-mark.png", width=800, height=565)
    canvas.create_image(163, 225, image=img)

    canvas.create_text(220, 130, text="少し休憩しませんか？", anchor="sw", font=("HG丸ゴシックM-PRO",20), fill="#F0E68C")
    canvas.create_text(240, 170, text="作業お疲れ様です。", font=("HG丸ゴシックM-PRO", 16))
    canvas.create_text(240, 190, text="ストレッチなどをして体を伸ばしましょう。", font=("HG丸ゴシックM-PRO", 16))
    root.resizable(False, False)

    with open("maou_se_onepoint28.wav", "rb") as f:
        data = f.read()
    winsound.PlaySound(data, winsound.SND_MEMORY)

    root.mainloop()