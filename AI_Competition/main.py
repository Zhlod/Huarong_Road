import os
import queue
import base64
from PIL import Image
import requests
import numpy as np
import json
import Pic_processing
import Move

def init_img():
    im = Image.open('AI_Competition/temp/Init_Pic.jpg')
    init_pos, empty_pos = Pic_processing.main(im)
    empty = init_pos[empty_pos]  # 找出空白块的目标位置
    return init_pos, empty, empty_pos


def main(img_path,step, swap):
    if not os.path.exists('AI_Competition/temp/'):
        os.mkdir("AI_Competition/temp") 
    
    f = open('AI_Competition/temp/Init_Pic.jpg', 'wb')
    f.write(base64.b64decode(img_path))
    f.close()
    
    init_pos, empty_pos, empty_init_pos = init_img()  # 初始序列, 空白块的目标位置, 空白块的初始位置

    print('初始序列: ',init_pos)
    print('空白块: ',empty_pos)
    print('交换步数：',step)
    print('交换位置：',swap)

    path, swap_pos = Move.main(init_pos, empty_pos, step, swap)
    return path, swap_pos



if __name__ == "__main__":
    url_get = 'http://47.102.118.1:8089/api/problem?stuid=031802137'
    url_post = 'http://47.102.118.1:8089/api/answer'
    r = requests.get(url_get)
    path, swap_pos = main(r.json()['img'], r.json()['step'], r.json()['swap'])
    s = json.dumps(
        {
            "uuid":r.json()['uuid'],
            "answer":{
                "operations": path,
                "swap": swap_pos
            }
        }
    )
    answer = requests.post(url_post, data=s, headers={'Content-Type':'application/json'})
    print('score: ', answer.json()['score'])
    print('time: ', answer.json()['time'])