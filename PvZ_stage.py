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
score = 0
peas = list()
sunflowers = list()
peashooters = list()
potatoes = list()
used = dict()
zombies = dict()
plants = list()
nuts = dict()
killed = True
plant = None
spd = 0
r = 3
n = 10
loss = False


def collision(event, button):
    xo1, yo1 = event.x, event.y
    xb1, xb2, yb1, yb2 = canvas.coords(button)[0], canvas.coords(button)[2], canvas.coords(button)[1], \
    canvas.coords(button)[3]
    if (xb1 < xo1 < xb2) and (yb1 < yo1 < yb2):
        return True
    return False


def collision_objects(obj1, obj2):
    xb1, xb2, yb1, yb2 = canvas.coords(obj1)[0], canvas.coords(obj1)[2], canvas.coords(obj1)[1], \
    canvas.coords(obj1)[3]
    xo1, xo2, yo1, yo2 = canvas.coords(obj2)[0], canvas.coords(obj2)[2], canvas.coords(obj2)[1], \
    canvas.coords(obj2)[3]
    if (xo1 <= xb1 <= xo2 or xo1 <= xb2 <= xo2) and (yo1 <= yb1 <= yo2 or yo1 <= yb2 <= yo2) or \
            (xb1 <= xo1 <= xb2 or xb1 <= xo2 <= xb2) and (yb1 <= yo1 <= yb2 or yb1 <= yo2 <= yb2):
        return True
    return False


def sunflower_draw(xs, ys):
    coord = canvas.create_oval((xs, ys), (xs + w // 10, ys + h // 5), outline="orange", fill="yellow")
    seeds = canvas.create_oval((xs + 20, ys + 20), (xs + w // 10 - 20, ys + h // 5 - 20), outline="#542626",
                               fill="#6E3131")
    return [coord, seeds]


def peashooter_draw(xp, yp):
    body = canvas.create_rectangle((xp, yp + h // 15), (xp + w // 10, yp + 2 * h // 15), fill="#ADFF2F",
                                   outline="#2E8B57")
    hole = canvas.create_rectangle((xp + w // 15, yp + h // 15 + 5), (xp + w // 10, yp + h // 15 + 35), fill="black")
    return [body, hole]


def potato_draw(xpt, ypt):
    mine = canvas.create_oval((xpt, ypt), (xpt + w // 10, ypt + h // 5), fill="#FFEE92", outline="#FFD500")
    led = canvas.create_oval((xpt + 30, ypt + 40), (xpt + w // 10 - 30, ypt + h // 5 - 40), fill="red")
    return [mine, led]


def nut_draw(xn, yn):
    wall = canvas.create_oval((xn, yn), (xn + w // 10, yn + h // 5), fill="#CDAB66", outline="#957E4F")
    crack = canvas.create_line((xn + w // 20, yn), (xn + w // 20, yn + h // 5), fill="#957E4F")
    return [wall, crack]


def zombie_spawn(x_l, y_l):
    global killed
    global spd
    global zombies
    global plants
    global potatoes
    global score
    global nuts
    global loss
    zombie_mob = canvas.create_oval((x_l, y_l), (x_l + w // 10, y_l + w // 10), fill="#808000", outline="#556B2F")
    health = 5
    zombies[zombie_mob] = health
    while canvas.coords(zombie_mob)[0] > 0:
        time.sleep(0.09)
        canvas.move(zombie_mob, -5 - spd, 0)
        canvas.update()
        for targ in plants:
            for enemy in zombies.keys():
                if (collision_objects(targ[0], enemy) or collision_objects(targ[1], enemy)) and not (targ[0] in nuts):
                    print(targ[0] in nuts)
                    plants.remove(targ)
                    del used[targ[0]]
                    for elem in targ:
                        canvas.delete(elem)
                    if targ in potatoes:
                        zombies[enemy] -= 10
                        if zombies[enemy] <= 0:
                            canvas.delete(enemy)
                            killed = True
                            del zombies[enemy]
                            score += 1
                        break
                elif collision_objects(targ[0], enemy) or collision_objects(targ[1], enemy) and targ[0] in nuts:
                    while nuts[targ[0]] > 0:
                        nuts[targ[0]] -= 1
                        canvas.move(enemy, 20, 0)
                        time.sleep(0.001)
                        while not collision_objects(targ[0], enemy):
                            time.sleep(0.09)
                            canvas.move(enemy, -1.5, 0)
                            canvas.update()
                    canvas.delete(targ[0])
                    canvas.delete(targ[1])
                    plants.remove(targ)
                    del nuts[targ[0]]
    if canvas.coords(zombie_mob)[0] <= 0:
        loss = True


def stage(event):
    global peas
    global killed
    global used
    global plant
    global suns
    global sunflowers
    global zombies
    global plants
    global r
    global peashooters
    global score
    global potatoes
    global n
    global loss
    global spd

    if collision(event, button_sunflower):
        plant = "Sunflower"
    if collision(event, button_peashooter):
        plant = "Peashooter"
    if collision(event, button_potato):
        plant = "Potato"
    if collision(event, button_nut):
        plant = "Nut"
    for pot in field:
        if collision(event, pot) and plant == "Sunflower" and pot not in used.values() and suns >= 500:
            a = sunflower_draw(canvas.coords(pot)[0], canvas.coords(pot)[1])
            sunflowers.append(a)
            plants.append(a)
            used[a[0]] = pot
            canvas.update()
            plant = None
            suns -= 500
            break
        if collision(event, pot) and plant == "Peashooter" and pot not in used.values() and suns >= 1000:
            a = peashooter_draw(canvas.coords(pot)[0], canvas.coords(pot)[1])
            peashooters.append(a)
            plants.append(a)
            used[a[0]] = pot
            canvas.update()
            plant = None
            suns -= 1000
            amount.config(text=f"Солнца: {suns}, убийства: {score} из {n}")
            amount.pack()
            break
        if collision(event, pot) and plant == "Potato" and pot not in used.values() and suns >= 5000:
            a = potato_draw(canvas.coords(pot)[0], canvas.coords(pot)[1])
            potatoes.append(a)
            plants.append(a)
            used[a[0]] = pot
            canvas.update()
            plant = None
            suns -= 5000
            amount.config(text=f"Солнца: {suns}, убийства: {score} из {n}")
            amount.pack()
            break
        if collision(event, pot) and plant == "Nut" and pot not in used.values() and suns >= 250:
            a = nut_draw(canvas.coords(pot)[0], canvas.coords(pot)[1])
            nuts[a[0]] = 5
            plants.append(a)
            used[a[0]] = pot
            canvas.update()
            plant = None
            suns -= 250
            amount.config(text=f"Солнца: {suns}, убийства: {score} из {n}")
            amount.pack()
            break
    for s_fl in sunflowers:
        if collision(event, s_fl[0]):
            suns += 100 * len(sunflowers)
            amount.config(text=f"Солнца: {suns}, убийства: {score} из {n}")
            amount.pack()
        for p_sh in peashooters:
            if collision(event, p_sh[0]) and len(peas) < 1:
                xb = canvas.coords(p_sh[1])[2]
                yb1 = canvas.coords(p_sh[1])[1]
                yb2 = canvas.coords(p_sh[1])[3]
                pea = canvas.create_oval((xb, yb1), (xb + (yb2 - yb1), yb2), fill="#00FF7F", outline="#3CB371")
                peas.append(pea)
                got = False
                while canvas.coords(pea)[2] < w:

                    time.sleep(0.05)
                    canvas.move(pea, 10, 0)
                    canvas.update()
                    for target in zombies:
                        if collision_objects(pea, target):
                            zombies[target] -= 1
                            y_zm = (random.randint(1, 4)) * h // 5 + h // 60
                            canvas.moveto(target, canvas.coords(target)[0], y_zm)
                            canvas.delete(pea)
                            peas.remove(pea)
                            got = True
                        if zombies[target] == 0:
                            canvas.delete(target)
                            killed = True
                            score += 1
                            amount.config(text=f"Солнца: {suns}, убийства: {score} из {n}")
                            amount.pack()
                            del zombies[target]
                            break
                if not got:
                    canvas.delete(pea)
                    peas.remove(pea)

    if len(plants) >= r and killed:
        x_z = w - w // 10
        y_z = (random.randint(1, 4)) * h // 5 + h // 60
        killed = False
        spd += 0.25
        zombie_spawn(x_z, y_z)
    if loss:
        for sol in plants:
            for elem in sol:
                canvas.delete(elem)
        for tr in zombies:
            canvas.delete(tr)
        canvas.create_text((w // 2, h // 2), font=("Masquerade", w // 10), text="Поражение", fill="red")
    if score == n:
        for sol in plants:
            for elem in sol:
                canvas.delete(elem)
        for tr in zombies:
            canvas.delete(tr)
        canvas.create_text((w // 2, h // 2), font=("Masquerade", w // 10), text="Победа", fill="#FFAB00")


amount = tkinter.Label(text=f"Солнца: {suns}, убийства: {score} из {n}")
amount.pack()
field = list()
colour = "green"

button_sunflower = canvas.create_rectangle((0, shift_y), (shift_x, (shift_y * 2)), fill="#D2B48C", outline="#8B4513")
xsa = canvas.coords(button_sunflower)[0]
ysa = canvas.coords(button_sunflower)[1]
canvas.create_text(xsa + w // 7, ysa * 1.5, font=("Masquerade", w // 83), text="500")
canvas.create_oval((xsa, ysa), (xsa + w // 10, ysa + h // 5), outline="orange", fill="yellow")
canvas.create_oval((xsa + w // 50, ysa + 20), (xsa + w // 10 - w // 50, ysa + h // 5 - h // 30), outline="#542626", fill="#6E3131")

button_peashooter = canvas.create_rectangle((0, shift_y * 2), (shift_x, (shift_y * 3)), fill="#D2B48C",
                                            outline="#8B4513")
canvas.create_text(xsa + w // 7, ysa * 2.5, font=("Masquerade", w // 83), text="1000")
peashooter_draw(canvas.coords(button_peashooter)[0], canvas.coords(button_peashooter)[1])

button_potato = canvas.create_rectangle((0, shift_y * 3), (shift_x, shift_y * 4), fill="#D2B48C", outline="#8B4513")
canvas.create_text(xsa + w // 7, ysa * 3.5, font=("Masquerade", w // 83), text="5000")
potato_draw(canvas.coords(button_potato)[0], canvas.coords(button_potato)[1])

button_nut = canvas.create_rectangle((0, shift_y * 4), (shift_x, shift_y * 5), fill="#D2B48C", outline="#8B4513")
canvas.create_text(xsa + w // 7, ysa * 4.5, font=("Masquerade", 12), text="250")
nut_draw(canvas.coords(button_nut)[0], canvas.coords(button_nut)[1])


for y in range(0, h, h // 5):
    if colour == "green":
        colour = "dark green"
    elif colour == "dark green":
        colour = "green"
    for x in range(shift_x, w, (w - shift_x) // 8):
        if colour == "green":
            square = canvas.create_rectangle((x, y), (x + w // 10, y + h // 5), fill=colour)
            colour = "dark green"
        else:
            square = canvas.create_rectangle((x, y), (x + w // 10, y + h // 5), fill=colour)
            colour = "green"
        field.append(square)

master.bind("<ButtonPress>", stage)
canvas.pack()
master.mainloop()
