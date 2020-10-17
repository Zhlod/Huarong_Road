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
                "letter": "H",
                "exclude": 7,
                "challenge": [
                    [8, 9, 6],
                    [5, 0, 1],
                    [4, 2, 3]
                ],
                "step": 15,
                "swap": [1, 9]
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
    
    for i in range(8,len(challenges)):
        print("------------------载入中------------------")
        print('赛题uuid：',challenges[i]['uuid'])
        print('第',i,'题')
        start = POST_start(url, params_POST_start,challenges[i]['uuid'] , token) 
        print('剩余挑战次数：',start['chanceleft'])
        path, swap_pos = main.main(start['data']['img'],start['data']['step'],start['data']['swap'])
        POST_submit(url, params_POST_submit, token,start['uuid'],path,swap_pos)
        print(path, swap_pos)
    '''

    ''' 获取全部赛题
    challenges = GET_Challenges(url,params_GET_challenges)
    r = json.dumps(challenges,indent=4)
    with open('challenges.json','w') as f:
        f.write(r)
    '''
    '''                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
    print("------------------载入中------------------")
    print('赛题uuid：',challenges[2]['uuid'])
    start = POST_start(url, params_POST_start,challenges[2]['uuid'] , token) 
    print('剩余挑战次数：',start['chanceleft'])
    path, swap_pos = main.main(start['data']['img'],start['data']['step'],start['data']['swap'])
    POST_submit(url, params_POST_submit, token,start['uuid'],path,swap_pos)
    print(path, swap_pos)
    '''
    #GET_record(url,params_GET_record,'9f156155-403d-42a2-be6b-48facbde1fca')


    ''' 创建赛题
    POST_Create(url, params_POST_create, token)
    '''


    

    '''
    POST_submit(url, params_POST_submit, token,uuid,path,swap)
    '''