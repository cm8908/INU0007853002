# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%


# %% [markdown]
# https://somjang.tistory.com/entry/MongoDB-Python%EA%B3%BC-Pymongo%EB%A5%BC-%ED%99%9C%EC%9A%A9%ED%95%98%EC%97%AC-%EB%8D%B0%EC%9D%B4%ED%84%B0-%EC%B6%94%EA%B0%80%ED%95%98%EA%B3%A0-%EC%B6%9C%EB%A0%A5%ED%95%B4%EB%B3%B4%EA%B8%B0

# %%
import pandas as pd
import pymongo
from pymongo import MongoClient
import time
import logging
logging.basicConfig(filename='csv_log.txt', encoding='utf-8', level=logging.DEBUG)


# %%
client = MongoClient()
db = client['lol']


# %%
match_col = db['match']
matches = match_col.find()

# %% [markdown]
# # Features

# %%
part_info = ['summonerName', 'puuid', 'summonerLevel', 'win']

f_objectives = ['damageDealtToObjectives', 'baronKills', 'dragonKills','objectivesStolen', 'objectivesStolenAssists',
                'neutralMinionsKilled']

f_towers = ['firstTowerKill', 'firstTowerAssist','inhibitorKills','turretKills']

f_damages = ['damageDealtToTurrets', 'damageSelfMitigated','magicDamageDealt', 'magicDamageDealtToChampions', 'magicDamageTaken',
            'physicalDamageDealt','physicalDamageDealtToChampions', 'physicalDamageTaken','totalDamageDealt', 'totalDamageDealtToChampions',
             'totalDamageShieldedOnTeammates', 'totalDamageTaken','trueDamageDealt', 'trueDamageDealtToChampions', 
             'trueDamageTaken', 'totalHealsOnTeammates','totalHeal',   'totalTimeCCDealt','totalUnitsHealed']

f_sight = ['detectorWardsPlaced', 'visionWardsBoughtInGame', 'wardsKilled', 'wardsPlaced','visionScore']

f_champ = ['championName', 'champLevel', 'champExperience', 'individualPosition','role', 'lane','totalMinionsKilled']

f_kdas = ['kills', 'deaths', 'assists',  'firstBloodKill','firstBloodAssist','doubleKills','tripleKills','quadraKills', 'pentaKills',
         'unrealKills', 'bountyLevel','killingSprees']
f_gold = ['goldEarned', 'goldSpent', 'consumablesPurchased', 'itemsPurchased']

feature_list = []
for li in [part_info, f_kdas, f_objectives, f_towers, f_damages, f_sight, f_champ, f_gold]:
    feature_list.extend(li)
    
print(feature_list,'\n', len(feature_list))

# %% [markdown]
# # Tier

# %%
# from riotwatcher import LolWatcher, ApiError
# from LolCrawler.config import config

# watcher = LolWatcher(api_key=config['api_key'])


# def set_tier(part, dic):
#     id = part['summonerId']
#     try:
#         data = watcher.league.by_summoner('KR', id)[0]
#     except ApiError, Exception:
#         print('Exception has been raised. Sleeping for 1 min')
#         time.sleep(60)

#     data['tier'][0] # I B S G P D M GM C
#     if data['tier'][:2] == 'GO':
#         tier = 'G'
#     elif data['tier'][:2] == 'GR':
#         tier = 'GM'
#     else:
#         tier = data['tier'][0]
    
#     if data['rank'] == 'I':
#         rank = '1'
#     elif data['rank'] == 'II':
#         rank = '2'
#     elif data['rank'] == 'III':
#         rank = '3'
#     elif data['rank'] == 'IV':
#         rank = '4'
    
#     if tier in ['C', 'GM', 'M']:
#         dic['tier'] = tier
#     else:
#         dic['tier'] = tier+rank
#     dic['leaguePoints'] = data['leaguePoints']
#     dic['winrate'] = data['wins'] / data['wins']+data['losses']


# %% [markdown]
# # Preparing

# %%
#N = matches.count()
batch = 10000


i = 0
Dic = []
N = match_col.count_documents(filter={})
try:
    #for match in matches[i:i+batch]:
    while i < N:
        match = matches[i]
        if match['info']['gameMode'] == 'CLASSIC':
            if i%batch == 0 and i != 0:
                df = pd.DataFrame(Dic)
                fname = f'{i-batch}-{i-1}.csv'
                df.to_csv('data/'+fname, index=False, encoding='UTF-8')
                Dic = []

                curtime = time.strftime("%Y-%m-%d %H:%M:%S")
                logging.info(curtime+' :: '+fname+' was created')
                print(curtime+' :: '+fname+' was created')
                

            for part in match['info']['participants']:
                if part['lane'] == 'TOP' and part['teamPosition'] == 'TOP':
                    dic = {}
                    dic['gameId'] = match['info']['gameId']
                    dic['gameDuration'] = match['info']['gameDuration']
                    #set_tier(part, dic)
                    for f in feature_list:
                        dic[f] = part[f]
                    Dic.append(dic)
        i += 1


    df = pd.DataFrame(Dic)
    fname = f'LAST.csv'
    df.to_csv('data/'+fname, index=False, encoding='UTF-8')

    curtime = time.strftime("%Y-%m-%d %H:%M:%S")
    logging.info(curtime+' :: '+fname+' was created\nCSV CREATION OVER')
    Dic = []
except Exception as e:
    curtime = time.strftime("%Y-%m-%d %H:%M:%S")
    logging.error(curtime+' :: Exception has been raised. Last index was = '+i)
    logging.error(e)





# %%



