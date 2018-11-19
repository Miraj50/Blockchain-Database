import tkinter as tk
import tkinter.messagebox as msgbox
from tkinter import scrolledtext, simpledialog
import tkinter.ttk as ttk
import requests
import os, hashlib
from Crypto.PublicKey import RSA

class BcD(tk.Tk):
	def __init__(self):
		super().__init__()
		self.sess = None
		self.uname = ""
		self.eG = None
		self.vG = None
		self.footer = tk.Label(self, text='The world is coming to an end... SAVE YOUR BUFFERS !', font='Verdana 9', bg='black', fg='springGreen')
		self.footer.grid(row=0, column=0, columnspan=2, sticky="nsew")
		self.Start()

	def Start(self):
		
		self.title("Welcome to BcD")
		self.grid_columnconfigure(0, weight=1)
		self.grid_columnconfigure(1, weight=1)

		login = tk.Frame(self)
		login.grid(row=1, column=0, columnspan=2, pady=(5,5))
		ttk.Separator(self, orient="horizontal").grid(row=2, column=0, columnspan=2, sticky='nsew')
		signup = tk.Frame(self)
		signup.grid(row=2, column=0, columnspan=2, pady=(5,5))

		#login
		loginText = tk.Label(login, text='Login', font='Fixedsys 16 bold', fg='darkblue')
		loginText.grid(row=0, column=0, columnspan=2, pady=(10,10))
		name = tk.Label(login, text='Username', font='Verdana 11')
		pword = tk.Label(login, text='Password', font='Verdana 11')
		name.grid(row=1, column=0, padx=(30,5), pady=(5,5), sticky="e")
		pword.grid(row=2, column=0, padx=(30,5), pady=(5,5), sticky="e")

		nameBox = tk.Entry(login)
		pwordBox = tk.Entry(login, show='*')
		nameBox.grid(row=1, column=1, padx=(0,30), pady=(5,5), sticky="w")
		nameBox.focus()
		pwordBox.grid(row=2, column=1, padx=(0,30), pady=(5,5), sticky="w")

		loginButton = tk.Button(login, text='Login', bg='blue', fg='white', command=lambda: self.CheckLogin(nameBox.get(), pwordBox.get()))
		loginButton.grid(row=3, column=0, columnspan=2, pady=(5,10))
		loginButton.bind('<Return>', lambda e: self.CheckLogin(nameBox.get(), pwordBox.get()))

		#Sign Up
		signUpText = tk.Label(signup, text='Sign Up', font='Fixedsys 16 bold', fg='brown')
		signUpText.grid(row=0, column=0, columnspan=2, pady=(10,10))

		SuName = tk.Label(signup, text='Choose Username', font='Verdana 11')
		SuPword = tk.Label(signup, text='Enter Password', font='Verdana 11')
		SuName.grid(row=1, column=0, padx=(30,5), pady=(5,1), sticky="e")
		SuPword.grid(row=2, column=0, padx=(30,5), pady=(1,5), sticky="e")

		SuNameBox = tk.Entry(signup)
		SuPwordBox = tk.Entry(signup, show='*')
		SuNameBox.grid(row=1, column=1, padx=(0,30), pady=(5,1), sticky="w")
		SuPwordBox.grid(row=2, column=1, padx=(0,30), pady=(1,5), sticky="w")

		SuPP = tk.Label(signup, text='Enter PassPhrase', font='Verdana 11')
		SuPP.grid(row=3, column=0, padx=(30,5), pady=(5,5), sticky="e")

		PPframe = tk.Frame(signup)

		passPh = tk.Entry(PPframe, show='*')
		passPh.grid(row=0, column=0, sticky="w")
		img = tk.PhotoImage(file='q.gif')
		PPhelp = tk.Button(PPframe, image=img, command=lambda: msgbox.showinfo('Help','This PassPhrase will be used for generating your Private Key'))
		PPhelp.image = img
		PPhelp.grid(row=0, column=1, sticky="w")

		PPframe.grid(row=3, column=1, padx=(0,30), sticky="w")

		SignUpButton = tk.Button(signup, text='Sign Up', bg='brown', fg='white', command=lambda: self.SignUp(SuNameBox.get(), SuPwordBox.get(), passPh.get()))
		SignUpButton.grid(row=4, column=0, columnspan=2, pady=(5,10))
		SignUpButton.bind('<Return>', lambda e: self.SignUp(SuNameBox.get(), SuPwordBox.get(), passPh.get()))

		self.update_idletasks()
		h = self.winfo_reqheight()
		w = self.winfo_reqwidth()
		ws = self.winfo_screenwidth()
		x = (ws/2) - (w/2)
		self.geometry("+%d+%d" % (x,h/4))

	def checkEmpty(self, uid, pword, passPh):
		if(len(uid)==0):
			self.footer.config(text='Username field is Empty !', bg='red2', fg='white')
			return 0
		if(len(pword)==0):
			self.footer.config(text='Password field is Empty !', bg='red2', fg='white')
			return 0
		if(len(passPh)==0):
			self.footer.config(text='PassPhrase field is Empty !', bg='red2', fg='white')
			return 0
		return 1

	def SignUp(self, uid, pword, passPh):
		if(not self.checkEmpty(uid, pword, passPh)):
			return

		pass_h = hashlib.sha256(pword.encode()).hexdigest()

		url = 'http://localhost/signup.php'
		post_data = {'uid': uid, 'pass': pass_h}
		try:
			self.footer.config(text='Signing Up...', bg='black', fg='springGreen')
			self.footer.update_idletasks()
			response = requests.post(url, data=post_data)
			text = response.text
		except (ConnectionError, requests.exceptions.RequestException) as e:
			self.footer.config(text='Some Error has Occurred !', bg='red2', fg='white')
			return
		
		if text == "S":
			key = RSA.generate(4096)
			encrypted_key = key.exportKey(passphrase=passPh, pkcs=8)
			with open(os.path.expanduser("~/"+uid+".pem"), "wb+") as f:
				f.write(encrypted_key)
			self.footer.config(text='Successfully Registered. Please Re-Login', bg='black', fg='springGreen')
		elif text == "M":
			self.footer.config(text='Username already taken !', bg='red2', fg='white')
		else:
			self.footer.config(text='Some Error has Occurred !', bg='red2', fg='white')

	def CheckLogin(self, uid, pword):
		if(not self.checkEmpty(uid, pword, passPh='None')):
			return

		self.sess = requests.Session()

		pass_h = hashlib.sha256(pword.encode()).hexdigest()

		url = 'http://localhost/login.php'
		post_data = {'uid': uid, 'pass': pass_h}
		
		try:
			self.footer.config(text='Checking Login Information...', bg='black', fg='springGreen')
			self.footer.update_idletasks()
			response = self.sess.post(url, data=post_data)
			text = response.text
		except (ConnectionError, requests.exceptions.RequestException) as e:
			self.footer.config(text='Some Error has Occurred !', bg='red2', fg='white')
			return

		if text == "S":
			self.uname = uid
			self.Home()
		elif text == "U":
			self.footer.config(text='Please SignUp !', bg='red2', fg='white')
		elif text == "D":
			self.footer.config(text='Some Error has Occurred !', bg='red2', fg='white')
		else:
			self.footer.config(text='Incorrect Username or Password !', bg='red2', fg='white')

	def Home(self):
		self.clear_widgets()
		self.attributes('-zoomed', True)
		self.title('Grades')
		self.grid_rowconfigure(3, weight=1)

		self.footer.config(text='Succesfully Logged in', bg='black', fg='springGreen')

		topF = tk.Frame(self)

		top = tk.Label(topF, text='Signed In as : ')
		top.pack(side='left', expand=False)
		u = tk.Label(topF, text=self.uname, font='Helvetica 10 bold', bg='lightblue')
		u.pack(side='left', expand=False)

		topF.grid(row=1, column=0, padx=(10,0), pady=(5,5), sticky="w")
		logoutButton = tk.Button(self, text='LogOut', bg='brown', fg='white', command=self.Logout)
		logoutButton.grid(row=1, column=1, padx=(0,10), pady=(5,5), sticky="e")

		ttk.Separator(self, orient="horizontal").grid(row=2, column=0, columnspan=2, sticky='nsew')

		enterButton = tk.Button(self, text='Enter Grades', bg='blue', fg='white', command=self.enterG)
		enterButton.grid(row=2, column=0, padx=(40,5), pady=(5,2), sticky="e")
		viewButton = tk.Button(self, text='View Grades', bg='blue', fg='white', command=self.viewG)
		viewButton.grid(row=2, column=1, padx=(5,40), pady=(5,2), sticky="w")

		ttk.Separator(self, orient="horizontal").grid(row=3, column=0, columnspan=2, sticky='nsew')

	def enterG(self):
		self.geometry("")

		if self.vG != None:
			self.vG.grid_forget()

		if self.eG == None:
			self.eG = tk.Frame(self)
			self.eG.grid_columnconfigure(0, weight=1) # Along with sticky=ewns will resize to full window

			enterGrades = scrolledtext.ScrolledText(self.eG, font='Times 11', wrap='word', spacing2=0, spacing3=7, width=65, height=12)
			enterGrades.pack(expand=True, fill="both")

			enterGBut = tk.Button(self.eG, text='Submit Grades', bg='green', fg='white', command=lambda: self.submitG(enterGrades.get("1.0", 'end-1c')))
			enterGBut.pack()
			self.eG.grid(row=3, column=0, columnspan=2, pady=(1,3), sticky="ns")
		else:
			self.eG.grid(row=3, column=0, columnspan=2, pady=(1,3), sticky="ns")

	def viewG(self):
		self.geometry("")

		if self.eG != None:
			self.eG.grid_forget()

		if self.vG == None:
			self.vG = tk.Frame(self)

			viewList = ttk.Treeview(self.vG, height=15)
			viewList['show'] = 'headings'
			viewList['columns'] = ('Roll', 'Name', 'Course', 'Grade')
			viewList.heading("#1", text='Roll No.', anchor='w')
			viewList.column("#1", stretch="no", width=100)
			viewList.heading("#2", text='Name', anchor='w')
			viewList.column("#2", stretch="no", width=160 )
			viewList.heading("#3", text='Course', anchor='w')
			viewList.column("#3", stretch="no", width=100)
			viewList.heading("#4", text='Grade', anchor='w')
			viewList.column("#4", stretch="no", width=100)

			viewList.insert("", "end", values=("160050029", "Rishabh Raj", "CS333", "AA"))
			viewList.insert("", "end", values=("160050057", "Kumar Saurav", "CS333", "AP"))
			viewList.insert("", "end", values=("160050056", "Kumar Saunack", "CS333", "AP"))
			viewList.pack(side="left", expand=True, fill="both")

			yscroll = tk.Scrollbar(self.vG, command=viewList.yview, orient="vertical")
			yscroll.pack(side="right", fill="y")

			viewList.configure(yscrollcommand=yscroll.set)
			viewList.bind("<Double-Button-1>", self.updateG)

			self.vG.grid(row=3, column=0, columnspan=2, pady=(1,7), sticky="ns")
		else:
			self.vG.grid(row=3, column=0, columnspan=2, pady=(1,7), sticky="ns")

	def submitG(self, grades):
		print(grades)

	def updateG(self, event):
		w = event.widget
		idx = w.selection()[0]
		item = w.item(w.selection())['values']

		uG = simpledialog.askstring('Update grade', 'Enter New Grade', parent=self, initialvalue=item[3])

		self.vG.winfo_children()[0].item(idx, values=(item[0], item[1], item[2], uG))

	def Logout(self):
		url = 'http://localhost/logout.php'
		try:
			response = self.sess.post(url)
		except (ConnectionError, requests.exceptions.RequestException) as e:
			self.footer.config(text='Some Error has Occurred !', bg='red2', fg='white')
		else:
			self.attributes('-zoomed', False)
			self.clear_widgets()
			self.uname = ""
			self.sess = None
			self.eG = None
			self.vG = None
			self.footer.config(text='Successfully Logged Out', bg='black', fg='springGreen')
			self.Start()

	def clear_widgets(self):
		for widget in self.winfo_children():
			if widget != self.footer:
				widget.destroy()


def quit():
	if app.sess is not None:
		app.Logout()
	else:
		app.destroy()

app = BcD()
app.protocol("WM_DELETE_WINDOW", quit)
app.mainloop()