"""GameDataHandler is responsible for loading Games info."""
from Game import Game
from WeatherHandler import WeatherHandler
from SqliteHandler import SqliteHandler


class GameDataHandler():

    def __init__(self, sqlite_handler: SqliteHandler,
                 weather_handler: WeatherHandler):
        """Short summary.

        Parameters
        ----------
        sqlite_handler : SqliteHandler
            Sqlite connection handler.
        weather_handler : WeatherHandler
            Weather Handler API handler.

        """
        self.sqlite_handler = sqlite_handler

        self.weather_handler = weather_handler

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
        # Store season_games
        season_games = []
        weather_info = {}

        # Request all season games.
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

            game = Game(
                game_data['id'],
                game_data['division'],
                game_data['season'],
                game_data['game_date'],
                game_data['home_team'],
                game_data['away_team'],
                game_data['ht_goals'],
                game_data['at_goals'],
                game_data['output'],
                bool(is_raining)
            )
            season_games.append(game)

        return season_games
