# Example file showing a circle moving on screen
import pygame
import random as r

# pygame setup
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
canPop = True
dt = 0
speed = 5
velocity = [0,0]
appleCount = 0
cellSize = 40
direc = [1,0]
bodyCountPerFrame = 2
growthTime = 100


#velocity and direction calculations
dot = lambda a, b: [a[0] * b[0] + a[1] * b[1]]
add_vec = lambda a, b: [a[0] + b[0], a[1] + b[1]]
scalar_mult = lambda a, c: [c * a[0], c * a[1]]

#for snake body
snakepos = [screen.get_width() / 2, screen.get_height() / 2 - 40]
bodypositions = [[int(screen.get_width() / 2-cellSize), int(screen.get_height() / 2 - 40)]]


#variables for screen changing
in_Game = False
title_Screen = True
end_Screen = False


# font stuff
font = pygame.font.SysFont('Helvetica', 14, bold=True, italic=False)
title = pygame.font.SysFont('Roboto', 100, True, False)
border = False

# rectangle sizes
snakeHead = pygame.Rect((snakepos[0], snakepos[1]),(cellSize, cellSize))
apple = pygame.Rect(((r.randint(20, screen.get_width() - 27),r.randint(20, screen.get_height() - 27))),(cellSize/2,cellSize/2))

while running:
    # poll for events
    
    ####################       input/event  stuff        ########################
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.USEREVENT:
            canPop = True

            
        if event.type == pygame.KEYDOWN:
            if title_Screen:
                if (event.key == pygame.K_a or event.key == pygame.K_LEFT):
                    border = True
                    print('BORDER IS NOW ONNNN')
                if (event.key == pygame.K_d or event.key == pygame.K_RIGHT):
                    border = False


            if in_Game:
                # check for key presses to save them and change snake v later 
                if (event.key == pygame.K_w or event.key == pygame.K_UP) and velocity[1] == 0:
                    direc = [0,-1]
                if (event.key == pygame.K_s or event.key == pygame.K_DOWN) and velocity[1] == 0:
                    direc = [0, 1]
                if (event.key == pygame.K_a or event.key == pygame.K_LEFT) and velocity[0] == 0:
                    direc = [-1,0]
                if (event.key == pygame.K_d or event.key == pygame.K_RIGHT) and velocity[0] == 0:
                    direc = [1,0]

                        
                # speed controls and stoping
                if event.key == pygame.K_h:
                    speed += 1 
                if event.key == pygame.K_j:
                    speed -= 1 
                if event.key == pygame.K_k:
                    print(speed) 
                if event.key == pygame.K_SPACE:
                    velocity = [0,0]
            
            # switch to in game when space is pressed
            if title_Screen:
                if event.key == pygame.K_SPACE:
                    title_Screen = False
                    in_Game = True

            #restart after game ends
            if end_Screen:
                if event.key == pygame.K_SPACE:
                    end_Screen = False
                    snakepos = [screen.get_width() / 2, screen.get_height() / 2 - 40]
                    bodypositions = [[int(screen.get_width() / 2-cellSize), int(screen.get_height() / 2 - 40)]]
                    snakeHead = pygame.Rect((snakepos[0], snakepos[1]),(cellSize, cellSize))
                    apple = pygame.Rect(((r.randint(20, screen.get_width() - 27),r.randint(20, screen.get_height() - 27))),(cellSize/2,cellSize/2))
                    velocity = [0,0]
                    appleCount = 0
                    direc = [1,0]
                    bodyCountPerFrame = 2
                    title_Screen = True






    #####################        update    ######################
    
    # in game code
    if in_Game:



        # lets set the snake's velocity, but only when it reaches a cell junction
        if snakeHead.x % cellSize <= 4 and snakeHead.y % cellSize <= 4: 
            velocity = scalar_mult(direc, speed)

        # make the snake move depending on current velocity
    
        snakeHead.x += velocity[0] 
        snakeHead.y += velocity[1] 

        # make the snake wrap around when border = false
        if not border:
            if snakeHead.x < 0 - snakeHead.width:
                snakeHead.x = screen.get_width()-1
            if snakeHead.x > screen.get_width():
                snakeHead.x = 0 - snakeHead.width
            if snakeHead.y >= screen.get_height():
                snakeHead.y = 0 - snakeHead.height
            if snakeHead.y < 0 - snakeHead.height:
                snakeHead.y = screen.get_height()
      

        #on collecting an apple, spawn a new apple and stop popping the snake body ofr a bit so it can grow
        if snakeHead.colliderect(apple):
            apple.x = r.randint(5, screen.get_width() - apple.width)
            apple.y = r.randint(5, screen.get_height() - apple.height)
            redo = True
            while redo:
                redo = False
                for i in range (80, len(bodypositions)):
                    collidable = pygame.Rect((bodypositions[i][0], bodypositions[i][1]),(cellSize, cellSize))
                    if apple.colliderect(collidable) or (apple.x % cellSize != 0 ) or (apple.y % cellSize != 0):
                        redo = True
                        apple.x = r.randint(5, screen.get_width() - cellSize) 
                        apple.y = r.randint(5, screen.get_height() - cellSize) 
                        break
            apple.x += cellSize/4
            apple.y += cellSize/4
            appleCount += 1
            canPop = False
            pygame.time.set_timer(pygame.USEREVENT, growthTime, loops = 1)

        else:
            #if the apple has not been consumed, pop the last bit of the snake body and add to the beginning (keeps length but moves snake)
            for i in range(bodyCountPerFrame):
                bodypositions.insert(i, [snakeHead.x - velocity[0] / bodyCountPerFrame * i, snakeHead.y - velocity[1] / bodyCountPerFrame * i])
            
            if canPop:
                for i in range(bodyCountPerFrame):
                    bodypositions.pop()
            


        # kills the snake on collision with itself
        try:
            for i in range (80, len(bodypositions)):
                collidable = pygame.Rect((bodypositions[i][0], bodypositions[i][1]),(cellSize, cellSize))
                if snakeHead.colliderect(collidable):
                    velocity = [0,0]
                    in_Game = False
                    end_Screen = True
        except:
            print('not enough bodies')

        if border:
            if (snakeHead.x <= -5) or snakeHead.x >= (screen.get_width()-(cellSize-5)) or (snakeHead.y <= -5) or snakeHead.y >= (screen.get_height()-(cellSize-5)):
                velocity = [0,0]
                in_Game = False
                end_Screen = True
                



        
    

    
    



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


        #draw the snake + body parts 
        
        for pos in bodypositions:
            pygame.draw.rect(screen, "green", pygame.Rect(pos[0],pos[1], cellSize, cellSize))
        
        pygame.draw.rect(screen, "pink", snakeHead, int(cellSize/8))
        #draw apple
        pygame.draw.rect(screen, "red", apple)



        #write the count of apples
        screen.blit(font.render(str(appleCount), True, "white"), (screen.get_width() - 30, 30))
    


    # code for the title screen
    if border:
        highlight = 'yellow'
        highlight2 = 'white'
    else:
        highlight2 = "yellow"
        highlight = 'white'
    
    #actally displaying the screen
    if title_Screen:
        screen.fill("white")
        screen.blit(title.render("Welcome to Snake", True, "black"), ((screen.get_width()/2) -300 , screen.get_height()/2-50))
        screen.blit(font.render("Play with border?", True, "black"), ((screen.get_width()/2) - 95, screen.get_height()/2+30))
        screen.blit(font.render("Yes", True, "black", highlight), ((screen.get_width()/2) + 30, screen.get_height()/2+30))
        screen.blit(font.render("No", True, "black", highlight2), ((screen.get_width()/2) + 60, screen.get_height()/2+30))
        screen.blit(font.render("press space to continue", True, "black"), ((screen.get_width()/2) - 80, screen.get_height()/2+50))

    if end_Screen:
        screen.blit(title.render("GAME OVER", True, "white"), ((screen.get_width()/2) -300 , screen.get_height()/2-50))

    
    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
