import pygame
import time
import random
import math

pygame.init()

display_width = 800
display_height = 600

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Super racer 0.1")
clock = pygame.time.Clock()

carImg = pygame.image.load("racer1.png")
car_width = carImg.get_rect().size[0]
car_height = carImg.get_rect().size[1]
car_side_to_side_speed = 10

global big_square_color

def big_squares_dodged(count):
    font = pygame.font.SysFont(None, 25)
    textSurface = font.render("Dodged: "+str(count), True, black)
    gameDisplay.blit(textSurface, (0,0))

def big_squares(big_squarex, big_squarey, big_squarew, big_squareh, color):
    pygame.draw.rect(gameDisplay, color, [big_squarex, big_squarey, big_squarew, big_squareh])

def car(x, y):
    gameDisplay.blit(carImg, (x, y))

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font("freesansbold.ttf", 100)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2), (display_height/2))
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()

    time.sleep(2)

    game_loop()

def crash():
    message_display("You Crashed!")

def crash_test(carx, cary, big_squarex, big_squarey, big_square_width, big_square_height):
    crashx = False
    crashy = False
    global big_square_color
    big_square_color = blue

    if carx >= big_squarex and carx <= big_squarex + big_square_width:
        crashx = True
    elif carx + car_width >= big_squarex and carx + car_width <= big_squarex + big_square_width:
        crashx = True

    if cary >= big_squarey and cary <= big_squarey + big_square_height:
        crashy = True
    elif cary + car_height >= big_squarey and cary + car_height <= big_squarey + big_square_height:
        crashy = True
    
    return crashx and crashy

def q():
    pygame.quit()
    quit()

def game_loop():
    x = (display_width - car_width) / 2
    y = display_height * 0.8 #(display_height - car_height) / 2

    big_square_speed = 5
    big_square_width = 100
    big_square_height = 100
    big_square_startx = random.randrange(0, display_width - big_square_width)
    big_square_starty = -600
    big_square_color = blue

    dodged = 0

    gameExit = False

    while not gameExit:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    gameExit = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            x = x - car_side_to_side_speed
        if keys[pygame.K_RIGHT]:
            x = x + car_side_to_side_speed

        gameDisplay.fill(white)

        big_squares(big_square_startx, big_square_starty, big_square_width, big_square_height, big_square_color)
        big_square_starty = big_square_starty + big_square_speed
        
        car(x, y)
        big_squares_dodged(dodged)

        if x > display_width - car_width or x < 0:
            crash()
            gameExit = True
            continue

        if big_square_starty > display_height:
            dodged += 1
            big_square_speed += 1
            #big_square_width += (dodged * 1.2)
            big_square_starty = -big_square_width
            big_square_startx = random.randrange(0, display_width - math.floor(big_square_width))

        if crash_test(x, y, big_square_startx, big_square_starty, big_square_width, big_square_height):
            crash()
            gameExit = True
            continue

        pygame.display.update()
        clock.tick(60)

game_loop()
pygame.quit()
quit()
