import requests
import json
import main

def GET_Challenges(url, params_GET_challenges):
    r = requests.get(url+params_GET_challenges)
    return r.json()

def GET_NOT_DO(url, params_GET_NOT_DO,tid):
    r = requests.get(url+params_GET_NOT_DO+tid)
    return r.json()

def GET_record(url, params_GET_record,uuid):
    r = requests.get(url+params_GET_record+uuid)
    for i in r.json():
        print(i)

def GET_All_Rank(url, params_GET_all_rank):
    r = requests.get(url+params_GET_all_rank)
    for i in r.json():
        print(i)
    

def GET_Rank(url, params_GET_rank):
    r = requests.get(url+params_GET_rank)
    return r.json()


def POST_Create(url, params_POST_create, token):
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
    s = json.dumps(
        {
            "teamid": 42,
            "token": token
        }
    )
    r = requests.post(url+params_POST_start+uuid, data=s,headers={'Content-Type':'application/json'})
    return(r.json())


def POST_submit(url, params_POST_submit, token,uuid,path,swap):
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
    params_GET_challenges = 'api/challenge/list'
    params_GET_rank = 'api/teamdetail/42'
    params_GET_all_rank = 'api/rank'
    params_GET_NOT_DO = 'api/team/problem/'
    params_POST_create = 'api/challenge/create'
    params_POST_start = 'api/challenge/start/'
    params_POST_submit = 'api/challenge/submit'
    params_GET_record = 'api/challenge/record/'

    '''获得总排行榜
    GET_All_Rank(url,params_GET_all_rank)
    '''

    ''' 获得我们的排行榜
    rank = GET_Rank(url,params_GET_rank)
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
    


    '''获取未通过赛题
    challenges = GET_NOT_DO(url,params_GET_NOT_DO,'42')
    r = json.dumps(challenges,indent=4)
    with open('AI_Competition\challenges.json','w') as f:
        f.write(r)
    '''

    ''' 获取全部赛题
    challenges = GET_Challenges(url,params_GET_challenges)
    r = json.dumps(challenges,indent=4)
    with open('AI_Competition\challenges.json','w') as f:
        f.write(r)
    '''
    '''手动输入赛题uuid解题
    print("------------------载入中------------------")
    uuid = '13029caf-17f9-4f62-adbd-bcfbc6d2a373'  # 指定题目的uuid
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