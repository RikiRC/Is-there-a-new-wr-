import requests, json

gamesList = ['gta1','gtal69','gtal61','gta2','gtaiii','gtaa','gtasa','gtalcs','gtavcs','gtaiv','gtatlad','gtacw','gtatbogt','gtao','gtav']

wr_database = {}
wr_database['data'] = []

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
            if playerType == 'user':
                wr = {
                    'game': k['run']['game'],
                    'category': k['run']['category'],
                    'playerType': k['run']['players'][0]['rel'],
                    'player': k['run']['players'][0]['id'],
                    'id': k['run']['id']
                }
                wr_database['data'].append(wr)
            elif playerType == 'guest':
                wr = {
                    'game': k['run']['game'],
                    'category': k['run']['category'],
                    'playerType': k['run']['players'][0]['rel'],
                    'player': k['run']['players'][0]['name'],
                    'id': k['run']['id']
                }
                wr_database['data'].append(wr)

jsonWrDatabase = json.dumps(wr_database, indent = 4)
with open("wrDatabase.json", "w") as outfile:
    outfile.write(jsonWrDatabase)
