# NBA Injury Report Bot

A Discord bot that provides injury reports for NBA players each night for each games. The bot uses the [Sportsdata IO API](https://sportsdata.io/developers/api-documentation/nba) to retrieve injury reports for NBA players and webscrapes the [Basketball Reference](https://www.basketball-reference.com/) website. I use it for a Fantasy Basketball league and I wanted to automate the process of checking the injury reports for each game.

## Overview

To launch the bot you just need to run the 'bot.py' file like this:

```bash
python3 bot.py
```

The bot will create JSON files with the data and fill  the list of injuries. Afterward, it will be up and running and will be able to provide injury reports 1 hour before the first game of each night.