#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This project is a demonstration of detecting insider attacks on databases using Blockchain
# Copyright (C) 2018  Rishabh Raj
# This code is licensed under GNU GPLv3 license. See LICENSE for details

import tkinter as tk
import tkinter.messagebox as msgbox
from tkinter import scrolledtext, simpledialog
import tkinter.ttk as ttk
import requests, os, hashlib
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
		self.Start()

	def Start(self):
		
		self.title("Welcome to BcD")
		self.grid_columnconfigure(0, weight=1)
		self.grid_columnconfigure(1, weight=1)

		login = tk.Frame(self)
		login.grid(row=1, column=0, columnspan=2, pady=(5,5))
		ttk.Separator(self, orient="horizontal").grid(row=2, column=0, columnspan=2, sticky='nsew')
		signup = tk.Frame(self)
		signup.grid(row=3, column=0, columnspan=2, pady=(5,5))

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

		loginButton = tk.Button(login, text='Login', bg='blue', fg='white', activebackground='blue3', activeforeground='white', command=lambda: self.CheckLogin(nameBox.get(), pwordBox.get(), stud.get()))
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

		#Footer
		Footer = tk.Frame(self, bg='black')
		Footer.grid(row=4, column=0, columnspan=2, sticky='ew')
		logos = tk.Frame(Footer, bg='black')
		logos.grid(row=0, column=0)
		py_img = "iVBORw0KGgoAAAANSUhEUgAAACQAAAAkCAMAAADW3miqAAAABGdBTUEAALGPC/xhBQAAAAFzUkdCAK7OHOkAAAIKUExURUdwTP/gSDNxpP/ZRDR5rzNvoP/RPDR4ri1roDR2qjR4rf/POv/TQDR2qv/TP+XITv/YRv/dQ//aSP/fSzRwoS1pnP/NODR4rv/NODFzqv/SPjR6sP/OOf/MNv/UQP/WQjRzpS5wqzt0nDNqlytupjR5rjR4rjR1qP/RPDd0ov/ZQTR1qP/NOP/LNTV7sjR4rP/LNv/QPf/MNzR4rzR5sDR6sP/PO//LNTR3rTR4rjR0pjR4rv/TP//TQDR0pzBvozR0pjRzpf7ZRjRyozJxpf/XQjRyo//ZRjRvoP/ZRv/XRP/WQv/XRP/bSjJqlzNsm//gSf/jS//WQjR6sP/POv7RPDR4rzV7sv/MN//ROv/LNTR3rTR6sP/OODV7s//LNjRyozV7sv/KNf/YRv/LNv/OOf/KNf/WRP/QPf/RPj10mjRyo//aR//WQ//VQv/bQP/VQitnmzRxoSxomv/lSjR4rillmzRzpP/hTP/fTo6kayhlmzNql/DeTzRypP/gT//UQf/NOP/LNjV7sv/LNf/OOf/LNv/OOv/POv/TQDR1qTR3rTR4rv/UQTR2qv/NODRun//QPP/RPv/POf/XRDR0pv/SPzRzpDRxof/WQzNtnTR0pTR1p//ZRzRyo//VQv/YRjRyov/XRTRxoP/dSzNsmzR6sf/aSP/eTv/bSjNrmf/PPP/MNjRypC6D/7MAAACJdFJOUwCACT+mnj4CZy706YmjGAQCgKml8puN+9NG99W0oXG1pCY4/iG3iKEtFB3rKN78G5GJPO3Mq/dfPHvA3v3h5HDt4BWwgoz21cH19u7MwqK4NW+U+OANcu7yN8nsnvtQahFr76X38lN9yqYr/BT95VXiWTiMRfwvtpr4DljsEdfPUJqFYkWr5O1nrM9NyAAAAj5JREFUOMt11GdXGkEUgOEbSlAwYFQCBKRE4NARJdh7TdTYK2p67733CkJQsYCJAmoAhfzHzLAscMLwft3n7Nm9e3cAslk/s6S1409F3NZGbT0DSHEW7ZZo1ONZWvrpdv9uZ6tJaHHaIrWL0mb912ajlXCj+ajGqmdlzE6kjYBOR7UAU1kTYBORVCKxZ80eEXk8XG6OWSah+Vqn02k0GtvTJg9xUOpiKkkrZbbYgjudnZO0qNeyUMdSKZVdvZTZEo4M9vUNXedjw2iYxjNMDSjzPMj8ETLPhHeDQQVWF8fJBiNkQt6SUlBJC5hDIfMsNq4WHUxZCpjDxwgh42qWg4Y27v9M1ev7d7HZWJVBUyEzrB+jzIoYuPRyrOeaqjfn1LP3KJPgQWY5NjvYbUV0D5+9Yg56vdis+K+CiDbPVW+fjB7BHUf1KAZo458Bbtq8U40MvYzH9/cPYtvh8Bp6L9r4eNBEffidbsP7ONn4xKBJmb+9klHabKOPEQplTbISGlImUvHoRZ5ZpcyVOijuwAMKVJwqzzcJbJJzfOB04yHuIVTAXLoGAHrl7UhgGSOiMdcJAAAuFHX19w/fKj+IxbAZGCtB2Wy2E7jzpszyMhgMQRllgg8+HKUy5f8IpWWUCXlPohwOx8JHEkob1wYaEO+731dJQuHdtWB6OWSmGnGSgOBy1iR+AFQTkTxr/F8NurlkNQHxFRnjXzB/S5pnSQeUoaelmTJohjOyGuJRBwKd/OaNCR5vQiz79GUy58I/v4utx9RLivoAAAAASUVORK5CYII="
		py_logo = tk.PhotoImage(data=py_img)
		py = tk.Label(logos, image=py_logo, font='Verdana 7 bold', bg='black')
		py.image = py_logo
		py.grid(row=0, column=0, sticky='e')
		php_img = "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"
		php_logo = tk.PhotoImage(data=php_img)
		php = tk.Label(logos, image=php_logo, font='Verdana 7 bold', bg='black')
		php.image = php_logo
		php.grid(row=0, column=1)
		mc_img = "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"
		mc_logo = tk.PhotoImage(data=mc_img)
		mc = tk.Label(logos, image=mc_logo, font='Verdana 7 bold', bg='black')
		mc.image = mc_logo
		mc.grid(row=0, column=2, sticky='w')
		tk.Label(logos, text='Powered By Python, PHP & MultiChain', font='Verdana 7 bold', bg='black', fg='white', bd=0).grid(row=1, column=0, columnspan=3)
		logos.grid_columnconfigure(0, weight=1)
		logos.grid_columnconfigure(1, weight=1)
		Footer.grid_columnconfigure(0, weight=1)
		tk.Label(Footer, text='Developed By', font='Verdana 7 underline', bg='black', fg='gray40', bd=0).grid(row=1, column=0, pady=(5,0))
		tk.Label(Footer, text='Rishabh Raj | Kumar Saurav | Kumar Saunack | Shourya Pandey', font='Fixedsys 7 bold', bg='black', fg='gray50', bd=0).grid(row=2, column=0)
		tk.Label(Footer, text='Contact', font='Verdana 7 underline', bg='black', fg='gray40', bd=0).grid(row=3, column=0)
		tk.Label(Footer, text='rishabhstpaul@gmail.com', font='Fixedsys 7 bold', bg='black', fg='gray50', bd=0).grid(row=4, column=0)

		self.update_idletasks()
		h = self.winfo_reqheight()
		hs = self.winfo_screenheight()
		w = self.winfo_reqwidth()
		ws = self.winfo_screenwidth()
		x = (ws/2) - (w/2)
		self.geometry("+%d+%d" % (x, hs-h*11/10))

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
		self.grid_rowconfigure(4, weight=1)

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
			self.eG.grid(row=4, column=0, columnspan=2, pady=(1,3), sticky="ns")
		else:
			self.eG.grid(row=4, column=0, columnspan=2, pady=(1,3), sticky="ns")

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

				self.vG.grid(row=4, column=0, columnspan=2, pady=(1,7), sticky="ns")
			else:
				self.vG.grid(row=4, column=0, columnspan=2, pady=(1,7), sticky="ns")
		elif flag == 1:
			text = self.getGrades()
			if text is None:
				return
			viewList = self.vG.winfo_children()[0]
			viewList.delete(*viewList.get_children())
			for row in text.split('&'):
				viewList.insert("", "end", values=row.split('%'))
			self.footer.config(text='Grades Retrieved Successfully', bg='black', fg='springGreen', relief='raised')
			self.vG.grid(row=4, column=0, columnspan=2, pady=(1,7), sticky="ns")

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