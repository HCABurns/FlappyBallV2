from tkinter import Tk,Canvas,Button
import tkinter
from PIL import Image,ImageTk
from random import randint
import math
import sys

class GUI():
    root = Tk()
    height = 768
    width=550
    def __init__(self):
        self.root.title("Flappy Ball V.2")
        self.root.geometry(f"{self.width}x{self.height}")

    def hide_frames(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def setLoadingScreen(self):
        self.hide_frames()
        button = Button(self.root,text="Press to start",command=startGame)
        button.pack()
        self.root.bind("<Escape>",end)

    def setGame(self):
        self.hide_frames()
        self.canvas = Canvas(self.root, width=self.width, height=self.height)
        self.canvas.pack()
        self.bgimage=tkinter.PhotoImage(file=r'imgs/bg.png')
        self.canvas.create_image(0,0,image=self.bgimage,anchor="nw")

        self.root.bind("<space>",jump)
        self.root.bind("<Escape>",reset)

    def addPlayer(self,player):
        self.player = self.canvas.create_oval(player.x, player.y, player.x+player.diameter, player.y+player.diameter, fill=player.colour, outline = player.colour)
        self.canvas.create_oval(0, 0, 0+player.diameter, 0+player.diameter, fill=player.colour, outline = player.colour)
        #self.image=tkinter.PhotoImage(file=r'test')
        #self.player = self.canvas.create_image(player.x+40,player.y,image=self.image)

    def addPipe(self,pipe):
        #self.pipes = []
        if pipe.id == 0:
            self.pipe = self.canvas.create_rectangle(pipe.x,pipe.y,pipe.x+pipe.width,pipe.gapStart,fill=pipe.colour)
            print(pipe.x,pipe.y,pipe.x+pipe.width,pipe.gapStart)
            return self.pipe
        else:
            self.pipe2 = self.canvas.create_rectangle(pipe.x,pipe.gapStart+pipe.gapSize,pipe.x+pipe.width,self.height,fill=pipe.colour)
            return self.pipe2
    
    def removePipe(self,pipe):
        """
        Removes the pipe from the screen.
        :param pipe: Tuple of the pipe in the form (topPipe,bottomPipe) 
        """
        self.canvas.delete(pipe[0])
        self.canvas.delete(pipe[1])

    def movePlayer(self,player):
        self.canvas.move(self.player, 0,player.velocity)
    
    def movePipe(self,pipe):
        self.canvas.move(pipe, Pipe.velocity*-1,0)



def startGame():
    game.setGame()

def jump(Event):
    game.player.jump()

def reset(Event):
    game.running = False
    game.gui.setLoadingScreen()

def end(Event):
    game.gui.end = True
    game.gui.root.destroy()

class Game():
    running=False
    gravity = 2
    def __init__(self):
        self.gui = GUI()

    def getGravity():
        return Game.gravity

    def loadingScreen(self):
        self.gui.setLoadingScreen()
        #print("yo")
 
    def setGame(self):
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
        self.singleplayer_Gameloop()

    def addNewPipe(self):
        pipe1 = Pipe(0)
        pipe2 = Pipe(1)
        print(len(self.pipes))
        self.pipes.append((pipe1,pipe2))
        pipe1 = self.gui.addPipe(pipe1)
        pipe2 = self.gui.addPipe(pipe2)
        self.pipeObjects.append((pipe1,pipe2))


    def collisionDetection(self, player, pipes):
        topPipe = pipes[0]
        playerX = player.x+(player.diameter/2)
        playerY = player.y+(player.diameter/2)

        self.gui.canvas.create_oval(playerX, playerY, playerX+2, playerY+2, fill="gold", outline = "gold")
        if topPipe.x < 120:
            print(abs(math.sqrt((playerX-(topPipe.x+topPipe.width))**2 + (playerY-topPipe.y2)**2)))
        #Top left bar
        if player.x+player.diameter > topPipe.x and player.y+player.diameter<topPipe.y2:
            print("SIDE WALL")
            return True
        
        #Top left corner
        elif abs(math.sqrt((playerX-topPipe.x)**2 + (playerY-topPipe.y2)**2)) < player.diameter/2:
            print(playerX,topPipe.x, playerY,topPipe.gapStart)
            print("top left")
            return True

        #Top Right corner
        elif abs(math.sqrt((playerX-(topPipe.x+topPipe.width))**2 + (playerY-topPipe.y2)**2)) < player.diameter/2:
            print("top right")
            return True

        #Top middle
        elif playerX>topPipe.x and playerX<topPipe.x+topPipe.width and player.y < topPipe.y2:
            print("top middle")
            return True

        #Bottom left corner
        elif abs(math.sqrt((playerX-topPipe.x)**2 + (playerY-topPipe.y3)**2)) < player.diameter/2:
            print("bot left")
            return True

        #Bottom Right corner
        elif abs(math.sqrt((playerX-(topPipe.x+topPipe.width))**2 + (playerY-topPipe.y3)**2)) < player.diameter/2:
            print("bot right")
            return True

        #Bottom middle
        elif playerX>topPipe.x and playerX<topPipe.x+topPipe.width and player.y+player.diameter > topPipe.y3:
            print("top middle")
            return True

        #Bottom left bar
        elif player.x+player.diameter > topPipe.x and player.y+player.diameter>topPipe.y3:
            print("left bar")
            return True
        #No collision occured.
        else:
            return False
        
        
    
    def singleplayer_Gameloop(self):
        if self.running==True:
            #Collision Detection
            if self.player.x<self.pipes[0][0].x+self.pipes[0][0].width:
                collision = self.collisionDetection(self.player,self.pipes[0])
            else:
                collision = self.collisionDetection(self.player,self.pipes[1])
            if collision:
                sys.exit()
                return False
            
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

class Player():
    def __init__(self):
        self.diameter = 50
        self.x = 40
        self.jumpHeight = 20
        self.maxSpeed = self.jumpHeight
        self.y = int(GUI.height//2 - self.diameter//2)
        self.velocity = 0
        self.colour="Black"

    def move(self):
        if self.y < 0: #Hit the floor so jump
            self.jumpHeight//4
        elif self.y+self.diameter > GUI.height:#Hit the roof so reverse the velocity and take away some for the bounce
            self.jump()
        #Carry out the normal move
        if self.velocity<self.maxSpeed:
            self.velocity += Game.gravity
        self.y += self.velocity

    def jump(self):
        print("jump")
        self.velocity = -self.jumpHeight


class Pipe():
    width = 60
    velocity = 3
    gapSize = 250
    colour="Lime"
    def __init__(self,id):
        """
        Creates a new pipe object.
        :param id: An ID that references if the pipe is a top pipe or bottom pipe. 0:Top, 1:Bottom.
        :retrun: None
        """
        self.x = GUI.width
        self.y = 0
        self.gapStart = 400#randint(300,GUI.height-300)
        self.y2 = self.gapStart
        self.y3 = self.gapStart+Pipe.gapSize
        self.y4 = GUI.height
        self.id = id #ID being 1 or 0 referring to if it is the top or bottom pipe for collision detection requirement

    def move(self):
        self.x -= self.velocity


#Make an AI that can move on its own
class AIPlayer(Player):
    def __init__(self):
        super.__init__()
        self.color="Black"
    
    def move(self):
        print(f"AI Moving {self.x}{self.y}")



if __name__ == "__main__":
    game=Game()
    game.loadingScreen()
    game.gui.root.mainloop()
    #print(Pipe.__init__.__doc__)
