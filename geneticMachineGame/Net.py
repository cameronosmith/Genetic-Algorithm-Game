#file to create a neural net for the agent. no learning, just random weights
import numpy
from collections import deque #many pops so more efficient
import random

#the properties of the neural net
numInputNodes = 18 #three categories for six sensors
numHiddenNodes = 10
numOutputNodes = 3 #in order of up left right
activationFunction = lambda x: 1.0/(1.0 + numpy.exp(-x)) #to limit output od nodes
formatInputs = lambda inputs: numpy.array(inputs, ndmin=2).T #to format the inputs as an array

class Net:

    """constructor for the neural net
    @param parent1: the first agent used to create this child or None if not a child
    @param parent2: the second agent used to create this child or None if not a child"""
    def __init__ (self, parent1=None, parent2=None):

        #random net identifier to check which net being used for debug
        self.randomIdentifier = random.randint(0,50)

        #the weights of the net
        #create the weights for the input to hidden w normalized random values
        self.wih = numpy.random.normal(0.0, pow(numInputNodes,-0.5), \
                (numHiddenNodes, numInputNodes))
        #same for hidden to output
        self.who = numpy.random.normal(0.0, pow(numHiddenNodes,-0.5), \
                (numOutputNodes, numHiddenNodes))
        #repopulate the random array with parent crossover values if available
        if parent1 is not None and parent2 is not None:
            global wih, who
            self.createWeights(self.wih, parent1.net.wih, parent2.net.wih)
            self.createWeights(self.who, parent1.net.who, parent2.net.who)

    """method to populate a weight array
    the weight array should already be populated with random vals and init. w size
    @param weightArr: the array to populate
    @param parentWeight1: the first weight array to draw values from
    @param parentWeight2: the second weight array to draw values from
    @return: the weights array"""
    def createWeights (self, weightArr, parentWeight1, parentWeight2):
        #iterate through rows and columns (every weight) to 
        for weightRow in range(len(weightArr)):
            for weightColumn in range(len(weightArr[weightRow])):
                #random mutation possibility to leave as random already initialized
                if numpy.random.randint(100) < 5:
                    continue
                #the parent we are using for this node
                parentUsed = parentWeight1 if numpy.random.randint(100) <= 50 else parentWeight2
                #populate index with random choice in using parent1 or 2 for val
                weightArr[weightRow][weightColumn] = parentUsed[weightRow][weightColumn]

    """"method to get the net's best action from the weights
    @param input: the 22 input nodes in a vector of inputs
    @return: list of probabilities for output nodes up, left, right"""
    def makeAction (self, inputs):
        #format inputs
        inputs = formatInputs(inputs)
        #get hidden nodes
        hiddenNodesPreActivation = numpy.dot(self.wih, inputs)
        hiddenNodes = activationFunction(hiddenNodesPreActivation)
        #final outoput node
        finalNodePreActivation = numpy.dot (self.who, hiddenNodes)
        finalOutput = activationFunction(finalNodePreActivation)
        #give back probability of us moving up left or right
        return finalOutput

    """helper method to get the highest of the actions 
    @param output: the output from the action
    @return: the index of the highest probability"""
    def getHighestAction (self, output):
        greatestIndex = 0 #the index with the highest probability
        if output[1] > output[greatestIndex]:
            greatestIndex = 1
        if output[2] > output[greatestIndex]:
            greatestIndex = 2
        return greatestIndex
