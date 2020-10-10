from PIL import Image
import numpy as np
import os
import sys
import json

path = 'GoalPic'
r = os.listdir('GoalPic')
imgs = []
for lisst in r:
    imgs.append(os.path.join(path, lisst))

die = []  # 总的数据
for img_path in imgs:
    img_pos = 0  # 该小块的位置
    data = {}  # 每张图片的总数据
    color = {}  # 每小块的像素均值
    pos = {}  # 每小块的目标位置
    img = Image.open(img_path)
    for y in range(3):
        for x in range(3):
            temp = np.array([0, 0, 0])
            croped = img.crop((300*x, 300*y, 300*(x+1), 300*(y+1)))
            croped = croped.resize((150, 150))
            r_croped = np.array(croped)
            for i in range(150):
                for j in range(150):
                    temp += r_croped[i][j]
            temp = temp/22500
            color[temp[0]] = 0
            pos[temp[0]] = img_pos
            img_pos += 1
    data['colors'] = color
    data['goal_pos'] = pos
    die.append(data)

die2 = json.dumps(die, indent=4)
f = open('datas.json', 'w')
f.write(die2)
f.close()
