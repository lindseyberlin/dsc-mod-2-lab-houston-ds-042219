"""Game class."""


class Game():

    def __init__(self, id: int, division: str, season: str, date: str,
               home_team: str, away_team,
               ht_goals, at_goals, output, is_raining: bool):
        self.id = id
        self.division = division
        self.season = season
        self.date = date
        self.home_team = home_team
        self.away_team = away_team
        self.ht_goals = ht_goals
        self.at_goals = at_goals
        self.output = output
        self.is_raining = is_raining

    def is_team_playing(self, team_name):
        # check if team in game
        return team_name in [self.home_team, self.away_team]

    def is_team_home(self, team_name):
        # check if team is playing at home
        return team_name == self.home_team

    def has_team_won(self, team_name):
        if not self.is_team_playing(team_name):
            return None
        elif self.is_team_home(team_name):
            return self.ht_goals > self.at_goals
        else:
            return self.at_goals > self.ht_goals

    def team_goals(self, team_name):
        if not self.is_team_playing(team_name):
            return None
        elif self.is_team_home(team_name):
            return self.ht_goals
        else:
            return self.at_goals


