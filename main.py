import requests
import pygame
import queue
from pygame.locals import *
import base64
from PIL import Image
import numpy as np
import json
import Pic_processing
import game
import sss

r = requests.get(r'http://47.102.118.1:8089/api/problem?stuid=031802137 ')
f = open('Temp.jpg', 'wb')
f.write(base64.b64decode(r.json()['img']))
f.close()

print(r.json()['step'])
print(r.json()['swap'])
print(r.json()['uuid'])

goal_pos = ['1','2','3','4','5','6','7','8','9']
im = Image.open('Temp.jpg')

temp_data, empty = Pic_processing.colors(im)
target_data = Pic_processing.FindGoalPic(temp_data)
now_pos = Pic_processing.FindGoalPosition(temp_data, target_data)

empty = now_pos[empty]

str1 = "".join(now_pos)
str2 = "".join(goal_pos)

print(empty)
print(str1)
print(str2)

if sss.Solvable(str1,empty):
    sss.sorrt(str1,str2,empty)
else:
    print('无解！')