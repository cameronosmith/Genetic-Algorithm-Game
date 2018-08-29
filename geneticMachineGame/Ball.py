import pygame
import GameProperties, Goal
import math
import LineIntersection as line

#the name of the ball node
nodeName = "ball"
#the radius of the ball
radius = 15
#the starting position of the ball
startPosition = (GameProperties.centerX, GameProperties.size[1]-GameProperties.bottomMargin-20)
#color of the ball
ballColor = (255, 155, 0) #orange
#the amount to move the ball 
moveMagnitude = 15

class Ball: 

    #the current position of the ball
    position = [startPosition[0], startPosition[1]]

    #the list of sensors for this ball
    sensors = []

    """method to draw a ball
    @param display: the display to draw on"""
    def draw (self, display):
        pygame.draw.circle(display, ballColor, self.position, radius)
        self.createSensors(display)

    """method to reset the ball to its original position"""
    def resetPosition (self):
        self.position = [startPosition[0], startPosition[1]] 
        self.sensors = []
    
    """method to update the ball to move up """
    def moveUp (self):
        self.position[1] -= moveMagnitude
        shiftSensorsPos(self.sensors, 0, -moveMagnitude)

    """method to update the ball to move up """
    def moveDown (self):
        self.position[1] += moveMagnitude
        shiftSensorsPos(self.sensors, 0, moveMagnitude)

    """method to move the ball right"""
    def moveRight (self):
        self.position[0] += moveMagnitude
        shiftSensorsPos(self.sensors, moveMagnitude, 0)

    """method to move the ball left"""
    def moveLeft (self):
        self.position[0] -= moveMagnitude
        shiftSensorsPos(self.sensors, -moveMagnitude, 0)

    """method to get the distance from the ball to the goal"""
    def getDistanceFromGoal (self):
        #use math to get distance to goal center
        return 10*math.sqrt((self.position[0] - Goal.centerPoint[0])**2 + \
                (self.position[1] - Goal.centerPoint[1])**2)/10


    """method to view what is in the sensors of the player
    @param display: the screen to draw to
    @return: the sensors array"""
    def createSensors (self, display):
        #create sensors only if empty sensors, else just draw
        if len(self.sensors) < 1:
            #we want 8 sensors starting at -20 degrees so 28 angle per sensor
            for sensorIndex in range(Sensor.numSensors):
                angle = -1*Sensor.sensorRange/(Sensor.numSensors-1) * sensorIndex #-1 since don't want to include last
                sensorDeltaX = math.cos(math.radians(angle)) * Sensor.sensorLength 
                sensorDeltaY = math.sin(math.radians(angle)) * Sensor.sensorLength 
                sensorEndCoord = [self.position[0]+sensorDeltaX, self.position[1]+sensorDeltaY]
                self.sensors.append (Sensor (display, [self.position[0], self.position[1]], sensorEndCoord))
        else:
            for sensor in self.sensors:
                sensor.draw(display)
    """method to check the sensors for stimulation
    @param gp: the game properties object to check nodes for"""
    def checkSensors (self, gp):
        #empty the current sensors
        Sensor.wallStimulations = []
        Sensor.playerStimulations = []
        Sensor.goalStimulations = []
        #get stimulations from every sensor
        stimulations = [] #only return the stimulations from the last sensor
        for sensor in self.sensors:
            stimulations = sensor.checkForStimulation(gp)
        return stimulations

#inner class to create the sensors for the ball

"""method to shift the position of the sensors
@param sensors: the list of sensors
@param shiftX: the shift in the xPos
@param shiftY: the shift in the yPos"""
def shiftSensorsPos (sensors, shiftX, shiftY):
    for sensor in sensors:
        sensor.startPoint[0] += shiftX
        sensor.endPoint[0] += shiftX
        sensor.startPoint[1] += shiftY
        sensor.endPoint[1] += shiftY

class Sensor: 

    sensorNeutralColor = (0,0,0) #black to start
    sensorStimulatedColor = (0,255,0) #green for stimulation
    currentColor = sensorNeutralColor
    lineThickness = 2 #the thickness of the sensor line

    sensorLength = 70 #length the sensor should detect for
    numSensors = 6 #the number of sensors
    sensorRange = 180 #the range the sensors should see

    #the list of stimulation distances for each type of object each elem is sensor distance
    wallStimulations = []
    playerStimulations = []
    goalStimulations = []
    #the value for non stimulated sensors
    nonStimulated = -1

    #for easier reference to the line intersect functions
    intersect = lambda x,a,b,c,d: line.calculateIntersectPoint(a,b,c,d)
    getIntersect = lambda x,a,b,c,d: line.getIntersectPoint(a,b,c,d)
    #the lines for easier reference for checking intersection
    leftWall = ((0,0),(0,GameProperties.size[1]))
    rightWall = ((GameProperties.size[0],0),(GameProperties.size[0],GameProperties.size[1]))
    upperWall = ((0,0),(GameProperties.size[0],0))

    """sensor constructor, draws the sensor as well
    @param display: the dislpay to draw the ball on
    @param startPoint: the starting point of the sensor line
    @param endPoint: the ending point of the sensor line"""
    def __init__(self, display, startPoint, endPoint):
        self.startPoint = startPoint
        self.endPoint = endPoint
        self.currentColor = self.sensorNeutralColor #the current color of the sensor
        self.draw (display)

    """method to draw the sensor
    @param display: the screen to draw on"""
    def draw (self, display):
        pygame.draw.line (display, self.currentColor, self.startPoint, \
                self.endPoint, self.lineThickness)

    """ method to check for intersection between the sensor line and anything else
    @param gp: the game properties object to get the other nodes from
    @return: list of the different sensors of size numSensors in order:
        the distances to any walls
        the distances to any soccer players
        the distances to the goal"""
    def checkForStimulation (self, gp):
        #check for stimulations
        #left wall
        if self.intersect (self.leftWall[0], self.leftWall[1], \
                self.startPoint, self.endPoint) is not None:
            self.currentColor = self.sensorStimulatedColor
            distance = self.distance(self.getIntersect(self.leftWall[0], self.leftWall[1],\
                self.startPoint, self.endPoint)[0])
            self.wallStimulations.append(distance)
        #right wall
        elif self.intersect (self.rightWall[0], self.rightWall[1], \
                self.startPoint, self.endPoint) is not None:
            self.currentColor = self.sensorStimulatedColor
            distance = self.distance(self.getIntersect(self.rightWall[0], self.rightWall[1],\
                self.startPoint, self.endPoint)[0])
            self.wallStimulations.append(distance)
        #upper wall
        elif self.intersect (self.upperWall[0], self.upperWall[1], \
                self.startPoint, self.endPoint) is not None:
            self.currentColor = self.sensorStimulatedColor
            distance = self.distance(self.getIntersect(self.upperWall[0], self.upperWall[1],\
                self.startPoint, self.endPoint)[0])
            self.wallStimulations.append(distance)
        else:
            self.currentColor = self.sensorNeutralColor
            self.wallStimulations.append(self.nonStimulated) #arbitrarily large num
        #any player stimulations
        encounteredPlayer = False #true if we encountered a player
        for player in gp.playersNodes:
            #the rect of the player
            playerRect = pygame.Rect (player.getRect())
            #bottom edge intersection
            if self.intersect (playerRect.bottomleft, playerRect.bottomright, \
                    self.startPoint, self.endPoint) is not None:
                self.currentColor = self.sensorStimulatedColor
                distance = self.distance(self.getIntersect(playerRect.bottomleft, playerRect.bottomright,\
                    self.startPoint, self.endPoint)[0])
                self.playerStimulations.append(distance)
                encounteredPlayer = True
            #left edge intersection
            elif self.intersect (playerRect.topleft, playerRect.bottomleft, \
                    self.startPoint, self.endPoint) is not None:
                self.currentColor = self.sensorStimulatedColor
                distance = self.distance(self.getIntersect(playerRect.topleft, playerRect.bottomleft,\
                    self.startPoint, self.endPoint)[0])
                self.playerStimulations.append(distance)
                encounteredPlayer = True
            #right edge intersection
            elif self.intersect (playerRect.bottomright, playerRect.topright, \
                    self.startPoint, self.endPoint) is not None:
                self.currentColor = self.sensorStimulatedColor
                distance = self.distance(self.getIntersect(playerRect.bottomright, playerRect.topright,\
                    self.startPoint, self.endPoint)[0])
                self.playerStimulations.append(distance)
                encounteredPlayer = True
        if not encounteredPlayer:
            self.playerStimulations.append(self.nonStimulated) #arbitrarily large

        #goal box stimulation
        gRect = Goal.asRect() #for easier reference
        #bottom boundary
        if self.intersect (gRect.bottomleft, gRect.bottomright, \
                self.startPoint, self.endPoint) is not None:
            self.currentColor = self.sensorStimulatedColor
            distance = self.distance(self.getIntersect(gRect.bottomleft, gRect.bottomright,\
                    self.startPoint, self.endPoint)[0])
            self.goalStimulations.append(distance)
        #left edge intersection
        elif self.intersect (gRect.topleft, gRect.bottomleft, \
                self.startPoint, self.endPoint) is not None:
            self.currentColor = self.sensorStimulatedColor
            distance = self.distance(self.getIntersect(gRect.topleft, gRect.bottomleft,\
                self.startPoint, self.endPoint)[0])
            self.goalStimulations.append(distance)
        #right edge intersection
        elif self.intersect (gRect.bottomright, gRect.topright, \
                self.startPoint, self.endPoint) is not None:
            self.currentColor = self.sensorStimulatedColor
            distance = self.distance(self.getIntersect(gRect.bottomright, gRect.topright,\
                self.startPoint, self.endPoint)[0])
            self.goalStimulations.append(distance)
        else:
            self.goalStimulations.append(self.nonStimulated) #arbitrarily large num
        
        #all the lists joined into one inputs
        return self.wallStimulations + self.playerStimulations + self.goalStimulations

    """helper method to get distance between ball and a point
    @param point: the point to get distance to the ball for
    @return: the distance between the point and the ball"""
    def distance (self, point):
        return math.sqrt((self.startPoint[0] - point[0])**2 + (self.startPoint[1] - point[1])**2)/10
