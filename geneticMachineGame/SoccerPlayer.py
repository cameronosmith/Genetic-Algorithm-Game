import pygame
import GameProperties

#properties of the team
teamFormation = [3,4,4]
#true if want to print the player debug
debug = False
#the name of a soccer player node
nodeName = "soccerPlayer"


class SoccerPlayer:
    #define the properties of a player
    playerColor = (255,0,0) #red
    playerWidth = 30
    playerHeight = 40
    
    """player constructor
    @param point: the point to draw the player at"""
    def __init__(self, point):
        self.position = point
        self.originalPosition = point #to keep track of where to return to
        self.nodeName = nodeName
    """method to get the rect of this player
    @return: the rect (x,y,w,h)"""
    def getRect (self):
        return [self.position[0], self.position[1], self.playerWidth, self.playerHeight]

    """method to draw the player
    @param display: the display to draw on"""
    def draw (self, display):
        pygame.draw.rect(display, self.playerColor, self.getRect() )

    """method to check for collisions between this player and the ball
    @param ball: the ball to check for collision
    @param radius: the radius of the ball
    @return: true if a collision"""
    def collidesWithBall (self, ball, radius):
        centerOfRect = (self.getRect()[0]+self.playerWidth/2,\
                self.getRect()[1]+self.playerHeight/2)
        dx = max(abs(ball.position[0] - centerOfRect[0]) - self.playerWidth / 2, 0);
        dy = max(abs(ball.position[1] - centerOfRect[1]) - self.playerHeight / 2, 0);
        return (dx**2 + dy**2) < radius**2

"""method to draw the whole team
@param display: the display to draw on
@return: the list of soccer players drawn"""
def drawTeam (display):
    ##testing draw the margins
    #pygame.draw.rect(display, (0,0,255), [0,0,GameProperties.size[0],GameProperties.topMargin])
    #pygame.draw.rect(display, (0,0,255), [0,GameProperties.size[1]-GameProperties.bottomMargin,GameProperties.size[0],GameProperties.bottomMargin])
    if (debug):
        print("drawing team")
    gameSize = GameProperties.size #for easier reference
    #the list of soccer players
    players = []
    #the dimensions of the field
    fieldHeight = gameSize[1] - GameProperties.bottomMargin - GameProperties.topMargin
    fieldWidth = gameSize[0]

    #vSpaceAlloted is the vertical spacing alloted for each row
    vSpaceAlloted = fieldHeight / len(teamFormation)

    # iterate through the formation to get node positions
    for fIndex, rowSize in enumerate(teamFormation):
        if (debug):
            print("fInex is",fIndex)
            print("row size is",rowSize)
        #skip if no players in the row
        if (rowSize is 0):
            continue
        #yPos is the y position for each player in the row 
        yPos = vSpaceAlloted*(fIndex) + GameProperties.topMargin
        #hSpaceAlloted is the horizontal space alloted for each player in the row
        hSpaceAlloted = fieldWidth / rowSize
        if (debug):
            print("h space alloted is ",hSpaceAlloted)
        # iterate through row to get x positions of indiv. players 
        for rIndex in range (1, rowSize+1):
            if (debug):
                print("rindex is",rIndex)
            #xPos is the x position of the player
            xPos = hSpaceAlloted * (rIndex) - hSpaceAlloted/2- SoccerPlayer.playerWidth/2 
            # create and add the player to the scene 
            sp = SoccerPlayer((xPos,yPos))
            sp.draw(display)
            players.append(sp)
            if (debug):
                print("adding player at: ",xPos,yPos)
    return players
