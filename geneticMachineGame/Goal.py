import pygame
import GameProperties

#class to manage the goal

#define the properties of a goal
goalWidth = int(GameProperties.size[0]/5)
goalHeight = GameProperties.topMargin - 40
goalImage = pygame.image.load('img/goal.png')
goalImage = pygame.transform.scale(goalImage, (goalWidth, goalHeight))
goalPosition = (int(GameProperties.size[0]/2-goalWidth/2),0)
centerPoint = (goalPosition[0] + goalWidth/2, 0)

""" method to draw the goal
@param display: the display to draw the goal on"""
def draw (display):
    display.blit(goalImage, goalPosition)

""" method to check if the ball collided with the goal
@param ball: the ball to check for collision
@param radius: the radius of the ball 
@return: true if ball is in goal"""
def collidesWithBall (ball, radius):
    if  ball.position[1] <= goalPosition[1]+goalHeight \
            and ball.position[0] > goalPosition[0] \
            and ball.position[0] < goalPosition[0] + goalWidth:
        return True
    else:
        return False

"""method to get the goal as a rect
@return: the goal as a rect"""
def asRect ():
    return pygame.Rect(goalPosition, (goalWidth, goalHeight))
