import tkinter
from math import inf
import time
import copy

"""
This class represents the state of a game of TicTacToe
It keeps track of a 3x3 grid, where each position of a grid is
1 if player 1 has claimed it
2 if player 2 has claimed it

"""
class TTTBoard:

    # These don't change from game to game, they should be static
    p1char = 'X'
    p2char = 'O'
    blankchar = ' '

    def __deepcopy__(self,memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k,v in self.__dict__.items():
            #print(type(v).__name__)
            if type(v).__name__ not in ('Canvas','PhotoImage'):
                if type(v).__name__ == 'list' and len(v) > 0 and type(v[0]).__name__ == 'PhotoImage':
                    continue
                setattr(result,k, copy.deepcopy(v,memo))
        return result

    """ Initialize the board """
    def __init__(self,canvas):
        # 0 represents blank
        # 1 represents player 1
        # 2 represents player 2
        self.meta_grid = None
        self.grid = [[0,0,0],[0,0,0],[0,0,0]]
        self.canvas = canvas
        self.curPlayer = 1
        #This is one way to keep track of the end state of the game
        self.totalmoves = 0

        #knight
        self.idleKnight = tkinter.PhotoImage(file = 'assets/Knight_idle_01.png')
        self.idleKnight = self.idleKnight.zoom(2,2)
        self.knight = [tkinter.PhotoImage(file = 'assets/Knight_attack_01.png'),tkinter.PhotoImage(file = 'assets/Knight_attack_02.png'),tkinter.PhotoImage(file = 'assets/Knight_attack_03.png'),tkinter.PhotoImage(file = 'assets/Knight_attack_04.png'),tkinter.PhotoImage(file = 'assets/Knight_attack_05.png'),tkinter.PhotoImage(file = 'assets/Knight_attack_06.png')]
        for i in range(len(self.knight)):
            self.knight[i] = self.knight[i].zoom(2,2)
        self.a = 0

        #ninja
        self.ninja_idle = tkinter.PhotoImage(file = 'assets/SNinja_idle 1.png')
        #self.ninja_idle = self.ninja_idle.rotate(180)
        self.ninja = [tkinter.PhotoImage(file = 'assets/SNinja_Atk 1.png'),tkinter.PhotoImage(file = 'assets/SNinja_Atk 2.png'),tkinter.PhotoImage(file = 'assets/SNinja_Atk 3.png'),tkinter.PhotoImage(file = 'assets/SNinja_Atk 4.png'),tkinter.PhotoImage(file = 'assets/SNinja_Atk 5.png'),tkinter.PhotoImage(file = 'assets/SNinja_Atk 6.png')]
        self.b = 0

        #visuals
        self.bg = tkinter.PhotoImage(file = 'assets/background.png')

        self.file = tkinter.PhotoImage(file = 'assets/Sword.png')
        self.file = self.file.subsample(3,3)

        self.file_shield = tkinter.PhotoImage(file = 'assets/shield.png')
        self.file_shield = self.file_shield.subsample(3,3)


    """ Return the plays whose turn it currently is """
    def currentPlayer(self):
        return self.curPlayer

    """ makeMove is changed slightly  to now receive a row and column
    directly, not a string. It doesn't have to return anything either"""
    def makeMove(self,r,c):
        if self.grid[r][c] == 0:
            self.grid[r][c] = self.curPlayer
            #Sneaky trick to switch players
            self.curPlayer = 3 - self.curPlayer
            self.totalmoves = self.totalmoves + 1

    def click(self,event):
        
        print('x',event.x,'y',event.y)
        row = (event.x - 480)//180
        col = (event.y - 20)//180
        print('r',row,'c',col)

        if 0 <= row < 3 and 0 <= col < 3:
            self.makeMove(row,col)

    def knightAttack(self,t = False):
        
        lastImg = 0
        #self.a = self.canvas.create_image(150,500, image = self.idleKnight)

        if(t == True):
            self.canvas.delete(self.a)

            for i in range(len(self.knight)):
                self.canvas.delete(lastImg)

                lastImg = self.canvas.create_image(150,500, image = self.knight[i])
                self.canvas.update()
                time.sleep(0.05)
            self.canvas.delete(lastImg)
        self.a = self.canvas.create_image(150,500, image = self.idleKnight)

    def NinjaAttack(self,t = False):
        
        print('attacking knight')
        lastImg = 0
        
        if(t == True):
            self.canvas.delete(self.b)
            time.sleep(0.2)
            for i in range(len(self.ninja)):
                self.canvas.delete(lastImg)

                lastImg = self.canvas.create_image(1250,575, image = self.ninja[i])
                self.canvas.update()
                time.sleep(0.05)
            self.canvas.delete(lastImg)
        self.b = self.canvas.create_image(1250,575, image = self.ninja_idle)


    def drawBoard(self):
    
        self.canvas.create_image(400,400, image = self.bg)
        self.canvas.create_rectangle(430,30, 970,570, outline = 'black', width = 4, fill = 'black',stipple = 'gray50')

        #draw the knight
        self.knightAttack()
        self.NinjaAttack()

        #Draw the lines for the tictactoe grid
        for i in range(610,970,180):
            self.canvas.create_line(i,30,i,570,fill = 'white', width = 4)
        for i in range(210,570,180):
            self.canvas.create_line(430,i,970,i,fill = 'white', width = 4)
        #For each player, draw the appropriate piece
        for i in range(3):
            for j in range(3):
                if self.grid[i][j] == 1:
                    
                    self.canvas.create_image(520+180*i,130+180*j, image = self.file)
                    
                    #self.canvas.create_oval(135+180*i,35+180*j,305+180*i,205+180*j,fill='red')
                elif self.grid[i][j] == 2:

                    self.canvas.create_image(520+180*i,130+180*j, image = self.file_shield)
                    #self.canvas.create_oval(135+180*i,35+180*j,305+180*i,205+180*j,fill='blue')




    """ Prints out a string representation of this object.
    This is very minimal and bare bones string representation
    Yours should be more interesting"""

    def __str__(self):
        # This is one of many ways to do this
        ans = '-------\n'
        for row in self.grid:
            for pos in row:
                ans = ans + '|'
                if pos == 1:
                    ans = ans + TTTBoard.p1char
                elif pos == 2:
                    ans = ans + TTTBoard.p2char
                else:
                    ans = ans + TTTBoard.blankchar
            ans = ans + '|\n'
            ans = ans + '-------\n'
        return ans


    """ Return the current winner of this board. 
        0 means the game is ongoing
        1 means Player 1 has won
        2 means Player 2 has won
        3 means a draw """
    def winner(self):
        #Horizontal tests
        for i in range(3):
            if self.grid[i][0] == self.grid[i][1] == self.grid[i][2] and self.grid[i][0] != 0:
                return self.grid[i][0]
        #Vertical tests
        for j in range(3):
            if self.grid[0][j] == self.grid[1][j] == self.grid[2][j] and self.grid[0][j] != 0:
                return self.grid[0][j]
        #Forward Diagonal
        if self.grid[0][0] == self.grid[1][1] == self.grid[2][2] and self.grid[0][0] != 0:
            return self.grid[0][0]
        #Backwards Diagonal
        if self.grid[0][2] == self.grid[1][1] == self.grid[2][0] and self.grid[0][2] != 0:
            return self.grid[0][2]
        #Check for draws
        if self.totalmoves == 9:
            return 3
        else:
            return 0


    #Return a list of tuples of legal moves
    def legalmoves(self):
        res = []
        for i in range(3):
            for j in range(3):
                if self.grid[i][j] == 0:
                    res.append( (i,j) )
        return res
