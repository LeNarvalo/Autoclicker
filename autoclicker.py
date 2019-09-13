import threading
from pynput import keyboard, mouse
from tkinter import *

master = Tk()
master.geometry('500x50+0+0')
master.configure(background='black')
v = StringVar()
Label(master, textvariable=v, fg="white", bg="black").pack()
top_windows = []
class activEvent:
	Position = (0,0)
	Statut = 0
	Clicks = 0
	
def onMousePos(x, y):
	if activEvent.Position != (x, y):
		'''STOP'''
		activEvent.Statut = 0
		v.set('MOUSE MOVED\nPLEASE WAIT A FEW SECONDS...\n')

def click():
	while activEvent.Statut:
		mouse_C.press(mouse.Button.left)
		mouse_C.release(mouse.Button.left) 
		activEvent.Clicks += 1
	activEvent.Statut = 0
	mouse_L.stop()
	v.set('GAME OVER\n')
	v.set('CLICKS : '+str(activEvent.Clicks)+'\n')
	activEvent.Clicks = 0

def onKeyboardPress(key):
	global mouse_L
	if key == keyboard.Key.enter:
		activEvent.Position = mouse_C.position
		activEvent.Statut = 1
		mouse_L = mouse.Listener(on_move=onMousePos)
		mouse_L.start()
		v.set('GAME STARTED\n')
		th=threading.Thread(target=click)
		th.daemon = True
		th.start()

	elif key == keyboard.Key.esc:
		activEvent.Statut = 0
		v.set('KEYBOARD ABORDED\nPLEASE WAIT A FEW SECONDS...\n')
 
keyboard_L = keyboard.Listener(on_press=onKeyboardPress)
keyboard_L.start()
mouse_C = mouse.Controller()

while 1:
	master.wm_attributes("-topmost", 1)
	master.mainloop()
	continue

