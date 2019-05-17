"""GameDataHandler is responsible for loading Games info."""
from Game import Game
from WeatherHandler import WeatherHandler
from SqliteHandler import SqliteHandler
from MongoHandler import MongoHandler


class GameDataHandler():

    GAMES_COLLECTION_NAME = 'games_collection'

    def __init__(self, sqlite_handler: SqliteHandler,
                 weather_handler: WeatherHandler,
                 mongo_handler: MongoHandler):
        """Short summary.

        Parameters
        ----------
        sqlite_handler : SqliteHandler
            Sqlite connection handler.
        weather_handler : WeatherHandler
            Weather Handler API handler.
        mongo_handler : MongoHandler
            Weather Handler API handler.

        """
        self.sqlite_handler = sqlite_handler
        self.weather_handler = weather_handler
        self.mongo_handler = mongo_handler

    def get_games_per_season(self, season: int):
        """Retrieve all games per season.

        Retrieves all games per season.

        Parameters
        ----------
        season : int
            Season for which we want the game list.

        Returns
        -------
        list
            List of Games.

        """
        # Check if already stored
        db_client = self.mongo_handler.get_client()
        games_collection = db_client[GameDataHandler.GAMES_COLLECTION_NAME]
        games = [record for record in games_collection.find({'season': season})]

        if not games:
            # Store season_games
            season_games = []
            weather_info = {}

            # Request all season games. We just retrieve data for D1 division
            # in order to lower our API credits cinsumption.
            cur = self.sqlite_handler.get_cursor()
            cur.execute("""
                SELECT Match_ID as id, Div as division, Season as season,
                Date as game_date, HomeTeam as home_team, AwayTeam as away_team,
                FTHG as ht_goals, FTAG as at_goals, FTR as output
                FROM Matches
                WHERE Season = {}
                AND Div = 'D1';
              """.format(season)
            )

            # Get record attributes
            attributes = [x[0] for x in cur.description]

            for row in cur.fetchall():
                # Build data dict
                game_data = dict(zip(attributes, row))

                # Retrieve weather info during game.
                is_raining = None
                if weather_info.get(game_data['game_date']):
                    is_raining = weather_info.get(game_data['game_date'])
                else:
                    is_raining = self.weather_handler.get_weather(
                        52.52437,
                        13.41053,
                        game_data['game_date']
                        )
                    weather_info[game_data['game_date']] = is_raining

                game_dict = {
                    'id': game_data['id'],
                    'division': game_data['division'],
                    'season': game_data['season'],
                    'game_date': game_data['game_date'],
                    'home_team': game_data['home_team'],
                    'away_team': game_data['away_team'],
                    'ht_goals': game_data['ht_goals'],
                    'at_goals': game_data['at_goals'],
                    'output': game_data['output'],
                    'is_raining': bool(is_raining)
                }
                season_games.append(game_dict)

            self.save_games_per_season(season_games)

        return [self.map_game_from_dict(record) for record in games_collection.find({'season': season})]

    def map_game_from_dict(self, game_dict: {}):
        return Game(
            game_dict['id'],
            game_dict['division'],
            game_dict['season'],
            game_dict['game_date'],
            game_dict['home_team'],
            game_dict['away_team'],
            game_dict['ht_goals'],
            game_dict['at_goals'],
            game_dict['output'],
            game_dict['is_raining']
        )

    def save_games_per_season(self, games: list):
        db_client = self.mongo_handler.get_client()
        games_collection = db_client[GameDataHandler.GAMES_COLLECTION_NAME]

        games_collection.insert_many(games)
