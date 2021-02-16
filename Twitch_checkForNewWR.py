'''
Copyright 2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance with the License. A copy of the License is located at
    http://aws.amazon.com/apache2.0/
This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

Based on https://github.com/twitchdev/chatbot-python-sample
Modifications 2021 by RikiRC
'''
import sys, irc.bot, requests, json, jsondiff

class TwitchBot(irc.bot.SingleServerIRCBot):
    def __init__(self, username, client_id, token, channel):
        self.client_id = client_id
        self.token = token.removeprefix("oauth:")
        self.channel = '#' + channel.lower()

        url = 'https://api.twitch.tv/kraken/users?login=' + channel
        headers = {'Client-ID': client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
        r = requests.get(url, headers=headers).json()
        self.channel_id = r['users'][0]['_id']

        server = 'irc.chat.twitch.tv'
        port = 6667
        print('Connecting to ' + server + ' on port ' + str(port) + '...')
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, 'oauth:'+self.token)], username, username)

    def on_welcome(self, c, e):
        print('Joining ' + self.channel)
        c.join(self.channel)
        print('Joined ' + self.channel)
        c.privmsg(self.channel, "Connected!")

    def on_pubmsg(self, c, e):
        if e.arguments[0][:1] == '!':
            cmd = e.arguments[0].split(' ')[0][1:]
            print('Received command: ' + cmd)
            self.do_command(e, cmd)
        return

    def do_command(self, e, cmd):
        c = self.connection

        if cmd == "checkforwr":
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
                    url = 'https://api.twitch.tv/kraken/channels/' + self.channel_id
                    headers = {'Client-ID': self.client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
                    r = requests.get(url, headers=headers).json()
                    c.privmsg(self.channel, 'New WR: ' + jsonGameName + ' - ' + jsonCategoryName + ' ' + jsonRunStats + ' by ' + jsonPlayerName + ' Congratz! More info at: ' + jsonRunStatsWeblink)
                print('Saving updated WR database...')
                jsonWrDatabase = json.dumps(wr_database_temp, indent = 4)
                with open("wrDatabase.json", "w") as outfile:
                    outfile.write(jsonWrDatabase)
            else:
                url = 'https://api.twitch.tv/kraken/channels/' + self.channel_id
                headers = {'Client-ID': self.client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
                r = requests.get(url, headers=headers).json()
                c.privmsg(self.channel, 'There are no new WR')
                print()
        else:
            c.privmsg(self.channel, "Did not understand command: " + cmd)

def main():
    if len(sys.argv) != 5:
        print("Usage: twitchbot <username> <client id> <token> <channel>")
        sys.exit(1)

    username  = sys.argv[1]
    client_id = sys.argv[2]
    token     = sys.argv[3]
    channel   = sys.argv[4]

    bot = TwitchBot(username, client_id, token, channel)
    bot.start()

if __name__ == "__main__":
    main()
