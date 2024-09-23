# Example file showing a circle moving on screen
import pygame
import random as r
import time

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
timeElapsed = 0
startTime = 0
speed = 4.6
velocity = [0,0]
appleCount = 0
cellSize = 80
pygame.font.init()
tolerance = 40


# ideas for later
# basically, save the last input into a list and have it check each time in update
# once it reaches  a junction, go the cardinal direction that was indicated last in the buffer
# don't forget to delete buffer list





# create a timer for move delays to hopefully keep it in 
#pygame.time.set_timer(pygame.USEREVENT, 1000)

#variables for screen changing
in_Game = False
title_Screen = True


# font stuff
font = pygame.font.SysFont('Helvetica', 14, bold=True, italic=False)
title = pygame.font.SysFont('Roboto', 100, True, False)

# rectangle sizes
snakeHead = pygame.Rect((screen.get_width() / 2, screen.get_height() / 2),(cellSize-10, cellSize-10))
apple = pygame.Rect(((r.randint(20, screen.get_width() - 27),r.randint(20, screen.get_height() - 27))),(40,40))

while running:
    # poll for events
    
    ####################       input/event  stuff        ########################
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

            
        if event.type == pygame.KEYDOWN:
            endTime = timeElapsed
            if in_Game:
                # check for key presses to change snake v
                
                if event.key == pygame.K_w and velocity[1] != speed:
                   while True:
                        if snakeHead.x % cellSize < tolerance:
                            velocity[1] = -speed 
                            velocity[0] = 0
                            break

                    
                    
                if event.key == pygame.K_s and velocity[1] != -speed:
                    while True:
                        if snakeHead.x % cellSize < tolerance:
                            velocity[1] = speed 
                            velocity[0] = 0
                            break
                        
                

                if event.key == pygame.K_a and velocity[0] != speed:
                    while True:
                        if snakeHead.y % cellSize < tolerance:
                            velocity[0] = -speed 
                            velocity[1] = 0 
                            break
                    
                if event.key == pygame.K_d and velocity[0] != -speed:
                    while True:
                        if snakeHead.y % cellSize < tolerance:
                            velocity[0] = speed
                            velocity[1] = 0 
                            break
                        

                if event.key == pygame.K_h:
                    speed += 1 
                if event.key == pygame.K_j:
                    speed -= 1 
                if event.key == pygame.K_k:
                    print(speed) 
                if event.key == pygame.K_SPACE:
                    velocity = [0,0]
                    startTime = timeElapsed
            
            # switch to in game when enter is pressed
            if title_Screen:
                if event.key == pygame.K_SPACE:
                    title_Screen = False
                    in_Game = True





    #####################        update    ######################
    
    # in game code
    if in_Game:

        timeElapsed += (dt*1000)
        # make the snake move depending on current velocity
        snakeHead.x += velocity[0] #* dt
        snakeHead.y += velocity[1] #* dt


        # make the snake wrap around
        if snakeHead.x < 0 - snakeHead.width:
            snakeHead.x = screen.get_width()
        if snakeHead.x > screen.get_width():
            snakeHead.x = 0 - snakeHead.width
        if snakeHead.y > screen.get_height():
            snakeHead.y = 0
        if snakeHead.y < 0 - snakeHead.height:
            snakeHead.y = screen.get_height()

        
        # apple is gonna appear at random x and y values on collision
        if snakeHead.colliderect(apple):
            apple.x = r.randint(20, screen.get_width() - apple.width)
            apple.y = r.randint(20, screen.get_height() - apple.height)
            appleCount += 1

        # on collision with the apple the snake grows one cell

    

        
    

    
    



##################     Display Stuff       ####################
    if in_Game:
        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")
        
        # create the grid that we play on
        
        for X in range(0,screen.get_width(), cellSize):
            y_start = 0
            if X % (cellSize*2) == 0:
                    y_start = cellSize
            for Y in range(y_start, screen.get_height(), cellSize*2):
                pygame.draw.rect(screen, (34,34,34) , (X, Y, cellSize, cellSize))


        pygame.draw.rect(screen, "pink", snakeHead, 4)
        pygame.draw.rect(screen, "red", apple)

        #write the count of apples
        screen.blit(font.render(str(appleCount), True, "white"), (screen.get_width() - 30, 30))
    
    # code for the title screen
    if title_Screen:
        screen.fill("white")
        screen.blit(title.render("Welcome to Snake", True, "black"), ((screen.get_width()/2) -300 , screen.get_height()/2-50))
        screen.blit(font.render("press space to continue", True, "black"), ((screen.get_width()/2) - 55, screen.get_height()/2+30))



    
    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()