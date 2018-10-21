from tkinter import *
from logic.field import Field, Cell
import threading
import multiprocessing as mp
import time
import sys
from logic.logic import Logic

del_step=[]
del_dots={}
count=0

def static(dx,dy,w,h):
	global count
	for y in range(h):
		for x in range(w):
			if logic.field.data[y][x]==Cell.Wall:
				c.create_rectangle(x*dx,y*dy,x*dx+dx,y*dy+dy, fill="blue")
	shift=15
	for y in range(h):
		for x in range(w):
			if logic.field.data[y][x]==Cell.Dot:
				del_dot=c.create_oval(x*dx+shift, y*dy+shift, x*dx+dx-shift, y*dy+dy-shift, fill='black')		
				del_dots[(x,y)]=del_dot
				count += 1
	return count			
	c.pack()			
					
def dynamic(c,info):
	pacman = info[0]
	ghosts = info[1]
	dots = info[2]	
	for item in del_step:
		c.delete(item)
	del_step.clear()	
	x_P=pacman[0]*dx
	y_P=pacman[1]*dy
	del_step.append(c.create_oval(x_P,y_P, x_P+dx, y_P+dy, fill="orange"))
	for ghost in range(len(ghosts)):
		x=ghosts[ghost][0]*dx
		y=ghosts[ghost][1]*dy
		col=ghosts[ghost][2]
		del_step.append(c.create_oval(x,y,x+dx,y+dy,fill=col))
	
	for dot in dots:
		c.delete(del_dots[dot])
		if ((count-len(dots))==0):
			logic.stop_game()
			c.create_text(380,350,fill="cyan",font="Purisa 50 bold",text="You win!")
			c.create_text(380,400,fill="magenta",font="Purisa 50 bold",text="You win!")
			c.create_text(380,450,fill="red",font="Purisa 50 bold",text="You win!")
    		

def control(logic, event):
	if event.char=='w':
		logic.move_pacman((0,-1))
	if event.char=='d':
		logic.move_pacman((1,0))
	if event.char=='s':
		logic.move_pacman((0,1))
	if event.char=='a':
		logic.move_pacman((-1,0))		





if __name__ == '__main__':
	root=Tk()
	Logic.set_thread_mode()
	logic=Logic.load_file('world.txt')
	info=logic.get_state()
	W=800
	H=800
	w=logic.field.width
	h=logic.field.height
	dx=W/w
	dy=H/h
	c=Canvas(root, width=W, height=H, bg='white')
	c.pack()
	root.bind('<Key>', lambda event: control(logic, event))

	def dyn():
		info=logic.get_state()
		dynamic(c, info)
		if not info[-1]:
			logic.stop_game()
			c.create_text(380,400,fill="maroon",font="Purisa 50 bold",text="GAME OVER!\n   You lose!")
		else:	
			root.after(250, dyn)
	
	static(dx,dy,w,h)
	root.after(250, dyn)
	def stop():
		logic.stop_game()
		time.sleep(0.1)
		sys.exit()
	root.protocol("WM_DELETE_WINDOW", stop)
	root.mainloop()
'''
c.create_rectangle(0,0,W,H,fill='black',width=10)
pG=c.create_oval(0,0,50,50,width=3,fill='green')
yG=c.create_oval(50,0,100,50,width=3,fill='yellow')
rG=c.create_oval(00,50,50,100,width=3,fill='red')
bG=c.create_oval(50,50,100,100,width=3,fill='lightblue')
PG=c.create_oval(750,750,800,800,width=3,fill='orange')
c.create_rectangle(0,100,100,150,width=2,fill='blue', outline="")
c.create_rectangle(150,0,200,150, width=2, fill="blue")
c.create_rectangle(300,50,700,100,width=2, fill='blue')
c.create_rectangle(100,200,150,700,width=2,fill='blue')
c.create_rectangle(250,200,300,700,width=2,fill='blue')
c.create_rectangle(400,200,450,700,width=2,fill='blue')
c.create_rectangle(550,200,600,700,width=2,fill='blue')
c.create_rectangle(700,200,750,700,width=2,fill='blue')
c.pack()
root.mainloop()
'''


	







