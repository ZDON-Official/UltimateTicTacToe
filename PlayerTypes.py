#This file contains classes for different types of Players that might play this
#game.
import random
import copy
import RTTTBoard
import TTTBoard
import math
import time

class HumanPlayer:
    def __init__(self,mainGame,board,canvas):
        self.mainGame = mainGame
        self.board = board
        self.canvas = canvas

    def decideMove(self):
        self.canvas.bind("<Button-1>",self.gameClick)

    def gameClick(self,event):
        self.board.click(event)
        self.mainGame.playerTurn()


class RandomPlayer:
    def __init__(self,mainGame,board):
        self.mainGame = mainGame
        self.board = board

    def decideMove(self):
        legalmoves = self.board.legalmoves()
        move = legalmoves[ random.randint(0,len(legalmoves)-1)]
        self.board.makeMove(move[0],move[1])
        self.mainGame.playerTurn()


'''
TODO
'''
class AIPlayer:
    def __init__(self,mainGame,playernum,board):
        self.mainGame = mainGame
        self.playernum = playernum
        self.board = board
        #self.lastMove = 0
        self.winop = 0
        self.winp = 0

    #Writing a heuristic evaluation function will be an important part of your AI
    #You can do something like this:
    def heuristic(self,board):
        if type(self.board).__name__ == 'TTTBoard':
            return self.TTTheuristic(board)
        elif type(self.board).__name__ == 'RTTTBoard':
            return self.RTTThueristic(board)
        else:
            return 0

    #Here's an example, very bad TTT heuristic. 
    #For me, a 100 is a win, -100 is a loss, 0 is a draw
    #My heuristic only looks at the middle element. If it is mine, I feel that the
    #board is worth 50. If it is the opponents, I feel that the board is worth -50.
    #Otherwise, I return 0
    def TTTheuristic(self,board):
        a = board.winner()
        pn = self.playernum
        cp = board.currentPlayer()
        opn = 3 - self.playernum
        val = 0

        for i in range(0,3,2):
                for j in range(0,3,2):
                    if board.grid[i][j] == 0:
                        val -= 15
                    if board.grid[i][j] == pn:
                        val += 20
                    if board.grid[i][j] == opn:
                        val -= 10

        for i in range(3):
            if board.grid[0][i] == board.grid[2][i] == pn:
                    return 75
            if board.grid[0][i] == board.grid[2][i] == opn:
                    return -75

        if board.grid[0][0] == board.grid[2][2] == pn:
            return 75
        if board.grid[0][0] == board.grid[2][2] == opn:
            return -75

        if a == 1:
            return 100
        if a == 2:
            return -100
        if a == 0:
            return 0
        for i in range(3):
            for j in range(3):
                if board.grid[i][j] == pn:
                    val += 15
                if board.grid[i][j] == opn:
                    val -= 15
        if board.grid[1][1] == self.playernum:
            return 50
        if board.grid[1][1] == 3 - self.playernum:
            return -50
        else:
            return 0

    #You write this
    def RTTThueristic(self,board):
        
        '''values = []
        for x in board.legalmoves():
            values.append(x)'''


        pn = self.playernum
        cp = board.currentPlayer()
        opn = 3 - self.playernum
        currentpwin = int(self.winp)
        currentopwin = int(self.winop)
        val = 0
        if board.lastMove != None:
            a = board.lastMove
            a = a.split()

            micR = int(a[0]) % 3
            micC = int(a[1]) % 3
            #print('mr', micR,' mc', micC)
            
            for i in range(7):
                for j in range(7):
                    if board.grid[i][j] == board.grid[i+1][j] == pn and board.grid[i+2][j] == opn:
                        val -= 5
                    elif board.grid[i][j] == board.grid[i][j+1] == pn and board.grid[i+2][j] == opn:
                        val -= 5
                    elif board.grid[i][j] == board.grid[i+1][j+1] == pn and board.grid[i+2][j] == opn:
                        val -= 5
                    elif board.grid[i][j+1] == board.grid[i+1][j] == pn and board.grid[i+2][j] == opn:
                        val -= 5

                    if board.grid[i][j] == pn and board.grid[i+1][j] == opn and board.grid[i+2][j] == pn:
                        val -= 5
                    elif board.grid[i][j] == pn and board.grid[i][j+1] == opn and board.grid[i+2][j] == pn:
                        val -= 5
                    elif board.grid[i][j] == pn and board.grid[i+1][j+1] == opn and board.grid[i+2][j] == pn:
                        val -= 5
                    elif board.grid[i][j+1] == pn and board.grid[i+1][j] == opn and board.grid[i+2][j] == pn:
                        val -= 5

                    if board.grid[i][j] == board.grid[i+1][j] == opn and board.grid[i+2][j] == pn:
                        val += 3
                    elif board.grid[i][j] == board.grid[i][j+1] == opn and board.grid[i+2][j] == pn:
                        val += 3                    
                    elif board.grid[i][j] == board.grid[i+1][j+1] == opn and board.grid[i+2][j] == pn:
                        val += 3
                    elif board.grid[i][j+1] == board.grid[i+1][j] == opn and board.grid[i+2][j] == pn:
                        val += 3
                    
                    if board.grid[i][j] == opn and board.grid[i+1][j] == pn and board.grid[i+2][j] == opn:
                        val += 3
                    elif board.grid[i][j] == opn and board.grid[i][j+1] == pn and board.grid[i+2][j] == opn:
                        val += 3                    
                    elif board.grid[i][j] == opn and board.grid[i+1][j+1] == pn and board.grid[i+2][j] == opn:
                        val += 3
                    elif board.grid[i][j+1] == opn and board.grid[i+1][j] == pn and board.grid[i+2][j] == opn:
                        val += 3

                    if board.grid[i][j] == board.grid[i+1][j] == pn and board.grid[i+2][j] == 0:
                        val += 5
                    elif board.grid[i][j] == board.grid[i][j+1] == pn and board.grid[i+2][j] == 0:
                        val += 5
                    elif board.grid[i][j] == board.grid[i+1][j+1] == pn and board.grid[i+2][j] == 0:
                        val += 5
                    elif board.grid[i][j+1] == board.grid[i+1][j] == pn and board.grid[i+2][j] == 0:
                        val += 5

                    if board.grid[i][j] == board.grid[i+1][j] == opn and board.grid[i+2][j] == 0:
                        val -= 3
                    elif board.grid[i][j] == board.grid[i][j+1] == opn and board.grid[i+2][j] == 0:
                        val -= 3                    
                    elif board.grid[i][j] == board.grid[i+1][j+1] == opn and board.grid[i+2][j] == 0:
                        val -= 3
                    elif board.grid[i][j+1] == board.grid[i+1][j] == opn and board.grid[i+2][j] == 0:
                        val -= 3
                    
                    #no three in a row
                    if board.grid[i][j] == board.grid[i+1][j] == pn == board.grid[i+2][j]:
                        val += 3
                    elif board.grid[i][j] == board.grid[i][j+1] == pn == board.grid[i+2][j]:
                        val += 3
                    elif board.grid[i][j] == board.grid[i+1][j+1] == pn == board.grid[i+2][j]:
                        val += 3
                    elif board.grid[i][j+1] == board.grid[i+1][j] == pn == board.grid[i+2][j]:
                        val += 3

                    if board.grid[i][j] == board.grid[i+1][j] == opn == board.grid[i+2][j]:
                        val -= 3
                    elif board.grid[i][j] == board.grid[i][j+1] == opn == board.grid[i+2][j]:
                        val -= 3                    
                    elif board.grid[i][j] == board.grid[i+1][j+1] == opn == board.grid[i+2][j]:
                        val -= 3
                    elif board.grid[i][j+1] == board.grid[i+1][j] == opn == board.grid[i+2][j]:
                        val -= 3


            #if corners empty, take em
            for i in range(0,9,3):
                for j in range(0,9,3):
                    if board.grid[i][j] == opn:
                        val -= 5
                    if board.grid[i + 2][j] == opn: #and i/3 == micR and j/3 == micC:
                        val -= 5
                    if board.grid[i][j] == pn:
                        val += 3
                    if board.grid[i + 2][j] == pn:
                        val += 3

            for i in range(9):
                for j in range(9):
                    if board.grid[i][j] == pn:
                        val += 2
                    if board.grid[i][j] == opn:
                        val -= 1
            
            for i in range(1,8,3):
                for j in range(1,8,3):
                    if board.grid[i][j] == opn:
                        val -= 5
                    elif board.grid[i][j] == pn:
                        val += 5

            for i in range(3):
                for j in range(3):
                    if board.meta_grid[i][j] == pn:
                        val += 10
                    if board.meta_grid[i][j] == opn:
                        val -= 10
        if val > 100 or val < -100:
            print('val =',val)
        return (val)

    def decideMove(self):

        depth = 4
        if type(self.board).__name__ == 'TTTBoard':
            depth = 8

        count = 0
        for i in range(9):
            for j in range(9):
                try:
                    if self.board.grid[i][j] == 0:
                        count += 1
                except:
                    pass
        if count <= 76 and count > 56:
            depth = 6
        elif count <= 56 and count > 36:
            depth = 8
        elif count <= 36 and count > 10:
            depth = 10
        elif count <= 10:
            depth = 5
        print('depth is ',depth)
        boardcopy = copy.deepcopy(self.board)
        m = self.minimax(boardcopy,depth,-100,100)
        move = m[1]
        try:
            if len(move) > 1:
                filter(lambda x: x!=None, move)
        except:
            move = self.board.legalmoves()
        print('move is',move)
        move = random.choice(move)
        print('moving =', move[0],move[1])
        self.board.makeMove(move[0],move[1])
        self.mainGame.playerTurn()



    def minimax(self, board, depth, alpha, beta):
        win = board.winner()
        
        pNumber = self.playernum
        opPlayer = 3 - self.playernum

        if depth == 0 or win != 0:
            if win == pNumber:
                #print('pl win', pNumber)
                return(100 - depth, None)
            elif win == opPlayer:
                #print('op win',opPlayer)
                return(-100 + depth, None)
            elif win == 3:
                return(0, None)
            else:
                return(self.heuristic(board),None)
            
        if pNumber == board.currentPlayer():
            bestvalue = -1000
            bestmove = []
            for move in board.legalmoves():
                board.makeMove(move[0],move[1])
                v = self.minimax(board ,depth-1,alpha,beta)
                board.grid[move[0]][move[1]] = 0
                value = v[0]
                if value > bestvalue:
                    bestvalue = value
                    bestmove.append(move)
                elif value == bestvalue:
                    bestmove.append(move)
                alpha = max(alpha,bestvalue)
                if beta <= alpha:
                    break
            return (bestvalue, bestmove)

        if opPlayer == board.currentPlayer():
            worstvalue = 1000
            worstmove = []
            for move in board.legalmoves():
                board.makeMove(move[0],move[1])
                v = self.minimax(board,depth-1,alpha,beta)
                board.grid[move[0]][move[1]] = 0
                value = v[0]
                if value < worstvalue:
                    worstvalue = value
                    worstmove.append(move)
                elif value == worstvalue:
                    worstmove.append(move)
                beta = min(beta, worstvalue)
                if beta <= alpha:
                    break
            return (worstvalue, worstmove) 

