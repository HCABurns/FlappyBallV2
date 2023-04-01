#----------------- Imports ---------------#
from tkinter import Tk,Canvas,Button,Label,font
import tkinter
from PIL import Image,ImageTk
from random import randint
import math
import sys
#-----------------------------------------#

class GUI():
    """
    This class is used to deal with anything that relates to the user interface.

    __init__() - Create a window.
    hide_frames() - Remove all frames that are currently on the screen.
    setLoadiongScreen() - Set the loading screen UI.
    setGame() - Set the game UI.
    addPlayer(player) - Adds the player to the UI.
    addPipe(pipe) - Adds the pipe to the UI.
    removePipe(pipes) - Tuple of pipe objects to be removed.
    movePipe(pipe) - Moves the pipe by it's velocity.
    movePlayer(player) - Moves the player by it's velocity.
    """
    root = Tk()
    height = 768
    width=550
    def __init__(self):
        """
        This function will create a window.
        """
        self.root.title("Flappy Ball V.2")
        self.root.geometry(f"{self.width}x{self.height}")

    def hide_frames(self):
        """
        This function will remove all widgets from the window.
        """
        for widget in self.root.winfo_children():
            widget.destroy()

    def setLoadingScreen(self):
        """
        This function sets the loading screen.
        """
        self.hide_frames()
        button = Button(self.root,text="Press to start",command=lambda : startGame(True))
        button.pack()
        button = Button(self.root,text="Press to start AI match",command=lambda : startGame(False))
        button.pack()
        self.root.bind("<Escape>",end)

    def setGame(self):
        """
        This function sets the ui for the game.
        """
        self.hide_frames()
        self.canvas = Canvas(self.root, width=self.width, height=self.height)
        self.canvas.pack()
        self.bgimage=tkinter.PhotoImage(file=r'imgs/bg.png')
        self.canvas.create_image(0,0,image=self.bgimage,anchor="nw")

        font = ("Arial",18,"bold")
        self.scoreLabel = Label(self.canvas, text = "Score: ", font = font).place(x=0,y=0)
        self.score = Label(self.canvas, text = 12, font = font)
        self.score.place(x=80,y=0)

        self.root.bind("<space>",jump)
        self.root.bind("<Escape>",reset)

    def addPlayer(self,player):
        """
        This function will add the player to the screen.

        Parameters
        -------------
        player : Player
            This is the player object that will be added to the screen.
        """
        self.player = self.canvas.create_oval(player.x, player.y, player.x+player.diameter, player.y+player.diameter, fill=player.colour, outline = player.colour)
        #self.image=tkinter.PhotoImage(file=r'test')
        #self.player = self.canvas.create_image(player.x+40,player.y,image=self.image)

    def addAI(self,ai):
        """
        This function will add the AI to the screen.

        Parameters
        -------------
        ai : AI
            This is the AI object that will be added to the screen.
        """
        self.ai = self.canvas.create_oval(ai.x, ai.y, ai.x+ai.diameter, ai.y+ai.diameter, fill=ai.colour, outline = ai.colour)

        
    def addPipe(self,pipe):
        """
        This function will add the pipes to the screen.

        Parameters
        -------------
        pipe : Pipe
            This is the pipe object that will be added to the screen.
        """
        if pipe.id == 0:
            self.pipe = self.canvas.create_rectangle(pipe.x,pipe.y,pipe.x+pipe.width,pipe.gapStart,fill=pipe.colour)
            return self.pipe
        else:
            self.pipe2 = self.canvas.create_rectangle(pipe.x,pipe.gapStart+pipe.gapSize,pipe.x+pipe.width,self.height,fill=pipe.colour)
            return self.pipe2
    
    def removePipe(self,pipe):
        """
        Removes the pipe from the screen.

        Parameters
        -------------
        pipe : Tuple(Pipe,Pipe)
            Tuple of pipe objects to be removed.
        """
        self.canvas.delete(pipe[0])
        self.canvas.delete(pipe[1])

    def movePlayer(self,player):
        """
        This function will move the player on the UI based on it's velocity.

        Parameters
        -------------
        player : Player
            This is the player object that will be moved.
        """
        self.canvas.move(self.player, 0,player.velocity)
        

    def moveAI(self,ai):
        """
        This function will move the AI on the UI based on it's velocity.

        Parameters
        -------------
        ai : AI
            This is the ai object that will be moved.
        """
        self.canvas.move(self.ai, 0,ai.velocity)

    
    def movePipe(self,pipe):
        """
        This function will move the pipe on the UI based on it's velocity.

        Parameters
        -------------
        pipe : Pipe
            This is the pipe object that will be moved.
        """
        self.canvas.move(pipe, Pipe.velocity*-1,0)


    def incrementScore(self):
        """
        This function will increment the score of the player.
        """
        self.score.config(text = int(self.score.cget("text"))+1)


def startGame(singleplayer):
    """
    This function will start the game.

    Parameters
    ---------------
    singleplayer : booolean
        True or false if it's singleplayer or not.
    """
    game.setGame(singleplayer)

def jump(event):
    """
    This function is called whenever the player wishes to jump.

    Paramters
    -------------
    event : tkinterEvent
        This is required however not used.
    """
    game.player.jump()

def reset(Event):
    """
    This will restart the game.

    Paramters
    -------------
    event : tkinterEvent
        This is required however not used.
    """
    game.running = False
    game.gui.setLoadingScreen()

def end(Event):
    """
    This function will end the game.

    Paramters
    -------------
    event : tkinterEvent
        This is required however not used.
    """
    game.gui.end = True
    game.gui.root.destroy()

class Game():
    """
    This function deals with everything related to the game.

    _init__() - Saves a variable of the GUI for calling changes to the UI.
    loadingScren() - Return to the loading screen.
    setGame() - Set the game up.
    addNewPipe() - Add a new pipe object.
    collisionDetection(player,pipes) - Check if the player has collided with a pipe.
    checkScore(player,pipes) - Check if the score needs to be updated.
    singleplayer_Gameloop() - Run the gameloop. (What plays the game)
    """
    running=False
    gravity = 2
    def __init__(self):
        """
        Saves a variable of the GUI for calling changes to the UI.
        """
        self.gui = GUI()


    def loadingScreen(self):
        """
        This function will return to the loading screen.
        """
        self.gui.setLoadingScreen()
 
    def setGame(self,singleplayer):
        """
        This function sets the game up.

        Parameters
        --------------
        singleplayer : boolean
            True or False if it's a singleplayer game or not
        """
        #Set game UI
        self.gui.setGame()
        #Add player
        self.player = Player()
        self.gui.addPlayer(self.player)
        #Add pipe
        self.pipes = []
        self.pipeObjects = []
        self.addNewPipe()
        #Start the game
        self.running=True
        if singleplayer:
            self.singleplayer_Gameloop()
        else:
            self.ai = AI()
            self.gui.addAI(self.ai)
            self.ai_gameloop()

    def addNewPipe(self):
        """
        This function will add a new pipe to the game.
        """
        pipe1 = Pipe(0)
        pipe2 = Pipe(1,pipe1.gapStart)
        self.pipes.append((pipe1,pipe2))
        pipe1 = self.gui.addPipe(pipe1)
        pipe2 = self.gui.addPipe(pipe2)
        self.pipeObjects.append((pipe1,pipe2))


    def collisionDetection(self, player, pipes):
        """
        This function will check if the player has collided with a pipe.

        Parameters
        -------------
        player : Player
            This is the player object to check if they have collided or not.
        pipes : List
            This is a list of tuples containing all the pipes on the screen.
        """
        topPipe = pipes[0]
        playerX = player.x+(player.diameter/2)
        playerY = player.y+(player.diameter/2)

        #Used for determining centre of the player. (Big fixing)
        #self.gui.canvas.create_oval(playerX, playerY, playerX+2, playerY+2, fill="gold", outline = "gold")

        #Top left bar
        if player.x+player.diameter > topPipe.x and player.y+player.diameter<topPipe.y2:
            return True
        
        #Top left corner
        elif abs(math.sqrt((playerX-topPipe.x)**2 + (playerY-topPipe.y2)**2)) < player.diameter/2:
            print(playerX,topPipe.x, playerY,topPipe.gapStart)
            return True

        #Top Right corner
        elif abs(math.sqrt((playerX-(topPipe.x+topPipe.width))**2 + (playerY-topPipe.y2)**2)) < player.diameter/2:
            return True

        #Top middle
        elif playerX>topPipe.x and playerX<topPipe.x+topPipe.width and player.y < topPipe.y2:
            return True

        #Bottom left corner
        elif abs(math.sqrt((playerX-topPipe.x)**2 + (playerY-topPipe.y3)**2)) < player.diameter/2:
            return True

        #Bottom Right corner
        elif abs(math.sqrt((playerX-(topPipe.x+topPipe.width))**2 + (playerY-topPipe.y3)**2)) < player.diameter/2:
            return True

        #Bottom middle
        elif playerX>topPipe.x and playerX<topPipe.x+topPipe.width and player.y+player.diameter > topPipe.y3:
            return True

        #Bottom left bar
        elif player.x+player.diameter > topPipe.x and player.y+player.diameter>topPipe.y3:
            return True
        #No collision occured.
        else:
            return False 


    def checkScore(self,player,pipes):
        """
        This function will check if the score needs to be incremented or not.
        This function will also increment the score if needed.

        Parameters
        -------------
        player: Player
            This is the player object that is being checked for a score.
        pipe : Tuple(Pipe,Pipe)
            Tuple of pipe object to be used to check against.
        """
        if player.x > pipes[0].x+pipes[0].width and pipes[0].score == 1:
            self.gui.incrementScore()
            pipes[0].score = 0
            pipes[1].score = 0
        
    
    def singleplayer_Gameloop(self):
        """
        This function will run the game loop. It runs the collision detection, moving of objects and score.
        """
        if self.running==True:
            #Collision Detection
            if self.player.x<self.pipes[0][0].x+self.pipes[0][0].width:
                collision = self.collisionDetection(self.player,self.pipes[0])
            else:
                collision = self.collisionDetection(self.player,self.pipes[1])
            if collision:
                sys.exit()
                return False

            #Check for score increment
            self.checkScore(self.player,self.pipes[0])
            
            #Move player
            self.player.move()
            self.gui.movePlayer(self.player)

            #Move pipe
            for topPipe,bottomPipe in self.pipes:
                topPipe.move()
                bottomPipe.move()
            #Check for removal of pipes
            if self.pipes[-1][0].x < GUI.width - Pipe.width*3:
                self.addNewPipe()
            if self.pipes[0][0].x < -Pipe.width:
                self.pipes.pop(0)
                self.gui.removePipe(self.pipeObjects.pop(0))
            #Move pipes on the screen
            for topPipe,bottomPipe in self.pipeObjects:
                self.gui.movePipe(topPipe)
                self.gui.movePipe(bottomPipe)

            #Run game loop
            self.gui.root.after(28,self.singleplayer_Gameloop)   #28

    def ai_gameloop(self):
        """
        This function will run the ai game loop. It runs the collision detection, moving of objects and score.
        """
        players = (self.player,self.ai)
        if self.running==True:
            #Collision Detection for AI and players
            for player in players:
                if player.x<self.pipes[0][0].x+self.pipes[0][0].width:
                    collision = self.collisionDetection(player,self.pipes[0])
                else:
                    collision = self.collisionDetection(player,self.pipes[1])
                if collision:
                    sys.exit()
                    return False

            #Check for score increment
            self.checkScore(self.player,self.pipes[0])
            
            #Move players
            self.player.move()
            self.gui.movePlayer(self.player)
            if self.player.x<self.pipes[0][0].x+self.pipes[0][0].width:
                self.ai.move(self.pipes[0])
            else:
                self.ai.move(self.pipes[1])
            self.gui.moveAI(self.ai)

            #Move pipe
            for topPipe,bottomPipe in self.pipes:
                topPipe.move()
                bottomPipe.move()
            #Check for removal of pipes
            if self.pipes[-1][0].x < GUI.width - Pipe.width*4:
                self.addNewPipe()
            if self.pipes[0][0].x < -Pipe.width:
                self.pipes.pop(0)
                self.gui.removePipe(self.pipeObjects.pop(0))
            #Move pipes on the screen
            for topPipe,bottomPipe in self.pipeObjects:
                self.gui.movePipe(topPipe)
                self.gui.movePipe(bottomPipe)

            #Run game loop
            self.gui.root.after(28,self.ai_gameloop)   #28
            

class Pipe():
    """
    This class deals with all the required information of the pipes.
    """
    width = 60
    velocity = 3
    gapSize = 250
    colour="Lime"
    def __init__(self,id,gapStart=None):
        """
        Creates a new pipe object.
        id : int
            An ID that references if the pipe is a top pipe or bottom pipe. 0:Top, 1:Bottom.
        """
        self.score = 1
        self.x = GUI.width
        self.y = 0
        if gapStart is None:
            self.gapStart = randint(200,GUI.height-200)
        else:
            self.gapStart = gapStart
        self.y2 = self.gapStart
        self.y3 = self.gapStart+Pipe.gapSize
        self.y4 = GUI.height
        self.id = id #ID being 1 or 0 referring to if it is the top or bottom pipe for collision detection requirement

    def move(self):
        """
        This function moves the pipe based on its velocity.
        """
        self.x -= self.velocity


class Player():
    """
    This is the player class to deal with anything related to the player.
    """
    def __init__(self):
        """
        This function defines all of the required paramters of a player.
        """
        self.diameter = 50
        self.x = 40
        self.jumpHeight = 20
        self.maxSpeed = self.jumpHeight
        self.y = int(GUI.height//2 - self.diameter//2)
        self.velocity = 0
        self.colour="Black"

    def move(self):
        """
        This function will move the player based on their position and if they are at the max speed or not.
        """
        if self.y < 0: #Hit the floor so jump
            self.jumpHeight//4
        elif self.y+self.diameter > GUI.height:#Hit the roof so reverse the velocity and take away some for the bounce
            self.jump()
        #Carry out the normal move
        if self.velocity<self.maxSpeed:
            self.velocity += Game.gravity
        self.y += self.velocity

    def jump(self):
        """
        This function is executed when the player wantes to jump.
        """
        self.velocity = -self.jumpHeight


#Make an AI that can move on its own
class AI(Player):
    """
    This class is a subclass of the Player class and deals with the AI player.
    """
    def __init__(self):
        super().__init__()
        self.colour="Gold"
    
    def move(self,pipe):
        """
        This function will move the AI based on rules.

        Paramters
        -------------
        pipe : Tuple
            Tuple object of the next pipe to be jumping through.
        """
        topPipe = pipe[0]
        bottomPipe = pipe[1]
        if self.y+self.diameter+25 > bottomPipe.y3:
            super().jump()
        super().move()
        #print(f"AI Moving {self.x}{self.y}")



if __name__ == "__main__":
    game=Game()
    game.loadingScreen()
    game.gui.root.mainloop()
    #print(Pipe.__init__.__doc__)
