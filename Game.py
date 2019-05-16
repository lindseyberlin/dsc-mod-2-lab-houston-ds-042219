class Game():

    def __init(self, id: int, division: str, season: str, date: str,
               home_team: str, away_team,
               ht_goals, at_goals, output, is_raining):
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

    def is_raining(self):
        return self.is_raining

    def team_has_win(self, team_name):
        # check if team in game
        if team_name not in [self.home_team, self.away_team]:
            return None
        elif team_name == self.home_team:
            return self.ht_goals > self.at_goals
        elif team_name == self.away_team:
            return self.at_goals > self.ht_goals
