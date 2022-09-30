from tkinter import *
from PIL import ImageTk,Image  
import sqlite3
import menuSystem

class LoginSystem:
    def __init__(self, master):
        self.master = master

        master.title("Login System")
        master.geometry("250x250")
        master.resizable(width=False, height=False)

        self.img = Image.open("loginsys.png")
        self.img = self.img.resize((120,100))
        self.photoimg = ImageTk.PhotoImage(self.img)

        self.imageLabel = Label(root,image=self.photoimg)
        self.imageLabel.pack()
        
        self.userLabel = Label(root, text="Username:")
        self.userLabel.pack()

        self.userEntry = Entry(root)
        self.userEntry.pack(pady=5)

        self.passLabel = Label(root, text="Password:")
        self.passLabel.pack()

        self.passEntry = Entry(root, width=20)
        self.passEntry.pack(pady=5)

        self.buttonWidget = Button(root, text="Enter", command=lambda: self.validateUser())
        self.buttonWidget.pack(pady=10)

        self.statusLabel = Label(root, text="")
        self.statusLabel.pack()

        self.entrybind()

    def createUser(self):
        user = str(self.userEntry.get())
        password = str(self.passEntry.get())

        cursor.execute('INSERT INTO users VALUES(?, ?, ?)', (user,password,'0'))
        conn.commit()
        print("Created User")

    def validateUser(self, event=None):
        user = str(self.userEntry.get())
        password = str(self.passEntry.get())
        
        if not user.strip() or not password.strip():
            return
        if len(user) <= 10 or len(password) <= 10:
            self.changeStatus(False)
            return

        self.loginUser()

    def loginUser(self, event=None):
        username = self.userEntry.get()
        password = self.passEntry.get()
        print("Username: " + self.userEntry.get())
        print("Password: " + self.passEntry.get())

        print("Logging in..")
        
        cursor.execute("SELECT * from users")
        items = cursor.fetchall()
        for item in items:
            if item[0] == username and item[1] == password:
                print("Login Successful")
                self.localUser(username)
                
                self.changeStatus(True)
                self.master.destroy()
                menuSystem.initialise()
                return
            if item[0] == username and item[1] != password:
                print("Login Unsuccessful")
                self.changeStatus(False)
                return
            
        print("Login details invalid")

        self.openPrompt()

    def changeStatus(self, condition):
        if condition:
            self.statusLabel.config(text='Login Successful')
        else:
            self.statusLabel.config(text='Login Unsuccessful')

    def entrybind(self):
        self.userEntry.bind("<Return>", self.validateUser)
        self.passEntry.bind("<Return>", self.validateUser)

    def openPrompt(self):
        self.window = Toplevel(self.master)
        self.window.resizable(0,0)
        self.promptlabel= Label(self.window, text="Create new user?")
        self.promptlabel.pack(padx=150,pady=20)
        self.createb = Button(self.window, text="Create",command=lambda:self.createUser())
        self.createb.pack()
        self.cancelb = Button(self.window, text="Exit",command=lambda:self.window.destroy())
        self.cancelb.pack()
        
    def localUser(self,username):
        userfile = open("local.txt","w+")
        userfile.write(username)
        userfile.close()
        
                        

root = Tk()
conn = sqlite3.connect('users.db')
cursor = conn.cursor()
my_gui = LoginSystem(root)

root.mainloop()
