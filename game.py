import tkinter
import time

master = tkinter.Tk()
canvas = tkinter.Canvas(master, bg="light green", width=1000, height=800)


def collision(obj, obst=0):
    xo1, yo1, xo2, yo2 = canvas.coords(obj)
    for wall in walls:
        xw1, yw1, xw2, yw2 = canvas.coords(wall)
        if (xw1 < xo1 < xw2 or xw1 < xo2 < xw2) and (yw1 < yo1 < yw2 or yw1 < yo2 < yw2):
            return True
    return False


def collision_goal(obj, goal):
    if canvas.coords(obj)[2] >= canvas.coords(goal)[0] and (
            canvas.coords(goal)[1] < canvas.coords(obj)[1] <
            canvas.coords(goal)[3] or canvas.coords(goal)[1] < canvas.coords(obj)[2] <
            canvas.coords(goal)[3]
    ):
        return True
    return False


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
        if collision(car):
            canvas.move(car, -10, 0)
    elif event.keycode == 38:
        canvas.move(car, 0, -10)
        if collision(car):
            canvas.move(car, 0, 10)
    elif event.keycode == 40:
        canvas.move(car, 0, 10)
        if collision(car):
            canvas.move(car, 0, -10)
    elif event.keycode == 37:
        canvas.move(car, -10, 0)
        if collision(car):
            canvas.move(car, 10, 0)
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
        while canvas.coords(bomb)[0] < canvas.winfo_reqwidth() and not collision((bomb)) and not \
                collision_goal(bomb, goal):
            time.sleep(0.03)
            canvas.move(bomb, 10, 0)
            canvas.update()
        if collision_goal(bomb, goal):
            canvas.itemconfig(goal, fill="green")
        canvas.delete(bomb)



walls = list()
goal = canvas.create_rectangle((900, 200), (1000, 600), fill="yellow")
wall = canvas.create_rectangle((400, 200), (550, 300), fill="pink")
car = canvas.create_rectangle((200, 150), (250, 180), fill="purple")
master.bind("<KeyPress>", handler)
walls.append(wall)
canvas.pack()
master.mainloop()



