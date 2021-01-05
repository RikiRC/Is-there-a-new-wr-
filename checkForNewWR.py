import requests, json, jsondiff

gamesList = ['gta1','gtal69','gtal61','gta2','gtaiii','gtaa','gtasa','gtalcs','gtavcs','gtaiv','gtatlad','gtacw','gtatbogt','gtao','gtav']

wr_database_temp = {}
wr_database_temp['data'] = []

for i in gamesList:
    url = 'https://www.speedrun.com/api/v1/games/'+i+'/records?top=1&miscellaneous=yes&scope=full-game&max=200'
    headers = {
        'User-Agent': 'Is-there-a-new-wr/0.2'
    }
    httpRequestForGame = requests.get(url, headers=headers)
    jsonData = json.loads(httpRequestForGame.text)
    for j in jsonData['data']:
        for k in j['runs']:
            playerType = k['run']['players'][0]['rel']
            if playerType == 'guest':
                wr = {
                    'game': k['run']['game'],
                    'category': k['run']['category'],
                    'playerType': k['run']['players'][0]['rel'],
                    'player': k['run']['players'][0]['name'],
                    'id': k['run']['id']
                }
                wr_database_temp['data'].append(wr)
            elif playerType == 'user':
                wr = {
                    'game': k['run']['game'],
                    'category': k['run']['category'],
                    'playerType': k['run']['players'][0]['rel'],
                    'player': k['run']['players'][0]['id'],
                    'id': k['run']['id']
                }
                wr_database_temp['data'].append(wr)

with open('wrDatabase.json') as wrDatabaseJson:
    wrDatabase = json.load(wrDatabaseJson)

checkDiff = jsondiff.diff(wrDatabase, wr_database_temp)

if checkDiff != {}:
    for k in checkDiff['data']:
        idTest = checkDiff['data'][k]['id']
        newWrEntry = list(filter(lambda x:x['id']==idTest,wr_database_temp['data']))
        url = 'https://www.speedrun.com/api/v1/games/'+newWrEntry[0]['game']
        gameName = requests.get(url, headers=headers)
        jsonGameName = json.loads(gameName.text)['data']['names']['international']
        url = 'https://www.speedrun.com/api/v1/categories/'+newWrEntry[0]['category']
        categoryName = requests.get(url, headers=headers)
        jsonCategoryName = json.loads(categoryName.text)['data']['name']
        url = 'https://www.speedrun.com/api/v1/runs/'+newWrEntry[0]['id']
        runStats = requests.get(url, headers=headers)
        jsonRunStats = json.loads(runStats.text)['data']['times']['primary']
        jsonRunStats = jsonRunStats.replace('PT','').replace('H','h ').replace('M','m ').replace('S','s')
        jsonRunStatsWeblink = json.loads(runStats.text)['data']['weblink']
        if newWrEntry[0]['playerType'] == 'user':
            url = 'https://www.speedrun.com/api/v1/users/'+newWrEntry[0]['player']
            playerName = requests.get(url, headers=headers)
            jsonPlayerName = json.loads(playerName.text)['data']['names']['international'] 
        elif newWrEntry[0]['playerType'] == 'guest':
            jsonPlayerName = newWrEntry[0]['player']
        print('New WR: ' + jsonGameName + ' - ' + jsonCategoryName + ' ' + jsonRunStats + ' by ' + jsonPlayerName + ' Congratz! More info at: ' + jsonRunStatsWeblink)
    print('Saving updated WR database...')
    jsonWrDatabase = json.dumps(wr_database_temp, indent = 4)
    with open("wrDatabase.json", "w") as outfile:
        outfile.write(jsonWrDatabase)
else:
    print('There are no new WR')
