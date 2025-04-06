import tkinter

master = tkinter.Tk()
canvas = tkinter.Canvas(master, bg="#FFFFFF", width=240, height=200)

canvas.create_polygon((20,100), (120,10), (220, 100), fill="#B07D2B", outline="#36260D")
canvas.create_polygon((160, 30), (160,45), (180, 64), (180, 30), fill="#B07D2B", outline="#36260D")

canvas.create_oval((160, 10), (220, 30), fill="#99CCFF", outline="#80C0FF")

canvas.create_oval((100, 40), (140, 80), fill="#FFE533", outline="#FFC333")
canvas.create_line((100, 60), (140, 60), fill="#FFC333")
canvas.create_line((120, 40), (120, 80), fill="#FFC333")

canvas.create_rectangle((30, 100), (210, 190), fill="#38B050", outline="#38B050")

canvas.create_rectangle((50, 110), (110, 160), fill="#FFE533", outline="#FFC333")
canvas.create_line((80, 110), (80, 160), fill="#FFC333")
canvas.create_line((50, 130), (110, 130), fill="#FFC333")

canvas.create_rectangle((130, 110), (190, 160), fill="#FFE533", outline="#FFC333")
canvas.create_line((160, 110), (160, 160), fill="#FFC333")
canvas.create_line((130, 130), (190, 130), fill="#FFC333")

canvas.pack()
master.mainloop()
