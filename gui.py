from tkinter import *
root=Tk()

c=Canvas(root, width=820, height=820, bg='white')
c.pack()
c.create_rectangle(0,0,800,800,fill='black',width=10)
c.create_oval(0,0,50,50,width=3,fill='red')
c.create_oval(50,0,100,50,width=3,fill='yellow')
c.create_oval(00,50,50,100,width=3,fill='lightgreen')
c.create_oval(50,50,100,100,width=3,fill='lightblue')
c.create_oval(750,750,800,800,width=3,fill='orange')
c.create_rectangle(0,100,100,150,width=2,fill='blue', outline="")
c.create_rectangle(150,0,200,150, width=2, fill="blue")
c.create_rectangle(300,50,700,100,width=2, fill='blue')
c.create_rectangle(100,200,150,700,width=2,fill='blue')
c.create_rectangle(250,200,300,700,width=2,fill='blue')
c.create_rectangle(400,200,450,700,width=2,fill='blue')
c.create_rectangle(550,200,600,700,width=2,fill='blue')
c.create_rectangle(700,200,750,700,width=2,fill='blue')


root.mainloop()




