#file to manage the properties of the game, contains the nodes as well

#windowSize
size = (500,600)
centerX = int(size[0]/2)

#margins of main field
bottomMargin = 100
topMargin = 120


class GameProperties:

    #the nodes of the game
    ballNode = None
    playersNodes = None

    #the number of frames we've run through
    numFramesRun = 1

    """constructor for keeping track of nodes
    @param pm: the population manager for this game"""
    def __init__ (self, pm) :
        self.score = [0,0] #wins, lost
        self.popManager = pm

    """ method to set the ball node for the game 
        @param ball: the ball node """
    def setBall (self, ball):
        self.ballNode = ball

    """ method to set the list of soccer players
        @param players: the list of players to set """
    def setPlayers (self, players):
        self.playersNodes = players

