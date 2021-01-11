# Is there a new wr?
Python script that checks speedrun.com for new WR in single game.
To use this script locally you have to:
- execute *createWRDatabase.py* to create initial database with WRs for list of games,
- execute *checkForNewWR.py* to compare existing WR database file with actual WRs on speedrun.com

To use Twitch bot you have to:
- execute *createWRDatabase.py* to create initial database with WRs for list of games,
- execute *Twitch_checkForNewWR.py* with following command `python3 Twitch_checkForNewWR.py <username> <client id> <token> <channel>`,
- type command *!checkforwr* in twitch chat and wait for results

More info abotu Twitch bot: https://twitchapps.com/tmi/ and https://github.com/twitchdev/chatbot-python-sample

In example I am using Grand Theft Auto series if you want to check WRs for another game/s you have to modify gamesList in both files.


# ToDo
- Modify script to get extended categories for games
