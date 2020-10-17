import pygame
from pygame.locals import *
import sys
import os
import random
import time
import json
import AI_Move

if not os.path.exists('Ranks.json'): # 判断有无Ranks文件
    with open('Ranks.json', 'w') as f:  # 读取排行榜信息
        f.write(json.dumps([]))
    Ranks =[]
else:
    with open('Ranks.json', 'r') as f:  # 读取排行榜信息
        Ranks = json.load(f)

FPS = 60  # 刷新率
CELL_SIZE = 100   # 方格大小
MARGIN = 10  # 方格的margin
PADDING = 10  # 方格的padding
WIN_WIDTH = (CELL_SIZE + MARGIN) * 3 + MARGIN + 400  # 屏幕宽度
WIN_HEIGHT = (CELL_SIZE + MARGIN) * 3 + MARGIN  # 屏幕高度

TITLE_COLOR = (0, 0, 0)  # 标题颜色
BACKGROUND_COLOR = (255, 218, 185)  # 背景颜色
BUTTON_COLOR = (0, 200, 0)  # 按钮颜色
BUTTON_CLICK_COLOR = (0, 255, 0)  # 按钮选中颜色
BUTTON_TXT_COLOR = (0, 0, 0)  # 按钮字体颜色
BACKGROUND_EMPTY_CELL_COLOR = (158, 148, 138)  # 空方格颜色
BACKGROUND_CELL_COLOR = (237, 194, 46)  # 方格颜色

pygame.init()  # 初始化
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
clock = pygame.time.Clock()


class Logic:  # 棋盘类
    def __init__(self):
        self.shape = 3
        self.empty_pos = 8  # 空白格所在位置, 空白格默认为 9
        self.tiles = ['1', '2', '3', '4', '5', '6', '7', '8', '9']  # 棋盘当前序列
        self.pos = [-3, -1, 1, 3]  # 定义方向矢量 s,d,a,w
        self.init_load()  # 初始化棋盘

    def init_load(self):
        '''初始化棋盘
        以正确序列为基础随机移动一千次
        '''
        for count in range(1000):  # 随机移动一千次
            pos = random.choice(self.pos)  # 获取随机移动的方向
            spot = self.empty_pos + pos  # 移动后空白块的位置
            if 0 <= spot and spot <= 8:  # 判断有无超出棋盘
                if pos == -3 and self.empty_pos not in [0, 1, 2]:
                    self.tiles[self.empty_pos], self.tiles[spot] = self.tiles[spot], self.tiles[self.empty_pos]
                    self.empty_pos = spot
                elif pos == -1 and self.empty_pos not in [0, 3, 6]:
                    self.tiles[self.empty_pos], self.tiles[spot] = self.tiles[spot], self.tiles[self.empty_pos]
                    self.empty_pos = spot
                elif pos == 1 and self.empty_pos not in [2, 5, 8]:
                    self.tiles[self.empty_pos], self.tiles[spot] = self.tiles[spot], self.tiles[self.empty_pos]
                    self.empty_pos = spot
                elif pos == 3 and self.empty_pos not in [6, 7, 8]:
                    self.tiles[self.empty_pos], self.tiles[spot] = self.tiles[spot], self.tiles[self.empty_pos]
                    self.empty_pos = spot

    def move(self, pos):
        '''移动函数，原理与初始化棋盘函数相同
        '''
        pos = self.pos[pos]  # 获取随机移动的方向
        spot = self.empty_pos + pos  # 移动后空白块的位置
        if 0 <= spot and spot <= 8:  # 判断有无超出棋盘
            if pos == -3 and self.empty_pos not in [0, 1, 2]:
                self.tiles[self.empty_pos], self.tiles[spot] = self.tiles[spot], self.tiles[self.empty_pos]
                self.empty_pos = spot
            elif pos == -1 and self.empty_pos not in [0, 3, 6]:
                self.tiles[self.empty_pos], self.tiles[spot] = self.tiles[spot], self.tiles[self.empty_pos]
                self.empty_pos = spot
            elif pos == 1 and self.empty_pos not in [2, 5, 8]:
                self.tiles[self.empty_pos], self.tiles[spot] = self.tiles[spot], self.tiles[self.empty_pos]
                self.empty_pos = spot
            elif pos == 3 and self.empty_pos not in [6, 7, 8]:
                self.tiles[self.empty_pos], self.tiles[spot] = self.tiles[spot], self.tiles[self.empty_pos]
                self.empty_pos = spot

    def is_win(self):
        '''判断胜利
        '''
        if self.tiles == ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
            return True

    def draw_num(self):
        '''绘制棋盘
        先绘制方格，再绘制数字，'9'为空白块不绘制数字
        '''
        i = 0
        for r in range(self.shape):  # 第几列
            for c in range(self.shape):  # 第几行
                num = self.tiles[i]
                i += 1
                if num != '9':  # 设置方格颜色，空白块与其他不同
                    color = BACKGROUND_CELL_COLOR
                else:
                    color = BACKGROUND_EMPTY_CELL_COLOR

                x = MARGIN * (c + 1) + c * CELL_SIZE
                y = MARGIN * (r + 1) + r * CELL_SIZE
                pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))
                if num != '9':  # 给非空白块绘制数字
                    font_size = int((CELL_SIZE - PADDING) / 1.3)
                    font = pygame.font.SysFont('arialBlod', font_size)
                    font_width, font_height = font.size(num)
                    screen.blit(font.render(num, True, (255, 255, 255)),
                                (x + (CELL_SIZE - font_width) // 2, y +
                                 (CELL_SIZE - font_height) // 2 + 5))


def Quit_Game():
    '''退出游戏
    '''
    pygame.quit()
    sys.exit()


def Return_Start():
    '''返回主菜单
    '''
    return False


def button(msg, x, y, w, h, ic, ac, action=None, logic=None):
    '''绘制按钮，定义功能
    x, y：按钮左上角坐标
    w, h：按钮宽, 高
    ic, ac：鼠标移到到按钮 前颜色，后颜色
    action：按钮功能
    logic：功能所需参数
    '''
    mouse = pygame.mouse.get_pos()  # 获取鼠标位置
    click = pygame.mouse.get_pressed()  # 获取鼠标按键信息
    if x + w > mouse[0] > x and y + h > mouse[1] > y:  # 判断鼠标是否在按钮上
        pygame.draw.rect(screen, ac, (x, y, w, h))  # 高亮按钮
        if click[0] == 1 and action != None:  # 点击左键触发事件
            if logic == None:
                return action()
            else:
                return action(logic)
    else:
        pygame.draw.rect(screen, ic, (x, y, w, h))
    # 绘制按钮
    ButtonText = pygame.font.SysFont(None, 30)
    textSurf = ButtonText.render(msg, True, BUTTON_TXT_COLOR)
    textRect = textSurf.get_rect()
    textRect.center = ((x+(w//2)), (y+(h//2)))
    screen.blit(textSurf, textRect)
    return True


def game_win(logic, text='You Win!'):
    '''获胜显示
            You Win!
         'ESC' to quit
    '''
    font = pygame.font.SysFont('Blod', WIN_WIDTH // 4)
    font_width, font_height = font.size(text)
    txt = "'ESC' to quit"
    font_txt = pygame.font.SysFont('Blod', WIN_WIDTH // 20)
    font_txt_width, font_txt_height = font_txt.size(txt)
    while True:
        if press(True, logic, None, None):  # 按ESC键返回菜单
            break
        screen.fill(BACKGROUND_COLOR)
        logic.draw_num()  # 绘制棋盘
        screen.blit(font.render(text, True, (255, 0, 0)), ((
            WIN_WIDTH - font_width) // 2, (WIN_HEIGHT - font_height) // 2))
        screen.blit(font_txt.render(txt, True, (255, 0, 0)), ((
            WIN_WIDTH - font_txt_width) // 2, (WIN_HEIGHT + font_height) // 2))
        pygame.display.update()
        clock.tick(FPS)


def press(is_game_over, logic, COUNT, seconds):
    '''用户事件监测
    '''
    for event in pygame.event.get():
        if event.type == COUNT and not is_game_over:  # 设置定时器，记录时间
            seconds += 1
            pygame.display.set_caption("数字华容道 -- %d" % seconds)  # 在标题上显示计时
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                return True
            elif event.key == K_a and not is_game_over:
                logic.move(2)
            elif event.key == K_d and not is_game_over:
                logic.move(1)
            elif event.key == K_w and not is_game_over:
                logic.move(3)
            elif event.key == K_s and not is_game_over:
                logic.move(0)

    if COUNT:
        return seconds


def RANK():
    '''排行榜
    '''
    pygame.display.set_caption('排行榜')
    Switch = True
    while Switch:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill(BACKGROUND_COLOR)
        i = 0
        for y in range(len(Ranks)):  # 8个为一列
            x = y // 8
            y = y % 8
            RankText = pygame.font.SysFont(None, 30)
            RankText_Surf = RankText.render(
                str(i+1)+'.  '+str(Ranks[i])+'s', True, BUTTON_TXT_COLOR)
            screen.blit(RankText_Surf, (MARGIN + 100 * x, MARGIN*(y+1) + 30*y))
            i += 1
        Switch = button("QUIT", 550, 150, 100, 50, BUTTON_COLOR,
                        BUTTON_CLICK_COLOR, Return_Start)
        pygame.display.update()
        clock.tick(FPS)


def AI(logic):
    '''AI演示
    获取当前棋盘序列信息，传入Move模块获取最有解步骤，
    AI按步骤执行
    '''
    init_pos = ''.join(logic.tiles)  # 将序列转换为字符串
    step = AI_Move.bfs(init_pos, '9')  # 获取最优解步骤
    print(step)
    for i in step:
        if i == 'w':
            logic.move(0)
        elif i == 's':
            logic.move(3)
        elif i == 'a':
            logic.move(1)
        elif i == 'd':
            logic.move(2)
        screen.fill(BACKGROUND_COLOR)
        logic.draw_num()  # 绘制棋盘
        pygame.display.update()
        time.sleep(0.5)
    game_win(logic)
    return False


def Game_Loop():
    '''游戏界面
    '''
    global Ranks
    pygame.display.set_caption('数字华容道 -- 0')
    logic = Logic()  # 定义棋盘
    COUNT = pygame.USEREVENT + 1  # 自定义计时事件
    pygame.time.set_timer(COUNT, 1000)  # 每1s发生一次计时事件
    seconds = 0  # 记录时间
    Switch = True
    while Switch:
        if logic.is_win():  # 判断游戏是否胜利
            Ranks.append(seconds)  # 添加排行榜记录
            Ranks.sort()  # 降序排序
            if len(Ranks) > 20:  # 最多存20个数据
                Ranks = Ranks[:20]
            with open('Ranks.json', 'w') as f:  # 写入文件
                f.write(json.dumps(Ranks))
            game_win(logic, text='Time: '+str(seconds))
            break
        seconds = press(False, logic, COUNT, seconds)  # 监控按键
        if type(seconds) == bool:
            break
        screen.fill(BACKGROUND_COLOR)
        logic.draw_num()  # 绘制棋盘
        if button("AI", 420, 150, 100, 50, BUTTON_COLOR, BUTTON_CLICK_COLOR, AI, logic) == False:
            break
        Switch = button("QUIT", 550, 150, 100, 50, BUTTON_COLOR,
                        BUTTON_CLICK_COLOR, Return_Start)
        pygame.display.update()
        clock.tick(FPS)


def Game_Start():
    '''主菜单
    '''
    title = pygame.font.SysFont(None, 100)
    title_width, title_height = title.size('Digital Push')
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.set_caption('数字华容道')
        screen.fill(BACKGROUND_COLOR)
        screen.blit(title.render('Digital Push', True, TITLE_COLOR), ((
            WIN_WIDTH - title_width)//2, (WIN_HEIGHT - title_height)//3))
        button("START", 120, 250, 100, 50, BUTTON_COLOR,
               BUTTON_CLICK_COLOR, Game_Loop)
        button("RANK", 320, 250, 100, 50,
               BUTTON_COLOR, BUTTON_CLICK_COLOR, RANK)
        button("QUIT", 520, 250, 100, 50, BUTTON_COLOR,
               BUTTON_CLICK_COLOR, Quit_Game)
        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    Game_Start()
