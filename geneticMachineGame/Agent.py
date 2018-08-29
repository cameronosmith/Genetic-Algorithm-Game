#class used to create each agent/genome to be acting
import Net
import Ball
import GameProperties
import random

#the maximum moves the agent is allowed to have
maxMoves = 30
#the arbitrarily high score for the agent winning a game
winFitness = 10000

class Agent:

    #the number of moves the agent has taken to prevent too many steps
    numMovesTaken = 0


    """constructor for the agent, creates its genetic properties
    @param parent1: the first agent parent, null if not a child
    @param parerent2: the second agent parent null if not a child"""
    def __init__(self, parent1=None, parent2=None):
        #the neural net and ball agent of this agent
        self.net = Net.Net(parent1, parent2)
        self.ball = Ball.Ball()
        #random identifier to identify the agent for debug
        self.identifier = random.randint(0,50)
        #true if the user won the game
        self.agentWon = False

    """method to determine the fitness of the agent"""
    def getFitness (self):
        if self.agentWon:
            return winFitness
        #fitness is the pane height - distance from goal
        return GameProperties.size[1] - self.ball.getDistanceFromGoal()

    """method to get decision of the agent
    @param inputs: the 18 input nodes to the net
    @return: the index of the highest action (0=up, left, right)"""
    def makeAction (self, inputs):
        #to keep track of inefficient paths limit moves
        self.numMovesTaken += 1 
        if self.numMovesTaken > maxMoves:
            return -1
        if self.numMovesTaken > 100:
            print("needa kill this one")
        #get the net decision and get the highest index from it
        netAction = self.net.makeAction(inputs)
        return self.net.getHighestAction(netAction)
