import requests
from PIL import Image
import numpy as np
import base64
import json

def colors(im):
    i = 0
    empty = 0
    data1 = []
    for y in range(3):
        for x in range(3):
            temp = np.array([0, 0, 0])
            croped = im.crop((300*x, 300*y, 300*(x+1), 300*(y+1)))
            croped = croped.resize((150,150))
            r_croped = np.array(croped)
            for w in range(150):
                for h in range(150):
                    temp += r_croped[w][h]
            temp = temp/22500
            data1.append(temp[0])
            if (temp == np.array([255., 255., 255.])).all():
                empty = i
                croped.save('temp/'+str(i)+'.jpg')
            else:
                croped.save('temp/'+str(i)+'.jpg')
            i += 1
    return data1,empty

def FindGoalPic(temp_data):
    with open('datas.json','r') as f:
        goals = json.load(f)
    for target_data in goals:
        mm = 0
        for i in range(9):
            if str(temp_data[i]) not in target_data['colors']:
                mm += 1
            if mm > 1:
                break
        if mm == 1:
            break
    f.close()
    return target_data

def FindGoalPosition(temp_data,target_data):
    for i in range(9):
            if str(temp_data[i]) in target_data['colors']:
                target_data['colors'][str(temp_data[i])] = 1
        
    goal_pos = []
    for i in range(9):
        if str(temp_data[i]) in target_data['colors']:
            goal_pos.append(str(target_data['goal_pos'][str(temp_data[i])]+1))
        else:
            goal_pos.append(str(target_data['goal_pos'][list(target_data['colors'].keys())[list(target_data['colors'].values()).index (0)]]+1))

    return goal_pos

if __name__ == "__main__":
    r = requests.get(r'http://47.102.118.1:8089/api/problem?stuid=031802137 ')
    f = open('Temp.jpg','wb')
    f.write(base64.b64decode(r.json()['img']))
    f.close()
    
    im = Image.open('Temp.jpg')

    temp_data,empty = colors(im)
    target_data = FindGoalPic(temp_data)
    goal_pos = FindGoalPosition(temp_data,target_data)

    print(goal_pos,empty)