import requests
import json
import pandas as pd
import datetime
from Teams import Team, Division

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def ncaa_elo(n):
    # Will be the real logic. Don't want to waste calls.
    input_date = datetime.date.today() - datetime.timedelta(days=1)
    res = requests.get(f'https://api.sportsdata.io/v3/cbb/scores/json/GamesByDateFinal/{input_date}?key=4854866e22114b1281822c787c0c8185')
    response = json.loads(res.text)
    # print(response)

    games_df = pd.DataFrame(response)

    while input_date > datetime.date(2025, 11, 3):
        input_date -= datetime.timedelta(days=1)
        res = requests.get(f'https://api.sportsdata.io/v3/cbb/scores/json/GamesByDateFinal/{input_date}?key=4854866e22114b1281822c787c0c8185')
        response = json.loads(res.text)
        temp_df = pd.DataFrame(response)
        games_df = pd.concat([games_df, temp_df])
        # print(len(df))

    games_df.to_csv('current_ncaa_games.csv')

    res = requests.get(f'https://api.sportsdata.io/v3/cbb/scores/json/teams?key=4854866e22114b1281822c787c0c8185')
    response = json.loads(res.text)
    teams_df = pd.DataFrame(response)
    teams_df.to_csv('ncaa_teams.csv')
    # print(teams_df.Conference.unique())


    # games_df = pd.read_csv('current_games.csv')
    # teams_df = pd.read_csv('teams.csv')

    # print(teams_df[teams_df.TeamID == 769])
    # print(teams_df[teams_df.TeamID == 224])

    # teams_df = teams_df.dropna(subset=['Conference'])

    # print(teams_df.head())
    # print(len(teams_df))
    # print(len(teams_df[teams_df.Active == True]))
    # print(sum(teams_df.Conference.value_counts()))

    games_df = games_df[games_df.Status == 'Final']
    games_df = games_df[['Status', 'Day', 'DateTime', 'AwayTeam', 'HomeTeam', 'AwayTeamID', 'HomeTeamID', 'AwayTeamScore', 'HomeTeamScore', 'NeutralVenue']]
    teams_df = teams_df[['TeamID', 'Key', 'School', 'Name', 'Conference']]
    teams_df.Conference = teams_df.Conference.fillna(0)

    # print(len(games_df))
    games_df = games_df.merge(teams_df, how='left', left_on='AwayTeamID', right_on='TeamID')
    games_df.columns = ['Status', 'Day', 'DateTime', 'AwayTeam', 'HomeTeam', 'AwayTeamID', 'HomeTeamID', 'AwayTeamScore', 'HomeTeamScore', 'NeutralVenue', 'AwayID', 'AwayKey', 'AwaySchool', 'AwayName', 'AwayConference']
    # print(len(games_df))
    games_df = games_df.merge(teams_df, how='left', left_on='HomeTeamID', right_on='TeamID')
    games_df.columns = ['Status', 'Day', 'DateTime', 'AwayTeam', 'HomeTeam', 'AwayTeamID', 'HomeTeamID', 'AwayTeamScore', 'HomeTeamScore', 'NeutralVenue', 'AwayID', 'AwayKey', 'AwaySchool', 'AwayName', 'AwayConference', 'HomeID', 'HomeKey', 'HomeSchool', 'HomeName', 'HomeConference']
    # print(len(games_df))
    # print(games_df.head())
    # print(teams_df.head())

    # test_team = Team(teams_df['TeamID'].iloc[0], teams_df['Key'].iloc[0], teams_df['School'].iloc[0], teams_df['Name'].iloc[0])
    # test_team.print_attributes()

    # test_division = Division()
    # test_division.add_team(teams_df['TeamID'].iloc[0], teams_df['Key'].iloc[0], teams_df['School'].iloc[0], teams_df['Name'].iloc[0])
    # test_division.add_team(teams_df['TeamID'].iloc[1], teams_df['Key'].iloc[1], teams_df['School'].iloc[1], teams_df['Name'].iloc[1])
    # test_division.print_teams()

    division = Division()

    for i in range(len(teams_df)):
        division.add_team(teams_df['TeamID'].iloc[i], teams_df['Key'].iloc[i], teams_df['School'].iloc[i], teams_df['Name'].iloc[i], teams_df['Conference'].iloc[i])

    # division.teams[101].print_attributes()

    # print(division.play_game(101, 1, 10, 20, 0))
    # print(games_df.loc[399])
    for p in range(n):
        for i in range(len(games_df)):
            division.play_game(games_df.AwayTeamID.iloc[i], games_df.HomeTeamID.iloc[i], games_df.AwayTeamScore.iloc[i], games_df.HomeTeamScore.iloc[i], games_df.NeutralVenue.iloc[i])
    #     if (games_df.AwayTeamID.iloc[i] == 101) or (games_df.HomeTeamID.iloc[i] == 101):
    #         print('Game ' + str(i))
    #         division.teams[games_df.AwayTeamID.iloc[i]].print_attributes()
    #         print('vs.')
    #         division.teams[games_df.HomeTeamID.iloc[i]].print_attributes()

    # division.print_elos()

    division.to_csv('current_elos.csv')

# ncaa_elo(2)

def nba_elo(n):
    # Will be the real logic. Don't want to waste calls.
    input_date = datetime.date.today() - datetime.timedelta(days=1)
    res = requests.get(f'https://api.sportsdata.io/v3/nba/scores/json/ScoresBasicFinal/{input_date}?key=4854866e22114b1281822c787c0c8185')
    response = json.loads(res.text)
    # print(response)

    games_df = pd.DataFrame(response)
    

    
    while input_date > datetime.date(2025, 10, 21):
        input_date -= datetime.timedelta(days=1)
        res = requests.get(f'https://api.sportsdata.io/v3/nba/scores/json/ScoresBasicFinal/{input_date}?key=4854866e22114b1281822c787c0c8185')
        response = json.loads(res.text)
        temp_df = pd.DataFrame(response)
        games_df = pd.concat([games_df, temp_df])
        # print(len(df))

    games_df = games_df.sort_values(by='DateTime', ascending=True)
    print(games_df.head())
    games_df.to_csv('current_nba_games.csv')
    # print(games_df.head())
    
    res = requests.get(f'https://api.sportsdata.io/v3/nba/scores/json/AllTeams?key=4854866e22114b1281822c787c0c8185')
    response = json.loads(res.text)
    teams_df = pd.DataFrame(response)
    teams_df.to_csv('nba_teams.csv')
    
    # print(teams_df.Conference.unique())

    """
    # games_df = pd.read_csv('current_games.csv')
    # teams_df = pd.read_csv('teams.csv')

    # print(teams_df[teams_df.TeamID == 769])
    # print(teams_df[teams_df.TeamID == 224])

    # teams_df = teams_df.dropna(subset=['Conference'])

    # print(teams_df.head())
    # print(len(teams_df))
    # print(len(teams_df[teams_df.Active == True]))
    # print(sum(teams_df.Conference.value_counts()))
    """
    
    games_df = games_df[(games_df.Status.isin(['Final', 'F/OT']))]
    games_df = games_df[['Status', 'Day', 'DateTime', 'AwayTeam', 'HomeTeam', 'AwayTeamID', 'HomeTeamID', 'AwayTeamScore', 'HomeTeamScore', 'NeutralVenue']]
    teams_df = teams_df[['TeamID', 'Key', 'City', 'Name', 'Conference']]
    teams_df.Conference = teams_df.Conference.fillna(0)
    # print(teams_df)
    
    # print(len(games_df))
    games_df = games_df.merge(teams_df, how='left', left_on='AwayTeamID', right_on='TeamID')
    games_df.columns = ['Status', 'Day', 'DateTime', 'AwayTeam', 'HomeTeam', 'AwayTeamID', 'HomeTeamID', 'AwayTeamScore', 'HomeTeamScore', 'NeutralVenue', 'AwayID', 'AwayKey', 'AwayCity', 'AwayName', 'AwayConference']
    # print(len(games_df))
    games_df = games_df.merge(teams_df, how='left', left_on='HomeTeamID', right_on='TeamID')
    games_df.columns = ['Status', 'Day', 'DateTime', 'AwayTeam', 'HomeTeam', 'AwayTeamID', 'HomeTeamID', 'AwayTeamScore', 'HomeTeamScore', 'NeutralVenue', 'AwayID', 'AwayKey', 'AwayCity', 'AwayName', 'AwayConference', 'HomeID', 'HomeKey', 'HomeCity', 'HomeName', 'HomeConference']
    # print(len(games_df))
    # print(games_df.head())
    
    # print(games_df.head())
    # print(teams_df.head())

    # test_team = Team(teams_df['TeamID'].iloc[0], teams_df['Key'].iloc[0], teams_df['City'].iloc[0], teams_df['Name'].iloc[0], teams_df['Conference'].iloc[0])
    # test_team.print_attributes()
    
    # test_division = Division()
    # test_division.add_team(teams_df['TeamID'].iloc[0], teams_df['Key'].iloc[0], teams_df['City'].iloc[0], teams_df['Name'].iloc[0], teams_df['Conference'].iloc[0])
    # test_division.add_team(teams_df['TeamID'].iloc[1], teams_df['Key'].iloc[1], teams_df['City'].iloc[1], teams_df['Name'].iloc[1], teams_df['Conference'].iloc[1])
    # test_division.print_teams()
    
    division = Division()

    for i in range(len(teams_df)):
        division.add_team(teams_df['TeamID'].iloc[i], teams_df['Key'].iloc[i], teams_df['City'].iloc[i], teams_df['Name'].iloc[i], teams_df['Conference'].iloc[i])

    # division.teams[101].print_attributes()

    # print(division.play_game(6, 1, 10, 20, 0))
    # print(games_df.loc[399])
    for p in range(n):
        for i in range(len(games_df)):
            division.play_game(games_df.AwayTeamID.iloc[i], games_df.HomeTeamID.iloc[i], games_df.AwayTeamScore.iloc[i], games_df.HomeTeamScore.iloc[i], games_df.NeutralVenue.iloc[i])
    #     if (games_df.AwayTeamID.iloc[i] == 101) or (games_df.HomeTeamID.iloc[i] == 101):
    #         print('Game ' + str(i))
    #         division.teams[games_df.AwayTeamID.iloc[i]].print_attributes()
    #         print('vs.')
    #         division.teams[games_df.HomeTeamID.iloc[i]].print_attributes()

    # division.print_elos()

    division.to_csv('current_nba_elos.csv')
    

# nba_elo(1)

def main_function():
    which_level = input('Would you like to compute the ELOs for current NBA or NCAAM teams? (NBA/NCAA) ')

    if which_level == 'NBA':
        nba_elo(1)
    elif which_level in ['NCAA', 'NCAAM']:
        ncaa_elo(1)
    else:
        print('Not a valid response. Please try again with \'NBA\' or \'NCAA\'')

main_function()