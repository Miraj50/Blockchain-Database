import tkinter as tk
import tkinter.messagebox as msgbox
from tkinter import scrolledtext, simpledialog
import tkinter.ttk as ttk
import requests
import os, hashlib
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5 as pkcs
from Crypto.Hash import SHA256

class BcD(tk.Tk):
	def __init__(self):
		super().__init__()
		self.sess = None
		self.uname = ""
		self.student = None
		self.eG = None
		self.vG = None
		self.reload_button = 0
		self.footer = tk.Label(self, text='The world is coming to an end... SAVE YOUR BUFFERS !', font='Verdana 9', bg='black', fg='springGreen', relief='raised')
		self.footer.grid(row=0, column=0, columnspan=2, sticky="nsew")
		# self.Home(0)
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

		stud = tk.IntVar()
		stud.set(0)
		checkStud = tk.Checkbutton(login, text='Login as Student', font='Fixedsys 8', variable=stud, onvalue=1, offvalue=0)
		checkStud.grid(row=3, column=1, padx=(0,30), sticky="w")

		loginButton = tk.Button(login, text='Login', bg='blue3', fg='white', activebackground='blue', activeforeground='white', command=lambda: self.CheckLogin(nameBox.get(), pwordBox.get(), stud.get()))
		loginButton.grid(row=4, column=0, columnspan=2, pady=(5,10))
		loginButton.bind('<Return>', lambda e: self.CheckLogin(nameBox.get(), pwordBox.get(), stud.get()))

		#Sign Up
		signUpTextF = tk.Frame(signup)
		signUpText = tk.Label(signUpTextF, text='Sign Up', font='Fixedsys 16 bold', fg='brown')
		instr_only = tk.Label(signUpTextF, text='(For Instructors only)', font='Verdana 8 italic', fg='gray25')
		signUpText.grid(row=0, column=0)
		instr_only.grid(row=1, column=0)
		signUpTextF.grid(row=0, column=0, columnspan=2, pady=(10,10))

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

		help_img = "R0lGODlhDAANAPZCACAgICEhISkpKTIyMj09PUJCQkZGRkpKSktLS1dXV1hYWF1dXV5eXmBgYGFhYWRkZHBwcHR0dHZ2dnd3d4SEhIWFhYeHh4qKio+Pj5GRkZKSkpmZmZubm52dnZ+fn6Ojo6ioqK2tra+vr7CwsLa2tre3t7y8vMPDw8jIyMvLy83NzdLS0tXV1dfX19jY2NnZ2eHh4eTk5OXl5enp6e7u7vHx8fLy8vPz8/X19fb29vf39/j4+Pn5+fr6+vv7+/z8/P39/f7+/v///wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAAAAAAAIf8LSW1hZ2VNYWdpY2sOZ2FtbWE9MC40NTQ1NDUALAAAAAAMAA0AAAeNgDg5PTIhFhYhMjw5jDkkDRIdHRMNJDo4OyILKjEgHispCyM7LQstMAQDBgImpS0XGUIlCC84BQ5CGhcNKEI8N0EkABhCKA0JLUJBQicBEDZCLQq8ykIUBzVCxQ0XGtUkH0DaGRcuCyzaFQ8+QiymOyMLKUA0Mz8pDKM5Oo8RGxwRKjXKwaPQoUSLcgQCADs="
		img = tk.PhotoImage(data=help_img)
		PPhelp = tk.Button(PPframe, image=img, command=lambda: msgbox.showinfo('Help', 'This PassPhrase will be used for generating your Private Key'))
		PPhelp.image = img
		PPhelp.grid(row=0, column=1, sticky="w")

		PPframe.grid(row=3, column=1, padx=(0,30), sticky="w")

		SignUpButton = tk.Button(signup, text='Sign Up', bg='brown', fg='white', activebackground='brown4', activeforeground='white', command=lambda: self.SignUp(SuNameBox.get(), SuPwordBox.get(), passPh.get()))
		SignUpButton.grid(row=4, column=0, columnspan=2, pady=(5,10))
		SignUpButton.bind('<Return>', lambda e: self.SignUp(SuNameBox.get(), SuPwordBox.get(), passPh.get()))

		self.update_idletasks()
		h = self.winfo_reqheight()
		w = self.winfo_reqwidth()
		ws = self.winfo_screenwidth()
		x = (ws/2) - (w/2)
		self.geometry("+%d+%d" % (x,h/4))

	def checkEmpty(self, uid, pword, passPh):
		if len(uid) == 0:
			self.footer.config(text='Username field is Empty !', bg='red2', fg='white', relief='raised')
			return 0
		if len(pword) == 0:
			self.footer.config(text='Password field is Empty !', bg='red2', fg='white', relief='raised')
			return 0
		if len(passPh) == 0:
			self.footer.config(text='PassPhrase field is Empty !', bg='red2', fg='white', relief='raised')
			return 0
		return 1

	def SignUp(self, uid, pword, passPh):
		if(not self.checkEmpty(uid, pword, passPh)):
			return

		key = RSA.generate(2048)
		pubkey = key.publickey().exportKey().hex()

		pass_h = hashlib.sha256(pword.encode()).hexdigest()

		url = 'http://localhost/signup.php'
		post_data = {'uid': uid, 'pass': pass_h, 'pubkey':pubkey}
		try:
			self.footer.config(text='Signing Up...', bg='black', fg='springGreen', relief='raised')
			self.footer.update_idletasks()
			response = requests.post(url, data=post_data)
			text = response.text
		except (ConnectionError, requests.exceptions.RequestException) as e:
			self.footer.config(text='Some Error has Occurred !', bg='red2', fg='white', relief='raised')
			return
		
		if text == "S":
			encrypted_key = key.exportKey(passphrase=passPh, pkcs=8)
			with open(os.path.expanduser("~/"+uid+".pem"), "wb+") as f:
				f.write(encrypted_key)
			self.footer.config(text='Successfully Registered. Please Re-Login', bg='black', fg='springGreen', relief='raised')
		elif text == "M":
			self.footer.config(text='Username already taken !', bg='red2', fg='white', relief='raised')
		else:
			self.footer.config(text='Some Error has Occurred !', bg='red2', fg='white', relief='raised')

	def CheckLogin(self, uid, pword, stud):
		if(not self.checkEmpty(uid, pword, passPh='None')):
			return

		self.sess = requests.Session()

		pass_h = hashlib.sha256(pword.encode()).hexdigest()

		url = 'http://localhost/login.php'
		post_data = {'uid': uid, 'pass': pass_h, 'student': stud}
		
		try:
			self.footer.config(text='Checking Login Information...', bg='black', fg='springGreen', relief='raised')
			self.footer.update_idletasks()
			response = self.sess.post(url, data=post_data)
			text = response.text
		except (ConnectionError, requests.exceptions.RequestException) as e:
			self.footer.config(text='Some Error has Occurred !', bg='red2', fg='white', relief='raised')
			return

		if text == "S":
			self.uname = uid
			self.student = stud
			self.Home(stud)
		elif text == "U":
			self.footer.config(text='Please SignUp !', bg='red2', fg='white', relief='raised')
		elif text == "D":
			self.footer.config(text='Some Error has Occurred !', bg='red2', fg='white', relief='raised')
		else:
			self.footer.config(text='Incorrect Username or Password !', bg='red2', fg='white', relief='raised')

	def Home(self, stud):
		self.clear_widgets()
		self.attributes('-zoomed', True)
		self.title('Grades')
		self.grid_rowconfigure(3, weight=1)

		self.footer.config(text='Succesfully Logged in', bg='black', fg='springGreen', relief='raised')

		topF = tk.Frame(self)

		top = tk.Label(topF, text='Signed In as : ')
		top.pack(side='left', expand=False)
		u = tk.Label(topF, text=self.uname, font='Helvetica 10 bold', bg='lightblue')
		u.pack(side='left', expand=False)

		topF.grid(row=1, column=0, padx=(10,0), pady=(5,5), sticky="w")
		logoutButton = tk.Button(self, text='LogOut', bg='brown4', fg='white', activebackground='brown', activeforeground='white', command=self.Logout)
		logoutButton.grid(row=1, column=1, padx=(0,10), pady=(5,5), sticky="e")

		ttk.Separator(self, orient="horizontal").grid(row=2, column=0, columnspan=2, sticky='nsew')

		viewButF = tk.Frame(self)

		viewButton = tk.Button(viewButF, text='View Grades', bg='blue3', fg='white', activebackground='blue', activeforeground='white', command=lambda: self.viewG(0))
		viewButton.grid(row=0, column=0)

		if stud == 0: # an instructor
			enterButton = tk.Button(self, text='Enter Grades', bg='blue3', fg='white', activebackground='blue', activeforeground='white', command=self.enterG)
			enterButton.grid(row=2, column=0, padx=(40,5), pady=(5,2), sticky="e")
			viewButF.grid(row=2, column=1, padx=(5,40), pady=(5,2), sticky="w")
		else: # a student
			viewButF.grid(row=2, column=0, columnspan=2, pady=(5,2))

		ttk.Separator(self, orient="horizontal").grid(row=3, column=0, columnspan=2, sticky='nsew')

	def enterG(self):
		self.geometry("")

		if self.vG is not None:
			self.vG.grid_forget()

		if self.eG is None:
			self.eG = tk.Frame(self)
			self.eG.grid_columnconfigure(0, weight=1) # Along with sticky=ewns will resize to full window

			enterGrades = scrolledtext.ScrolledText(self.eG, font='Verdana 11', wrap='word', spacing2=0, spacing3=7, width=50, height=12)
			enterGrades.pack(expand=True, fill="both")
			self.eG.winfo_children()[0].winfo_children()[1].tag_configure("error", background="gray80", foreground="red")

			enterGBut = tk.Button(self.eG, text='Submit Grades', bg='green', fg='white', activebackground='forestgreen' ,activeforeground='white', command=lambda: self.submitG(enterGrades.get("1.0", 'end-1c')))
			enterGBut.pack()
			self.eG.grid(row=3, column=0, columnspan=2, pady=(1,3), sticky="ns")
		else:
			self.eG.grid(row=3, column=0, columnspan=2, pady=(1,3), sticky="ns")

	def getGrades(self):
		url = 'http://localhost/view.php'
		try:
			self.footer.config(text='Retrieving Grades...', bg='black', fg='springGreen', relief='raised')
			self.footer.update_idletasks()
			response = self.sess.post(url)
			text = response.text
		except (ConnectionError, requests.exceptions.RequestException) as e:
			self.footer.config(text='Some Error has Occurred !', bg='red2', fg='white', relief='raised')
			return

		if text == "UFO":
			self.footer.config(text='!!!  BREACH DETECTED  !!!', bg='gold', fg='red3', borderwidth=2, relief='sunken')
			self.footer.update_idletasks()
			return None
		if text == "D":
			self.footer.config(text='Some Error has Occurred !', bg='red2', fg='white', relief='raised')
			return None
		return text

	def viewG(self, flag):
		self.geometry("")

		if self.eG is not None:
			self.eG.grid_forget()

		if flag == 0 or (flag == 1 and self.vG is None):
			if self.vG is None:

				text = self.getGrades()
				if text is None:
					return

				self.footer.config(text='Grades Retrieved Successfully', bg='black', fg='springGreen', relief='raised')

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

				for row in text.split('&'):
					viewList.insert("", "end", values=row.split('%'))

				viewList.pack(side="left", expand=True, fill="both")

				yscroll = tk.Scrollbar(self.vG, command=viewList.yview, orient="vertical")
				yscroll.pack(side="right", fill="y")

				viewList.configure(yscrollcommand=yscroll.set)
				if self.student == 0:
					viewList.bind("<Double-Button-1>", self.updateG)

				self.vG.grid(row=3, column=0, columnspan=2, pady=(1,7), sticky="ns")
			else:
				self.vG.grid(row=3, column=0, columnspan=2, pady=(1,7), sticky="ns")
		elif flag == 1:
			text = self.getGrades()
			if text is None:
				return
			viewList = self.vG.winfo_children()[0]
			viewList.delete(*viewList.get_children())
			for row in text.split('&'):
				viewList.insert("", "end", values=row.split('%'))
			self.footer.config(text='Grades Retrieved Successfully', bg='black', fg='springGreen', relief='raised')
			self.vG.grid(row=3, column=0, columnspan=2, pady=(1,7), sticky="ns")

	def submitG(self, grades):
		
		post_data = {'data':[]}
		gradeList = grades.split('\n')
		num = 0

		passPh = simpledialog.askstring("PassPhrase", "Enter PassPhrase:", show='*')

		with open(os.path.expanduser("~/"+self.uname+".pem"), "r") as f:
			privkey = RSA.importKey(f.read(), passphrase=passPh)

		for row in gradeList:
			temp = row.split()

			if len(temp) != 3 or len(temp[0]) > 128 or len(temp[1]) >10 or len(temp[2]) != 2:
				self.footer.config(text='Please Follow the required Format !', bg='red2', fg='white', relief='raised')
				return
			else:
				digest = SHA256.new()
				digest.update("".join(temp).encode())
				sig = pkcs.new(RSA.importKey(privkey.exportKey())).sign(digest).hex()

				post_data['data'].append({'uid':temp[0], 'course':temp[1], 'grade':temp[2], 'identifier':self.uname, 'sig':sig})
				num = num+1

		post_data['count'] = num

		url = 'http://localhost/insert.php'
		try:
			self.footer.config(text='Submitting Grades...', bg='black', fg='springGreen', relief='raised')
			self.footer.update_idletasks()
			response = self.sess.post(url, json=post_data)
			text = response.text
			# print(text)
		except (ConnectionError, requests.exceptions.RequestException) as e:
			self.footer.config(text='Some Error has Occurred !', bg='red2', fg='white')
			return

		if text == "UFO":
			self.footer.config(text='!!!  BREACH DETECTED  !!!', bg='gold', fg='red3', borderwidth=2, relief='sunken')
		elif text == "N":
			self.footer.config(text='Please Follow the required Format !', bg='red2', fg='white', relief='raised')
		elif text[0] == "D":
			self.footer.config(text='Some Grades could not be Submitted !', bg='red2', fg='white', relief='raised')
			textBox = self.eG.winfo_children()[0].winfo_children()[1]
			textBox.delete(1.0, float(text[1:])+1.0)
			textBox.tag_add("error", "1.0", "2.0")
		elif text == "S":
			self.footer.config(text='Grades Entered Successfully', bg='black', fg='springGreen', relief='raised')
			self.eG.winfo_children()[0].winfo_children()[1].delete(1.0, "end")
			# Put reload button (only once)
			if self.reload_button == 0:
				ref_img = "iVBORw0KGgoAAAANSUhEUgAAABYAAAAWCAMAAADzapwJAAAABGdBTUEAALGPC/xhBQAAAAFzUkdCAK7OHOkAAAIcUExURf///ya6oSe6oTS/pzO+pjG+pim7ojK+pv3+/jW/pyW6oCi7oi+9pTvBqjjAqTa/py28pD/CrDS+pyO5n0bEr/7+/qfj2Sq8ozS+pje/qFLItEfFr1rLuP7//zG+pSq7ooTYyt/18TzBq/z+/Se7oSy8ozjAqD7CqznAqWrQvkfEry69pG3RwCi7oS68pG7RwCa6oDC9pSu8o+f39CK5nya7oSe7ouj39SG5n2TOvCO6nyG4nyq7o/f8+/X8++f39eL28iS6oOv59mLNuyu7oyW5oOr49pPd0EXEruD18nfUxOD18f7//iO5oLHm3UHDraHi18ft5mzQv0bErii6os/w62vQv6Ti16Pi1+v49tXy7dz08N718aLh1/P7+un39ajk2cbt58vu6I/cz6nk2vH6+T3Cq0/HskLDrVTJtFPItJHc0Jbe0Sy8pDC+pXbUxKrk2oLXycLr5IjZy/T7+rnp4fn9/JHcz4PYySW6oeH28rTn3/X8+vb8+7zq4jK9pmbPvX/WyDO+p9Hx62fPvXnVxUzGsT3Bq1/MuW/RwHLSwmPOvIXYyuL18lrKt1nKt5fe0lbJtVfKtlbJto7bznDSwc7w6vz+/oPXyWfOvabj2LXo34fZy8bt5j/Cq+T39E7HsjK+pXzVxlfJtpbd0nHSwn/Wx33Wx6Dh1t708e/6+GPNvCq8otDw65bd0dfy7eX39FvKuNjz7iS6n1GSCawAAAG/SURBVBjTNdFVd9tAEAXgK2ml1UqWjDHHFFOYmZmatCmmTZmZmZmZUmZuk7bpH+zKPpmHmXO+h905dwCgQEXP+sqQ3R4qezEAtQC5UnHmvlPoi8iy3FaV+XSaQ0677o5FqKgQmtRd8tjHYctVnAzVm3ri+JFLT8dHpL6sOBS3/Og9IS3erEUhsABzf/Vs8lE7f2R3iyneBg7uu94b+42On4rRfQxY6dzruwX1gK4per9tFn8ydY6tjfBqgZpw16FWF5MYSXz+jpcj25pWoGypRCpSe/yUUlJ9LY5pbAnWLUaJjVDKKG98CM2FRYhp1AMmu3zBZQsdea/yYqKUUAZG/b6z2FzPLCYVzlVhRZIZSmj3FRThvJD3cwHebB5Uuq/2cL7jtP6gfkepg0jlxfC2vvsyjs6vGco3vNj0qrE3GtAWYeBNyp0exTeXJur90ZiK51HZqAUG/xm/wj8w/Phy84fXwDPBbNnEM2l/KGaV4AzPiaf19omYLt/RYQUbHxLMVOTG/g0bT10wFDO5fSof+OgDN2WKZqtuaCDv3TtXz5/n8GBCaOPryTUnjF1r85o78brJ5R67fUnxmk6olv4HiD1RWB2GYT8AAAAASUVORK5CYII="
				ref = tk.PhotoImage(data=ref_img)
				refreshG = tk.Button(self.winfo_children()[4], image=ref, activebackground='cyan4', command=lambda: self.viewG(1))
				refreshG.image = ref
				refreshG.grid(row=0, column=1)
			self.reload_button = 1

	def updateG(self, event):
		w = event.widget
		idx = w.selection()[0]
		item = w.item(w.selection())['values']

		uG = simpledialog.askstring('Update grade', 'Enter New Grade', parent=self, initialvalue=item[3])
		passPh = simpledialog.askstring("PassPhrase", "Enter PassPhrase:", show='*')

		with open(os.path.expanduser("~/"+self.uname+".pem"), "r") as f:
			privkey = RSA.importKey(f.read(), passphrase=passPh)

		digest = SHA256.new()
		digest.update("".join([item[0], item[2], uG]).encode())
		sig = pkcs.new(RSA.importKey(privkey.exportKey())).sign(digest).hex()

		post_data = {'uid':item[0], 'course':item[2], 'grade':uG, 'identifier':self.uname, 'sig':sig}

		url = 'http://localhost/update.php'
		try:
			self.footer.config(text='Updating Grade...', bg='black', fg='springGreen')
			self.footer.update_idletasks()
			response = self.sess.post(url, data=post_data)
			text = response.text
			print(text)
		except (ConnectionError, requests.exceptions.RequestException) as e:
			self.footer.config(text='Some Error has Occurred !', bg='red2', fg='white', relief='raised')
			return

		if text == "D":
			self.footer.config(text='Some Error has Occurred !', bg='red2', fg='white', relief='raised')
		elif text == "S":
			self.footer.config(text='Grade Updated Successfully', bg='black', fg='springGreen', relief='raised')
			self.vG.winfo_children()[0].item(idx, values=(item[0], item[1], item[2], uG))
		elif text == "UFO":
			self.footer.config(text='!!!  BREACH DETECTED  !!!', bg='gold', fg='red3', borderwidth=2, relief='sunken')

	def Logout(self):
		url = 'http://localhost/logout.php'
		try:
			response = self.sess.post(url)
		except (ConnectionError, requests.exceptions.RequestException) as e:
			self.footer.config(text='Some Error has Occurred !', bg='red2', fg='white', relief='raised')
		else:
			self.attributes('-zoomed', False)
			self.clear_widgets()
			self.uname = ""
			self.student = None
			self.sess = None
			self.eG = None
			self.vG = None
			self.reload_button = 0
			self.footer.config(text='Successfully Logged Out', bg='black', fg='springGreen', relief='raised')
			self.Start()

	def clear_widgets(self):
		for widget in self.winfo_children():
			if widget != self.footer:
				widget.destroy()

def quit():
	if app.uname != "":
		app.Logout()
	else:
		app.destroy()

app = BcD()
app.protocol("WM_DELETE_WINDOW", quit)
app.mainloop()