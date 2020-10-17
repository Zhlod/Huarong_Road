import os
import base64
import Pic_processing
import Move

def init_img():
    im = Image.open('temp/Init_Pic.jpg')
    init_pos, empty_pos, goal_img_path = Pic_processing.main(im)
    empty = init_pos[empty_pos]  # 找出空白块的目标位置
    return init_pos, empty, empty_pos, goal_img_path


def main(img_path, step, swap):
    if not os.path.exists('temp/'):
        os.mkdir("temp") 

    f = open('temp/Init_Pic.jpg', 'wb')
    f.write(base64.b64decode(img_path))
    f.close()

    init_pos, empty_pos, empty_init_pos, goal_img_path= init_img()  # 初始序列, 空白块的目标位置, 空白块的初始位置

    print('初始序列: ',init_pos)
    print('空白块: ',empty_pos)
    print('交换步数：',step)
    print('交换位置：',swap)

    path, swap_pos = Move.main(init_pos, empty_pos, step, swap)
    return path, swap_pos



if __name__ == "__main__":
    main()
