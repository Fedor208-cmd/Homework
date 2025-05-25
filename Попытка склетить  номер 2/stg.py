import tkinter
import time
import random

w = 1000
h = 600
shift_x = w // 5
shift_y = h // 5

master_stage = tkinter.Tk()
canvas_stage = tkinter.Canvas(master_stage, bg="light blue", width=w, height=h)

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


# Функция проверки клика
def collision(event, button):
    xo1, yo1 = event.x, event.y
    xb1, xb2, yb1, yb2 = canvas_stage.coords(button)[0], canvas_stage.coords(button)[2], canvas_stage.coords(button)[1], \
        canvas_stage.coords(button)[3]
    if (xb1 < xo1 < xb2) and (yb1 < yo1 < yb2):
        return True
    return False


# Функция проверки пересечения объектов
def collision_objects(obj1, obj2):
    xb1, xb2, yb1, yb2 = canvas_stage.coords(obj1)[0], canvas_stage.coords(obj1)[2], canvas_stage.coords(obj1)[1], \
        canvas_stage.coords(obj1)[3]
    xo1, xo2, yo1, yo2 = canvas_stage.coords(obj2)[0], canvas_stage.coords(obj2)[2], canvas_stage.coords(obj2)[1], \
        canvas_stage.coords(obj2)[3]
    if (xo1 <= xb1 <= xo2 or xo1 <= xb2 <= xo2) and (yo1 <= yb1 <= yo2 or yo1 <= yb2 <= yo2) or \
            (xb1 <= xo1 <= xb2 or xb1 <= xo2 <= xb2) and (yb1 <= yo1 <= yb2 or yb1 <= yo2 <= yb2):
        return True
    return False


# Функции отрисовки растений
def sunflower_draw(xs, ys):
    coord = canvas_stage.create_oval((xs, ys), (xs + w // 10, ys + h // 5), outline="orange", fill="yellow")
    seeds = canvas_stage.create_oval((xs + 20, ys + 20), (xs + w // 10 - 20, ys + h // 5 - 20), outline="#542626",
                                     fill="#6E3131")
    return [coord, seeds]


def peashooter_draw(xp, yp):
    body = canvas_stage.create_rectangle((xp, yp + h // 15), (xp + w // 10, yp + 2 * h // 15), fill="#ADFF2F",
                                         outline="#2E8B57")
    hole = canvas_stage.create_rectangle((xp + w // 15, yp + h // 15 + 5), (xp + w // 10, yp + h // 15 + 35),
                                         fill="black")
    return [body, hole]


def potato_draw(xpt, ypt):
    mine = canvas_stage.create_oval((xpt, ypt), (xpt + w // 10, ypt + h // 5), fill="#FFEE92", outline="#FFD500")
    led = canvas_stage.create_oval((xpt + 30, ypt + 40), (xpt + w // 10 - 30, ypt + h // 5 - 40), fill="red")
    return [mine, led]


def nut_draw(xn, yn):
    wall = canvas_stage.create_oval((xn, yn), (xn + w // 10, yn + h // 5), fill="#CDAB66", outline="#957E4F")
    crack = canvas_stage.create_line((xn + w // 20, yn), (xn + w // 20, yn + h // 5), fill="#957E4F")
    return [wall, crack]


# Убийства и солнца игрока
amount_stage = tkinter.Label(text=f"Уровень: солнца: {suns}, убийства: {score} из {n}")
amount_stage.pack()

field = list()
colour = "green"

# Отрисовка кнопок выбора растений
button_sunflower = canvas_stage.create_rectangle((0, shift_y), (shift_x, (shift_y * 2)), fill="#D2B48C", outline="#8B4513")
xsa = canvas_stage.coords(button_sunflower)[0]
ysa = canvas_stage.coords(button_sunflower)[1]
canvas_stage.create_text(xsa + w // 7, ysa * 1.5, font=("Masquerade", w // 83), text="500")
canvas_stage.create_oval((xsa, ysa), (xsa + w // 10, ysa + h // 5), outline="orange", fill="yellow")
canvas_stage.create_oval((xsa + w // 50, ysa + 20), (xsa + w // 10 - w // 50, ysa + h // 5 - h // 30), outline="#542626", fill="#6E3131")

button_peashooter = canvas_stage.create_rectangle((0, shift_y * 2), (shift_x, (shift_y * 3)), fill="#D2B48C",
                                                outline="#8B4513")
canvas_stage.create_text(xsa + w // 7, ysa * 2.5, font=("Masquerade", w // 83), text="1000")
peashooter_draw(canvas_stage.coords(button_peashooter)[0], canvas_stage.coords(button_peashooter)[1])

button_potato = canvas_stage.create_rectangle((0, shift_y * 3), (shift_x, shift_y * 4), fill="#D2B48C", outline="#8B4513")
canvas_stage.create_text(xsa + w // 7, ysa * 3.5, font=("Masquerade", w // 83), text="5000")
potato_draw(canvas_stage.coords(button_potato)[0], canvas_stage.coords(button_potato)[1])

button_nut = canvas_stage.create_rectangle((0, shift_y * 4), (shift_x, shift_y * 5), fill="#D2B48C", outline="#8B4513")
canvas_stage.create_text(xsa + w // 7, ysa * 4.5, font=("Masquerade", 12), text="250")
nut_draw(canvas_stage.coords(button_nut)[0], canvas_stage.coords(button_nut)[1])

# Отрисовка поля
for y in range(0, h, h // 5):
    if colour == "green":
        colour = "dark green"
    elif colour == "dark green":
        colour = "green"
    for x in range(shift_x, w, (w - shift_x) // 8):
        if colour == "green":
            square = canvas_stage.create_rectangle((x, y), (x + w // 10, y + h // 5), fill=colour)
            colour = "dark green"
        else:
            square = canvas_stage.create_rectangle((x, y), (x + w // 10, y + h // 5), fill=colour)
            colour = "green"
        field.append(square)



def stage_play(event):
    # Зомби
    def zombie_spawn(x_l, y_l):
        global killed
        global spd
        global zombies
        global plants
        global potatoes
        global score
        global nuts
        global loss
        # Отрисовка
        zombie_mob = canvas_stage.create_oval((x_l, y_l), (x_l + w // 10, y_l + w // 10), fill="#808000", outline="#556B2F")
        health = 5
        zombies[zombie_mob] = health
        # Движение
        while canvas_stage.coords(zombie_mob)[0] > 0:
            time.sleep(0.09)
            canvas_stage.move(zombie_mob, -5 - spd, 0)
            canvas_stage.update()
            for targ in plants:
                for enemy in zombies.keys():
                    if (collision_objects(targ[0], enemy) or collision_objects(targ[1], enemy)) and not (targ[0] in nuts):
                        # Ест растение
                        print(targ[0] in nuts)
                        plants.remove(targ)
                        del used[targ[0]]
                        for elem in targ:
                            canvas_stage.delete(elem)
                        if targ in potatoes:
                            # Взрывается об картошку
                            zombies[enemy] -= 10
                            if zombies[enemy] <= 0:
                                canvas_stage.delete(enemy)
                                killed = True
                                del zombies[enemy]
                                score += 1
                            break
                    elif collision_objects(targ[0], enemy) or collision_objects(targ[1], enemy) and targ[0] in nuts:
                        # Прогрызает орех
                        while nuts[targ[0]] > 0:
                            nuts[targ[0]] -= 1
                            canvas_stage.move(enemy, 20, 0)
                            time.sleep(0.001)
                            while not collision_objects(targ[0], enemy):
                                time.sleep(0.09)
                                canvas_stage.move(enemy, -1.5, 0)
                                canvas_stage.update()
                        canvas_stage.delete(targ[0])
                        canvas_stage.delete(targ[1])
                        plants.remove(targ)
                        del nuts[targ[0]]
        # Зомби дошёл до конца
        if canvas_stage.coords(zombie_mob)[0] <= 0:
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
        # Выбор растения
        if collision(event, button_sunflower):
            plant = "Sunflower"
        if collision(event, button_peashooter):
            plant = "Peashooter"
        if collision(event, button_potato):
            plant = "Potato"
        if collision(event, button_nut):
            plant = "Nut"
        # Установка растения
        for pot in field:
            if collision(event, pot) and plant == "Sunflower" and pot not in used.values() and suns >= 500:
                a = sunflower_draw(canvas_stage.coords(pot)[0], canvas_stage.coords(pot)[1])
                sunflowers.append(a)
                plants.append(a)
                used[a[0]] = pot
                canvas_stage.update()
                plant = None
                suns -= 500
                break
            if collision(event, pot) and plant == "Peashooter" and pot not in used.values() and suns >= 1000:
                a = peashooter_draw(canvas_stage.coords(pot)[0], canvas_stage.coords(pot)[1])
                peashooters.append(a)
                plants.append(a)
                used[a[0]] = pot
                canvas_stage.update()
                plant = None
                suns -= 1000
                amount_stage.config(text=f"Уровень: солнца: {suns}, убийства: {score} из {n}")
                amount_stage.pack()
                break
            if collision(event, pot) and plant == "Potato" and pot not in used.values() and suns >= 5000:
                a = potato_draw(canvas_stage.coords(pot)[0], canvas_stage.coords(pot)[1])
                potatoes.append(a)
                plants.append(a)
                used[a[0]] = pot
                canvas_stage.update()
                plant = None
                suns -= 5000
                amount_stage.config(text=f"Уровень: солнца: {suns}, убийства: {score} из {n}")
                amount_stage.pack()
                break
            if collision(event, pot) and plant == "Nut" and pot not in used.values() and suns >= 250:
                a = nut_draw(canvas_stage.coords(pot)[0], canvas_stage.coords(pot)[1])
                nuts[a[0]] = 5
                plants.append(a)
                used[a[0]] = pot
                canvas_stage.update()
                plant = None
                suns -= 250
                amount_stage.config(text=f"Уровень: солнца: {suns}, убийства: {score} из {n}")
                amount_stage.pack()
                break
        # Функционал подсолнуха
        for s_fl in sunflowers:
            if collision(event, s_fl[0]):
                suns += 100 * len(sunflowers)
                amount_stage.config(text=f"Уровень: солнца: {suns}, убийства: {score} из {n}")
                amount_stage.pack()
        # Функционал горохострела
        for p_sh in peashooters:
            if collision(event, p_sh[0]) and len(peas) < 1:
                # Выстрел
                xb = canvas_stage.coords(p_sh[1])[2]
                yb1 = canvas_stage.coords(p_sh[1])[1]
                yb2 = canvas_stage.coords(p_sh[1])[3]
                pea = canvas_stage.create_oval((xb, yb1), (xb + (yb2 - yb1), yb2), fill="#00FF7F", outline="#3CB371")
                peas.append(pea)
                got = False
                # Горошина летит
                while canvas_stage.coords(pea)[2] < w:
                    time.sleep(0.05)
                    canvas_stage.move(pea, 10, 0)
                    canvas_stage.update()
                    for target in zombies:
                        # Наносит урон
                        if collision_objects(pea, target):
                            zombies[target] -= 1
                            y_zm = (random.randint(1, 4)) * h // 5 + h // 60
                            canvas_stage.moveto(target, canvas_stage.coords(target)[0], y_zm)
                            canvas_stage.delete(pea)
                            peas.remove(pea)
                            got = True
                        # Убивает
                        if zombies[target] == 0:
                            canvas_stage.delete(target)
                            killed = True
                            score += 1
                            amount_stage.config(text=f"Уровень: солнца: {suns}, убийства: {score} из {n}")
                            amount_stage.pack()
                            del zombies[target]
                            break
                # Промах
                if not got:
                    canvas_stage.delete(pea)
                    peas.remove(pea)
        # Спавн зомби
        if len(plants) >= r and killed:
            x_z = w - w // 10
            y_z = (random.randint(1, 4)) * h // 5 + h // 60
            killed = False
            spd += 0.25
            zombie_spawn(x_z, y_z)
        # Проигрыш
        if loss:
            for sol in plants:
                for elem in sol:
                    canvas_stage.delete(elem)
            for tr in zombies:
                canvas_stage.delete(tr)
            canvas_stage.create_text((w // 2, h // 2), font=("Masquerade", w // 10), text="Поражение", fill="red")
        # Победа
        if score == n:
            for sol in plants:
                for elem in sol:
                    canvas_stage.delete(elem)
            for tr in zombies:
                canvas_stage.delete(tr)
            canvas_stage.create_text((w // 2, h // 2), font=("Masquerade", w // 10), text="Победа", fill="#FFAB00")



    master_stage.bind("<ButtonPress>", stage)
    canvas_stage.pack()
    master_stage.mainloop()