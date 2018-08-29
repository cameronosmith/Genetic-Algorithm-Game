import pygame
import GameProperties, PopulationManager
import GameLogic

pygame.init()

#define screen properties
screen = pygame.display.set_mode(GameProperties.size)
pygame.display.set_caption("machine game")

#the pop manager to keep track of genetics stuff
pm = PopulationManager.PopulationManager()

#the game properties object
gp = GameProperties.GameProperties(pm)

#used to keep track of how fast the screen should update
clock = pygame.time.Clock()

"""method to run the game"""
def runGame ():
    #to keep track of when the user closes the game
    userQuit = False
    # ~~~~~main program loop~~~~~~~~
    while not userQuit:
        #check for game events
        for event in pygame.event.get():
            userQuit = GameLogic.checkForEvents(event, gp, screen)
        #screen clearing
        screen.fill((255,255,255))
        #draw code
        GameLogic.draw(gp, screen)
        pygame.display.flip() #update the screen with what drawn
        #handle net event
        GameLogic.getAndHandleNetAction(pm, gp)
        #game logic
        GameLogic.collisionCheck(pm, gp)
        #set refresh rate to 60 frames per second
        clock.tick(600)
        gp.numFramesRun += 1

#run game only if calling from main program
if __name__ == "__main__":
    runGame()
    #terminated so quit
    pygame.quit()

