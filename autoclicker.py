import threading, time, os, winsound
from pynput import keyboard, mouse
from tkinter import *
from tkinter.messagebox import *

chemin = os.path.expanduser('~\\autoclicker')
	
OK = 1
master = Tk()
master.configure(background='black',bd=1)
master.overrideredirect(True)
v = StringVar()
Label(master, textvariable=v, fg="white", bg="black").grid(row=0, column=0, columnspan=3, sticky=N+S+W+E)
v.set('PRESS ENTER TO START')
l = Label(master,text="CLICKS BY SECOND :")
l.grid(row=1, column=0, sticky=N+S+W+E)
launched = 0
sec = 0
mouseSens = 1
listen = 1
timeLaunch = time.time()

class activEvent:
	Position = (0,0)
	Statut = 0
	Clicks = 0

def callback(empty):
	th2 = threading.Timer(0.5,getTimer)
	th2.start()
	print("callback")
		
def getTimer():
	global sec	
	if int(var.get()) <= 0 or int(var.get()) > 1000 :
			sec = 1
			var.set("1")
	else:
		sec = 1/int(var.get())

var = StringVar()
s = Spinbox(master, from_=1, to=1000,width=5,increment=5,textvariable=var)
s.bind("<ButtonRelease-1>", callback)
s.grid(row=1, column=1, columnspan=2, sticky=N+S+W+E)
var.set("20")
	
def onMousePos(x, y):
	if activEvent.Position != (x, y) and mouseSens:
		'''STOP'''
		activEvent.Statut = 0
		v.set('MOUSE MOVED\nPLEASE WAIT A FEW SECONDS...')

def click():
	global launched
	while activEvent.Statut:
		mouse_C.press(mouse.Button.left)
		mouse_C.release(mouse.Button.left) 
		activEvent.Clicks += 1
		v.set('CURRENT CLICKS : '+str(activEvent.Clicks)+'')
		time.sleep(sec)
	activEvent.Statut = 0
	mouse_L.stop()
	v.set('GAME OVER')
	v.set('TOTAL CLICKS : '+str(activEvent.Clicks)+' IN '+str(int(round((time.time()-startingTime),3)*1000))+' MILLISECONDS')
	activEvent.Clicks = 0
	s.configure(state=NORMAL)
	c.configure(state=NORMAL)
	c3.configure(state=NORMAL)
	launched = 0
	th5 = threading.Thread(target=delayOver)
	th5.start()
	s.bind("<ButtonRelease-1>", callback)
	c.bind("<ButtonRelease-1>", cochage)
	try:
		c2.bind("<ButtonRelease-1>", cochage2)
	except:
		None
	c3.bind("<ButtonRelease-1>", cochage3)
	
def onScroll(x, y, dx, dy):
	if dy > 0:
		var.set(str(int(var.get())+5))
	else :
		var.set(str(int(var.get())-5))
	callback(None)	

def blink():
	count = 0
	while count < 5:
		master.configure(bg="white")
		time.sleep(0.1)
		master.configure(bg="black")
		time.sleep(0.1)
		count+=1	
		
def onKeyboardPress(key):
	global mouse_L, sec, OK, startingTime, launched
	if key == keyboard.Key.enter and activEvent.Statut == 0:
		s.unbind("<ButtonRelease-1>")
		c.unbind("<ButtonRelease-1>")
		try:
			c2.unbind("<ButtonRelease-1>")
		except:
			None
		c3.unbind("<ButtonRelease-1>")
		th6 = threading.Thread(target=blink)
		th6.start()
		launched = 1
		if int(var.get()) == 0 or int(var.get()) > 1000 :
			sec = 1
			var.set("1")
		else:
			sec = 1/int(var.get())
		activEvent.Position = mouse_C.position
		activEvent.Statut = 1
		mouse_L = mouse.Listener(on_move=onMousePos)
		mouse_L.start()
		v.set('GAME STARTED')
		s.configure(state=DISABLED)
		c.configure(state=DISABLED)
		c3.configure(state=DISABLED)
		startingTime = time.time()
		th=threading.Thread(target=click)
		th.start()

	elif key == keyboard.Key.esc and activEvent.Statut == 1:
		activEvent.Statut = 0
		v.set('KEYBOARD ABORDED\nPLEASE WAIT A FEW SECONDS...')
	
	elif key == keyboard.Key.esc and activEvent.Statut == 0:
		OK = 0
		v.set('BYE BYE...')
		time.sleep(3)
		master.destroy()
 


def cochage(empty):
	th3 = threading.Timer(0.5,getCoche)
	th3.start()

def getCoche():
	global mouseSens
	mouseSens = msv.get()

msv = IntVar()
c = Checkbutton(master, text="MOUSE'S MOVE ABLE TO STOP", variable=msv,state=NORMAL)
c.grid(row=2, column=0, columnspan=2,sticky=N+S+N+S+W+E)
c.bind("<ButtonRelease-1>", cochage)
c.select()

def cochage2(empty):
	th4 = threading.Timer(0.5,getCoche2)
	th4.start()
	
def getCoche2():
	file = open(chemin+"\\yet_read.txt","w")
	if msg.get():
		file.write("Ne plus afficher cette fenêtre au lancement")
	else:
		file.write=""
	file.close()

def help():
	global msg,c2
	top=Toplevel(master)
	top.title("Maitriser ce logiciel en 42 étapes ☻")
	top.resizable(0,0)	
	lab2=Label(top, text='ATTENTION : Ce logiciel peut entrainer des erreurs irrémédiables si vous ne l\'utilisez pas correctement!!!',font=("Arial Black", 12),wraplength=500,justify=CENTER,fg="red")
	lab=Label(top, text='Ce logiciel permet de cliquer à l\'endroit de votre curseur automatiquement et à une fréquence définie.\n\nAppuyez sur Entrée pour commencer et Echap pour arrêter le clic automatique ou fermer le logiciel. Lorsque vous cochez "MOUSE\'S MOVE ABLE TO STOP" les mouvements de la souris arrêtent le clic automatique également. La molette de votre souris permet d\'accélerer ou diminuer le nombre de cliques par seconde.\n\nMinimum : 1/sec\nMaximum : 1000/sec si votre ordinateur le permet.',wraplength=500,justify=LEFT)
	line = Canvas(top, width=450, height=5)
	line.create_line(10,5,490,5, width=2, fill="red")	
	line2 = Canvas(top, width=450, height=5)
	line2.create_line(10,5,490,5, width=2, fill="red")
	msg = IntVar()
	c2 = Checkbutton(top, text="Ne plus afficher cette fenêtre au lancement", variable=msg)
	c2.bind("<ButtonRelease-1>", cochage2)
	liste=[lab2,line,lab,line2,c2]
	r = -1	
	for arg in liste:
		r+=1
		arg.grid(row=r,column=0,sticky=W)
	winsound.MessageBeep()
	top.geometry("500x370+250+150")
	msg.set(nePlusAficher())

def delayOver():
	while not launched:
		if (int(time.time()) - int(timeLaunch))%30==0:
			blink()
		time.sleep(0.75)
		
def nePlusAficher():
	try:
		file = open(chemin+"\\yet_read.txt","r")
		text = file.read()
		file.close()
		if "Ne plus afficher cette fenêtre au lancement" in text:
			return 1
		else:
			return 0
	except:
		return 0
		
h = Button(master,text="?",command=help)
h.grid(row=2,column=2,  sticky=N+S+W+E)

def cochage3(empty):
	global listen, keyboard_L, mouse_L2, mouse_L
	listen = 1-ltn .get()
	if not listen:
		try:
			keyboard_L.stop()
			mouse_L2.stop()
			mouse_L.stop()
		except:
			None
	else:
		start()
	print(listen)

ltn = IntVar()
c3 = Checkbutton(master, text="LISTENING", variable=ltn ,state=NORMAL)
c3.grid(row=3, column=0, columnspan=3,sticky=N+S+N+S+W+E)
c3.bind("<ButtonRelease-1>", cochage3)
c3.select()

th5 = threading.Thread(target=delayOver)
th5.start()

def start():
	global keyboard_L, mouse_L2
	keyboard_L = keyboard.Listener(on_press=onKeyboardPress)
	keyboard_L.start()
	mouse_L2 = mouse.Listener(on_scroll=onScroll)
	mouse_L2.start()
	
mouse_C = mouse.Controller()	
start()

if not nePlusAficher():
	help()

while OK:	
	master.wm_attributes("-topmost", 1)
	master.mainloop()
	continue


