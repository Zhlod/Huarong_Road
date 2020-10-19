from PIL import Image
import numpy as np
import json


def crop(im):
    '''
    将乱序图片切块，并记录每一小块的像素值储存到列表中
    并且将每一小块从左上按行从1~9命名保存到temp文件夹下
    '''
    i = 1
    empty_pos = 0  # 空白块的位置
    data = []  # 每一小块的像素值,字符串形式
    for y in range(3):  # 切成9小块并计算每小块的像素均值
        for x in range(3):
            temp = np.array([0, 0, 0])
            croped = im.crop((300*x, 300*y, 300*(x+1), 300*(y+1)))  # 切块
            croped = croped.resize((150, 150))  # 压缩
            r_croped = np.array(croped)  # 将图片信息转化为数组

            for w in range(150):  # 计算像素值
                for h in range(150):
                    temp += r_croped[w][h]
            temp = temp/22500
            data.append(str(temp[0]))

            if (temp == np.array([255., 255., 255.])).all():  # 纯白即为空白块
                empty_pos = i  # 标记空白块初始位置
                croped.save('AI_Competition/temp/'+str(i)+'.jpg')
            else:
                croped.save('AI_Competition/temp/'+str(i)+'.jpg')
            i += 1
    return data, empty_pos


def FindGoalPic(temp_data):
    '''
    从所有目标图片中找出乱序图片的目标图片的信息。
    目标图片的信息组成（一个字典）：键为每一小块的像素值，值为每一小块的目标位置。
    通过逐一查找乱序图片每一小块的像素值与各目标图片没一小块像素值不相同的小块个数，有且只有一个小块的像素值不一样的图片即为目标图片。
    temp_data: 乱序图片9个小块的信息，列表形式
    '''
    with open('AI_Competition\Goal_Pic_datas\datas.json', 'r') as f:
        goals = json.load(f)  # 读入所有目标图片的信息,goals是一个列表
    f.close()

    for target_data in goals:
        count = 0  # 待处理图片与该目标图片不相同小块的数量
        for i in range(9):
            if temp_data[i] not in target_data['goal_pos']:
                count += 1
            if count > 1:  # 超过1个小块不一样就不是目标图片
                break
        if count == 1:  # 有且仅有一个小块不一样(空白块),就是目标图片
            break
    return target_data  # 返回目标图片的信息


def FindInitPosition(temp_data, target_data):
    '''
    将乱序图片信息转换成初始位置序列，用字符串表示
    temp_data: 乱序图片小块信息
    target_data: 目标图片信息
    '''
    for key in target_data['goal_pos'].keys():  # 找出被挖空的小块
        if key not in temp_data:
            blanked = key

    init_pos = ''  # 储存初始位置序列
    for i in range(9):
        if temp_data[i] in target_data['goal_pos']:
            init_pos += target_data['goal_pos'][temp_data[i]]
        else:
            init_pos += target_data['goal_pos'][blanked]

    return init_pos


def main(img):
    data, empty_pos = crop(img)  # 获取乱序图片小块信息, 空白块初始位置
    target_data = FindGoalPic(data)  # 查找目标图片, 并返回目标图片信息
    init_pos = FindInitPosition(data, target_data)  # 将乱序图片转化为位置序列
    return init_pos, empty_pos-1


if __name__ == "__main__":
    pass
