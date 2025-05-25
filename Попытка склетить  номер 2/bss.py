import tkinter
import time

w = 1000
h = 600
shift_x = w // 5
shift_y = h // 5

master_boss = tkinter.Tk()
canvas_boss = tkinter.Canvas(master_boss, bg="light blue", width=w, height=h)

suns = 500
score = 0
sunflowers = list()
peashooters = list()
potatoes = list()
used = dict()
zombies = dict()
plants = list()
nuts = dict()
peas = list()
plant = None
r = 3
n = 1
loss = False
fight = False


# Функция проверки клика
def collision(event, button):
    xo1, yo1 = event.x, event.y
    xb1, xb2, yb1, yb2 = canvas_boss.coords(button)[0], canvas_boss.coords(button)[2], canvas_boss.coords(button)[1], \
        canvas_boss.coords(button)[3]
    if (xb1 < xo1 < xb2) and (yb1 < yo1 < yb2):
        return True
    return False


# Функция проверки пересечения объектов
def collision_objects(obj1, obj2):
    xb1, xb2, yb1, yb2 = canvas_boss.coords(obj1)[0], canvas_boss.coords(obj1)[2], canvas_boss.coords(obj1)[1], \
        canvas_boss.coords(obj1)[3]
    xo1, xo2, yo1, yo2 = canvas_boss.coords(obj2)[0], canvas_boss.coords(obj2)[2], canvas_boss.coords(obj2)[1], \
        canvas_boss.coords(obj2)[3]
    if (xo1 <= xb1 <= xo2 or xo1 <= xb2 <= xo2) and (yo1 <= yb1 <= yo2 or yo1 <= yb2 <= yo2) or \
            (xb1 <= xo1 <= xb2 or xb1 <= xo2 <= xb2) and (yb1 <= yo1 <= yb2 or yb1 <= yo2 <= yb2):
        return True
    return False


# Функции отрисовки растений
def sunflower_draw(xs, ys):
    coord = canvas_boss.create_oval((xs, ys), (xs + w // 10, ys + h // 5), outline="orange", fill="yellow")
    seeds = canvas_boss.create_oval((xs + 20, ys + 20), (xs + w // 10 - 20, ys + h // 5 - 20), outline="#542626",
                                    fill="#6E3131")
    return [coord, seeds]


def peashooter_draw(xp, yp):
    body = canvas_boss.create_rectangle((xp, yp + h // 15), (xp + w // 10, yp + 2 * h // 15), fill="#ADFF2F",
                                        outline="#2E8B57")
    hole = canvas_boss.create_rectangle((xp + w // 15, yp + h // 15 + 5), (xp + w // 10, yp + h // 15 + 35),
                                        fill="black")
    return [body, hole]


def potato_draw(xpt, ypt):
    mine = canvas_boss.create_oval((xpt, ypt), (xpt + w // 10, ypt + h // 5), fill="#FFEE92", outline="#FFD500")
    led = canvas_boss.create_oval((xpt + 30, ypt + 40), (xpt + w // 10 - 30, ypt + h // 5 - 40), fill="red")
    return [mine, led]


def nut_draw(xn, yn):
    wall = canvas_boss.create_oval((xn, yn), (xn + w // 10, yn + h // 5), fill="#CDAB66", outline="#957E4F")
    crack = canvas_boss.create_line((xn + w // 20, yn), (xn + w // 20, yn + h // 5), fill="#957E4F")
    return [wall, crack]


# Убийства и солнца игрока
amount_boss = tkinter.Label(text=f"Босс: солнца: {suns}, убийства: {score} из {n}")
amount_boss.pack()

field = list()
colour = "green"

# Отрисовка кнопок выбора растений
button_sunflower = canvas_boss.create_rectangle((0, shift_y), (shift_x, (shift_y * 2)), fill="#D2B48C", outline="#8B4513")
xsa = canvas_boss.coords(button_sunflower)[0]
ysa = canvas_boss.coords(button_sunflower)[1]
canvas_boss.create_text(xsa + 150, ysa * 1.5, font=("Masquerade", 12), text="500")
canvas_boss.create_oval((xsa, ysa), (xsa + w // 10, ysa + h // 5), outline="orange", fill="yellow")
canvas_boss.create_oval((xsa + 20, ysa + 20), (xsa + w // 10 - 20, ysa + h // 5 - 20), outline="#542626", fill="#6E3131")

button_peashooter = canvas_boss.create_rectangle((0, shift_y * 2), (shift_x, (shift_y * 3)), fill="#D2B48C",
                                                outline="#8B4513")
canvas_boss.create_text(xsa + 150, ysa * 2.5, font=("Masquerade", 12), text="1000")
peashooter_draw(canvas_boss.coords(button_peashooter)[0], canvas_boss.coords(button_peashooter)[1])

button_potato = canvas_boss.create_rectangle((0, shift_y * 3), (shift_x, shift_y * 4), fill="#D2B48C", outline="#8B4513")
canvas_boss.create_text(xsa + 150, ysa * 3.5, font=("Masquerade", 12), text="5000")
potato_draw(canvas_boss.coords(button_potato)[0], canvas_boss.coords(button_potato)[1])

button_nut = canvas_boss.create_rectangle((0, shift_y * 4), (shift_x, shift_y * 5), fill="#D2B48C", outline="#8B4513")
canvas_boss.create_text(xsa + 150, ysa * 4.5, font=("Masquerade", 12), text="250")
nut_draw(canvas_boss.coords(button_nut)[0], canvas_boss.coords(button_nut)[1])

# Отрисовка поля
for y in range(0, h, h // 5):
    if colour == "green":
        colour = "dark green"
    elif colour == "dark green":
        colour = "green"
    for x in range(shift_x, w, (w - shift_x) // 8):
        if colour == "green":
            square = canvas_boss.create_rectangle((x, y), (x + w // 10, y + h // 5), fill=colour)
            colour = "dark green"
        else:
            square = canvas_boss.create_rectangle((x, y), (x + w // 10, y + h // 5), fill=colour)
            colour = "green"
        field.append(square)



def boss_play(event):
    # Зомби
    def boss_spawn(x_l):
        global zombies
        global plants
        global potatoes
        global score
        global nuts
        global loss
        # Отрисовка
        zombie_mob = canvas_boss.create_oval((x_l, 0), (x_l + w // 10, h), fill="#808000", outline="#556B2F")
        health = 70
        zombies[zombie_mob] = health
        # Движение
        while canvas_boss.coords(zombie_mob)[0] > 0:
            time.sleep(0.09)
            canvas_boss.move(zombie_mob, -1.5, 0)
            canvas_boss.update()
            for targ in plants:
                for enemy in zombies.keys():
                    if (collision_objects(targ[0], enemy) or collision_objects(targ[1], enemy)) and not (targ[0] in nuts):
                        # Ест растение
                        print(targ[0] in nuts)
                        plants.remove(targ)
                        del used[targ[0]]
                        for elem in targ:
                            canvas_boss.delete(elem)
                        if targ in potatoes:
                            # Взрывается об картошку
                            zombies[enemy] -= 10
                            if zombies[enemy] <= 0:
                                canvas_boss.delete(enemy)
                                del zombies[enemy]
                                score += 1
                            break
                    elif collision_objects(targ[0], enemy) or collision_objects(targ[1], enemy) and targ[0] in nuts:
                        # Прогрызает орех
                        while nuts[targ[0]] > 0:
                            nuts[targ[0]] -= 1
                            canvas_boss.move(enemy, 20, 0)
                            time.sleep(0.001)
                            while not collision_objects(targ[0], enemy):
                                time.sleep(0.09)
                                canvas_boss.move(enemy, -1.5, 0)
                                canvas_boss.update()
                        canvas_boss.delete(targ[0])
                        canvas_boss.delete(targ[1])
                        plants.remove(targ)
                        del nuts[targ[0]]
        # Зомби дошёл до конца
        if canvas_boss.coords(zombie_mob)[0] == 0:
            loss = True


    def stage(event):
        global plant
        global suns
        global used
        global sunflowers
        global zombies
        global plants
        global r
        global peashooters
        global score
        global potatoes
        global n
        global loss
        global fight
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
            if collision(event, pot) and plant == "Sunflower" and pot not in used and suns >= 500:
                a = sunflower_draw(canvas_boss.coords(pot)[0], canvas_boss.coords(pot)[1])
                sunflowers.append(a)
                plants.append(a)
                used[a[0]] = pot
                canvas_boss.update()
                plant = None
                suns -= 500
                break
            if collision(event, pot) and plant == "Peashooter" and pot not in used and suns >= 1000:
                a = peashooter_draw(canvas_boss.coords(pot)[0], canvas_boss.coords(pot)[1])
                peashooters.append(a)
                plants.append(a)
                used[a[0]] = pot
                canvas_boss.update()
                plant = None
                suns -= 1000
                amount_boss.config(text=f"Босс: солнца: {suns}, убийства: {score} из {n}")
                amount_boss.pack()
                break
            if collision(event, pot) and plant == "Potato" and pot not in used and suns >= 5000:
                a = potato_draw(canvas_boss.coords(pot)[0], canvas_boss.coords(pot)[1])
                potatoes.append(a)
                plants.append(a)
                used[a[0]] = pot
                canvas_boss.update()
                plant = None
                suns -= 1000
                amount_boss.config(text=f"Босс: солнца: {suns}, убийства: {score} из {n}")
                amount_boss.pack()
                break
            if collision(event, pot) and plant == "Nut" and pot not in used and suns >= 250:
                a = nut_draw(canvas_boss.coords(pot)[0], canvas_boss.coords(pot)[1])
                nuts[a[0]] = 5
                plants.append(a)
                used[a[0]] = pot
                canvas_boss.update()
                plant = None
                suns -= 250
                amount_boss.config(text=f"Босс: солнца: {suns}, убийства: {score} из {n}")
                amount_boss.pack()
                break
        # Функционал подсолнуха
        for s_fl in sunflowers:
            if collision(event, s_fl[0]):
                suns += 100 * len(sunflowers)
                amount_boss.config(text=f"Босс: солнца: {suns}, убийства: {score} из {n}")
                amount_boss.pack()
        # Функционал горохострела
        for p_sh in peashooters:
            if collision(event, p_sh[0]) and len(peas) == 0:
                # Выстрел
                xb = canvas_boss.coords(p_sh[1])[2]
                yb1 = canvas_boss.coords(p_sh[1])[1]
                yb2 = canvas_boss.coords(p_sh[1])[3]
                pea = canvas_boss.create_oval((xb, yb1), (xb + (yb2 - yb1), yb2), fill="#00FF7F", outline="#3CB371")
                peas.append(pea)
                got = False
                # Горошина летит
                while canvas_boss.coords(pea)[2] < w:
                    time.sleep(0.05)
                    canvas_boss.move(pea, 10, 0)
                    canvas_boss.update()
                    for target in zombies:
                        # Выстрел
                        if collision_objects(pea, target):
                            zombies[target] -= 1
                            canvas_boss.delete(pea)
                            peas.remove(pea)
                            got = True
                            break
                        # Убивает
                        if zombies[target] == 0:
                            canvas_boss.delete(target)
                            score += 1
                            amount_boss.config(text=f"Босс: солнца: {suns}, убийства: {score} из {n}")
                            amount_boss.pack()
                            del zombies[target]
                            break
                # Промах
                if not got:
                    canvas_boss.delete(pea)
                    peas.clear()
        # Спавн зомби
        if len(plants) == r and not fight:
            x_z = 900
            r += 0
            fight = True
            boss_spawn(x_z)
        # Проигрыш
        if loss:
            for sol in plants:
                for elem in sol:
                    canvas_boss.delete(elem)
            for tr in zombies:
                canvas_boss.delete(tr)
            canvas_boss.create_text((w // 2, h // 2), font=("Masquerade", 100), text="Поражение", fill="red")
        # Победа
        if score == n:
            for sol in plants:
                for elem in sol:
                    canvas_boss.delete(elem)
            for tr in zombies:
                canvas_boss.delete(tr)
            canvas_boss.create_text((w // 2, h // 2), font=("Masquerade", 100), text="Победа", fill="#FFAB00")

    master_boss.bind("<ButtonPress>", stage)
    canvas_boss.pack()
    master_boss.mainloop()