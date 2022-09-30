from tkinter import *
from PIL import ImageTk,Image
import sqlite3
import string
import csv
import os
import menuSystem

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

global localscore
global qnum

root = Tk()

BoardFrame = Frame(root)
BoardFrame.grid(row=0,column=0)
root.title('Chess Puzzle System')
root.geometry("1000x600")
root.resizable(width=False, height=False)

localscore = 0
qnum = 0

chessDict = dict()
pieces = ['pawn', 'bishop', 'knight', 'rook', 'queen', 'king']
colours = ['w', 'b']
listPiece = []
listPosition = []

pieces_folder = os.getcwd() + r"\pieces"

wpawn_pimg = ImageTk.PhotoImage(Image.open(pieces_folder + "\\wpawn.png"))
wknight_pimg = ImageTk.PhotoImage(Image.open(pieces_folder + "\\wknight.png"))
wbishop_pimg = ImageTk.PhotoImage(Image.open(pieces_folder + "\\wbishop.png"))
wrook_pimg = ImageTk.PhotoImage(Image.open(pieces_folder + "\\wrook.png"))
wqueen_pimg = ImageTk.PhotoImage(Image.open(pieces_folder + "\\wqueen.png"))
wking_pimg = ImageTk.PhotoImage(Image.open(pieces_folder + "\\wking.png"))
bpawn_pimg = ImageTk.PhotoImage(Image.open(pieces_folder + "\\bpawn.png"))
bknight_pimg = ImageTk.PhotoImage(Image.open(pieces_folder + "\\bknight.png"))
bbishop_pimg = ImageTk.PhotoImage(Image.open(pieces_folder + "\\bbishop.png"))
brook_pimg = ImageTk.PhotoImage(Image.open(pieces_folder + "\\brook.png"))
bqueen_pimg = ImageTk.PhotoImage(Image.open(pieces_folder + "\\bqueen.png"))
bking_pimg = ImageTk.PhotoImage(Image.open(pieces_folder + "\\bking.png"))

def generateFiles():
    fileList = []    
    folderpath = os.getcwd()

    difficulty = menuSystem.getDifficulty()

    if difficulty == "A":
        folderpath += "\\A"
    elif difficulty == "B":
        folderpath += "\\B"
    elif difficulty == "C":
        folderpath += "\\C"

    return folderpath

def retrieveFile(num):
    folderpath = generateFiles()
    arr = os.listdir(folderpath)
    maxn = len(arr)+ 1

    try:
        if arr[num]:
            item = str(arr[num])
            filepath = folderpath + "\\" +str(arr[num])
            return filepath
    except:
       mainMenu()
       
            
    return item
        
def retrieveImg(pieceRow,pieceColumn):
    filepath = retrieveFile(qnum)
        
    with open(filepath, 'r') as puzzles:
        reader = csv.reader(puzzles,delimiter=',')
        piecelist = pieceRow,pieceColumn
        desiredKey = ""
            
        for position,pieces in chessDict.items():
            if pieces == piecelist:
                desiredKey = position
                    
        for row in reader:
            if row[0] == desiredKey:
                return row[1]
def retrieveQ():
    filepath = retrieveFile(qnum)
    prompt = ""
    with open(filepath,'r') as question:
        reader = csv.reader(question,delimiter=',')
        for row in reader:
            if row[0] == "qprompt":
                return row[1]
        
                
def retrieveOpts():
    optlist = []
    filepath = retrieveFile(qnum)
        
    with open(filepath,'r') as question:
        reader = csv.reader(question,delimiter=',')
        for row in reader:
            try:
                if row[0] == "opt1":
                    optlist.insert(0,row[1])
                elif row[0] == "opt2":
                    optlist.insert(1,row[1])
                elif row[0] == "opt3":
                    optlist.insert(2,row[1])
            except:
                pass
    return optlist[0],optlist[1],optlist[2]
    
def checkOpt(opt,num,b1,b2,b3):
    b1.destroy()
    b2.destroy()
    b3.destroy()

    filepath = retrieveFile(num)
        
    with open(filepath,'r') as option:
        reader = csv.reader(option,delimiter=',')
        for row in reader:
            try:
                if row[1] == str(opt):
                    global localscore
                    global qnum
                    localscore = localscore + 1
                    qnum = qnum + 1
                    refresh()
                    break
                else:
                    qnum = qnum + 1
                    refresh()
                    break
            except:
                pass
           
def generatePiece(slot,pieceRow,pieceColumn):
    img = retrieveImg(pieceRow,pieceColumn)
    local_img = None

    if img  == "wpawn":
        local_img = wpawn_pimg
    elif img == "wknight":
        local_img = wknight_pimg
    elif img == "wbishop":
         local_img = wbishop_pimg
    elif img == "wrook":
         local_img = wrook_pimg
    elif img == "wqueen":
        local_img = wqueen_pimg
    elif img == "wking":
         local_img = wking_pimg
    elif img == "bpawn":
         local_img = bpawn_pimg
    elif img == "bknight":
         local_img = bknight_pimg
    elif img == "bbishop":
         local_img = bbishop_pimg
    elif img == "brook":
        local_img = brook_pimg
    elif img == "bqueen":
        local_img = bqueen_pimg
    elif img == "bking":
        local_img = bking_pimg
    else:
        local_img = None
            
    PieceLabel = Label(BoardFrame,padx=30,pady=25,bg=slot,image=local_img)
    PieceLabel.grid(row=pieceRow,column=pieceColumn,sticky="nsew")

def generateBoard():
    slot = "white"
    pieceRow = 0 
    pieceColumn = 0

    for piecex in range(64):
        if pieceColumn % 8 == 0:
             pieceColumn = 0
                
        if slot == "white":
            if piecex % 8 == 0:
                if piecex == 0:
                    pass
                else:
                    pieceRow = pieceRow + 1                   
            slot = "grey"
            if pieceRow % 2 == 0 and pieceColumn == 0:
                slot = "white"
            generatePiece(slot,pieceRow,pieceColumn)
                
        elif slot == "grey":
            if piecex % 8 == 0:
                if piecex == 0:
                    pass
                else:
                    pieceRow = pieceRow + 1
            slot = "white"

            if pieceRow  % 2 != 0  and pieceColumn == 0:
                slot = "grey"
            generatePiece(slot,pieceRow,pieceColumn)
        pieceColumn = pieceColumn + 1
            
def generateLayout():
    alphalist = list(string.ascii_lowercase[0:8])
    numberlist = list(string.digits[1:9])
    numberlist.reverse()
        
    for i in range(0,8):
        imageLabel = Label(BoardFrame,padx=20,pady=5,text=alphalist[i],font='Arial 12 bold')
        imageLabel.grid(row=8,column=i)

    for i in range(0,8):
        imageLabel1 = Label(BoardFrame,text=numberlist[i],padx=20,pady=5,font='Arial 12 bold')
        imageLabel1.grid(row=i,column=9)
    
def generateUI():
    endbutton = Button(BoardFrame,text='End Round',command=lambda: mainMenu())
    endbutton.grid(row=7,column=10)

    scorelabel = Label(BoardFrame,text='Score: ' + str(localscore))
    scorelabel.grid(row=8,column=10)

def generatePositions():
     index = 1
     for color in colours:
         for piece in pieces:
             index = index + 1
             color, piece = str(color), str(piece)
             colorPiece = color + piece
             listPiece.append(colorPiece)

     piecePositions = list(string.ascii_lowercase[0:8])
     for i in range(1, 9):
         for item in piecePositions:
             chessDict[item + str(i)] = None
             listPosition.append(item + str(i))
                
     nindex = 0
        
     for i1 in range (7,-1,-1):
         for i2 in range (0,8):
             chessDict[listPosition[nindex]] = i1,i2
             nindex = nindex + 1
        
def changeOptionPrompts():
    qlabel = Label(BoardFrame, padx=75,pady=20,text='',font='Arial 10 bold')
    qlabel.grid(row=0,column=10)

    button1 = Button(BoardFrame,text='OPT1',command=lambda: checkOpt('opt1',qnum,button1,button2,button3))
    button1.grid(row=1,column=10)

    button2 = Button(BoardFrame,text='OPT2',command=lambda: checkOpt('opt2',qnum,button1,button2,button3))
    button2.grid(row=2,column=10)

    button3 = Button(BoardFrame,text='OPT3',command=lambda: checkOpt('opt3',qnum,button1,button2,button3))
    button3.grid(row=3,column=10)
        
    prompt = retrieveQ()
    qlabel.config(text=prompt)

    opt1,opt2,opt3 = retrieveOpts()

    button1.config(text=opt1)
    button2.config(text=opt2)
    button3.config(text=opt3)

def inputScore():
    userfile = open("local.txt","r+")
    username = userfile.read()
    cursor.execute('UPDATE users SET score = score + (?) WHERE username = (?)', (localscore,username))
    conn.commit()

def mainMenu():
    inputScore()
    root.withdraw()
    
    for child in BoardFrame.winfo_children():
        child.destroy()
    global localscore
    localscore = 0
    
    menuSystem.initialise()

def initialise():
    global qnum
    qnum = 0
    
    root.deiconify()
    
    generatePositions()
    generateLayout()
    generateUI()
    generateBoard()
    changeOptionPrompts()
    root.mainloop()

def refresh():
    generateLayout()
    generateUI()
    generateBoard()
    changeOptionPrompts()
