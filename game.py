import pygame
import sys
import os
import math
import time
from pygame.locals import *

FPS = 60
WINWIDTH = 450  # 屏幕宽度
WINHEIGHT = 450  # 屏幕高度
BACKGROUND_COLOR = "#92877d"  # 背景颜色

def get_img():
        path = 'temp'
        r = os.listdir('temp')
        imgs = []
        img = []
        for img_name in r:
            imgs.append(os.path.join(path, img_name))
        for i in imgs:
            img.append(pygame.image.load(i))
        return img


class Logic:
    def __init__(self,empty,init_pos):
        self.img = get_img()
        self.empty_pos = empty
        self.goal_pos = ['1','2','3','4','5','6','7','8','9']
        self.now_pos = list(init_pos)

    def move(self,move_path):
        if move_path == 'a':
            if self.empty_pos != 0 and self.empty_pos != 3 and self.empty_pos != 6:
                self.img[self.empty_pos], self.img[self.empty_pos-1] = self.img[self.empty_pos-1], self.img[self.empty_pos]
                self.now_pos[self.empty_pos], self.now_pos[self.empty_pos-1] = self.now_pos[self.empty_pos-1], self.now_pos[self.empty_pos]
                self.empty_pos -= 1
        elif move_path == 'd':
            if self.empty_pos != 2 and self.empty_pos != 5 and self.empty_pos != 8:
                self.img[self.empty_pos], self.img[self.empty_pos+1] = self.img[self.empty_pos+1], self.img[self.empty_pos]
                self.now_pos[self.empty_pos], self.now_pos[self.empty_pos+1] = self.now_pos[self.empty_pos+1], self.now_pos[self.empty_pos]
                self.empty_pos += 1
        elif move_path == 'w':
            if self.empty_pos != 0 and self.empty_pos != 1 and self.empty_pos != 2:
                self.img[self.empty_pos], self.img[self.empty_pos-3] = self.img[self.empty_pos-3], self.img[self.empty_pos]
                self.now_pos[self.empty_pos], self.now_pos[self.empty_pos-3] = self.now_pos[self.empty_pos-3], self.now_pos[self.empty_pos]
                self.empty_pos -= 3
        elif move_path == 's':
            if self.empty_pos != 6 and self.empty_pos != 7 and self.empty_pos != 8:
                self.img[self.empty_pos], self.img[self.empty_pos+3] = self.img[self.empty_pos+3], self.img[self.empty_pos]
                self.now_pos[self.empty_pos], self.now_pos[self.empty_pos+3] = self.now_pos[self.empty_pos+3], self.now_pos[self.empty_pos]
                self.empty_pos += 3

    def is_win(self):
        if self.now_pos == self.goal_pos:
            return True

def press(is_game_over,logic,COUNT,seconds):
    for event in pygame.event.get():
        if event.type == COUNT and not is_game_over:  # 设置定时器，记录时间
            seconds += 1
            pygame.display.set_caption("数字华容道 -- %d" % seconds)
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_a:
                logic.move('a')
            elif event.key == K_d:
                logic.move('d')
            elif event.key == K_w:
                logic.move('w')
            elif event.key == K_s:
                logic.move('s')
            elif event.key == 13:
                return True
    if COUNT:
        return seconds


def init_game():
    # 初始化游戏
    pygame.init()
    screen = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
    pygame.display.set_caption('数字华容道 -- 0')
    return screen

def draw_pic(logic,screen):
    i = 0
    for y in range(3):
        for x in range(3):
            screen.blit(logic.img[i],(x*150,y*150))
            i += 1

def game_win(screen, logic, clock, text='You Win!'):
    font = pygame.font.SysFont('Blod', int(WINWIDTH / 4))
    font_width, font_height = font.size(str(text))
    while True:
        if press(True, logic, None, None):
            break
        screen.fill(pygame.Color(BACKGROUND_COLOR))
        draw_pic(logic, screen)
        screen.blit(font.render(str(text), True, (255, 0, 0)),
                    ((WINWIDTH - font_width) / 2,
                     (WINHEIGHT - font_height) / 2))
        pygame.display.update()
        clock.tick(FPS)

def main(init_pos,empty,step=None,switch=False):
    screen = init_game()
    clock = pygame.time.Clock()
    logic = Logic(empty,init_pos)
    COUNT = pygame.USEREVENT + 1  # 自定义计时事件
    pygame.time.set_timer(COUNT,1000)  # 每1s发生一次计时事件
    seconds = 0  # 记录时间
    if switch == False:
        while True:
            if logic.is_win():  # 判断游戏是否胜利
                break
            seconds = press(False,logic,COUNT,seconds)  #监控按键
            screen.fill(pygame.Color(BACKGROUND_COLOR))
            draw_pic(logic,screen)
            pygame.display.update()
            clock.tick(FPS)
        game_win(screen,logic,clock,text='Time: '+str(seconds))
        pygame.quit()
    else:
        for i in step:
            logic.move(i)
            screen.fill(pygame.Color(BACKGROUND_COLOR))
            draw_pic(logic,screen)
            pygame.display.update()
            time.sleep(0.5)
        game_win(screen,logic,clock)
        pygame.quit()

if __name__ == "__main__":
    pass