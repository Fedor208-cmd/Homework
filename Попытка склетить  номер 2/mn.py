import tkinter
from ttrl import tutorial_play
from stg import stage_play
from bss import boss_play

w = 1000
h = 600
shift_x = w // 5
shift_y = h // 5

master = tkinter.Tk()
canvas = tkinter.Canvas(master, bg="light blue", width=w, height=h)


# Функция проверки нажатия
def click(event, button):
    xo1, yo1 = event.x, event.y
    xb1, xb2, yb1, yb2 = (canvas.coords(button)[0], canvas.coords(button)[2], canvas.coords(button)[1],
                          canvas.coords(button)[3])
    if (xb1 < xo1 < xb2) and (yb1 < yo1 < yb2):
        print("hghghghg")
        return True
    print("afdasefe")
    return False


# Отрисовываем меню
name_txt = canvas.create_text(w // 2, h // 12, font=("Masquerade", 50), text="Plants VS Zombies")
creator = canvas.create_text(w // 2, h // 5, font=("Masquerade", 10), text="By Фалев Фёдор из 8 класса М")

button_tutorial = canvas.create_rectangle((2,  h // 3), (w // 3 - w // 50, 2 * h // 3), fill="grey")
txt_tutorial = canvas.create_text(w // 6, h // 2, font=("Masquerade", 40), fill="lime", text="Обучение")

button_stage = canvas.create_rectangle((w // 3 + w // 50,  h // 3), (2 * w // 3 - w // 50, 2 * h // 3), fill="grey")
txt_stage = canvas.create_text(w // 2, h // 2, font=("Masquerade", 40), fill="lime", text="Уровень")

button_boss = canvas.create_rectangle((2 * w // 3 + w // 50,  h // 3), (w - 2, 2 * h // 3), fill="grey")
txt_boss = canvas.create_text(5 * w // 6, h // 2, font=("Masquerade", 40), fill="lime", text="Босс")


def menu(event):
    # Проверка куда нажал игрок
    global button_tutorial, button_stage, button_boss
    if click(event, button_tutorial):
        tutorial_play(event)
    elif click(event, button_stage):
        stage_play(event)
    elif click(event, button_boss):
        boss_play(event)


master.bind("<ButtonPress>", menu)
canvas.pack()
master.mainloop()
