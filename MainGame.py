import TTTBoard
import RTTTBoard
import tkinter
from PlayerTypes import *
import pygame
import time


class GameCentral():

    def __init__(self):
        music = 'assets/music.mp3'
        #os.system('Windows Media Player' + file)

        pygame.mixer.init()
        pygame.mixer.music.load(music)
        pygame.mixer.music.play()

        self.root = tkinter.Tk()
        self.root.title("Welcome to Game Central")
        
        self.st = tkinter.PhotoImage(file = 'assets/bridge.png')
        
        self.canvas = tkinter.Canvas(self.root,height=800,width=1400)
        self.canvas.pack()
        self.gameboard = None
        self.startscreen = {}
        self.startscreen['gameType'] = None
        self.startscreen['P1'] = None
        self.startscreen['P2'] = None
        self.startscreen['ready'] = False
        self.player1 = None
        self.player2 = None
        self.drawStartScreen()
        self.canvas.mainloop()

    ''' Each screen function is responsible for drawing the screen and setting
    up  the appropriate bindings 

    Note: This is fairly messy GUI coding. A better way could have been to define a
    "Button" class, and use that Button class.
    '''
    def drawStartScreen(self):
        print(self.startscreen['ready'])
        #Delete anything else on the screen
        self.canvas.delete('all')
        self.canvas.create_image(700, 400, image = self.st)
        if self.startscreen['gameType'] and self.startscreen['P1'] and self.startscreen['P2']:
            self.startscreen['ready'] = True
        #Draw the screen
        print('image')
        self.canvas.create_text(700,100, font =('Bold',20), text='Welcome to Game Central')
        
        
        #Game Choice
        if self.startscreen['gameType'] == 'TTT':
            self.canvas.create_rectangle(400,200,600,300, fill='yellow')
        else:
            self.canvas.create_rectangle(400,200,600,300,fill = 'white', stipple = 'gray75')
        self.canvas.create_text(500,250, font =('Bold',18),text='Play TicTacToe')
        if self.startscreen['gameType'] == 'RTTT':
            self.canvas.create_rectangle(800,200,1000,300,fill='yellow')
        else:
            self.canvas.create_rectangle(800,200,1000,300, fill = 'white', stipple = 'gray75')
        self.canvas.create_text(900,250,font =('Bold',18), text='Play Recursive \n TicTacToe')

        #Player 1
        self.canvas.create_text(700,325,font =('Bold',20), text='Choose Player 1', fill = 'blue')
        if self.startscreen['P1'] == 'Human':
            self.canvas.create_rectangle(400,350,600,450, fill='yellow')
        else:
            self.canvas.create_rectangle(400,350,600,450, fill = 'white', stipple = 'gray75')
        self.canvas.create_text(500,400,font =('Bold',16), text='Human')
        if self.startscreen['P1'] == 'Random':
            self.canvas.create_rectangle(600,350,800,450, fill='yellow')
        else:
            self.canvas.create_rectangle(600,350,800,450, fill = 'white', stipple = 'gray75')
        self.canvas.create_text(700,400, font =('Bold',16), text='Random')
        if self.startscreen['P1'] == 'AI':
            self.canvas.create_rectangle(800,350,1000,450, fill='yellow')
        else:
            self.canvas.create_rectangle(800,350,1000,450, fill = 'white', stipple = 'gray75')
        self.canvas.create_text(900,400,font =('Bold',16),text='AI')


        self.canvas.create_text(700,475, font =('Bold',20), text='Choose Player 2', fill = 'blue')
        if self.startscreen['P2'] == 'Human':
            self.canvas.create_rectangle(400,500,600,600, fill='yellow')
        else:
            self.canvas.create_rectangle(400,500,600,600, fill = 'white', stipple = 'gray75')
        self.canvas.create_text(500,550, font =('Bold',16), text='Human')
        if self.startscreen['P2'] == 'Random':
            self.canvas.create_rectangle(600,500,800,600, fill='yellow')
        else:
            self.canvas.create_rectangle(600,500,800,600, fill = 'white', stipple = 'gray75')
        self.canvas.create_text(700,550, font =('Bold',16), text='Random')
        if self.startscreen['P2'] == 'AI':
            self.canvas.create_rectangle(800,500,1000,600, fill='yellow')
        else:
            self.canvas.create_rectangle(800,500,1000,600, fill = 'white', stipple = 'gray75')
        self.canvas.create_text(900,550, font =('Bold',16), text='AI')


        #Start Button
        if self.startscreen['ready']:
            self.canvas.create_rectangle(600,650,800,750,fill='green')
        else:
            self.canvas.create_rectangle(600,650,800,750,fill='red')
        self.canvas.create_text(700,700, font =('Bold',20), text='Start!')


        #Bind the mouse button
        self.canvas.bind("<Button-1>",self.startScreenClick)

    def startScreenClick(self,event):
        print("Start Screen was clicked")
        if 400 <= event.x <= 600 and 200 <= event.y <= 300 :
            self.startscreen['gameType'] = 'TTT'
            self.drawStartScreen()
        elif 800 <= event.x <= 1000 and 200 <= event.y <= 300 :
            self.startscreen['gameType'] = 'RTTT'
            self.drawStartScreen()
        elif 400 <= event.x <= 600 and 350 <= event.y <= 450 :
            self.startscreen['P1'] = 'Human'
            self.drawStartScreen()
        elif 600 <= event.x <= 800 and 350 <= event.y <= 450 :
            self.startscreen['P1'] = 'Random'
            self.drawStartScreen()
        elif 800 <= event.x <= 1000 and 350 <= event.y <= 450 :
            self.startscreen['P1'] = 'AI'
            self.drawStartScreen()
        elif 400 <= event.x <= 600 and 500 <= event.y <= 600 :
            self.startscreen['P2'] = 'Human'
            self.drawStartScreen()
        elif 600 <= event.x <= 800 and 500 <= event.y <= 600 :
            self.startscreen['P2'] = 'Random'
            self.drawStartScreen()
        elif 800 <= event.x <= 1000 and 500 <= event.y <= 600 :
            self.startscreen['P2'] = 'AI'
            self.drawStartScreen()

        elif 600 <= event.x <= 800 and 650 <= event.y <= 750 and self.startscreen['ready']:
            print('GameTime!')
            if self.startscreen['gameType'] == 'TTT':
                self.gameboard = TTTBoard.TTTBoard(self.canvas)
            else:
                self.gameboard = RTTTBoard.RTTTBoard(self.canvas)

            if self.startscreen['P1'] == 'Human':
                self.player1 = HumanPlayer(self,self.gameboard,self.canvas)
            elif self.startscreen['P1'] == 'Random':
                self.player1 = RandomPlayer(self,self.gameboard)
            else:
                self.player1 = AIPlayer(self,1,self.gameboard)

            if self.startscreen['P2'] == 'Human':
                self.player2 = HumanPlayer(self,self.gameboard,self.canvas)
            elif self.startscreen['P2'] == 'Random':
                self.player2 = RandomPlayer(self,self.gameboard)
            else:
                self.player2 = AIPlayer(self,2,self.gameboard)

            self.playerTurn()

    def playerTurn(self):
        winner = self.gameboard.winner()
        if winner != 0:
            self.drawEndScreen(winner)
            return
        #Delete anything else on the screen
        self.canvas.delete('all')
        #Draw the game screen
        self.gameboard.drawBoard()
        #Draw a prompt for the player
        self.canvas.create_text(700,700, font =('Bold',18), text=("Player " + str(self.gameboard.currentPlayer())+ "'s turn!"))
        #Bind the mouse button
        if self.gameboard.currentPlayer() == 1:
            curplayer = self.player1
        else:
            curplayer = self.player2
        curplayer.decideMove()
        #self.canvas.bind("<Button-1>",self.gameClick)

    def drawEndScreen(self,winner):
        self.canvas.delete('all')
        #Draw the final game screen
        self.gameboard.drawBoard()
        if winner != 3:
            self.canvas.create_text(700,700, font =('Bold',18), text=('Player '+str(winner)+' wins!'))
        else:
            self.canvas.create_text(700,700, font =('Bold',18), text=('It was a draw!'))
        self.canvas.create_rectangle(400,650,600,750, fill = 'white', stipple = 'gray75')
        self.canvas.create_text(500,700, font =('Bold',18), text='Play Again')
        self.canvas.create_rectangle(800,650,1000,750, fill = 'white', stipple = 'gray75')
        self.canvas.create_text(900,700, font =('Bold',18), text='Quit')
        self.canvas.bind("<Button-1>",self.endClick)
        
    def endClick(self,event):
        if 400 <= event.x <= 700 and 650 <= event.y <= 750 :
            self.startscreen['gameType'] = None
            self.startscreen['P1'] = None
            self.startscreen['P2'] = None
            self.startscreen['ready'] = False
            self.drawStartScreen()
        elif 800 <= event.x <= 1000 and 650 <= event.y <= 750 :
            #This ends the mainloop call, and the game.
            self.root.quit()


# The main function is much simpler in an event-driven programming setup
def main():
    m = GameCentral()


if __name__ == "__main__":
    main()
