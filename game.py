import pygame
import math
from pygame.locals import *


def gaming(img,empty):
    
    pygame.init()
    screen = pygame.display.set_mode((450, 450))
    position = [[0,0],[150,0],[300,0],
                [0,150],[150,150],[300,150],
                [0,300],[150,300],[300,300]]

    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit
                elif event.key == K_d:
                    if empty != 0 and empty != 3 and empty != 6:
                        img[empty][0],img[empty-1][0] = img[empty-1][0],img[empty][0]
                        empty -= 1
                elif event.key == K_w:
                    if empty != 6 and empty != 7 and empty != 8:
                        img[empty][0],img[empty+3][0] = img[empty+3][0],img[empty][0]
                        empty += 3
                elif event.key == K_a:
                    if empty != 2 and empty != 5 and empty != 8:
                        img[empty][0],img[empty+1][0] = img[empty+1][0],img[empty][0]
                        empty += 1
                elif event.key == K_s:
                    if empty != 0 and empty != 1 and empty != 2:
                        img[empty][0],img[empty-3][0] = img[empty-3][0],img[empty][0]
                        empty -= 3

        screen.fill((0, 0, 0))       
        for i in img:
            screen.blit(i[0],position[i[1]])

        pygame.display.update()

if __name__ == "__main__":
    gaming(2)