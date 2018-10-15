from tkinter import *
from logic.field import Field, Cell
import threading
import multiprocessing as mp
import time



root=Tk()
W=800
H=800
w=16
h=16
dx=W/w
dy=H/h
c=Canvas(root, width=W, height=H, bg='white')
c.pack()
c.create_rectangle(0,0,W,H,fill='black',width=10)
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
c.pack()
root.mainloop()

def GetCoord():
	for y in range(h):
		for x in range(w):
			x=x*dx
			y=y*dy
			cell=field.data[y][x]
	
def GetChar(f):
	key=f.readline().strip('\n')			
	n=f.readline().strip()
	for i in range(len(n)):
		chars = list(f.readline().split(','))
		for char in chars:
			if char=='#':
				field.cell=Cell.Wall
			if char=='r':
				field.cell=Cell.RGhost
			if char=='b':
				field.cell=Cell.BGhost
			if char=='p':
				field.cell=Cell.PGhost
			if char=='y':
				field.cell=Cell.YGhost
			if char==' ':
				field.cell=Cell.Empty
			if char=='P':
				field.cell=Cell.Pacman				
	


data={}
with open('world.txt') as f:
	while True:
		try:
			GetChar(f)
			next(f)
		except StopIteration:
			break
			
matrix=[]
def GetSquares(matrix):
	for dy in range(field.height):
		matrix.append([])
		dy+=dy
		for dx in range(field.width):
			matrix[y].append(Cell())
			dx+=dx





