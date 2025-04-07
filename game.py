import tkinter

master = tkinter.Tk()
canvas = tkinter.Canvas(master, bg="light green", width=1000, height=800)

def handler(event):
    if canvas.coords(car)[0] < 0:
        canvas.moveto(car, 949)
    if canvas.coords(car)[1] < 0:
        canvas.moveto(car, y=729)
    if canvas.coords(car)[2] > 1000:
        canvas.moveto(car, 0)
    if canvas.coords(car)[3] > 800:
        canvas.moveto(car, y=0)
    if event.keycode == 39:
        canvas.move(car, 10, 0)
    elif event.keycode == 38:
        canvas.move(car, 0, -10)
    elif event.keycode == 40:
        canvas.move(car, 0, 10)
    elif event.keycode == 37:
        canvas.move(car, -10, 0)
    elif event.char == "b":
        canvas.itemconfig(car, fill="cyan")
    elif event.char == "y":
        canvas.itemconfig(car, fill="yellow")
    elif event.char == "o":
        canvas.itemconfig(car, fill="orange")
    elif event.char == "m":
        canvas.moveto(car, event.x, event.y)
    if event.char == "f":
        x1 = canvas.coords(car)[2]
        y1 = canvas.coords(car)[1]
        x2 = x1 + 30
        y2 = y1 + 30
        pr = canvas.create_oval((x1, y1), (x2, y2), fill="black")
        while canvas.coords(pr)[2] < 1000:
            canvas.move(pr, 10, 0)

car = canvas.create_rectangle((200, 150), (250, 180), fill="purple")
master.bind("<KeyPress>", handler)

canvas.pack()
master.mainloop()