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
    if event.keycode == 39 and not (
        canvas.coords(wall)[0] <= canvas.coords(car)[2] <= canvas.coords(wall)[2] and
        (canvas.coords(wall)[1] <= canvas.coords(car)[1] <= canvas.coords(wall)[3] or
         canvas.coords(wall)[1] <= canvas.coords(car)[3] <= canvas.coords(wall)[3])
    ):
        canvas.move(car, 10, 0)
    elif event.keycode == 38 and not (canvas.coords(wall)[1] <= canvas.coords(car)[1] <= canvas.coords(wall)[3] and (
            canvas.coords(wall)[0] <= canvas.coords(car)[2] <= canvas.coords(wall)[2] or
            canvas.coords(wall)[0] <= canvas.coords(car)[0] <= canvas.coords(wall)[2]
    )):
        canvas.move(car, 0, -10)
    elif event.keycode == 40 and not (canvas.coords(wall)[1] <= canvas.coords(car)[3] <= canvas.coords(wall)[3] and (
            canvas.coords(wall)[0] <= canvas.coords(car)[2] <= canvas.coords(wall)[2] or
            canvas.coords(wall)[0] <= canvas.coords(car)[0] <= canvas.coords(wall)[2]
    )):
        canvas.move(car, 0, 10)
    elif event.keycode == 37 and not (canvas.coords(wall)[0] <= canvas.coords(car)[0] <= canvas.coords(wall)[2] and (
            (canvas.coords(wall)[1] <= canvas.coords(car)[1] <= canvas.coords(wall)[3] or
             canvas.coords(wall)[1] <= canvas.coords(car)[3] <= canvas.coords(wall)[3])
    )):
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
        while canvas.coords(bomb)[0] < canvas.winfo_reqwidth() and not (
         canvas.coords(wall)[0] <= canvas.coords(bomb)[2] <= canvas.coords(wall)[2] and (
                canvas.coords(wall)[1] <= canvas.coords(bomb)[1] <= canvas.coords(wall)[3] or
                canvas.coords(wall)[1] <= canvas.coords(bomb)[3] <= canvas.coords(wall)[3])
        ):
            time.sleep(0.03)
            canvas.move(bomb, 10, 0)
            canvas.update()
        if canvas.coords(bomb)[0] > canvas.coords(goal)[0] and (
         canvas.coords(goal)[1] < canvas.coords(bomb)[1] <
         canvas.coords(goal)[3] or canvas.coords(goal)[1] < canvas.coords(bomb)[2] <
         canvas.coords(goal)[3]
         ):
            canvas.itemconfig(goal, fill="green")


goal = canvas.create_rectangle((900, 200), (1000, 600), fill="yellow")
wall = canvas.create_rectangle((400, 200), (450, 300), fill="pink")
car = canvas.create_rectangle((200, 150), (250, 180), fill="purple")
master.bind("<KeyPress>", handler)

canvas.pack()
master.mainloop()
