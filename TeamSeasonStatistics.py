'''
TeamSeasonStatistics is responsible for parsing required statistics for the team per season, 
and for calculating further required statistics
'''
from Game import Game
from WeatherHandler import WeatherHandler
from SqliteHandler import SqliteHandler
from GameDataHandler import GameDataHandler

class TeamSeasonStatistics():
    def __init__(self, team_name, season, game_data_handler: GameDataHandler):
        self.team_name = team_name
        self.season = season
        self.game_data_handler = game_data_handler
        self.team_season_games = list(filter(lambda game: game.home_team == team_name 
            or game.away_team == team_name, self.game_data_handler.games))

    def get_statistics(self):
        # Gathers data from Game
        team_statistics = {
            "name": self.team_name,
            "season": self.season,
            "total_goals_scored": self.get_total_goals(),
            "total_wins": self.get_total_wins(),
            "rain_win_percentage": self.calculate_rain_win_pct()
        }
        return team_statistics
            
    
    def get_total_goals(self):
        # Calculates the sum of goals made by the team per season
        total_goals = 0

        for game in self.team_season_games:
            team_goals += game.team_goals(self.team_name)

        return total_goals
    
    def get_total_wins(self):
        # Sums number of wins per season
        total_wins = 0

        for game in self.team_season_games:
            if game.has_team_won(self.team_name):
                total_wins += 1

        return total_wins
    
    def calculate_rain_win_pct(self):
        # Calculates the percentage of games won while it was raining
        raining_wins = list(filter(lambda game: game.has_team_won() and game.is_raining, self.team_season_games))

        return (len(raining_wins)/ self.get_total_wins()) * 100