import tkinter
import time

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
        bomb = canvas.create_oval((canvas.coords(car)[2] - 5, canvas.coords(car)[1]),
                                  (canvas.coords(car)[2] + 25, canvas.coords(car)[1] + 30), fill="black")
        while canvas.coords(bomb)[0] < canvas.winfo_reqwidth():
            time.sleep(0.03)
            canvas.move(bomb, 10, 0)
            canvas.update()


car = canvas.create_rectangle((200, 150), (250, 180), fill="purple")
master.bind("<KeyPress>", handler)

canvas.pack()
master.mainloop()
