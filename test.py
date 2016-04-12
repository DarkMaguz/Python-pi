import pygame

pygame.init()

# to spam the pygame.KEYDOWN event every 100ms while key being pressed
pygame.key.set_repeat(100, 100)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                print 'go forward'
            if event.key == pygame.K_s:
                print 'go backward'
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_q:
		run = False
            print 'stop'

pygame.quit()
