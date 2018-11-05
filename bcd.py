from tkinter import *
import tkinter.messagebox as msgbox
from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError
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
 
	name = Label(startS, text='Username') # More labels
	pword = Label(startS, text='Password') # ^
	name.grid(row=2, column=1, padx=(0,5), pady=(5,5), sticky=E)
	pword.grid(row=3, column=1, padx=(0,5), pady=(5,5), sticky=E)
 
	nameBox = Entry(startS) # The entry input
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
	uname='sudarsha'
	homeP = Tk()
	# homeP = maxWindow().tk
	# homeP.grid_rowconfigure(0, weight=1)
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

def enterG():
	global homeP

	eGrade = Frame(homeP)
	eGrade.grid(row=2, column=0, columnspan=2, padx=(10,10), pady=(2,5))

	enterGrades = Text(eGrade, height=10, font='Times 11', wrap='word', relief='raised', spacing2=0, spacing3=7)
	enterGrades.grid(row=0, column=0)

	yscroll = Scrollbar(eGrade, command=enterGrades.yview, orient=VERTICAL)
	yscroll.grid(row=0, column=1, sticky='nws')

	enterGrades.configure(yscrollcommand=yscroll.set)

	enterGBut = Button(eGrade, text='Submit Grades', bg='green', fg='white', command=lambda: submitG(enterGrades.get("1.0", 'end-1c')))
	enterGBut.grid(row=1, column=0, columnspan=2, pady=(5,0), sticky="ns")
	
def submitG(grades):
	print(grades)

	# height = 5
	# width = 5
	# for i in range(height): #Rows
	#     for j in range(width): #Columns
	#         b = Entry(root, text="")
	#         b.grid(row=i, column=j)

	# print('MeraBaba')

def viewG():
	global homeP
	viewF = Frame(homeP)
	width = 3
	height = 5
	for i in range(height):
		for j in range(width):
			b = Text(viewF, height=1, width=24).grid(row=i, column=j)
	viewF.grid(row=2, column=0, columnspan=2, padx=(10,10), pady=(5,5))

def Logout():
	global homeP
	url = 'http://localhost/logout.php'
	# data = urlencode(post_data).encode('utf-8')
	try:
		response = urlopen(url).read().decode()
	except HTTPError as e:
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
	data = urlencode(post_data).encode('utf-8')
	try:
		response = urlopen(url, data).read().decode()
	except HTTPError as e:
		msgbox.showerror('Error', 'Some Error has Occurred !')
		return

	if response == "S":
		# msgbox.showinfo('Success', 'Success')
		uname = uid
		startS.destroy()
		Home()
	elif response == "U":
		msgbox.showerror('Error', 'Please SignUp !')
	else:
		msgbox.showerror('Error', 'Incorrect Username or Password')


def SignUp(uid, pword, passPh):

	if(not checkEmpty(uid, pword)):
		return

	pass_h = hashlib.sha256(pword.encode()).hexdigest()

	url = 'http://localhost/signup.php'
	post_data = {'uid': uid, 'pass': pass_h}
	data = urlencode(post_data).encode('utf-8')
	try:
		response = urlopen(url, data).read().decode()
	except HTTPError as e:
		msgbox.showerror('Error', 'Some Error has Occurred !')
		return
	
	if response == "S":
		msgbox.showinfo('Success', 'Successfully Registered\n\nPlease Re-login')
		key = RSA.generate(4096)
		encrypted_key = key.exportKey(passphrase=passPh, pkcs=8)
		with open(os.path.expanduser("~/"+uid+".pem"), "wb+") as f:
			f.write(encrypted_key)
	elif response == "M":
		msgbox.showerror('Error', 'Username already taken !')
	else:
		msgbox.showerror('Error', 'Some Error has Occurred !')
	# print(key.publickey().exportKey())


# Start()
Home()
