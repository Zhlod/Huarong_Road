import requests
import json
import main

def GET_Challenges(url, params_GET_challenges):
    '''获取所有赛题'''
    r = requests.get(url+params_GET_challenges)
    return r.json()

def GET_NOT_DO(url, params_GET_NOT_DO,tid):
    '''获取未挑战或挑战失败的赛题'''
    r = requests.get(url+params_GET_NOT_DO+tid)
    return r.json()

def GET_record(url, params_GET_record,uuid):
    '''获取解出指定题目的队伍数据'''
    r = requests.get(url+params_GET_record+uuid)
    for i in r.json():
        print(i)

def GET_All_Rank(url, params_GET_all_rank):
    '''获取总排行榜'''
    r = requests.get(url+params_GET_all_rank)
    for i in r.json():
        print(i)
    

def GET_My_Rank(url, params_GET_rank):
    '''获取本组参赛信息'''
    r = requests.get(url+params_GET_rank)
    return r.json()


def POST_Create(url, params_POST_create, token):
    '''创建并提交自建赛题
       手动修改赛题信息
    '''
    s = json.dumps(
        {
            "teamid": 42,
            "data": {
                "letter": "A",
                "exclude": 3,
                "challenge": [
                    [8, 9, 6],
                    [5, 7, 1],
                    [4, 2, 0]
                ],
                "step": 0,
                "swap": [1, 2]
            },
            "token": token
        }
    )
    r = requests.post(url+params_POST_create, data=s,headers={'Content-Type':'application/json'})
    return r.json()


def POST_start(url, params_POST_start, uuid, token):
    '''获取指定赛题数据'''
    s = json.dumps(
        {
            "teamid": 42,
            "token": token
        }
    )
    r = requests.post(url+params_POST_start+uuid, data=s,headers={'Content-Type':'application/json'})
    return(r.json())


def POST_submit(url, params_POST_submit, token,uuid,path,swap):
    '''提交指定赛题的答案'''
    s = json.dumps(
        {
            "uuid": uuid,
            "teamid": 42,
            "token": token,
            "answer": {
                "operations": path,
                "swap": swap
            }
        }
    )
    r = requests.post(url+params_POST_submit, data=s,headers={'Content-Type':'application/json'})
    print(r.json())


if __name__ == "__main__":
    start = []
    challenges = []
    rank = []
    token = '7cff3bc5-f3bf-42a4-932a-aa970a82aa9a'
    team_id = 42
    url = 'http://47.102.118.1:8089/'
    params_GET_challenges = 'api/challenge/list'  # 所有赛题
    params_GET_rank = 'api/teamdetail/42'  # 本队信息
    params_GET_all_rank = 'api/rank'  # 总榜
    params_GET_NOT_DO = 'api/team/problem/'  # 未挑战或未通过赛题
    params_POST_create = 'api/challenge/create'  # 创建赛题
    params_POST_start = 'api/challenge/start/'  # 获取赛题信息
    params_POST_submit = 'api/challenge/submit'  # 提交答案
    params_GET_record = 'api/challenge/record/'  # 获取解开某题队伍信息

    '''获得总排行榜
    GET_All_Rank(url,params_GET_all_rank)
    '''

    ''' 获得我们的排行榜
    rank = GET_My_Rank(url,params_GET_rank)
    print('rank:',rank['rank'])
    print('score:',rank['score'])
    print('success:')
    for i in rank['success']:
        print(i)
    print('fail:')
    for i in rank['fail']:
        print(i)
    print('unsolved:')
    for i in rank['unsolved']:
        print(i)
    '''
    


    '''获取为挑战或未通过赛题,并存为文件
    challenges = GET_NOT_DO(url,params_GET_NOT_DO,'42')
    r = json.dumps(challenges,indent=4)
    with open('AI_Competition\challenges_not.json','w') as f:
        f.write(r)
    '''

    ''' 获取全部赛题,并存为文件
    challenges = GET_Challenges(url,params_GET_challenges)
    r = json.dumps(challenges,indent=4)
    with open('AI_Competition\challenges_all.json','w') as f:
        f.write(r)
    '''

    '''手动输入赛题uuid解题
    print("------------------载入中------------------")
    uuid = 'cb2337fa-cc56-4d15-9942-e2471d95ff96'  # 指定题目的uuid
    print('赛题uuid：',uuid)
    start = POST_start(url, params_POST_start,uuid , token) 
    print('剩余挑战次数：',start['chanceleft'])
    print('挑战uuid：',start['uuid'])
    path, swap_pos = main.main(start['data']['img'],start['data']['step'],start['data']['swap'])
    POST_submit(url, params_POST_submit, token,start['uuid'],path,swap_pos)
    print(path, swap_pos)
    '''

    '''获取解出指定题目的队伍数据
    uuid = ''  # 指定题目的uuid
    GET_record(url,params_GET_record,uuid)
    '''

    ''' 创建赛题
    print(POST_Create(url, params_POST_create, token))
    '''