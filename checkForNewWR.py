import requests, json, jsondiff

url = 'https://www.speedrun.com/api/v1/games/gtavc/records?top=1&miscellaneous=yes&scope=full-game'
headers = {
    'User-Agent': 'Is-there-a-new-wr/0.1'
}

httpRequestForGame = requests.get(url, headers=headers)
jsonData = json.loads(httpRequestForGame.text)

wr_database_temp = {}
wr_database_temp['data'] = []

for i in jsonData['data']:
    for j in i['runs']:
        wr = {
            'game': j['run']['game'],
            'category': j['run']['category'],
            'player': j['run']['players'][0]['id'],
            'id': j['run']['id']            
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
        jsonGameName = json.loads(gameName.text)
        url = 'https://www.speedrun.com/api/v1/categories/'+newWrEntry[0]['category']
        categoryName = requests.get(url, headers=headers)
        jsonCategoryName = json.loads(categoryName.text)
        url = 'https://www.speedrun.com/api/v1/users/'+newWrEntry[0]['player']
        playerName = requests.get(url, headers=headers)
        jsonPlayerName = json.loads(playerName.text)
        url = 'https://www.speedrun.com/api/v1/runs/'+newWrEntry[0]['id']
        runStats = requests.get(url, headers=headers)
        jsonRunStats = json.loads(runStats.text)
        print('New WR: ' + jsonGameName['data']['names']['international'] + ' - ' + jsonCategoryName['data']['name'] + ' ' + jsonRunStats['data']['times']['primary'].replace('PT','').replace('H','h ').replace('M','m ').replace('S','s') + ' by ' + jsonPlayerName['data']['names']['international'] + ' Congratz! More info at: ' + jsonRunStats['data']['weblink'])
    print('Saving updated WR database...')
    jsonWrDatabase = json.dumps(wr_database_temp, indent = 4)
    with open("wrDatabase.json", "w") as outfile:
        outfile.write(jsonWrDatabase)
else:
    print('There are no new WR')