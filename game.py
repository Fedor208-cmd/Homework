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



import tkinter
import time
import random

w = 1000
h = 600
shift_x = w // 5
shift_y = h // 5

master = tkinter.Tk()
canvas = tkinter.Canvas(master, bg="light blue", width=w, height=h)

suns = 500
peashooters = list()
sunflowers = list()
used = list()
zombies = list()


def collision(event, button):
    xo1, yo1 = event.x, event.y
    xb1, xb2, yb1, yb2 = canvas.coords(button)[0], canvas.coords(button)[2], canvas.coords(button)[1], canvas.coords(button)[3]
    if (xb1 < xo1 < xb2) and (yb1 < yo1 < yb2):
        return True
    return False


def sunflower_draw(xs, ys):
    coord = canvas.create_oval((xs, ys), (xs + w // 10, ys + h // 5), outline="orange", fill="yellow")
    canvas.create_oval((xs + 20, ys + 20), (xs + w // 10 - 20, ys + h // 5 - 20), outline="#542626", fill="#6E3131")
    return coord


def peashooter_draw(xp, yp):
    coord = canvas.create_rectangle((xp, yp), (xp + w // 10, yp + h // 5), fill="green", outline="black")
    canvas.create_rectangle((xp + w // 15, yp + 30), (xp + w // 10 - 2, yp + h // 5 - 30), fill="black")
    return coord


def zombie(x_l, y_l):
    global zombies
    zombie_mob = canvas.create_oval((x_l, y_l), (x_l + w // 10, y_l + w // 10), fill="#008000", outline="#808000")
    zombies.append(zombie_mob)
    while canvas.coords(zombie_mob)[0] < 0:
        time.sleep(0.05)
        canvas.move(zombie_mob, -10, 0)
        canvas.update()


plant = None


def handler(event):
    global used
    global plant
    global suns
    global sunflowers

    if collision(event, button_sunflower):
        plant = "Sunflower"
    if collision(event, button_peashooter):
        plant = "Peashooter"
    for pot in field:
        if collision(event, pot) and plant == "Sunflower" and pot not in used and suns >= 500:
            sunflowers.append(sunflower_draw(canvas.coords(pot)[0], canvas.coords(pot)[1]))
            used.append(pot)
            canvas.update()
            plant = None
            suns -= 500
            break
        if collision(event, pot) and plant == "Peashooter" and pot not in used and suns >= 1000:
            peashooters.append(peashooter_draw(canvas.coords(pot)[0], canvas.coords(pot)[1]))
            used.append(pot)
            canvas.update()
            plant = None
            suns -= 1000
            break

    for s_fl in sunflowers:
        if collision(event, s_fl):
            suns += 100 * len(sunflowers)
            amount.config(text=f"Солнца: {suns}")
            amount.pack()
    for p_sh in peashooters:
        if collision(event, p_sh):
            yp1, xp2, yp2 = canvas.coords(p_sh)[1], canvas.coords(p_sh)[2], canvas.coords(p_sh)[3]
            bomb = canvas.create_oval((xp2, yp1), (xp2 + yp2, yp2), fill="black")
            while canvas.coords(bomb)[2] < 0:
                time.sleep(0.05)
                canvas.move(bomb, 10, 0)
                canvas.update()


amount = tkinter.Label(text=f"Солнца: {suns}")
amount.pack()
field = list()
colour = "green"
button_sunflower = canvas.create_rectangle((0, shift_y), (shift_x, (shift_y * 2)), fill="#D2B48C", outline="#8B4513")

xsa = canvas.coords(button_sunflower)[0]
ysa = canvas.coords(button_sunflower)[1]
canvas.create_text(xsa + 150, ysa * 1.5, font=("Masquerade", 12), text="500")
canvas.create_oval((xsa, ysa), (xsa + w // 10, ysa + h // 5), outline="orange", fill="yellow")
canvas.create_oval((xsa + 20, ysa + 20), (xsa + w // 10 - 20, ysa + h // 5 - 20), outline="#542626", fill="#6E3131")

button_peashooter = canvas.create_rectangle((0, shift_y * 2), (shift_x, (shift_y * 3)), fill="#D2B48C", outline="#8B4513")
xpa = canvas.coords(button_peashooter)[0]
ypa = canvas.coords(button_peashooter)[1]
canvas.create_text(xpa + 150, ypa * 1.25, font=("Masquerade", 12), text="1000")
canvas.create_rectangle((xpa, ypa), (xpa + w // 10, ypa + h // 5), fill="green", outline="black")
canvas.create_rectangle((xpa + w // 15, ypa + 30), (xpa + w // 10 - 2, ypa + h // 5 - 30), fill="black")

for y in range(0, h, h // 5):
    if colour == "green":
        colour = "dark green"
    elif colour == "dark green":
        colour = "green"
    for x in range(shift_x, w, (w - shift_x) // 8):
        if colour == "green":
            square = canvas.create_rectangle((x, y), (x + 100, y + 120), fill=colour)
            colour = "dark green"
        else:
            square = canvas.create_rectangle((x, y), (x + 100, y + 120), fill=colour)
            colour = "green"
        field.append(square)

master.bind("<ButtonPress>", handler)
canvas.pack()
master.mainloop()

