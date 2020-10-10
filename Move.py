import queue

def Solvable(now_pos,empty):
    lenght = len(now_pos)
    count = 0
    for i in range(lenght-1):
        if now_pos[i] == empty:
            continue
        for j in range(i+1,lenght):
            if now_pos[j] == empty:
                continue
            if now_pos[i] > now_pos[j]:
                count += 1
    if count%2 == 0:
        return True
    else:
        return False


def getempty(now_pos,empty):
    for i in range(len(now_pos)):
        if now_pos[i] == empty:
            return i


def sorrt(now_pos,goal_pos,empty):
    dir = [2,3,2,3,4,3,2,3,2]
    dis = [[1,3],[0,2,4],[1,5],[0,4,6],[1,3,5,7],[2,4,8],[3,7],[4,6,8],[5,7]]
    mp = {}
    q = queue.Queue()
    w = queue.Queue()
    q.put(now_pos)
    w.put(0)
    while(not q.empty()):
        temp1_pos = q.get()
        step = w.get()
        pos = getempty(temp1_pos,empty)
        if temp1_pos == goal_pos: 
            print(step)
        for i in range(dir[pos]):
            temp2_pos = list(temp1_pos)
            temp2_pos[pos],temp2_pos[dis[pos][i]] = temp2_pos[dis[pos][i]],temp2_pos[pos]
            temp2_pos = ''.join(temp2_pos)
            if temp2_pos not in mp:
                mp[temp2_pos] = 1
            elif mp[temp2_pos] == 1:
                continue
            q.put(temp2_pos)
            w.put(step+1)

if __name__ == "__main__":
    a = '956348217'
    b = '123456789'
    if Solvable(a,'6'):
        sorrt(a,b,'6')
    else:
        print('无解！')