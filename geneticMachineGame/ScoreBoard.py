import pygame
import GameProperties

#class to draw the score on the screen

#the font of the game
pygame.font.init()
scoreFont = pygame.font.SysFont('Arial', 40)
#the font position
position = (GameProperties.size[0] - 300, GameProperties.topMargin/3)


""" method to draw the score on the screen
@param score: the score of the game
@param display: the display of the game to draw on """
def drawScore (score, display):
    #create the score surface
    scoreboard = scoreFont.render("Won: "+str(score[0])+" Lost: "+str(score[1]),\
            False, (0, 0, 0))
    display.blit(scoreboard, position)
