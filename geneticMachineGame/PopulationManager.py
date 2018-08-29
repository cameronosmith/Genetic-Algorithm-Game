#file used to manage the populations and create new children
from Agent import Agent
import random

#the properties of the population
populationSize = 10

class PopulationManager:

    #the number of generations we created
    numGenerations = 0

    #the current population
    currentPopulation = []

    #the current individual index we are using as the main agent
    currentAgentIndex = 0

    """constructor: creates the initial population"""
    def __init__(self):
        self.createPopulation(None, None)

    """"method to create a population
    @param parent1: the first net parent
    @param parent2: the second net parent
    leave parents none if first generation"""
    def createPopulation (self, parent1, parent2):
        #create the population size number of members
        for _ in range(populationSize):
            self.currentPopulation.append (Agent(parent1, parent2))
        #set needed population properties
        self.currentAgentIndex = 0
        self.numGenerations += 1
        #debug
        print("~~~~~~~~~~~~~~~~~~~~~~~~")
        print("creating new generation: generation %d", self.numGenerations) 
        print("~~~~~~~~~~~~~~~~~~~~~~~~")

    """method to get a random agent with higher probability to higher fitnesses
    @return: the agent to use """
    def getProbabilisticAgent (self):
        #get the sum of all the fitnesses
        totalFitnessSum = 0
        for agent in self.currentPopulation:
            totalFitnessSum += agent.getFitness()
        #generated number between 0 and 1
        randomProb = random.random()
        #loop agents, minus their prob from random, stop where prob less than next
        for agent in self.currentPopulation:
            #the fitness percentage of all the fitnesses
            fitnessShare = agent.getFitness()/totalFitnessSum
            #check if we should use this or continue to next agent
            if randomProb < fitnessShare:
                return agent
            else:
                randomProb -= fitnessShare

    """method to kill the population and repopulate with a new one"""
    def restartPopulation (self):
        #the parents to generate the next population with
        parent1 = self.getProbabilisticAgent()
        parent2 = self.getProbabilisticAgent()
        #restart and create the individual
        self.currentPopulation = []
        self.createPopulation (parent1, parent2)
        #debug
        print("first parent score was %d", parent1.getFitness())
        print("second parent score was %d", parent2.getFitness())

    """method to move to the next agnet since the current one won/lost
    @param gp: the game prop object to change the ball node on screen"""
    def advanceAgent(self, gp):
        print("advancing agent") #debug
        print("end agent fitness was ", \
                self.currentPopulation[self.currentAgentIndex].getFitness()) #debug
        #advance agent used and check if done with population
        self.currentAgentIndex += 1
        if self.currentAgentIndex == populationSize:
            self.restartPopulation()
        #change the main agent on screen
        gp.setBall (self.currentPopulation[self.currentAgentIndex].ball)
    
    """method to get the current agent
    @return: the current agent"""
    def getCurrentAgent(self):
        return self.currentPopulation[self.currentAgentIndex]
