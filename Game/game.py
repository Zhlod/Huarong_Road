import pygame
from pygame.locals import *
import sys
import os
import random
import time
import json
import AI_Move

Ranks_3X3 = []
Ranks_4X4 = []

SHAPE = 4  # 棋盘大小(SHAPE * SHAPE)
FPS = 60  # 刷新率
CELL_SIZE = 100   # 方格大小
MARGIN = 10  # 方格的margin
PADDING = 10  # 方格的padding
WIN_WIDTH = (CELL_SIZE + MARGIN) * 4 + MARGIN + 200  # 屏幕宽度
WIN_HEIGHT = (CELL_SIZE + MARGIN) * 4 + MARGIN  # 屏幕高度

TITLE_COLOR = (0, 0, 0)  # 标题颜色
TIP_COLOR = (0,0,0)  # 帮助颜色
BACKGROUND_COLOR = (255, 218, 185)  # 背景颜色
BUTTON_COLOR = (0, 200, 0)  # 按钮颜色
BUTTON_CLICK_COLOR = (0, 255, 0)  # 按钮选中颜色
BUTTON_TXT_COLOR = (0, 0, 0)  # 按钮字体颜色
BACKGROUND_EMPTY_CELL_COLOR = (158, 148, 138)  # 空方格颜色
BACKGROUND_CELL_COLOR = (237, 194, 46)  # 方格颜色

pygame.init()  # 初始化
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
clock = pygame.time.Clock()


def RANK_FILE():
    '''读取排行榜文件，若无则创建
    '''
    global Ranks_3X3
    global Ranks_4X4
    if not os.path.exists('Game\Ranks_3X3.json'):  # 判断有无Ranks_3X3文件
        with open('Game\Ranks_3X3.json', 'w') as f:  # 创建文件
            f.write(json.dumps([]))
    else:
        with open('Game\Ranks_3X3.json', 'r') as f:  # 读取排行榜信息
            Ranks_3X3 = json.load(f)

    if not os.path.exists('Game\Ranks_4X4.json'):  # 判断有无Ranks_4X4文件
        with open('Game\Ranks_4X4.json', 'w') as f:  # 创建文件
            f.write(json.dumps([]))
    else:
        with open('Game\Ranks_4X4.json', 'r') as f:  # 读取排行榜信息
            Ranks_4X4 = json.load(f)


class Logic:  # 棋盘类
    def __init__(self):
        self.shape = SHAPE  # 棋盘大小
        self.empty_pos = SHAPE * SHAPE - 1  # 空白格所在位置, 空白格默认为右下角
        self.tiles = []  # 棋盘当前序列
        self.goal = []  # 棋盘目标序列
        self.pos = [-SHAPE, -1, 1, SHAPE]  # 定义方向矢量 s,d,a,w
        self.border = [[], [], [], []]  # 棋盘边界  上 左 下 右
        self.init_load()  # 初始化棋盘

    def init_load(self):
        '''初始化棋盘
        以正确序列为基础随机移动一千次
        '''

        for i in range(self.shape*self.shape):  # 生成正确的棋盘序列
            self.tiles.append(str(i+1))
            self.goal.append(str(i+1))
        #self.goal = self.tiles  (这是错误的方法, 这回导致goal与titles始终一样)

        for i in range(2):  # 生成棋盘边界
            mod1 = i*(self.shape-1)+1
            mod2 = int(((self.shape-1)/mod1)*self.shape)
            for j in range(self.shape):
                self.border[i].append(mod1*j)
                self.border[i+2].append(mod1*j+mod2)

        for count in range(1000):  # 随机移动一千次
            pos = random.choice(self.pos)  # 获取随机移动的方向
            spot = self.empty_pos + pos  # 移动后空白块的位置
            if pos == -self.shape and self.empty_pos not in self.border[0]:
                self.tiles[self.empty_pos], self.tiles[spot] = self.tiles[spot], self.tiles[self.empty_pos]
                self.empty_pos = spot
            elif pos == -1 and self.empty_pos not in self.border[1]:
                self.tiles[self.empty_pos], self.tiles[spot] = self.tiles[spot], self.tiles[self.empty_pos]
                self.empty_pos = spot
            elif pos == 1 and self.empty_pos not in self.border[3]:
                self.tiles[self.empty_pos], self.tiles[spot] = self.tiles[spot], self.tiles[self.empty_pos]
                self.empty_pos = spot
            elif pos == self.shape and self.empty_pos not in self.border[2]:
                self.tiles[self.empty_pos], self.tiles[spot] = self.tiles[spot], self.tiles[self.empty_pos]
                self.empty_pos = spot

    def move(self, pos):
        '''移动函数，原理与初始化棋盘函数相同
        '''
        pos = self.pos[pos]  # 获取随机移动的方向
        spot = self.empty_pos + pos  # 移动后空白块的位置
        if pos == -self.shape and self.empty_pos not in self.border[0]:
            self.tiles[self.empty_pos], self.tiles[spot] = self.tiles[spot], self.tiles[self.empty_pos]
            self.empty_pos = spot
        elif pos == -1 and self.empty_pos not in self.border[1]:
            self.tiles[self.empty_pos], self.tiles[spot] = self.tiles[spot], self.tiles[self.empty_pos]
            self.empty_pos = spot
        elif pos == 1 and self.empty_pos not in self.border[3]:
            self.tiles[self.empty_pos], self.tiles[spot] = self.tiles[spot], self.tiles[self.empty_pos]
            self.empty_pos = spot
        elif pos == self.shape and self.empty_pos not in self.border[2]:
            self.tiles[self.empty_pos], self.tiles[spot] = self.tiles[spot], self.tiles[self.empty_pos]
            self.empty_pos = spot

    def is_win(self):
        '''判断胜利
        '''
        if self.tiles == self.goal:
            return True

    def draw_num(self):
        '''绘制棋盘
        先绘制方格，再绘制数字，右下角为空白块不绘制数字
        '''
        empty_num = str(self.shape * self.shape)
        i = 0
        for r in range(self.shape):  # 第几列
            for c in range(self.shape):  # 第几行
                num = self.tiles[i]
                i += 1
                if num != empty_num:  # 设置方格颜色，空白块与其他不同
                    color = BACKGROUND_CELL_COLOR
                else:
                    color = BACKGROUND_EMPTY_CELL_COLOR

                x = MARGIN * (c + 1) + c * CELL_SIZE
                y = MARGIN * (r + 1) + r * CELL_SIZE
                pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))
                if num != empty_num:  # 给非空白块绘制数字
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


def game_win(logic, text='Win!'):
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


def RANK_3X3():
    '''3X3排行榜
    '''
    global Ranks_3X3
    pygame.display.set_caption('3X3排行榜')
    Switch = True
    while Switch:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill(BACKGROUND_COLOR)
        i = 0
        for y in range(len(Ranks_3X3)):  # 11个为一列
            x = y // 11
            y = y % 11
            RankText = pygame.font.SysFont(None, 40)
            RankText_Surf = RankText.render(
                str(i+1)+'.  '+str(Ranks_3X3[i])+'s', True, BUTTON_TXT_COLOR)
            screen.blit(RankText_Surf, (MARGIN + 150 * x, MARGIN*(y+1) + 30*y))
            i += 1
        Switch = button("QUIT", 490, WIN_HEIGHT//2-25, 100, 50, BUTTON_COLOR,
                        BUTTON_CLICK_COLOR, Return_Start)
        pygame.display.update()
        clock.tick(FPS)


def RANK_4X4():
    '''4X4排行榜
    '''
    global Ranks_4X4
    pygame.display.set_caption('4X4排行榜')
    Switch = True
    while Switch:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill(BACKGROUND_COLOR)
        i = 0
        for y in range(len(Ranks_4X4)):  # 11个为一列
            x = y // 11
            y = y % 11
            RankText = pygame.font.SysFont(None, 30)
            RankText_Surf = RankText.render(
                str(i+1)+'.  '+str(Ranks_4X4[i])+'s', True, BUTTON_TXT_COLOR)
            screen.blit(RankText_Surf, (MARGIN + 100 * x, MARGIN*(y+1) + 30*y))
            i += 1
        Switch = button("QUIT", 490, WIN_HEIGHT//2-25, 100, 50, BUTTON_COLOR,
                        BUTTON_CLICK_COLOR, Return_Start)
        pygame.display.update()
        clock.tick(FPS)


def AI(logic):
    '''AI演示
    获取当前棋盘序列信息，传入Move模块获取最有解步骤，
    AI按步骤执行
    '''
    pygame.display.set_caption('AI演示')
    tip = pygame.font.SysFont(None,WIN_WIDTH // 4)
    tip_width, tip_height = tip.size('--loading--')
    screen.blit(tip.render('--loading--', True, TIP_COLOR), ((
            WIN_WIDTH - tip_width) // 2, (WIN_HEIGHT - tip_height) // 2))
    pygame.display.update()
    init_pos = ''.join(logic.tiles)  # 将序列转换为字符串
    step = AI_Move.bfs(init_pos, '9')  # 获取最优解步骤
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


def Game_Loop_3X3():
    '''3X3游戏界面
    '''
    global Ranks_3X3
    global SHAPE
    SHAPE = 3
    pygame.display.set_caption('数字华容道 -- 0')
    logic = Logic()  # 定义棋盘
    COUNT = pygame.USEREVENT + 1  # 自定义计时事件
    pygame.time.set_timer(COUNT, 1000)  # 每1s发生一次计时事件
    seconds = 0  # 记录时间
    Switch = True
    while Switch:
        if logic.is_win():  # 判断游戏是否胜利
            Ranks_3X3.append(seconds)  # 添加排行榜记录
            Ranks_3X3.sort()  # 降序排序
            if len(Ranks_3X3) > 33:  # 最多存33个数据
                Ranks_3X3 = Ranks_3X3[:33]
            with open('Game\Ranks_3X3.json', 'w') as f:  # 写入文件
                f.write(json.dumps(Ranks_3X3))
            game_win(logic, text='Time: '+str(seconds))
            break
        seconds = press(False, logic, COUNT, seconds)  # 监控按键
        if type(seconds) == bool:
            break
        screen.fill(BACKGROUND_COLOR)
        logic.draw_num()  # 绘制棋盘
        if button("AI", 120, 370, 100, 50, BUTTON_COLOR, BUTTON_CLICK_COLOR, AI, logic) == False:
            break
        Switch = button("QUIT", 490, WIN_HEIGHT//2-25, 100, 50, BUTTON_COLOR,
                        BUTTON_CLICK_COLOR, Return_Start)
        pygame.display.update()
        clock.tick(FPS)


def Game_Loop_4X4():
    '''4X4游戏界面
    '''
    global Ranks_4X4
    global SHAPE
    SHAPE = 4
    pygame.display.set_caption('数字华容道 -- 0')
    logic = Logic()  # 定义棋盘
    COUNT = pygame.USEREVENT + 1  # 自定义计时事件
    pygame.time.set_timer(COUNT, 1000)  # 每1s发生一次计时事件
    seconds = 0  # 记录时间
    Switch = True
    while Switch:
        if logic.is_win():  # 判断游戏是否胜利
            Ranks_4X4.append(seconds)  # 添加排行榜记录
            Ranks_4X4.sort()  # 降序排序
            if len(Ranks_4X4) > 33:  # 最多存33个数据
                Ranks_4X4 = Ranks_4X4[:33]
            with open('Game\Ranks_4X4.json', 'w') as f:  # 写入文件
                f.write(json.dumps(Ranks_4X4))
            game_win(logic, text='Time: '+str(seconds))
            break
        seconds = press(False, logic, COUNT, seconds)  # 监控按键
        if type(seconds) == bool:
            break
        screen.fill(BACKGROUND_COLOR)
        logic.draw_num()  # 绘制棋盘
        Switch = button("QUIT", 490, WIN_HEIGHT//2-25, 100, 50, BUTTON_COLOR,
                        BUTTON_CLICK_COLOR, Return_Start)
        pygame.display.update()
        clock.tick(FPS)


def jump_3X3_4X4():
    pygame.display.set_caption('数字华容道')
    Switch = True
    while Switch:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill(BACKGROUND_COLOR)
        button("3X3", 275, 100, 100, 50, BUTTON_COLOR,
               BUTTON_CLICK_COLOR, Game_Loop_3X3)
        button("4X4", 275, 200, 100, 50, BUTTON_COLOR,
               BUTTON_CLICK_COLOR, Game_Loop_4X4)
        Switch = button("QUIT", 275, 300, 100, 50, BUTTON_COLOR,
                        BUTTON_CLICK_COLOR, Return_Start)
        pygame.display.update()
        clock.tick(FPS)


def Rank_3X3_4X4():
    pygame.display.set_caption('排行榜')
    Switch = True
    while Switch:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill(BACKGROUND_COLOR)
        button("3X3", 275, 100, 100, 50, BUTTON_COLOR,
               BUTTON_CLICK_COLOR, RANK_3X3)
        button("4X4", 275, 200, 100, 50, BUTTON_COLOR,
               BUTTON_CLICK_COLOR, RANK_4X4)
        Switch = button("QUIT", 275, 300, 100, 50, BUTTON_COLOR,
                        BUTTON_CLICK_COLOR, Return_Start)
        pygame.display.update()
        clock.tick(FPS)


def Game_Start():
    '''主菜单
    '''
    RANK_FILE()  # 读取排行榜文件
    title = pygame.font.SysFont(None, 100)
    title_width, title_height = title.size('Digital Push')

    Help1 = pygame.font.SysFont(None, 50)
    Help2 = pygame.font.SysFont(None, 50)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.set_caption('数字华容道')
        screen.fill(BACKGROUND_COLOR)
        screen.blit(title.render('Digital Push', True, TITLE_COLOR), ((
            WIN_WIDTH - title_width)//2, (WIN_HEIGHT - title_height)//4))
        screen.blit(Help1.render('Press w, a, s, d,', True, TIP_COLOR), ((
            100, 240)))
        screen.blit(Help2.render('to move blank', True, TIP_COLOR), ((
            100, 290)))
        button("START", 425, 200, 100, 50, BUTTON_COLOR,
               BUTTON_CLICK_COLOR, jump_3X3_4X4)
        button("RANK", 425, 270, 100, 50,
               BUTTON_COLOR, BUTTON_CLICK_COLOR, Rank_3X3_4X4)
        button("QUIT", 425, 340, 100, 50, BUTTON_COLOR,
               BUTTON_CLICK_COLOR, Quit_Game)
        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    Game_Start()