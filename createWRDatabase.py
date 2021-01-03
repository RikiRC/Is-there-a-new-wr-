import requests, json

url = 'https://www.speedrun.com/api/v1/games/gtavc/records?top=1&miscellaneous=yes&scope=full-game'
headers = {
    'User-Agent': 'Is-there-a-new-wr/0.1'
}

httpRequestForGame = requests.get(url, headers=headers)
jsonData = json.loads(httpRequestForGame.text)

wr_database = {}
wr_database['data'] = []

for i in jsonData['data']:
    for j in i['runs']:
        wr = {
            'game': j['run']['game'],
            'category': j['run']['category'],
            'player': j['run']['players'][0]['id'],
            'id': j['run']['id']
        }
        wr_database['data'].append(wr)

jsonWrDatabase = json.dumps(wr_database, indent = 4)
with open("wrDatabase.json", "w") as outfile:
    outfile.write(jsonWrDatabase)
