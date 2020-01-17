import pygame
from pygame.locals import QUIT,MOUSEBUTTONDOWN
import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Button,Label
import time
import random

global choices
choices=[[0,0],[0,2],[2,0],[2,2],[1,1],[0,1],[1,0],[1,2],[2,1]]

def initializeGame():
    global finish,turn,grid,winner,draw,choices
    draw=False
    finish=False
    turn='X'
    grid=[[None,None,None],[None,None,None],[None,None,None]]
    winner=None
    choices=[[0,0],[0,2],[2,0],[2,2],[1,1],[0,1],[1,0],[1,2],[2,1]]

initializeGame()

def initializeBoard(xxx):
    background=pygame.Surface(xxx.get_size())
    background=background.convert()
    background.fill((250,250,250))

    pygame.draw.line(background,(0,0,0),(300,0),(300,900),2)
    pygame.draw.line(background,(0,0,0),(600,0),(600,900),2)

    pygame.draw.line(background,(0,0,0),(0,300),(900,300),2)
    pygame.draw.line(background,(0,0,0),(0,600),(900,600),2)

    return background

def showStatus (board):
    global turn, winner,finish

    if (winner is None):
        message = turn + "'s turn"
    else:
        message = winner + " won!"
        finish=True
    try:    
        font = pygame.font.Font(None, 36)
        text = font.render(message, 1, (10, 10, 10))
        board.fill ((250, 250, 250), (0, 900, 900, 25))
        board.blit(text, (10, 900))
    except pygame.error:
        pass


def showBoard(xxx,board):
    showStatus(board)
    try:
        xxx.blit (board, (0, 0))
        pygame.display.flip()
    except pygame.error:
        pass

def showRadom(xxx,board):
    global finish
    if winner is not None:
        finish=True
    try:
        xxx.blit (board, (0, 0))
        pygame.display.flip()
    except pygame.error:
        pass

def boardPosition (mouseX, mouseY):
    if (mouseY < 300):
        row = 0
    elif (mouseY < 600):
        row = 1
    else:
        row = 2

    if (mouseX < 300):
        col = 0
    elif (mouseX < 600):
        col = 1
    else:
        col = 2
    return (row, col)

def showMove(board,row,column,piece):
    global draw,freeSlots
    centerX = ((column) * 300) + 150
    centerY = ((row) * 300) + 150
    if (piece == 'O'):
        pygame.draw.circle (board, (0,0,0), (centerX, centerY), 88, 2)
    else:
        pygame.draw.line (board, (0,0,0), (centerX - 66, centerY - 66), \
                         (centerX + 66, centerY + 66), 2)
        pygame.draw.line (board, (0,0,0), (centerX + 66, centerY - 66), \
                         (centerX - 66, centerY + 66), 2)
    grid[row][column]=piece
    freeSlots=0
    for x in range (0,3):
        for y in range (0,3):
            if grid[x][y]==None:
                freeSlots=freeSlots+1
    if freeSlots==0:
        draw=True

rando=False

def randomMove(board,row,column,piece):
    global draw,freeSlots,rando
    centerX = ((column) * 300) + 150
    centerY = ((row) * 300) + 150
    if (piece == 'O'):
        pygame.draw.circle (board, (0,0,0), (centerX, centerY), 88, 2)
    else:
        pygame.draw.line (board, (0,0,0), (centerX - 66, centerY - 66), \
                         (centerX + 66, centerY + 66), 2)
        pygame.draw.line (board, (0,0,0), (centerX + 66, centerY - 66), \
                         (centerX - 66, centerY + 66), 2)
    grid[row][column]=piece
    freeSlots=0
    for x in range (0,3):
        for y in range (0,3):
            if grid[x][y]==None:
                freeSlots=freeSlots+1
    if freeSlots==0:
        draw=True

def autoMove(board,row,column,piece):
    if grid[row][column]=='X' or grid[row][column]=='O':
        return 
    global draw,auto
    centerX = ((column) * 300) + 150
    centerY = ((row) * 300) + 150
    if auto==False:
        pygame.draw.circle (board, (0,0,0), (centerX, centerY), 88, 2)
        grid[row][column]='O'
    auto=True

def testMove(board,row,column,piece):
    global draw,grid,auto
    centerX = ((column) * 300) + 150
    centerY = ((row) * 300) + 150

    pygame.draw.line (board, (0,0,0), (centerX - 66, centerY - 66), \
                    (centerX + 66, centerY + 66), 2)
    pygame.draw.line (board, (0,0,0), (centerX + 66, centerY - 66), \
                    (centerX - 66, centerY + 66), 2)
    grid[row][column]='X'
    freeSlots=0
    for x in range (0,3):
        for y in range (0,3):
            if grid[x][y]==None:
                freeSlots=freeSlots+1
    if freeSlots==0:
        draw=True
    auto=False

def clickBoard(board):
    global grid,turn
    (mouseX,mouseY)=pygame.mouse.get_pos()
    (row,column)=boardPosition(mouseX,mouseY)

    if grid[row][column]=='X' or grid[row][column]=='O':
        return
    
    showMove(board,row,column,turn)

    if(turn=='X'):
        turn='O'
    else:
        turn='X'

def randomBoard(board):
    global grid,turn,rando,freeSlots,draw,choices

    freeSlots=0
    for x in range (0,3):
        for y in range (0,3):
            if grid[x][y]==None:
                freeSlots=freeSlots+1
    if freeSlots>6:
        if(turn=='X'):
            turn='O'
        else:
            turn='X'
        move=random.choice(choices)
        randomMove(board,move[0],move[1],turn)
        choices.remove(move)
        time.sleep(0.5)
    else:
        for x in range (0,3):
            for y in range (0,3):
                if grid[x][y]==None:
                    if(turn=='X'):
                        turn='O'
                    else:
                        turn='X'
                    randomMove(board,x,y,turn)
                    time.sleep(0.1)

def testBoard(board):
    global grid,turn,auto
    (mouseX,mouseY)=pygame.mouse.get_pos()
    (row,column)=boardPosition(mouseX,mouseY)
    if grid[row][column]=='X' or grid[row][column]=='O':
        return  

    testMove(board,row,column,turn)

    freeSlots=0
    for x in range (0,3):
        for y in range (0,3):
            if grid[x][y]==None:
                freeSlots=freeSlots+1

    if grid[0][2]=='X' and grid[2][2]=='X':
        autoMove(board,1,2,'O')

    for row in range (0, 3):
        if grid [row][0] == 'O' and  grid[row][1] =='O' and grid[row][2]==None:
            autoMove(board,row,2,'O')   
            break
        if grid [row][0] == 'O' and  grid[row][2] =='O' and grid[row][1]==None:
            autoMove(board,row,1,'O')   
            break
        if grid [row][2] == 'O' and  grid[row][1] =='O' and grid[row][0]==None:
            autoMove(board,row,0,'O')   
            break
    for col in range (0, 3):
        if grid[0][col]== 'O' and grid[1][col]=='O' and grid[2][col]==None:
            autoMove(board,2,col,'O')   
            break  
        if grid[0][col]== 'O' and grid[2][col]=='O' and grid[1][col]==None:
            autoMove(board,1,col,'O')   
            break          
        if grid[2][col]== 'O' and grid[1][col]=='O' and grid[0][col]==None:
            autoMove(board,0,col,'O')
            break          
    
    if grid[0][0] == 'O' and grid[1][1]=='O':
        autoMove(board,2,2,'O')
    elif grid[2][2] == 'O' and grid[1][1]=='O':
        autoMove(board,0,0,'O')
    elif grid[0][0] == 'O' and grid[2][2]=='O':
        autoMove(board,1,1,'O')
        
    if grid[0][2] == 'O' and grid[1][1]=='O':
        autoMove(board,2,0,'O')
    elif grid[2][0] == 'O' and grid[1][1]=='O':
        autoMove(board,0,2,'O')
    elif grid[0][2] == 'O' and grid[2][0]=='O':
        autoMove(board,1,1,'O')


    if freeSlots==2 or freeSlots==6 or freeSlots==4:
        for row in range (0, 3):
            if grid [row][0] == 'X' and  grid[row][1] =='X' and grid[row][2]==None:
                autoMove(board,row,2,'O')   
                break
            if grid [row][0] == 'X' and  grid[row][2] =='X' and grid[row][1]==None:
                autoMove(board,row,1,'O')   
                break
            if grid [row][2] == 'X' and  grid[row][1] =='X' and grid[row][0]==None:
                autoMove(board,row,0,'O')   
                break
        for col in range (0, 3):
            if grid[0][col]== 'X' and grid[1][col]=='X' and grid[2][col]==None:
                autoMove(board,2,col,'O')   
                break  
            if grid[0][col]== 'X' and grid[2][col]=='X' and grid[1][col]==None:
                autoMove(board,1,col,'O')   
                break          
            if grid[2][col]== 'X' and grid[1][col]=='X' and grid[0][col]==None:
                autoMove(board,0,col,'O')
                break          
        
    if grid[0][0] == 'X' and grid[1][1]=='X':
        autoMove(board,2,2,'O')
    elif grid[2][2] == 'X' and grid[1][1]=='X':
        autoMove(board,0,0,'O')
    elif grid[0][0] == 'X' and grid[2][2]=='X':
        autoMove(board,1,1,'O')
        
    if grid[0][2] == 'X' and grid[1][1]=='X':
        autoMove(board,2,0,'O')
    elif grid[2][0] == 'X' and grid[1][1]=='X':
        autoMove(board,0,2,'O')
    elif grid[0][2] == 'X' and grid[2][0]=='X':
        autoMove(board,1,1,'O')


    if grid[1][1]=='X':
        if freeSlots==8:
            choices=[[0,0],[0,2],[2,0],[2,2]]
            move=random.choice(choices)
            autoMove(board,move[0],move[1],'O')

    if grid[1][1]=='X' and grid[2][2]=='X':
        autoMove(board,0,2,'O')
    elif grid[2][0]=='X' and grid[1][1]=='X':
        autoMove(board,2,2,'O')
    elif grid[0][2]=='X' and grid[1][1]=='X':
        autoMove(board,2,2,'O')
    elif grid[0][0]=='X' and grid[1][1]=='X':
        autoMove(board,2,0,'O')

            
    elif grid[1][1]==None:
        autoMove(board,1,1,'O')
    else:
        for x in range (0,3):
            for y in range (0,3):
                if grid[x][y]==None:
                    autoMove(board,x,y,'O')


    if freeSlots==2:
        for x in range (0,3):
            for y in range (0,3):
                if grid[x][y]==None:
                    autoMove(board,x,y,'O')
                
    

def gameWon(board):
    
    global grid, winner, running

    for row in range (0, 3):
        if ((grid [row][0] == grid[row][1] == grid[row][2]) and \
           (grid [row][0] is not None)):
            winner = grid[row][0]
            pygame.draw.line (board, (250,0,0), (0, (row + 1)*300 - 150), \
                              (900, (row + 1)*300 - 150), 2)
            break

    for col in range (0, 3):
        if (grid[0][col] == grid[1][col] == grid[2][col]) and \
           (grid[0][col] is not None):
            winner = grid[0][col]
            pygame.draw.line (board, (250,0,0), ((col + 1)* 300 - 150, 0), \
                              ((col + 1)* 300 - 150, 900), 2)
            break

    if (grid[0][0] == grid[1][1] == grid[2][2]) and \
       (grid[0][0] is not None):
        winner = grid[0][0]
        pygame.draw.line (board, (250,0,0), (150, 150), (750, 750), 2)

    if (grid[0][2] == grid[1][1] == grid[2][0]) and \
       (grid[0][2] is not None):
        winner = grid[0][2]
        pygame.draw.line (board, (250,0,0), (750, 150), (150, 750), 2)


def randomWon(board):
    
    global grid, winner, running
    if winner is None:
        for row in range (0, 3):
            if ((grid [row][0] == grid[row][1] == grid[row][2]) and \
            (grid [row][0] is not None)):
                winner = grid[row][0]
                pygame.draw.line (board, (250,0,0), (0, (row + 1)*300 - 150), \
                                (900, (row + 1)*300 - 150), 2)
                break
            
    if winner is None:
        for col in range (0, 3):
            if (grid[0][col] == grid[1][col] == grid[2][col]) and \
            (grid[0][col] is not None):
                winner = grid[0][col]
                pygame.draw.line (board, (250,0,0), ((col + 1)* 300 - 150, 0), \
                                ((col + 1)* 300 - 150, 900), 2)
                break
    
    if winner is None:
        if (grid[0][0] == grid[1][1] == grid[2][2]) and \
        (grid[0][0] is not None):
            winner = grid[0][0]
            pygame.draw.line (board, (250,0,0), (150, 150), (750, 750), 2)

    if winner is None:
        if (grid[0][2] == grid[1][1] == grid[2][0]) and \
        (grid[0][2] is not None):
            winner = grid[0][2]
            pygame.draw.line (board, (250,0,0), (750, 150), (150, 750), 2)


def playerVsCPU():
    pygame.init()
    xxx=pygame.display.set_mode((900,925))
    pygame.display.set_caption("TicTacToe")

    board=initializeBoard(xxx)

    running=1

    while running==1:
        for event in pygame.event.get():
            if event.type is QUIT:
                running=0
            if finish:
                running=0
                messagebox.showinfo("Winner",winner+" won!")
                initializeGame()
                pygame.quit()
            if draw:
                running=0
                messagebox.showinfo("Draw","Draw game!")
                initializeGame()
                pygame.quit()
            elif event.type is MOUSEBUTTONDOWN:
                testBoard(board)

            gameWon(board)

            showBoard(xxx,board)

def cpuVsCPU():
    global freeSlots
    pygame.init()

    xxx=pygame.display.set_mode((900,925))
    pygame.display.set_caption("TicTacToe")
    board=initializeBoard(xxx)

    running=1

    while running==1:
        for event in pygame.event.get():
            if event.type is QUIT:
                running=0
            if finish:
                running=0
                messagebox.showinfo("Winner",winner+" won!")
                initializeGame()
                pygame.display.quit()
                pygame.quit()
                quitMain()
            if draw:
                running=0
                messagebox.showinfo("Draw","Draw game!")
                initializeGame()
                pygame.display.quit()
                pygame.quit()
                quitMain()
            randomBoard(board)

            randomWon(board)

            showRadom(xxx,board)


def playerVsPlayer():

    pygame.init()

    xxx=pygame.display.set_mode((900,925))
    pygame.display.set_caption("TicTacToe")

    board=initializeBoard(xxx)

    running=1

    while running==1:
        for event in pygame.event.get():
            if event.type is QUIT:
                running=0
            if finish:
                running=0
                messagebox.showinfo("Winner",winner+" won!")
                initializeGame()
                pygame.quit()
            if draw:
                running=0
                messagebox.showinfo("Draw","Draw game!")
                initializeGame()
                pygame.quit()
            elif event.type is MOUSEBUTTONDOWN:
                clickBoard(board)

            gameWon(board)

            showBoard(xxx,board)

def refreshWindow():
    mainWindow()
    try:
        root.focus_force()
    except Exception:
        pass

def quitMain():
    root.destroy()

def mainWindow():
    global root
    root=tk.Tk()
    root.title("TicTacTui")
    w=300
    h=300
    ws=root.winfo_screenwidth() 
    hs=root.winfo_screenheight() 
    x=(ws/2)-(w/2)
    y=(hs/2)-(h/2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    root.resizable(0,0)

    space0=Label(root, text="")
    space0.pack()
    space1=Label(root, text="")
    space1.pack()
    pvpButton=Button(root,text="Player vs Player",command=playerVsPlayer)
    pvpButton.pack()
    space2=Label(root, text="")
    space2.pack()
    pvcButton=Button(root,text="Player vs CPU", command=playerVsCPU)
    pvcButton.pack()
    space3=Label(root, text="")
    space3.pack()
    cvcButton=Button(root,text="CPU vs CPU",command=cpuVsCPU)
    cvcButton.pack()
    space4=Label(root, text="")
    space4.pack()
    space5=Label(root, text="")
    space5.pack()
    space6=Label(root, text="")
    space6.pack()
    quitButton=Button(root,text="Quit",command=quitMain)
    quitButton.pack()

    root.mainloop()

if __name__ == "__main__":
    mainWindow()    