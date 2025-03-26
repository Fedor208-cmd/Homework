import tkinter

master = tkinter.Tk()
canvas = tkinter.Canvas(master, bg="white", width=800, height=600)

# Геометрия

# Голова
canvas.create_oval((350, 10), (450, 110), fill="pink", outline="red")
# Глаза
canvas.create_oval((370, 20), (390, 40), fill="yellow", outline="orange")
canvas.create_oval((410, 20), (430, 40), fill="yellow", outline="orange")
# Нос
canvas.create_polygon((390, 60), (410, 60), (400, 100), fill="orange", outline="orange")
# Тело
canvas.create_rectangle((200, 110), (600, 300), fill="purple", outline="blue")
# Пуговицы
canvas.create_polygon((400, 120), (390, 200), (410, 200), fill="green", outline="black")
canvas.create_polygon((400, 210), (390, 290), (410, 290), fill="green", outline="black")
# Руки
canvas.create_oval((180, 185), (200, 205), fill="red", outline="pink")
canvas.create_oval((600, 185), (620, 205), fill="red", outline="pink")
# Ноги
canvas.create_rectangle((300, 300), (350, 450), fill="green", outline="green")
canvas.create_rectangle((450, 300), (500, 450), fill="green", outline="green")
# Ботинки
canvas.create_rectangle((150, 450), (350, 550), fill="grey", outline="black")
canvas.create_rectangle((450, 450), (650, 550), fill="grey", outline="black")
# Солнце
canvas.create_oval((600, -200), (1000, 200), fill="yellow", outline="orange")

canvas.pack()
master.mainloop()
