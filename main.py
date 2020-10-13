import requests
import os
import time
import pygame
import queue
from pygame.locals import *
import base64
from PIL import Image
import numpy as np
import json
import Pic_processing
import Move

# print(r.json()['step'])
# print(r.json()['swap'])
# print(r.json()['uuid'])


def init_img():
    im = Image.open('Init_Pic.jpg')
    init_pos, empty_pos, goal_img_path = Pic_processing.main(im)
    empty = init_pos[empty_pos]  # 找出空白块的目标位置
    return init_pos, empty, empty_pos, goal_img_path


def get_step(init_pos, goal_pos, empty_pos, empty_init_pos):
    return Move.main(init_pos, goal_pos, empty_pos)


def main():
    while True:
        print("------------------载入中------------------")
        r = requests.get(r'http://47.102.118.1:8089/api/problem?stuid=031802137 ')
        f = open('Init_Pic.jpg', 'wb')
        f.write(base64.b64decode(r.json()['img']))
        f.close()

        goal_pos = '123456789'  # 目标序列
        init_pos, empty_pos, empty_init_pos, goal_img_path= init_img()  # 初始序列, 空白块的目标位置, 空白块的初始位置


        
        print('初始序列: ',init_pos)
        print('空白块: ',empty_pos)
        
        
        if Move.Solvable(init_pos, empty_pos) :  # 判断有无解
            step = get_step(init_pos, goal_pos, empty_pos, empty_init_pos)  # 获取最优步骤
            print(step)
            return init_pos, empty_init_pos, goal_img_path
        else:
            return False
        


if __name__ == "__main__":
    main()
