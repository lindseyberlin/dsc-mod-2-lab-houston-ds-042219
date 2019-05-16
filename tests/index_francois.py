# %%
%load_ext autoreload

%autoreload 2

# %%
from SqliteHandler import SqliteHandler
from WeatherHandler import WeatherHandler
from GameDataHandler import GameDataHandler
import config

sql_handler = SqliteHandler('database.sqlite')
weather_handler = WeatherHandler(config.API_key)
games_handler = GameDataHandler(sql_handler, weather_handler)

games = games_handler.get_games_per_season(2011)

# %%
print(games[0].away_team)
print(games[0].home_team)
print(games[0].ht_goals)
print(games[0].at_goals)
# print(games[0].is_raining())
print(games[0].is_raining)

print(games[0].has_team_won('dsds'))
print(games[0].has_team_won('Bayern Munich'))
