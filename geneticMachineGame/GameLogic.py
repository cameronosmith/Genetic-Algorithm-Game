#file to run the logic of the game 
import pygame
import GameProperties
import SoccerPlayer, Ball, Goal, ScoreBoard

""" method to run the start of the game (drawing)
@param gp: the game properties object
@param display: the display to draw on """
def draw (gp, display) :
    #draw the goal and score
    Goal.draw(display)
    ScoreBoard.drawScore(gp.score, display)
    #create the soccer team and ball nodes if first draw or just draw else
    if gp.playersNodes is None:
        gp.setPlayers(SoccerPlayer.drawTeam(display))
    else:
        for player in gp.playersNodes:
            player.draw(display)
    if gp.ballNode is None:
        gp.setBall(Ball.Ball())
        gp.ballNode.draw(display)
    else:
        gp.ballNode.draw(display)

"""method to check for intersection between ball and soccer player and goal
must be called after the draw method
@param pm: the population manager of the gamee
@param gp: the game properties obj"""
def collisionCheck (pm, gp): 
    #break if players not set yet
    if gp.playersNodes is None:
        return
    #check the node rects for collision    
    for player in gp.playersNodes :
        if player.collidesWithBall(gp.ballNode, Ball.radius):
        #    print("game lost")
            endLevel(False, pm, gp)
    #check if player scored
    if Goal.collidesWithBall(gp.ballNode, Ball.radius):
        print("game won")
        endLevel(True, pm, gp)
    else: #check for user colliding with walls
        if gp.ballNode.position[1] < Ball.radius \
                or gp.ballNode.position[1] > GameProperties.size[1] - Ball.radius \
                or gp.ballNode.position[0] < Ball.radius \
                or gp.ballNode.position[0] > GameProperties.size[0] + Ball.radius:
                    endLevel(False, pm, gp)

""" method to handle when the user wins or loses the  game
@param win: true if the user won 
@param pm: the population manager of the gamee
@param gp: the game properties obj"""
def endLevel (win, pm, gp):
    #if agent won give it a very high score
    if win:
        pm.getCurrentAgent().agentWon = True

    #advance and reset the agent
    pm.advanceAgent(gp)
    gp.setBall(pm.getCurrentAgent().ball)
    
    #just tallying scores kinda irrelivant now
    if win:
        gp.score[0] += 1
        gp.ballNode.resetPosition() #reset game
    else: #same but for losing
        gp.score[1] += 1
        gp.ballNode.resetPosition() #reset game

"""method to check for in game events 
@param event: the event to check for
@param gp: the game properties obj
@param display: the display to draw the arrow keys on
@return: true if user wants to quit"""
def checkForEvents (event, gp, display):
    #to quit game
    if event.type == pygame.QUIT or \
            (event.type == pygame.KEYDOWN and event.key == pygame.K_q) :
                return True
    #to move player
    elif event.type == pygame.KEYDOWN:
        #break if ball undefined
        if gp.ballNode is None:
            return False
        if event.key == pygame.K_LEFT:
            gp.ballNode.moveLeft()
        elif event.key == pygame.K_RIGHT:
            gp.ballNode.moveRight()
        elif event.key == pygame.K_UP:
            gp.ballNode.moveUp()
        elif event.key == pygame.K_DOWN:
            gp.ballNode.moveDown()
    else: 
        return False
"""method to restart the game
@param gp: the game properties obj"""
def restartGame (gp):
    gp.ballNode.resetPosition()
"""method to export the current game data for the neural net
@param gp: the game properties
@return: the inputs to the neural net, which are
the lists of sensor inputs for the walls, players, and goal
 """
def exportGameForNet (gp):
    return gp.ballNode.checkSensors (gp)

""" method to get the action from the neural net and handles its choice
@param net: the neural net obj
@param pm: the population manager obj"""
def getAndHandleNetAction (pm, gp):
    #give net inputs and handle response
    netAction = pm.getCurrentAgent().makeAction(exportGameForNet(gp)) 
    if netAction == 0:
        gp.ballNode.moveUp()
    elif netAction == 1:
        gp.ballNode.moveLeft()
    elif netAction == 2:
        gp.ballNode.moveRight()
    else: #need to kiil this one
        endLevel(False, pm, gp)
    #print probability only if last digit is 0 (every 5)
    #if gp.numFramesRun % 10 == 0:
    #    print("probability was ", netAction)
    #subtracting for motion would be better for if players were moving
