import tkinter

master = tkinter.Tk()
canvas = tkinter.Canvas(master, bg="#FFFFFF", width=200, height=210)

canvas.create_oval((70, 70), (130, 200), fill="#FFEAAE", outline="#A99F84")

canvas.create_arc((30, 30), (170, 170), extent=180, fill="red", outline="red")

canvas.create_oval((50, 70), (70, 90), fill="white", outline="white")
canvas.create_oval((130, 70), (150, 90), fill="white", outline="white")
canvas.create_oval((90, 40), (110, 60), fill="white", outline="white")

canvas.create_rectangle((80, 190), (120, 200), fill="white", outline="white")

canvas.create_rectangle((30, 180), (170, 190), fill="#75E421", outline="#2ECD1C")

canvas.pack()
master.mainloop()
