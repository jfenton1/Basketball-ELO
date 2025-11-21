import pandas as pd

class Team:
    def __init__(self, id, key, name, mascot, conference):
        self.id = id
        self.key = key
        self.name = name
        self.mascot = mascot
        self.conference = conference
        self.elo = 1000
        self.wins = 0
        self.losses = 0
        if self.conference in ['Atlantic Coast', 'Big East', 'Big 12', 'Big Ten', 'Southeastern']:
            self.level = 3
        elif self.conference in ['American', 'Coastal Athletic Association', 'America East', 'Atlantic Sun', 'Conference USA', 'Big South', 'Atlantic 10', 'Mid-American', 'Big Sky', 'Summit', 'Western Athletic', 'Sun Belt', 'Big West', 'Missouri Valley', 'Horizon League', 'Ivy League', 'Metro Atlantic Athletic', 'Mid-Eastern', 'Southwestern Athletic', 'Mountain West', 'Northeast', 'Ohio Valley', 'Pac-12', 'Patriot League''Southern', 'Southland', 'West Coast']:
            self.level = 2
        elif self.conference in ['Eastern', 'Western']:
            self.level = 4
        else:
            self.level = 1

    def print_attributes(self):
        print(f"Team ID: {self.id} \nTeam Key: {self.key} \nSchool or City: {self.name} \nMascot: {self.mascot} \nCurrent ELO: {self.elo} \nConference: {self.conference} \nWins: {self.wins} \nLosses: {self.losses}")
    
    def set_elo(self, val):
        self.elo = val

    def print_elo(self):
        print(f'Team: {self.name} -- {self.elo}')

class Division:
    def __init__(self):
        self.teams = {}

    def add_team(self, id, key, school, mascot, conference):
        self.teams[id] = Team(id, key, school, mascot, conference)

    def print_teams(self):
        for team in self.teams.keys():
            if self.teams[team].elo >= 200:
                self.teams[team].print_attributes()
    
    def print_elos(self):
        for team in self.teams.keys():
            if self.teams[team].elo >= 200:
                self.teams[team].print_elo()
    
    def play_game(self, away_id, home_id, away_score, home_score, neutral_site):
        game_level = min(self.teams[home_id].level, self.teams[away_id].level)
        if game_level >= 3:
            k = 40
        elif game_level == 2:
            k = 20
        elif game_level == 1:
            k = 10
        else:
            k = 0
        j = 0
        # if (self.teams[home_id].conference != 0) and (self.teams[away_id].conference != 0):
        #     j += abs(home_score - away_score) / 3
        if self.teams[home_id].conference == 0:
            home_elo = 100
        else:
            home_elo = self.teams[home_id].elo
        if self.teams[away_id].conference == 0:
            away_elo = 100
        else:
            away_elo = self.teams[away_id].elo
        if neutral_site == 'False':
            home_elo += 40
        
        rating_diff = home_elo-away_elo
        div_400 = -1 * rating_diff / 400
        power = 10 ** div_400
        home_win_prob = 1 / (1 + power)
        away_win_prob = 1 - home_win_prob
        if home_score > away_score:
            if self.teams[away_id].conference in ['Atlantic Coast', 'Big East', 'Big 12', 'Big Ten', 'Southeastern']:
                j += abs(home_score - away_score) / 3
            elif self.teams[away_id].conference in ['American', 'Coastal Athletic Association', 'America East', 'Atlantic Sun', 'Conference USA', 'Big South', 'Atlantic 10', 'Mid-American', 'Big Sky', 'Summit', 'Western Athletic', 'Sun Belt', 'Big West', 'Missouri Valley', 'Horizon League', 'Ivy League', 'Metro Atlantic Athletic', 'Mid-Eastern', 'Southwestern Athletic', 'Mountain West', 'Northeast', 'Ohio Valley', 'Pac-12', 'Patriot League''Southern', 'Southland', 'West Coast']:
                j += abs(home_score - away_score) / 20
            adjustment = (away_win_prob * k) + j
            self.teams[home_id].set_elo(self.teams[home_id].elo + adjustment)
            self.teams[away_id].set_elo(away_elo - adjustment)
            self.teams[home_id].wins += 1
            self.teams[away_id].losses += 1
        else:
            if self.teams[home_id].conference in ['Atlantic Coast', 'Big East', 'Big 12', 'Big Ten', 'Southeastern']:
                j += abs(home_score - away_score) / 3
            elif self.teams[home_id].conference in ['American', 'Coastal Athletic Association', 'America East', 'Atlantic Sun', 'Conference USA', 'Big South', 'Atlantic 10', 'Mid-American', 'Big Sky', 'Summit', 'Western Athletic', 'Sun Belt', 'Big West', 'Missouri Valley', 'Horizon League', 'Ivy League', 'Metro Atlantic Athletic', 'Mid-Eastern', 'Southwestern Athletic', 'Mountain West', 'Northeast', 'Ohio Valley', 'Pac-12', 'Patriot League''Southern', 'Southland', 'West Coast']:
                j += abs(home_score - away_score) / 10
            adjustment = (home_win_prob * k) + j
            self.teams[home_id].set_elo(self.teams[home_id].elo - adjustment)
            self.teams[away_id].set_elo(away_elo + adjustment)
            self.teams[away_id].wins += 1
            self.teams[home_id].losses += 1

        return home_elo, away_elo, self.teams[home_id].elo, self.teams[away_id].elo, k, adjustment
    
    def to_csv(self, filename):
        results = []
        for team in self.teams:
            if self.teams[team].conference == 0:
                conf = 'n/a'
                elo = 100
            else:
                conf = self.teams[team].conference
                elo = self.teams[team].elo
            results.append({
                'ID': self.teams[team].id,
                'Key': self.teams[team].key,
                'Name': self.teams[team].name,
                'Mascot': self.teams[team].mascot,
                'Conference': conf,
                'ELO': elo,
                'Record': f'{self.teams[team].wins} - {self.teams[team].losses}'
            })
        
        results_df = pd.DataFrame(results)
        results_df = results_df.sort_values(by='ELO', ascending=False)

        results_df.to_csv(filename)