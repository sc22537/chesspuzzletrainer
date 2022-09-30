from tkinter import *
import sqlite3

diffList = []
conn = sqlite3.connect('users.db')
cursor = conn.cursor()


def initialise():
    master = Tk()
    master.title("Menu System")
    master.geometry("250x250")
    master.resizable(width=False, height=False)
    buttonWidget = Button(master, text="A",command=lambda:puzzle(master,"A"))
    buttonWidget.pack(pady=10)
    buttonWidget1 = Button(master, text="B",command=lambda:puzzle(master,"B"))
    buttonWidget1.pack(pady=10)
    buttonWidget2 = Button(master, text="C",command=lambda:puzzle(master,"C"))
    buttonWidget2.pack(pady=10)
    
    localscore = 0
    userfile = open("local.txt","r+")
    username = userfile.read()
    cursor.execute("SELECT * from users")
    items = cursor.fetchall()
    
    for item in items:
        if item[0] == username:
            localscore = item[2]

    userlabel = Label(master,text='Username: ' + username)
    userlabel.pack(pady=10)
    scorelabel = Label(master,text='Score: ' + str(localscore))
    scorelabel.pack(pady=1)
    master.mainloop()       
                
    diffList.clear()


def puzzle(master,opt):
    master.destroy()
    diffList.append(opt)
    import chessSystem
    chessSystem.initialise()

def getDifficulty():
    difficulty = None
    
    for i in diffList:
        difficulty = i
    return difficulty
