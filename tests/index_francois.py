# %%
%load_ext autoreload
%autoreload 2

# %%
from SqliteHandler import SqliteHandler
from MongoHandler import MongoHandler
from WeatherHandler import WeatherHandler
from GameDataHandler import GameDataHandler
import config

sql_handler = SqliteHandler(config.STAT_SQLITE_DB)
weather_handler = WeatherHandler(config.API_key)
mongo_handler = MongoHandler(config.STAT_MONGO_CONNECTION, config.STAT_MONGO_DB_NAME)
games_handler = GameDataHandler(sql_handler, weather_handler, mongo_handler)

games = games_handler.get_games_per_season(2011)

# %%
games

# %%
print(games[0].away_team)
print(games[0].home_team)
print(games[0].ht_goals)
print(games[0].at_goals)
# print(games[0].is_raining())
print(games[0].is_raining)

print(games[0].has_team_won('dsds'))
print(games[0].has_team_won('Bayern Munich'))

# %%
from TeamSeasonStatistics import TeamSeasonStatistics

stats_bayern = TeamSeasonStatistics('Bayern Munich', 2011, games_handler, mongo_handler)

stats_bayern.get_statistics()
stats_bayern.save()
