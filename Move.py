import queue


def Path_search(mp, init_pos, goal_pos, empty):
    '''输出路径
    
    '''
    father = ''
    child = goal_pos
    path = []
    i = 0
    while(child != init_pos):
        father = mp.get(child)
        father_empty = get_empty_pos(father, empty)
        child_empty = get_empty_pos(child, empty)
        count = father_empty - child_empty
        if count == -3:
            path.append('s')
        elif count == -1:
            path.append('d')
        elif count == 1:
            path.append('a')
        elif count == 3:
            path.append('w')
        child = father
    return list(reversed(path))


def Solvable(now_pos, empty):
    ''' 判断有无解
    通过计算逆序数，偶序列有解，奇序列无解
    '''
    lenght = 9
    count = 0
    for i in range(lenght-1):
        if now_pos[i] == empty:
            continue
        for j in range(i+1, lenght):
            if now_pos[j] == empty:
                continue
            if now_pos[i] > now_pos[j]:
                count += 1
    print('逆序数: ',count)
    if count % 2 == 0:
        return True
    else:
        return False


def get_empty_pos(now_pos, empty):
    '''遍历找出空白位置'''

    for i in range(len(now_pos)):
        if now_pos[i] == empty:
            return i


def main(init_pos, goal_pos, empty):
    ''' 核心算法
    通过广搜找出最优解
    '''
    dir = [2, 3, 2, 3, 4, 3, 2, 3, 2]
    dis = [[1, 3], [0, 2, 4], [1, 5], [0, 4, 6], [
        1, 3, 5, 7], [2, 4, 8], [3, 7], [4, 6, 8], [5, 7]]
    mp = {}
    q1 = queue.Queue()  # 储存序列信息
    q2 = queue.Queue()  # 储存步数
    q1.put(init_pos)
    q2.put(0)

    while(not q1.empty()):
        father_pos = q1.get()
        step = q2.get()
        pos = get_empty_pos(father_pos, empty)
        if father_pos == goal_pos:
            print(step)
            return Path_search(mp, init_pos, goal_pos, empty)
        for i in range(dir[pos]):
            child_pos = list(father_pos)
            child_pos[pos], child_pos[dis[pos][i]] = child_pos[dis[pos][i]], child_pos[pos]  # 移动空白
            child_pos = ''.join(child_pos)
            if child_pos not in mp:  # 重复标记
                mp[child_pos] = father_pos  
            elif child_pos in mp:
                continue
            q1.put(child_pos)
            q2.put(step+1)


if __name__ == "__main__":
    a = '941628753'
    b = '123456789'

    print(Solvable('123687594','8'))
    '''
    if Solvable(a, '9'):
        main(a, b, '9')
    else:
        print('无解！')
    '''