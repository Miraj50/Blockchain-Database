from tkinter import *
import tkinter.messagebox as msgbox
from tkinter import scrolledtext
from tkinter import simpledialog
import requests
import os, hashlib
from Crypto.PublicKey import RSA
import tkinter.ttk

class maxWindow:
	def __init__(self):
		self.tk = Tk()
		self.tk.attributes('-zoomed', True)
		# self.frame = Frame(self.tk)
		# self.frame.pack()
		self.state = False
		self.tk.bind("<F11>", self.toggle_fullscreen)
		self.tk.bind("<Escape>", self.end_fullscreen)

	def toggle_fullscreen(self, event=None):
		self.state = not self.state  # Just toggling the boolean
		self.tk.attributes("-fullscreen", self.state)
		return "break"

	def end_fullscreen(self, event=None):
		self.state = False
		self.tk.attributes("-fullscreen", False)
		return "break"

sess = requests.Session()



def Start():
	global startS
	global uname

	startS = Tk()
	# startS = maxWindow().tk
	startS.title('Welcome to BcD')
	startS.grid_columnconfigure(0, weight=1)
	startS.grid_columnconfigure(4, weight=1)
	# startS.grid_rowconfigure(0, weight=1)
	startS.grid_rowconfigure(11, weight=1)

	#Login
	loginText = Label(startS, text='Login', font='Helvetica 16 bold', fg='darkblue')
	loginText.grid(row=1, columnspan=2, column=1, pady=(5,10))
 
	name = Label(startS, text='Username')
	pword = Label(startS, text='Password')
	name.grid(row=2, column=1, padx=(0,5), pady=(5,5), sticky=E)
	pword.grid(row=3, column=1, padx=(0,5), pady=(5,5), sticky=E)
 
	nameBox = Entry(startS)
	pwordBox = Entry(startS, show='*')
	nameBox.grid(row=2, column=2, padx=(0,0), pady=(5,5))
	pwordBox.grid(row=3, column=2, padx=(0,0), pady=(5,5))
 
	loginButton = Button(startS, text='Login',bg='blue',fg='white', command=lambda: CheckLogin(nameBox.get(), pwordBox.get()))
	loginButton.grid(columnspan=2, row=4, column=1, pady=(5,10))
	# loginButton.bind('<Return>', lambda e: CheckLogin(nameBox.get(), pwordBox.get()))

	tkinter.ttk.Separator(startS, orient=HORIZONTAL).grid(column=1, row=5, columnspan=3, sticky='nsew')

	#SignUp
	signUpText = Label(startS, text='Sign Up', font='Helvetica 16 bold', fg='brown')
	signUpText.grid(row=5, columnspan=2, column=1, pady=(10,10))
	
	SuName = Label(startS, text='Choose Username') # More labels
	SuPword = Label(startS, text='Enter Password') # ^
	SuName.grid(row=6, column=1, padx=(30,5), pady=(5,5), sticky=E)
	SuPword.grid(row=7, column=1, padx=(30,5), pady=(5,5), sticky=E)
	
	SuNameBox = Entry(startS) # The entry input
	SuPwordBox = Entry(startS, show='*')
	SuNameBox.grid(row=6, column=2, padx=(0,0), pady=(5,5))
	SuPwordBox.grid(row=7, column=2, padx=(0,0), pady=(5,5))

	text = Label(startS, text='Enter PassPhrase')
	text.grid(row=8, column=1, padx=(30,0), pady=(5,5))
	passPh = Entry(startS, show='*')
	passPh.grid(row=8, column=2, padx=(0,0), pady=(5,5), sticky=W)

	SignUpButton = Button(startS, text='Sign Up', bg='brown', fg='white', command=lambda: SignUp(SuNameBox.get(), SuPwordBox.get(), passPh.get()))
	SignUpButton.grid(columnspan=2, row=10, column=1, pady=(5,10))

	img = PhotoImage(file='q.gif')
	PPhelp = Button(startS, image=img, text='?', command=lambda :msgbox.showinfo('Info','This PassPhrase will be used for generating your Private Key'))
	PPhelp.grid(row=8, column=3, padx=(0,20))

	startS.mainloop()

def checkEmpty(uid, pword):
	if(len(uid)==0):
		msgbox.showerror('Error', 'Please Enter Username')
		return 0
	if(len(pword)==0):
		msgbox.showerror('Error', 'Please Enter Password')
		return 0
	return 1

def submitPP(passP):
	pass

def Home():
	# global uname
	global homeP
	uname='puru'
	homeP = Tk()
	# homeP = maxWindow().tk
	homeP.grid_rowconfigure(2, weight=1)
	homeP.grid_columnconfigure(1, weight=1)
	homeP.grid_columnconfigure(0, weight=1)
	homeP.title('Grades')

	topF = Frame(homeP)

	top = Label(topF, text='Signed In as : ')
	# top.grid(row=0, column=0, padx=(20,0), pady=(5,5), sticky="ew")
	top.pack(side='left', expand=False)
	u = Label(topF, text=uname, font='Helvetica 10 bold', bg='lightblue')
	# u.grid(row=0, column=1, padx=(0,100), pady=(5,5))
	u.pack(side='left', expand=False)

	topF.grid(row=0, column=0, padx=(10,0), pady=(5,5), sticky="w")
	logoutButton = Button(homeP, text='LogOut', bg='brown', fg='white', command=Logout)
	logoutButton.grid(row=0, column=1, padx=(0,10), pady=(5,5), sticky="e")

	tkinter.ttk.Separator(homeP, orient=HORIZONTAL).grid(column=0, row=1, columnspan=2, sticky='nsew')

	enterButton = Button(homeP, text='Enter Grades', bg='blue', fg='white', command=enterG)
	enterButton.grid(row=1, column=0, padx=(40,5), pady=(5,2), sticky="e")
	viewButton = Button(homeP, text='View Grades', bg='blue', fg='white', command=viewG)
	viewButton.grid(row=1, column=1, padx=(5,40), pady=(5,2), sticky="w")

	tkinter.ttk.Separator(homeP, orient=HORIZONTAL).grid(column=0, row=2, columnspan=2, sticky='nsew')	

	homeP.mainloop()

curFrame = ''

def enterG():
	global homeP
	global eGrade
	global vGrade
	global curFrame

	homeP.geometry("") #Thanks to Bryan Oakley "stackoverflow.com/questions/53170983"

	if curFrame == 'v':
		vGrade.grid_forget()
	
	if 'eGrade' not in globals(): #Prevent Leaks
		eGrade = Frame(homeP)
		# eGrade.grid_columnconfigure(0, weight=1) # Along with sticky=ewns will resize to full window
		eGrade.grid_rowconfigure(0, weight=1)

		enterGrades = scrolledtext.ScrolledText(eGrade, font='Times 11', wrap='word', spacing2=0, spacing3=7, width=64, height=10)
		enterGrades.grid(row=0, column=0, sticky="ewns")

		enterGBut = Button(eGrade, text='Submit Grades', bg='green', fg='white', command=lambda: submitG(enterGrades.get("1.0", 'end-1c')))
		enterGBut.grid(row=1, column=0, columnspan=2, pady=(0,0), sticky="ns")
		eGrade.grid(row=2, column=0, columnspan=2, padx=(10,10), pady=(1,5), sticky="ns")
	else:
		eGrade.grid(row=2, column=0, columnspan=2, padx=(10,10), pady=(1,5), sticky="ns")
	curFrame = 'e'

	# for name, value in globals().copy().items():
	# 	print(name, value)
	
def submitG(grades):
	print(grades)

def viewG():
	global homeP
	global eGrade
	global vGrade
	global curFrame

	if curFrame == 'e':
		eGrade.grid_forget()

	if 'vGrade' not in globals(): #Prevent Leaks
		vGrade = Frame(homeP)
		# vGrade.grid_columnconfigure(0, weight=1)
		vGrade.grid_rowconfigure(0, weight=1)

		viewList = Listbox(vGrade, font='Times 11', width=64, height=15, relief='sunken', justify="center")
		viewList.insert(1, "160050029    |    CS333    |    AA")
		viewList.insert(2, "160050056    |    CS333    |    AP")
		viewList.insert(3, "160050057    |    CS333    |    AP")
		viewList.grid(row=0, column=0, sticky="ns")

		yscroll = Scrollbar(vGrade, command=viewList.yview, orient=VERTICAL)
		yscroll.grid(row=0, column=1, sticky='nws')

		viewList.configure(yscrollcommand=yscroll.set)
		viewList.bind("<Double-Button-1>", updateG)

		vGrade.grid(row=2, column=0, columnspan=2, padx=(10,10), pady=(1,7), sticky="ns")
	else:
		vGrade.grid(row=2, column=0, columnspan=2, padx=(10,10), pady=(1,7), sticky="ns")
	curFrame = 'v'

	# for name, value in globals().copy().items():
	# 	print(name, value)

def updateG(event):
	global homeP
	global vGrade
	idx = int(event.widget.curselection()[0])
	value = event.widget.get(idx).split('|')

	uG = simpledialog.askstring('Update grade', 'Enter New Grade', parent=homeP, initialvalue=value[2].strip())
	value[2] = "    " + uG
	vGrade.winfo_children()[0].delete(idx)
	vGrade.winfo_children()[0].insert(idx, "|".join(value))



def Logout():
	global homeP
	url = 'http://localhost/logout.php'
	try:
		response = sess.post(url)
		# print(response.text)
	except ConnectionError as e:
		msgbox.showerror('Error', 'Some Error has Occurred !')
	else:
		homeP.destroy()
		Start()
		# msgbox.showinfo('Logout', 'Logged Out')
 
def CheckLogin(uid, pword):
	global uname
	global startS

	if(not checkEmpty(uid, pword)):
		return

	pass_h = hashlib.sha256(pword.encode()).hexdigest()

	url = 'http://localhost/login.php'
	post_data = {'uid': uid, 'pass': pass_h}
	
	try:
		response = sess.post(url, data = post_data)
		text = response.text
	except ConnectionError as e:
		msgbox.showerror('Error', 'Some Error has Occurred !')
		return

	if text == "S":
		# msgbox.showinfo('Success', 'Success')
		uname = uid
		startS.destroy()
		Home()
	elif text == "U":
		msgbox.showerror('Error', 'Please SignUp !')
	else:
		msgbox.showerror('Error', 'Incorrect Username or Password')


def SignUp(uid, pword, passPh):

	if(not checkEmpty(uid, pword)):
		return

	pass_h = hashlib.sha256(pword.encode()).hexdigest()

	url = 'http://localhost/signup.php'
	post_data = {'uid': uid, 'pass': pass_h}
	try:
		response = requests.post(url, data = post_data)
		text = response.text
	except ConnectionError as e:
		msgbox.showerror('Error', 'Some Error has Occurred !')
		return
	
	if text == "S":
		msgbox.showinfo('Success', 'Successfully Registered\n\nPlease Re-login')
		key = RSA.generate(4096)
		encrypted_key = key.exportKey(passphrase=passPh, pkcs=8)
		with open(os.path.expanduser("~/"+uid+".pem"), "wb+") as f:
			f.write(encrypted_key)
	elif text == "M":
		msgbox.showerror('Error', 'Username already taken !')
	else:
		msgbox.showerror('Error', 'Some Error has Occurred !')
	# print(key.publickey().exportKey())

# Start()
Home()