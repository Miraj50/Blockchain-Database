import tkinter as tk
import tkinter.messagebox as msgbox
from tkinter import scrolledtext, simpledialog
import tkinter.ttk
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
		self.start()

	def start(self):
		self.sess = requests.Session()
		self.title("Welcome to BcD")
		# self.resizable(0,0) #Remove Maximize
		self.grid_columnconfigure(0, weight=1)
		self.grid_columnconfigure(4, weight=1)

		#Login
		loginText = tk.Label(self, text='Login', font='Helvetica 16 bold', fg='darkblue')
		loginText.grid(row=1, columnspan=2, column=1, pady=(5,10))

		name = tk.Label(self, text='Username')
		pword = tk.Label(self, text='Password')
		name.grid(row=2, column=1, padx=(0,5), pady=(5,5), sticky="e")
		pword.grid(row=3, column=1, padx=(0,5), pady=(5,5), sticky="e")

		nameBox = tk.Entry(self)
		pwordBox = tk.Entry(self, show='*')
		nameBox.grid(row=2, column=2, padx=(0,0), pady=(5,5))
		pwordBox.grid(row=3, column=2, padx=(0,0), pady=(5,5))

		loginButton = tk.Button(self, text='Login',bg='blue',fg='white', command=lambda: self.CheckLogin(nameBox.get(), pwordBox.get()))
		loginButton.grid(columnspan=2, row=4, column=1, pady=(5,10))
		# loginButton.bind('<Return>', lambda e: CheckLogin(nameBox.get(), pwordBox.get()))

		tkinter.ttk.Separator(self, orient="horizontal").grid(column=1, row=5, columnspan=3, sticky='nsew')

		#SignUp
		signUpText = tk.Label(self, text='Sign Up', font='Helvetica 16 bold', fg='brown')
		signUpText.grid(row=5, columnspan=2, column=1, pady=(10,10))

		SuName = tk.Label(self, text='Choose Username')
		SuPword = tk.Label(self, text='Enter Password')
		SuName.grid(row=6, column=1, padx=(30,5), pady=(5,1), sticky="e")
		SuPword.grid(row=7, column=1, padx=(30,5), pady=(1,5), sticky="e")

		SuNameBox = tk.Entry(self)
		SuPwordBox = tk.Entry(self, show='*')
		SuNameBox.grid(row=6, column=2, padx=(0,0), pady=(5,1))
		SuPwordBox.grid(row=7, column=2, padx=(0,0), pady=(1,5))

		SuPP = tk.Label(self, text='Enter PassPhrase')
		SuPP.grid(row=8, column=1, padx=(30,0), pady=(5,5))
		passPh = tk.Entry(self, show='*')
		passPh.grid(row=8, column=2, padx=(0,0), pady=(5,5), sticky="w")

		SignUpButton = tk.Button(self, text='Sign Up', bg='brown', fg='white', command=lambda: self.SignUp(SuNameBox.get(), SuPwordBox.get(), passPh.get()))
		SignUpButton.grid(columnspan=2, row=10, column=1, pady=(5,10))

		img = tk.PhotoImage(file='q.gif')
		PPhelp = tk.Button(self, image=img, command=lambda :msgbox.showinfo('Info','This PassPhrase will be used for generating your Private Key'))
		PPhelp.image = img
		PPhelp.grid(row=8, column=3, padx=(0,20))

		self.update_idletasks()
		h = self.winfo_reqheight()
		ws = self.winfo_screenwidth()
		x = (ws/2) - (h/2)
		self.geometry("+%d+%d" % (x,h/4))

	def checkEmpty(self, uid, pword):
		if(len(uid)==0):
			msgbox.showerror('Error', 'Please Enter Username')
			return 0
		if(len(pword)==0):
			msgbox.showerror('Error', 'Please Enter Password')
			return 0
		return 1

	def SignUp(self, uid, pword, passPh):
		if(not self.checkEmpty(uid, pword)):
			return

		pass_h = hashlib.sha256(pword.encode()).hexdigest()

		url = 'http://localhost/signup.php'
		post_data = {'uid': uid, 'pass': pass_h}
		try:
			response = requests.post(url, data=post_data)
			text = response.text
		except ConnectionError as e:
			msgbox.showerror('Error', 'Some Error has Occurred !')
			return
		
		if text == "S":
			key = RSA.generate(4096)
			encrypted_key = key.exportKey(passphrase=passPh, pkcs=8)
			with open(os.path.expanduser("~/"+uid+".pem"), "wb+") as f:
				f.write(encrypted_key)
			msgbox.showinfo('Success', 'Successfully Registered\n\nPlease Re-login')
		elif text == "M":
			msgbox.showerror('Error', 'Username already taken !')
		else:
			msgbox.showerror('Error', 'Some Error has Occurred !')

	def CheckLogin(self, uid, pword):
		if(not self.checkEmpty(uid, pword)):
			return

		pass_h = hashlib.sha256(pword.encode()).hexdigest()

		url = 'http://localhost/login.php'
		post_data = {'uid': uid, 'pass': pass_h}
		
		try:
			response = self.sess.post(url, data=post_data)
			text = response.text
		except (ConnectionError, requests.exceptions.RequestException) as e:
			msgbox.showerror('Error', 'Some Error has Occurred !')
			return

		if text == "S":
			self.uname = uid
			self.Home()
		elif text == "U":
			msgbox.showerror('Error', 'Please SignUp !')
		else:
			msgbox.showerror('Error', 'Incorrect Username or Password')

	def Home(self):
		self.clear_widgets()
		# self.attributes('-zoomed', True)
		self.title('Grades')
		self.grid_rowconfigure(2, weight=1)
		self.grid_columnconfigure(1, weight=1)
		self.grid_columnconfigure(0, weight=1)

		topF = tk.Frame(self)

		top = tk.Label(topF, text='Signed In as : ')
		# top.grid(row=0, column=0, padx=(20,0), pady=(5,5), sticky="ew")
		top.pack(side='left', expand=False)
		u = tk.Label(topF, text=self.uname, font='Helvetica 10 bold', bg='lightblue')
		# u.grid(row=0, column=1, padx=(0,100), pady=(5,5))
		u.pack(side='left', expand=False)

		topF.grid(row=0, column=0, padx=(10,0), pady=(5,5), sticky="w")
		logoutButton = tk.Button(self, text='LogOut', bg='brown', fg='white', command=self.Logout)
		logoutButton.grid(row=0, column=1, padx=(0,10), pady=(5,5), sticky="e")

		tkinter.ttk.Separator(self, orient="horizontal").grid(column=0, row=1, columnspan=2, sticky='nsew')

		enterButton = tk.Button(self, text='Enter Grades', bg='blue', fg='white', command=self.enterG)
		enterButton.grid(row=1, column=0, padx=(40,5), pady=(5,2), sticky="e")
		viewButton = tk.Button(self, text='View Grades', bg='blue', fg='white', command=self.viewG)
		viewButton.grid(row=1, column=1, padx=(5,40), pady=(5,2), sticky="w")

		tkinter.ttk.Separator(self, orient="horizontal").grid(column=0, row=2, columnspan=2, sticky='nsew')

	def enterG(self):
		self.geometry("")

		if self.eG == None:
			self.eG = tk.Frame(self)
			# eGrade.grid_columnconfigure(0, weight=1) # Along with sticky=ewns will resize to full window
			self.eG.grid_rowconfigure(0, weight=1)

			enterGrades = scrolledtext.ScrolledText(self.eG, font='Times 11', wrap='word', spacing2=0, spacing3=7, width=64, height=10)
			enterGrades.grid(row=0, column=0, sticky="ewns")

			enterGBut = tk.Button(self.eG, text='Submit Grades', bg='green', fg='white', command=lambda: self.submitG(enterGrades.get("1.0", 'end-1c')))
			enterGBut.grid(row=1, column=0, columnspan=2, pady=(0,0), sticky="ns")
			self.eG.grid(row=2, column=0, columnspan=2, padx=(10,10), pady=(1,5), sticky="ns")
		else:
			if self.vG != None:
				self.vG.grid_forget()
			self.eG.grid(row=2, column=0, columnspan=2, padx=(10,10), pady=(1,5), sticky="ns")

	def viewG(self):
		self.geometry("")

		if self.vG == None:
			self.vG = tk.Frame(self)
			# vGrade.grid_columnconfigure(0, weight=1)
			self.vG.grid_rowconfigure(0, weight=1)

			viewList = tk.Listbox(self.vG, font='Times 11', width=64, height=15, relief='sunken', justify="center")
			viewList.insert(1, "160050029    |    Rishabh Raj    |    CS333    |    AA")
			viewList.insert(2, "160050056    |    Kumar Saurav   |    CS333    |    AP")
			viewList.insert(3, "160050057    |    Kumar Saunack  |    CS333    |    AP")
			viewList.grid(row=0, column=0, sticky="ns")

			yscroll = tk.Scrollbar(self.vG, command=viewList.yview, orient="vertical")
			yscroll.grid(row=0, column=1, sticky='nws')

			viewList.configure(yscrollcommand=yscroll.set)
			viewList.bind("<Double-Button-1>", self.updateG)

			self.vG.grid(row=2, column=0, columnspan=2, padx=(10,10), pady=(1,7), sticky="ns")
		else:
			if self.eG != None:
				self.eG.grid_forget()
			self.vG.grid(row=2, column=0, columnspan=2, padx=(10,10), pady=(1,7), sticky="ns")

	def submitG(self, grades):
		print(grades)

	def updateG(self, event):
		idx = int(event.widget.curselection()[0])
		value = event.widget.get(idx).split('|')

		uG = simpledialog.askstring('Update grade', 'Enter New Grade', parent=self, initialvalue=value[3].strip())
		value[3] = "    " + uG
		self.vG.winfo_children()[0].delete(idx)
		self.vG.winfo_children()[0].insert(idx, "|".join(value))

	def Logout(self):
		url = 'http://localhost/logout.php'
		try:
			response = self.sess.post(url)
			# print(response.text)
		except (ConnectionError, requests.exceptions.RequestException) as e:
			msgbox.showerror('Error', 'Some Error has Occurred !')
		else:
			self.attributes('-zoomed', False)
			# self.text_data = self.txt.get(1.0, "end-1c")
			self.clear_widgets()
			self.uname = ""
			self.eG = None
			self.vG = None
			self.start()

	def clear_widgets(self):
		for widget in self.winfo_children():
			widget.destroy()

BcD().mainloop()