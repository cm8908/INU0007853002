# %%
import pymongo
from pymongo import MongoClient
import logging
logging.basicConfig(filename='log.txt', encoding='utf-8', level=logging.DEBUG)


# %%
client = MongoClient()
db = client['lol']

# %%
matchlist_col = db['matchlist']
#matchlists = matchlist_col.find(no_cursor_timeout=True)

# %% [markdown]
# # Tier

# %%
from riotwatcher import LolWatcher, ApiError
from LolCrawler.config import config
import time

watcher = LolWatcher(api_key=config['api_key'])

## get_tier
def get_tier(puuid):
    while True:
        try:
            summoner = watcher.summoner.by_puuid('KR', puuid) 
            time.sleep(3)
            data = watcher.league.by_summoner('KR', summoner['id'])
            time.sleep(3)
            if len(data) > 0:
                data = data[0]
            else:
                return 'U', 0, 0
            break
        except Exception as e:
            logging.error(time.strftime('%m-%d %H:%M :: ')+'[get_tier] Exception has been raised. Sleeping for 10 mins')
            logging.error(e)
            time.sleep(600)


    data['tier'][0] # I B S G P D M GM C
    if data['tier'][:2] == 'GO':
        tier = 'G'
    elif data['tier'][:2] == 'GR':
        tier = 'GM'
    else:
        tier = data['tier'][0]
    
    if data['rank'] == 'I':
        rank = '1'
    elif data['rank'] == 'II':
        rank = '2'
    elif data['rank'] == 'III':
        rank = '3'
    elif data['rank'] == 'IV':
        rank = '4'
    
    lp = data['leaguePoints']
    winrate = round(data['wins'] / (data['wins']+data['losses']) * 100, 2)

    if tier in ['C', 'GM', 'M']:
        return tier, lp, winrate
    else:
        return tier+rank, lp, winrate


# %% [markdown]
# # Do

# %%
# puuid = 'QY3_i7hwfkU5n9w0N57pOitmePy1LYp3J8B0nu9Qi-bsHyA0IW6Cq1tfRXW0qBDsfiWh3bkRkgpiJg'

# # %%
# for index, user in enumerate(matchlists):
#     if user['_id'] == puuid:
#         print(index)
    

# %%
#i = 35988
while True:
    matchlists = matchlist_col.find(filter={'extractions': {'region': 'ASIA'}}, no_cursor_timeout=True)
    try:
        for user in matchlists:
            puuid = user['_id']
            tier, lp, winrate = get_tier(puuid)
            user['extractions']['tier'] = tier
            user['extractions']['leaguePoints'] = lp
            user['extractions']['winrate'] = winrate
            matchlist_col.replace_one(filter={'_id': puuid}, replacement=user, upsert=False)
    except Exception as e:
        logging.error(time.strftime('%m-%d %H:%M :: ')+'[main] Exception has been raised. Sleeping for 10 min :: puuid = '+puuid)
        logging.error(e)
        matchlists = matchlist_col.find(filter={'extractions': {'region': 'ASIA'}}, no_cursor_timeout=True)
        # for index, user in enumerate(matchlists):
        #     if user['_id'] == puuid:
        #         i = index
        time.sleep(600)
        

# %%
from IPython.display import Audio
Audio('D:\long_success.wav', autoplay=True)


