# Is there a new wr?
Python script that checks speedrun.com for new WR in single game.
To use this script you have to:
- execute *createWRDatabase.py* to create initial database with WRs for single game,
- execute *checkForNewWR.py* to compare existing WR database file with actual WRs on speedrun.com

In example I am using gta:vc if you want to check WRs for another game you have to change url in both files - https://github.com/speedruncomorg/api/blob/master/version1/games.md#get-gamesidrecords

# ToDo
- Create script for multiple games,
- Modify script to get extended categories for games,
- Integration with Twitter API,
- Integration with Twitch API,
