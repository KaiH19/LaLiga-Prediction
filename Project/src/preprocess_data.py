import pandas as pd

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    team_stats = []

    for season, season_df in df.groupby("Season"):
        season_teams = {}
        for _, row in season_df.iterrows():
            home, away = row['HomeTeam'], row['AwayTeam']
            fthg, ftag, ftr = row['FTHG'], row['FTAG'], row['FTR']

            for team in [home, away]:
                if team not in season_teams:
                    season_teams[team] = {
                        'Season': season, 'Team': team,
                        'Points': 0, 'GoalsScored': 0, 'GoalsConceded': 0,
                        'HomeWins': 0, 'AwayWins': 0, 'Matches': 0
                    }

            # Update stats
            season_teams[home]['GoalsScored'] += fthg
            season_teams[home]['GoalsConceded'] += ftag
            season_teams[away]['GoalsScored'] += ftag
            season_teams[away]['GoalsConceded'] += fthg
            season_teams[home]['Matches'] += 1
            season_teams[away]['Matches'] += 1

            if ftr == 'H':
                season_teams[home]['Points'] += 3
                season_teams[home]['HomeWins'] += 1
            elif ftr == 'A':
                season_teams[away]['Points'] += 3
                season_teams[away]['AwayWins'] += 1
            else:
                season_teams[home]['Points'] += 1
                season_teams[away]['Points'] += 1

        # Determine winner for that season
        sorted_teams = sorted(season_teams.values(), key=lambda x: x['Points'], reverse=True)
        for team_stat in sorted_teams:
            team_stat['GoalDifference'] = team_stat['GoalsScored'] - team_stat['GoalsConceded']
            team_stat['WinRate'] = (team_stat['HomeWins'] + team_stat['AwayWins']) / team_stat['Matches']
            team_stat['AvgGoals'] = team_stat['GoalsScored'] / team_stat['Matches']
            team_stat['Winner'] = 1 if team_stat == sorted_teams[0] else 0

        team_stats.extend(season_teams.values())

    return pd.DataFrame(team_stats)