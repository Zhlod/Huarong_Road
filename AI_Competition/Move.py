import queue

step = 0
def Path_search(mp, init_pos, now_pos, empty):
    '''输出路径(逆推法)
    '''
    father = ''
    child = now_pos
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
    通过计算逆序数, 偶序列有解, 奇序列无解
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
    if count % 2 == 0:
        return True
    else:
        return False


def get_empty_pos(now_pos, empty):
    '''遍历找出空白位置'''

    for i in range(len(now_pos)):
        if now_pos[i] == empty:
            return i


def bfs(init_pos, empty, stop_step=100000):
    ''' 核心算法
    通过bfs+哈希判重找出最优解
    init_pos: 初始序列
    empty: 空白块对应的字符
    stop_step: 停机步, 即为发生交换的步数。默认100000, 即不交换。
    '''
    global step  # 当前步数
    dir = [2, 3, 2, 3, 4, 3, 2, 3, 2]  # 对应位置可移动的方向个数
    dis = [[1, 3], [0, 2, 4], [1, 5], [0, 4, 6],  # 对应位置可移动到的位置
         [1, 3, 5, 7], [2, 4, 8], [3, 7], [4, 6, 8], [5, 7]]
    mp = {}
    q1 = queue.Queue()  # 储存序列信息
    q2 = queue.Queue()  # 储存步数
    q1.put(init_pos)
    q2.put(0)

    while(not q1.empty()):
        father_pos = q1.get()
        step = q2.get()
        if step == stop_step:  # 当前步数等于交换步数, 停止搜索, 返回现在的位置序列和解题步骤
            return father_pos, Path_search(mp,init_pos, father_pos,empty)
        pos = get_empty_pos(father_pos, empty)  # 获取空白块的位置
        if father_pos == '123456789':  # 达到目标, 输出解题步骤
            return init_pos, Path_search(mp,init_pos, father_pos,empty)
        for i in range(dir[pos]):  # bfs搜索
            child_pos = list(father_pos)  # 将字符串转化为列表, Python中字符串不可变
            child_pos[pos], child_pos[dis[pos][i]] = child_pos[dis[pos][i]], child_pos[pos]  # 移动空白
            child_pos = ''.join(child_pos)  # 转换回字符串, 列表不能作为字典的键
            if child_pos not in mp:  # 重复标记
                mp[child_pos] = father_pos  
            elif child_pos in mp:
                continue
            q1.put(child_pos)
            q2.put(step+1)

def main(init_pos, empty, swap_step, swap_pos):
    '''主函数(5种情况)
    1. 始状态有解, 强制交换发生在最优解步数之前。
    2. 初始状态有解, 强制交换发生在最优解步数之后, 且交换后有解。
    3. 初始状态有解, 强制交换发生在最优解步数之后, 且交换后无解。
    4. 初始状态无解, 交换后有解。
    5. 初始状态无解, 交换后无解。
    '''
    is_Solvable = Solvable(init_pos, empty)  # 判断初始有无解
    if is_Solvable:  # 初始有解则计算最优解步数
        bfs(init_pos, empty)
    #print(is_Solvable)
    if is_Solvable and step < swap_step:  # 初始有解, 且最优解步数 < 交换发生步数
        return ''.join(path),[]
    elif is_Solvable and step >= swap_step:  # 初始有解, 且最优解步数 >= 交换发生步数
        init_pos, path = bfs(init_pos, empty, swap_step)  # 获取交换发生步数前的最优解
        init_pos = list(init_pos)  # 开始交换
        init_pos[swap_pos[0]-1], init_pos[swap_pos[1]-1] = init_pos[swap_pos[1]-1], init_pos[swap_pos[0]-1]
        init_pos = ''.join(init_pos)
        is_Solvable = Solvable(init_pos, empty)  # 判断交换后有无解
        #print(is_Solvable)
        if is_Solvable:  # 有解则搜索交换后的最优解, 最终步骤 = 交换前+交换后
            init_pos, Path = bfs(init_pos,empty)
            return ''.join(path+Path),[]
        else:  # 无解则原位置交换回来
            init_pos = list(init_pos)
            init_pos[swap_pos[0]-1], init_pos[swap_pos[1]-1] = init_pos[swap_pos[1]-1], init_pos[swap_pos[0]-1]
            init_pos = ''.join(init_pos)
            init_pos, Path = bfs(init_pos,empty)
            return ''.join(path+Path),[swap_pos[1],swap_pos[0]]
    elif not is_Solvable: # 初始无解
        init_pos, path = bfs(init_pos,empty,swap_step)  # 获取交换发生步数前的最优解
        init_pos = list(init_pos)  # 交换
        init_pos[swap_pos[0]-1], init_pos[swap_pos[1]-1] = init_pos[swap_pos[1]-1], init_pos[swap_pos[0]-1]
        init_pos = ''.join(init_pos)
        is_Solvable = Solvable(init_pos, empty)  # 判断交换后有无解
        #print(is_Solvable)
        if is_Solvable:  # 有解则搜索交换后的最优解, 最终步骤 = 交换前+交换后
            init_pos, Path = bfs(init_pos,empty)
            return ''.join(path+Path),[]
        else:  # 无解
            for i in range(9):  # 选择自由交换的位置
                if init_pos[i] != empty and init_pos[i+1] != empty:
                    init_pos = list(init_pos)
                    init_pos[i], init_pos[i+1] = init_pos[i+1], init_pos[i]
                    init_pos = ''.join(init_pos)
                    break
            init_pos, Path = bfs(init_pos,empty)
            return ''.join(path+Path),[i+1,i+2]



if __name__ == "__main__":
    a = '278641539'
    path, swap_pos = main(a,'9',19,[1,2])
    print(path, swap_pos)
    