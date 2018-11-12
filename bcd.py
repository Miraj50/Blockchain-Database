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
		self.footer.grid(row=0, column=0, columnspan=4, sticky="nsew")
		self.start()

	def start(self):
		self.geometry("")
		self.sess = requests.Session()
		self.title("Welcome to BcD")
		self.grid_columnconfigure(0, weight=1)
		self.grid_columnconfigure(1, weight=1)

		#Login
		loginText = tk.Label(self, text='Login', font='Helvetica 16 bold', fg='darkblue')
		loginText.grid(row=1, columnspan=2, column=0, pady=(5,10))

		name = tk.Label(self, text='Username')
		pword = tk.Label(self, text='Password')
		name.grid(row=2, column=0, padx=(0,5), pady=(5,5), sticky="e")
		pword.grid(row=3, column=0, padx=(0,5), pady=(5,5), sticky="e")

		nameBox = tk.Entry(self)
		pwordBox = tk.Entry(self, show='*')
		nameBox.grid(row=2, column=1, padx=(0,0), pady=(5,5), sticky="w")
		pwordBox.grid(row=3, column=1, padx=(0,0), pady=(5,5), sticky="w")

		loginButton = tk.Button(self, text='Login',bg='blue',fg='white', command=lambda: self.CheckLogin(nameBox.get(), pwordBox.get()))
		loginButton.grid(columnspan=2, row=4, column=0, pady=(5,10))
		# loginButton.bind('<Return>', lambda e: self.CheckLogin(nameBox.get(), pwordBox.get()))

		ttk.Separator(self, orient="horizontal").grid(column=0, row=5, columnspan=3, sticky='nsew')

		#SignUp
		signUpText = tk.Label(self, text='Sign Up', font='Helvetica 16 bold', fg='brown')
		signUpText.grid(row=5, columnspan=2, column=0, pady=(10,10))

		SuName = tk.Label(self, text='Choose Username')
		SuPword = tk.Label(self, text='Enter Password')
		SuName.grid(row=6, column=0, padx=(30,5), pady=(5,1), sticky="e")
		SuPword.grid(row=7, column=0, padx=(30,5), pady=(1,5), sticky="e")

		SuNameBox = tk.Entry(self)
		SuPwordBox = tk.Entry(self, show='*')
		SuNameBox.grid(row=6, column=1, padx=(0,0), pady=(5,1), sticky="w")
		SuPwordBox.grid(row=7, column=1, padx=(0,0), pady=(1,5), sticky="w")

		SuPP = tk.Label(self, text='Enter PassPhrase')
		SuPP.grid(row=8, column=0, padx=(30,0), pady=(5,5), sticky="e")

		PPframe = tk.Frame(self)

		passPh = tk.Entry(PPframe, show='*')
		passPh.grid(row=0, column=0, sticky="w")
		img = tk.PhotoImage(file='q.gif')
		PPhelp = tk.Button(PPframe, image=img, command=lambda :msgbox.showinfo('Info','This PassPhrase will be used for generating your Private Key'))
		PPhelp.image = img
		PPhelp.grid(row=0, column=1, sticky="w")

		PPframe.grid(row=8, column=1, padx=(0,30), sticky="w")

		SignUpButton = tk.Button(self, text='Sign Up', bg='brown', fg='white', command=lambda: self.SignUp(SuNameBox.get(), SuPwordBox.get(), passPh.get()))
		SignUpButton.grid(row=9, column=0, columnspan=2, pady=(5,10))

		self.update_idletasks()
		h = self.winfo_reqheight()
		ws = self.winfo_screenwidth()
		x = (ws/2) - (h/2)
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
		self.grid_columnconfigure(1, weight=1)
		self.grid_columnconfigure(0, weight=1)

		self.footer.config(text='Succesfully Logged in', bg='black', fg='springGreen')

		topF = tk.Frame(self)

		top = tk.Label(topF, text='Signed In as : ')
		# top.grid(row=0, column=0, padx=(20,0), pady=(5,5), sticky="ew")
		top.pack(side='left', expand=False)
		u = tk.Label(topF, text=self.uname, font='Helvetica 10 bold', bg='lightblue')
		# u.grid(row=0, column=1, padx=(0,100), pady=(5,5))
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
			# eGrade.grid_columnconfigure(0, weight=1) # Along with sticky=ewns will resize to full window
			self.eG.grid_rowconfigure(0, weight=1)

			enterGrades = scrolledtext.ScrolledText(self.eG, font='Times 11', wrap='word', spacing2=0, spacing3=7, width=65, height=12)
			enterGrades.grid(row=0, column=0, sticky="ewns")

			enterGBut = tk.Button(self.eG, text='Submit Grades', bg='green', fg='white', command=lambda: self.submitG(enterGrades.get("1.0", 'end-1c')))
			enterGBut.grid(row=1, column=0, columnspan=2, pady=(0,0), sticky="ns")
			self.eG.grid(row=3, column=0, columnspan=2, padx=(10,10), pady=(1,3), sticky="ns")
		else:
			self.eG.grid(row=3, column=0, columnspan=2, padx=(10,10), pady=(1,3), sticky="ns")

	def viewG(self):
		self.geometry("")

		if self.eG != None:
			self.eG.grid_forget()

		if self.vG == None:
			self.vG = tk.Frame(self)
			# vGrade.grid_columnconfigure(0, weight=1)
			self.vG.grid_rowconfigure(0, weight=1)

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
			viewList.grid(row=0, column=0, sticky="ns")

			yscroll = tk.Scrollbar(self.vG, command=viewList.yview, orient="vertical")
			yscroll.grid(row=0, column=1, sticky='ns')

			viewList.configure(yscrollcommand=yscroll.set)
			viewList.bind("<Double-Button-1>", self.updateG)

			self.vG.grid(row=3, column=0, columnspan=2, padx=(10,10), pady=(1,7), sticky="ns")
		else:
			self.vG.grid(row=3, column=0, columnspan=2, padx=(10,10), pady=(1,7), sticky="ns")

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
			# print(response.text)
		except (ConnectionError, requests.exceptions.RequestException) as e:
			msgbox.showerror('Error', 'Some Error has Occurred !')
		else:
			self.attributes('-zoomed', False)
			self.clear_widgets()
			self.uname = ""
			self.eG = None
			self.vG = None
			self.footer.config(text='Successfully Logged Out', bg='black', fg='springGreen')
			self.start()

	def clear_widgets(self):
		for widget in self.winfo_children():
			if widget != self.footer:
				widget.destroy()

BcD().mainloop()