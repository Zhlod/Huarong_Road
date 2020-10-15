from PIL import Image
import numpy as np
import os
import sys
import json

path = 'GoalPic'
r = os.listdir('GoalPic')
imgs = []
for img_name in r:
    imgs.append(os.path.join(path, img_name))

die = []  # 总的数据
for img_path in imgs:
    img_pos = 1  # 该小块的目标位置
    data = {}  # 单张图片的小块数据，键为小块的像素值，值为该小块的目标位置
    total = {}  # 单张图片的总数据，包含图片路径，小块数据
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
            data[temp[0]] = str(img_pos)
            img_pos += 1
    total['name'] = img_path[8:-4]
    total['goal_pos'] = data
    die.append(total)

die = json.dumps(die, indent=4)
f = open('datas.json', 'w')
f.write(die)
f.close()
