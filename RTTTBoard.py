#worked with Sean
import tkinter
import time
from math import inf
import copy


class RTTTBoard:

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

    def __init__(self,canvas):
        self.meta_grid = [[0,0,0],[0,0,0],[0,0,0]]    
        self.grid = [[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],]
        self.curPlayer = 1
        self.totalmoves = 0
        self.canvas = canvas
        self.rem = []
        self.last_move_counter = []
        self.lastMove = None

        #highlighted box
        self.squarebox = []

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
        #self.bigSword = tkinter.PhotoImage(file = 'Sword.png') 
        #self.bigSword = self.bigSword.subsample(3,3)
        self.file = self.file.subsample(7,7)

        self.file_shield = tkinter.PhotoImage(file = 'assets/shield.png')
        #self.bigShield = self.file_shield.subsample(3,3)
        self.file_shield = self.file_shield.subsample(7,7)
        
        
        self.lastMove = None

    def currentPlayer(self):
        return self.curPlayer

    def makeMove(self,row,col):
        
        r = row
        c = col
        a = self.force_Pos(r,c,self.lastMove)
        
        try:
            if a == True:
                if self.grid[r][c] == 0:
                    self.grid[r][c] = self.curPlayer
                    #Sneaky trick to switch players
                    self.curPlayer = 3 - self.curPlayer
                    self.totalmoves = self.totalmoves + 1
                    self.lastMove = str(r) + ' '  + str(c)
                    self.highlight(self.lastMove)
                    return True
                else:
                    return False
        except:
            return False
    

    #for the drawing board clicking
    def click(self, event):

        row = (event.x - 420)//60
        col = (event.y - 20)//60
        #print('row =',row,'col =',col)

        if 0 <= row < 9 and 0 <= col < 9:
            self.makeMove(row,col)


    def drawBoard(self):

        self.canvas.create_image(400,400, image = self.bg)
        self.canvas.create_rectangle(430,30, 970,570, outline = 'black', width = 4, fill = 'white')#,stipple = 'gray25')

        self.knightAttack()
        self.NinjaAttack()

        #Draw the lines for the tictactoe grid
        #vertical
        for i in range(610,970,180):
            self.canvas.create_line(i,30,i,570, width = 4)
        #horizontal
        for i in range(210,570,180):
            self.canvas.create_line(430,i,970,i, width = 4)

        #smaller grids
        #repeats 9 times creating smaller grids
        for x in range(3):
            for y in range(3):
                for i in range(490,610,60):
                    self.canvas.create_line(i + 180*x,35 + 180*y,i + 180*x,205 + 180*y,fill = 'black',width = 2)
                for i in range (90,210,60):
                    self.canvas.create_line(435 + 180*x,i + 180*y,605 + 180*x,i + 180*y,fill = 'black',width = 2)

        

        #For each player, draw the appropriate piece
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 1:
                    self.canvas.create_image(460+60*i,60+60*j, image = self.file)
                    #self.canvas.create_oval(135+180*i,35+180*j,305+180*i,205+180*j,fill='red')
                elif self.grid[i][j] == 2:
                    self.canvas.create_image(460+60*i,60+60*j, image = self.file_shield)
                    #self.canvas.create_oval(135+180*i,35+180*j,305+180*i,205+180*j,fill='blue')

        if self.lastMove != None:
            self.highlight()


    def highlight(self,input = None):
        
        #print('input =',input)
        if input == None:
            x = (self.squarebox[0]*60) + 430
            y = (self.squarebox[1]*60) + 30
            self.canvas.create_rectangle(x,y,x + 180,y + 180,fill = 'yellow',stipple = 'gray25')
        else:
            last_move = input.split()
            a = int(last_move[0])
            b = int(last_move[1])

            micro_grid_r = a%3
            micro_grid_c = b%3

            a = micro_grid_r * 3
            b = micro_grid_c * 3
            self.squarebox = [a,b]

    def knightAttack(self,t = False):
        lastImg = 0
        
        if(t == True):
            self.canvas.delete(self.a)
            time.sleep(0.2)
            for i in range(len(self.knight)):
                self.canvas.delete(lastImg)

                lastImg = self.canvas.create_image(150,500, image = self.knight[i])
                self.canvas.update()
                time.sleep(0.05)
            self.canvas.delete(lastImg)
        self.a = self.canvas.create_image(150,500, image = self.idleKnight)

    def NinjaAttack(self,t = False):
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






    #Prints out a string representation of this object
    def __str__(self):
            return ''

    #only position determined by this function are valid to land on
    def force_Pos(self, r, c, last_move):
        if last_move == None:
            return True
        else:
            last_move = last_move.split()
            a = int(last_move[0])
            b = int(last_move[1])
            
            #Position where player needs to move
            micro_grid_r = a%3
            micro_grid_c = b%3

            r = int(r/3)
            c = int(c/3)        
            if(r == micro_grid_r and c == micro_grid_c):
                return True        
        
        return False

    def fillBoard(self,a,b,val):

        #last player meta grid position    
        meta_grid_a = int(a/3)
        meta_grid_b = int(b/3) 

        #adds to the smaller meta grid
        self.meta_grid[meta_grid_a][meta_grid_b] = val
        a = str(meta_grid_a) + ' ' + str(meta_grid_b)
        a = a.split()


        #for last move 
        if len(self.last_move_counter) > 0:
            for i in self.last_move_counter:
                if i[0] == a[0] and a[1] == i[1]:
                    break
            else:
                self.last_move_counter.append(a)
                self.lastMove = None
        elif len(self.last_move_counter) == 0:
            self.last_move_counter.append(a)
            self.lastMove = None

        for i in range(0,9):
            for j in range(0,9):
                if int(i / 3) == meta_grid_a and int(j / 3) == meta_grid_b:
                    
                    if self.grid[i][j] == val:
                        continue
                    else:
                        self.grid[i][j] = val
                
                if int(i % 3) == meta_grid_a and int(j % 3) == meta_grid_b and self.grid[i][j] == 0:
                    self.grid[i][j] = val


    #bug in here
    def attack(self,x,y,val):
        meta_grid_x = int(x/3)
        meta_grid_y = int(y/3) 
        
        if len(self.rem) > 0:
            for i in self.rem:
                if i[0] == meta_grid_x and i[1] == meta_grid_y and i[2] == val:
                    return False

            self.rem.append([meta_grid_x,meta_grid_y,val])

            if val == 1:
                self.knightAttack(True)
            elif val == 2:
                self.NinjaAttack(True)
        else:
            self.rem.append([meta_grid_x,meta_grid_y,val])
            if val == 1:
                self.knightAttack(True)
            elif val == 2:
                self.NinjaAttack(True)



    #helper function, grades micro grids 
    def helper_grader(self,a):        
        for i in range(0,9):
            #horizontal test
            if self.grid[a][i] == self.grid[a + 1][i] == self.grid[a + 2][i] and self.grid[a][i] != 0:
                self.fillBoard(a,i, self.grid[a][i])
                if hasattr(self,'canvas'):
                    self.attack(a,i,self.grid[a][i])
            #vertical test
            if self.grid[i][a] == self.grid[i][a + 1] == self.grid[i][a + 2] and self.grid[i][a] != 0:
                self.fillBoard(i,a, self.grid[i][a])
                if hasattr(self,'canvas'):
                    self.attack(i,a,self.grid[i][a])        
        for i in range(0,9,3):    
            #Forward Diagonal
            if self.grid[a][i] == self.grid[a + 1][i + 1] == self.grid[a + 2][i + 2] and self.grid[a][i] != 0:
                self.fillBoard(a, i, self.grid[a][i])
                if hasattr(self,'canvas'):
                    self.attack(a,i,self.grid[a][i])     
            #Backwards Diagonal
            if self.grid[a + 2][i] == self.grid[a + 1][i + 1] == self.grid[a][i + 2] and self.grid[a][i + 2] != 0:
                self.fillBoard(a, i + 2, self.grid[a][i + 2])
                if hasattr(self,'canvas'):
                    self.attack(a,i,self.grid[a][i + 2])

    def winner(self):
        for i in range(0,9,3):
            self.helper_grader(i)
        
        #Horizontal tests
        for i in range(3):
            if self.meta_grid[i][0] == self.meta_grid[i][1] == self.meta_grid[i][2] and self.meta_grid[i][0] != 0:
                return self.meta_grid[i][0]
        #Vertical tests
        for j in range(3):
            if self.meta_grid[0][j] == self.meta_grid[1][j] == self.meta_grid[2][j] and self.meta_grid[0][j] != 0:
                return self.meta_grid[i][0]
        #Forward Diagonal
        if self.meta_grid[0][0] == self.meta_grid[1][1] == self.meta_grid[2][2] and self.meta_grid[0][0] != 0:
            return self.meta_grid[0][0]
        #Backwards Diagonal
        if self.meta_grid[0][2] == self.meta_grid[1][1] == self.meta_grid[2][0] and self.meta_grid[0][2] != 0:
            return self.meta_grid[0][2]
        #Check for draws
        if self.totalmoves == 81:
            return 3

        else:
            return 0

    #Return a list of tuples of legal moves
    def legalmoves(self):
        res = []
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0 and self.force_Pos(i,j,self.lastMove) == True:
                    res.append( (i,j) )
        return res