import os
import pandas as pd

# Define the directory containing the standardized season files
DATA_DIR = './data/files/StandardizedSeasonMatches'

# Ensure the output directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(os.path.join(DATA_DIR, "../TeamFiles"), exist_ok=True)
os.makedirs(os.path.join(DATA_DIR, "../Standings"), exist_ok=True)

# Helper function to extract season from file name
def extract_season_from_filename(filename):
    return filename.replace("EPLS", "").replace(".csv", "")[:4] + "/" + filename.replace("EPLS", "").replace(".csv", "")[4:]

# Load all seasonal files
all_data = []
for file in os.listdir(DATA_DIR):
    if file.startswith("EPLS") and file.endswith(".csv"):
        season = extract_season_from_filename(file)
        print(f"Processing file: {file}, Season: {season}")  # Debugging: Print file name and season
        try:
            # Read the CSV file with error handling for encoding and malformed rows
            season_data = pd.read_csv(
                os.path.join(DATA_DIR, file),
                encoding='latin1',  # Handle non-UTF-8 characters
                on_bad_lines='skip'  # Skip problematic lines
            )
            season_data['Season'] = season  # Add season column
            all_data.append(season_data)
        except pd.errors.ParserError as e:
            print(f"Error parsing file {file}: {e}")

# Combine all seasonal data into one DataFrame
data = pd.concat(all_data, ignore_index=True)

# Remove the Division column if it exists
if 'Div' in data.columns:
    data = data.drop(columns=['Div'])

# Create Team IDs as integers starting from 1
teams = pd.concat([data['HomeTeam'], data['AwayTeam']]).dropna().unique()
teams = [str(team) for team in teams]  # Ensure all team names are strings
team_id_map = {team: idx + 1 for idx, team in enumerate(teams)}  # Assign integer IDs starting from 1

# Add homeTeamID and awayTeamID columns using integer IDs
data['homeTeamID'] = data['HomeTeam'].map(team_id_map)
data['awayTeamID'] = data['AwayTeam'].map(team_id_map)

# Create Match IDs as integers starting from 1
data['matchID'] = range(1, len(data) + 1)

# Save all-time matches for each team
columns_to_keep = [
    'homeTeamID', 'awayTeamID', 'matchID', 'Date', 'HomeTeam', 'AwayTeam',
    'FTHG', 'FTAG', 'FTR', 'HTHG', 'HTAG', 'HTR', 'Referee', 'HS', 'AS',
    'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR', 'B365H',
    'B365D', 'B365A'
]

# Group all matches by team and save to individual files
for team in teams:
    team_matches = data[(data['HomeTeam'] == team) | (data['AwayTeam'] == team)]
    team_matches = team_matches[columns_to_keep]  # Keep only the specified columns
    team_matches.to_csv(os.path.join(DATA_DIR, "../TeamFiles", f"{team}AllTime.csv"), index=False)

# Create yearly standings
data['PointsHome'] = data['FTR'].map({'H': 3, 'D': 1, 'A': 0})
data['PointsAway'] = data['FTR'].map({'H': 0, 'D': 1, 'A': 3})

standings = []
for season in data['Season'].unique():
    season_data = data[data['Season'] == season]
    season_teams = pd.concat([season_data['HomeTeam'], season_data['AwayTeam']]).dropna().unique()
    season_teams = [str(team) for team in season_teams]  # Ensure all team names are strings
    teams_stats = []
    for team in season_teams:
        home_matches = season_data[season_data['HomeTeam'] == team]
        away_matches = season_data[season_data['AwayTeam'] == team]

        stats = {
            'TeamId': team_id_map.get(team),  # Use integer TeamId
            'Team': team,
            'Season': season,
            'MatchesPlayed': len(home_matches) + len(away_matches),
            'Wins': len(home_matches[home_matches['FTR'] == 'H']) + len(away_matches[away_matches['FTR'] == 'A']),
            'Draws': len(home_matches[home_matches['FTR'] == 'D']) + len(away_matches[away_matches['FTR'] == 'D']),
            'Losses': len(home_matches[home_matches['FTR'] == 'A']) + len(away_matches[away_matches['FTR'] == 'H']),
            'Points': home_matches['PointsHome'].sum() + away_matches['PointsAway'].sum(),
            'AvgB365H': pd.concat([home_matches['B365H'], away_matches['B365H']]).mean(),
            'AvgB365D': pd.concat([home_matches['B365D'], away_matches['B365D']]).mean(),
            'AvgB365A': pd.concat([home_matches['B365A'], away_matches['B365A']]).mean(),
        }

        # Calculate the overall average of B365H, B365D, and B365A
        stats['AvgB365Overall'] = (
            stats['AvgB365H'] + stats['AvgB365D'] + stats['AvgB365A']
        ) / 3

        # Add per-game and total stats for the requested columns
        for col in ['HS', 'AS', 'HST', 'AST', 'HC', 'AC', 'HF', 'AF', 'HY', 'AY', 'HR', 'AR']:
            stats[f"Total{col}"] = home_matches[col].sum() + away_matches[col].sum()
            stats[f"PerGame{col}"] = stats[f"Total{col}"] / stats['MatchesPlayed'] if stats['MatchesPlayed'] > 0 else 0

        teams_stats.append(stats)

    standings_df = pd.DataFrame(teams_stats)

    # Skip empty DataFrames
    if standings_df.empty:
        print(f"Debug: No data found for season {season}")
        continue

    # Reorder columns to place TeamId as the first column
    columns_order = ['TeamId'] + [col for col in standings_df.columns if col != 'TeamId']
    standings_df = standings_df[columns_order]

    standings_df = standings_df.sort_values(by='Points', ascending=False).reset_index(drop=True)
    standings_df.to_csv(os.path.join(DATA_DIR, "../Standings", f"EPLStandings{season.replace('/', '-')}.csv"), index=False)
    standings.append(standings_df)

# Create final dataset for all teams
history = []
for standing in standings:
    for _, row in standing.iterrows():
        history.append({
            'TeamId': row['TeamId'],
            'Team': row['Team'],
            'SeasonsPlayed': 1,  # Increment by 1 for each season the team appears
            'GamesPlayed': row['MatchesPlayed'],  # Total games played
            'Wins': row['Wins'],
            'Losses': row['Losses'],
            'Draws': row['Draws'],
            'Points': row['Points'],
            'PointsPerGame': row['Points'] / row['MatchesPlayed'] if row['MatchesPlayed'] > 0 else 0,
            'Relegations': 1 if row.name >= len(standing) - 3 else 0,
            'Titles': 1 if row.name == 0 else 0,
        })

history_df = pd.DataFrame(history)
history_df = history_df.groupby(['TeamId', 'Team']).agg({
    'SeasonsPlayed': 'sum',  # Sum up the seasons played
    'GamesPlayed': 'sum',  # Sum up the games played
    'Wins': 'sum',
    'Losses': 'sum',
    'Draws': 'sum',
    'Points': 'sum',
    'PointsPerGame': 'mean',
    'Relegations': 'sum',
    'Titles': 'sum',
}).reset_index()

history_df.to_csv(os.path.join(DATA_DIR, "../EPLHistory.csv"), index=False)