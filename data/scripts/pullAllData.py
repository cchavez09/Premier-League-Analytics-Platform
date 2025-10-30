import os
import pandas as pd
import requests

# Directories
DATA_DIR = "data/files/StandardizedSeasonMatches"
TEAM_FILES_DIR = "data/files/TeamFiles"
STANDINGS_DIR = "data/files/Standings"
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(TEAM_FILES_DIR, exist_ok=True)
os.makedirs(STANDINGS_DIR, exist_ok=True)

# Columns to keep
columns_to_keep = [
    'homeTeamID', 'awayTeamID', 'MatchID', 'Date', 'HomeTeam', 'AwayTeam',
    'FTHG', 'FTAG', 'FTR', 'HTHG', 'HTAG', 'HTR', 'Referee', 'HS', 'AS',
    'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR', 'B365H',
    'B365D', 'B365A'
]


# Global match ID counter
match_id_counter = 1

team_data_map = {
    1: { "long_name": "Arsenal", "short_name": "Arsenal", "stadium": "Emirates Stadium, London" },
    2: { "long_name": "Aston Villa", "short_name": "Aston Villa", "stadium": "Villa Park, Birmingham" },
    3: { "long_name": "Birmingham", "short_name": "Birmingham", "stadium": "St Andrew's, Birmingham" },
    4: { "long_name": "Blackburn Rovers", "short_name": "Blackburn", "stadium": "Ewood Park, Blackburn" },
    5: { "long_name": "Blackpool", "short_name": "Blackpool", "stadium": "Bloomfield Road, Blackpool" },
    6: { "long_name": "Bolton Wanderers", "short_name": "Bolton", "stadium": "University of Bolton Stadium" },
    7: { "long_name": "Bournemouth", "short_name": "Bournemouth", "stadium": "Vitality Stadium, Bournemouth" },
    8: { "long_name": "Brentford", "short_name": "Brentford", "stadium": "Gtech Community Stadium, London" },
    9: { "long_name": "Brighton", "short_name": "Brighton", "stadium": "Amex Stadium, Brighton" },
    10: { "long_name": "Burnley", "short_name": "Burnley", "stadium": "Turf Moor, Burnley" },
    11: { "long_name": "Cardiff City", "short_name": "Cardiff", "stadium": "Cardiff City Stadium, Cardiff" },
    12: { "long_name": "Charlton Athletic", "short_name": "Charlton", "stadium": "The Valley, London" },
    13: { "long_name": "Chelsea", "short_name": "Chelsea", "stadium": "Stamford Bridge, London" },
    14: { "long_name": "Crystal Palace", "short_name": "Crystal Palace", "stadium": "Selhurst Park, London" },
    15: { "long_name": "Derby County", "short_name": "Derby", "stadium": "Pride Park, Derby" },
    16: { "long_name": "Everton", "short_name": "Everton", "stadium": "Goodison Park, Liverpool" },
    17: { "long_name": "Fulham", "short_name": "Fulham", "stadium": "Craven Cottage, London" },
    18: { "long_name": "Huddersfield Town", "short_name": "Huddersfield", "stadium": "John Smith’s Stadium, Huddersfield" },
    19: { "long_name": "Hull City", "short_name": "Hull", "stadium": "MKM Stadium, Hull" },
    20: { "long_name": "Ipswich Town", "short_name": "Ipswich", "stadium": "Portman Road, Ipswich" },
    21: { "long_name": "Leeds United", "short_name": "Leeds", "stadium": "Elland Road, Leeds" },
    22: { "long_name": "Leicester City", "short_name": "Leicester", "stadium": "King Power Stadium, Leicester" },
    23: { "long_name": "Liverpool", "short_name": "Liverpool", "stadium": "Anfield, Liverpool" },
    24: { "long_name": "Luton Town", "short_name": "Luton", "stadium": "Kenilworth Road, Luton" },
    25: { "long_name": "Manchester City", "short_name": "Man City", "stadium": "Etihad Stadium, Manchester" },
    26: { "long_name": "Manchester United", "short_name": "Man United", "stadium": "Old Trafford, Manchester" },
    27: { "long_name": "Middlesbrough", "short_name": "Middlesbrough", "stadium": "Riverside Stadium, Middlesbrough" },
    28: { "long_name": "Newcastle United", "short_name": "Newcastle", "stadium": "St James’ Park, Newcastle" },
    29: { "long_name": "Norwich City", "short_name": "Norwich", "stadium": "Carrow Road, Norwich" },
    30: { "long_name": "Nottingham Forest", "short_name": "Nott'm Forest", "stadium": "City Ground, Nottingham" },
    31: { "long_name": "Portsmouth", "short_name": "Portsmouth", "stadium": "Fratton Park, Portsmouth" },
    32: { "long_name": "Queens Park Rangers", "short_name": "QPR", "stadium": "Loftus Road, London" },
    33: { "long_name": "Reading", "short_name": "Reading", "stadium": "Select Car Leasing Stadium, Reading" },
    34: { "long_name": "Sheffield United", "short_name": "Sheffield United", "stadium": "Bramall Lane, Sheffield" },
    35: { "long_name": "Southampton", "short_name": "Southampton", "stadium": "St Mary’s Stadium, Southampton" },
    36: { "long_name": "Stoke City", "short_name": "Stoke", "stadium": "bet365 Stadium, Stoke-on-Trent" },
    37: { "long_name": "Sunderland", "short_name": "Sunderland", "stadium": "Stadium of Light, Sunderland" },
    38: { "long_name": "Swansea City", "short_name": "Swansea", "stadium": "Liberty Stadium, Swansea" },
    39: { "long_name": "Tottenham Hotspur", "short_name": "Tottenham", "stadium": "Tottenham Hotspur Stadium, London" },
    40: { "long_name": "Watford", "short_name": "Watford", "stadium": "Vicarage Road, Watford" },
    41: { "long_name": "West Bromwich Albion", "short_name": "West Brom", "stadium": "The Hawthorns, West Bromwich" },
    42: { "long_name": "West Ham United", "short_name": "West Ham", "stadium": "London Stadium, London" },
    43: { "long_name": "Wigan Athletic", "short_name": "Wigan", "stadium": "DW Stadium, Wigan" },
    44: { "long_name": "Wolverhampton Wanderers", "short_name": "Wolves", "stadium": "Molineux Stadium, Wolverhampton" },
}

# Create mappings for short names, long names, and team IDs
short_to_team_id = {info["short_name"]: team_id for team_id, info in team_data_map.items()}
long_to_team_id = {info["long_name"]: team_id for team_id, info in team_data_map.items()}
short_to_long_name = {info["short_name"]: info["long_name"] for info in team_data_map.values()}
def download_and_process_season(season_code, season_name):
    """Download and process a single season's data."""
    global match_id_counter
    url = f"https://www.football-data.co.uk/mmz4281/{season_code}/E0.csv"
    response = requests.get(url)
    
    if response.status_code == 200:
        # Save the raw CSV file
        raw_file_path = os.path.join(DATA_DIR, f"{season_name}.csv")
        with open(raw_file_path, "wb") as file:
            file.write(response.content)
        
        # Load the CSV into a DataFrame
        try:
            df = pd.read_csv(raw_file_path)
        except Exception as e:
            print(f"Error reading file {raw_file_path}: {e}")
            return
        
        expected_columns = [
            'Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR', 'HTHG', 'HTAG', 'HTR',
            'Referee', 'HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR',
            'B365H', 'B365D', 'B365A'
        ]
        missing_columns = [col for col in expected_columns if col not in df.columns]
        extra_columns = [col for col in df.columns if col not in expected_columns]

        if missing_columns:
            print(f"File {raw_file_path} is missing required columns: {missing_columns}. Skipping...")
            return
        
        if extra_columns:
            print(f"File {raw_file_path} has extra columns: {extra_columns}. These will be ignored.")
            df = df[expected_columns]  # Keep only the expected columns

        if df.isnull().any(axis=1).sum() > 0:
            print(f"Warning: {df.isnull().any(axis=1).sum()} rows with empty columns found in {raw_file_path}. These rows will be removed.")
            df = df.dropna()


        # Format the Date column to dd/mm/yyyy
        try:
            df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce').dt.strftime('%d/%m/%Y')
        except Exception as e:
            print(f"Error formatting dates in file {raw_file_path}: {e}")
            return
        # Replace short team names with long names
        df['HomeTeam'] = df['HomeTeam'].map(short_to_long_name).fillna(df['HomeTeam'])
        df['AwayTeam'] = df['AwayTeam'].map(short_to_long_name).fillna(df['AwayTeam'])

        # Map team names to unique IDs
        df['homeTeamID'] = df['HomeTeam'].map(long_to_team_id)
        df['awayTeamID'] = df['AwayTeam'].map(long_to_team_id)

        # Assign unique match IDs
        df['MatchID'] = range(match_id_counter, match_id_counter + len(df))
        match_id_counter += len(df)
        
        # Reorder columns to place IDs first
        id_columns = ['MatchID', 'homeTeamID', 'awayTeamID']
        other_columns = [col for col in df.columns if col not in id_columns]
        df = df[id_columns + other_columns]

        # Save the processed file
        processed_file_path = os.path.join(DATA_DIR, f"{season_name}.csv")
        df.to_csv(processed_file_path, index=False)
        print(f"Processed and saved: {processed_file_path}")
    else:
        print(f"Failed to download data for season {season_name} (HTTP {response.status_code})")
        
        

        
def pullalldata():
    """Download and process data for all seasons from 2005-06 to 2025-26."""
    # Generate season codes in ascending order (oldest to newest)
    season_codes = [
        "0506", "0607", "0708", "0809", "0910", 
        "1011", "1112", "1213", "1314", "1415", 
        "1516", "1617", "1718", "1819", "1920", 
        "2021", "2122", "2223", "2324", "2425", "2526"
    ]    
    print(f"Season codes to process: {season_codes}")
    for season_code in season_codes:
        season_name = f"EPLS{season_code}"
        download_and_process_season(season_code, season_name)


def pullrecentdata(season_code):
    """Download and process data for a specific season."""
    global match_id_counter

    try:
        # Load existing data to get the current match ID count
        all_files = [os.path.join(DATA_DIR, f) for f in os.listdir(DATA_DIR) if f.endswith(".csv")]
        if all_files:
            all_data_frames = []
            for file in all_files:
                try:
                    df = pd.read_csv(file)
                    all_data_frames.append(df)
                except Exception as e:
                    print(f"Error reading file {file}: {e}")
                    continue

            if all_data_frames:
                all_data = pd.concat(all_data_frames, ignore_index=True)
                if 'MatchID' in all_data.columns:
                    match_id_counter = all_data['MatchID'].max() + 1  # Set counter to the next available MatchID
                else:
                    print("Warning: 'MatchID' column not found in existing data. Starting from 1.")
                    match_id_counter = 1
            else:
                print("No valid data found in existing files. Starting from MatchID 1.")
                match_id_counter = 1
        else:
            print("No existing data files found. Starting from MatchID 1.")
            match_id_counter = 1

        # Process the specified season
        season_name = f"EPLS{season_code}"
        download_and_process_season(season_code, season_name)
        print(f"Season {season_code} has been downloaded and processed. Call updateyearlystandings('{season_code}') to update standings for this season.")
    except Exception as e:
        print(f"Error in pullrecentdata for season {season_code}: {e}")
        
def savealltimematches():
    """Save all-time matches for each team."""
    all_files = [os.path.join(DATA_DIR, f) for f in os.listdir(DATA_DIR) if f.endswith(".csv")]
    all_data_frames = []
    for f in all_files:
        try:
            print(f"Reading file: {f}")
            df = pd.read_csv(f)
            all_data_frames.append(df)
        except Exception as e:
            print(f"Error reading file {f}: {e}")
            continue

    if not all_data_frames:
        print("No valid data found.")
        return

    all_data = pd.concat(all_data_frames, ignore_index=True)
    
    for team_id, team_info in team_data_map.items():
        team = team_info["long_name"]
        team_matches = all_data[(all_data['HomeTeam'] == team) | (all_data['AwayTeam'] == team)]
        team_matches = team_matches[columns_to_keep]  # Keep only the specified columns
        
        # Save the team-specific dataset
        team_file_path = os.path.join(TEAM_FILES_DIR, f"{team}AllTime.csv")
        team_matches.to_csv(team_file_path, index=False)
        print(f"Updated team dataset saved: {team}AllTime.csv")


def createyearlystandings():
    """Create yearly standings with per-game and total stats."""
    all_files = [os.path.join(DATA_DIR, f) for f in os.listdir(DATA_DIR) if f.endswith(".csv")]
    all_data_frames = []

    for f in all_files:
        try:
            print(f"Reading file: {f}")
            df = pd.read_csv(f)

            # Extract the season from the file name (e.g., "EPLS0708.csv" -> "2007/08")
            season_code = os.path.basename(f).split('.')[0]  # Get the file name without extension
            season = f"20{season_code[-4:-2]}/20{season_code[-2:]}"  # Convert "0708" to "2007/08"

            # Add the Season column
            df['Season'] = season

            all_data_frames.append(df)
        except Exception as e:
            print(f"Error reading file {f}: {e}")
            continue

    if not all_data_frames:
        print("No valid data found.")
        return

    all_data = pd.concat(all_data_frames, ignore_index=True)

    # Map points for home and away matches
    all_data['PointsHome'] = all_data['FTR'].map({'H': 3, 'D': 1, 'A': 0})
    all_data['PointsAway'] = all_data['FTR'].map({'H': 0, 'D': 1, 'A': 3})

    standings = []
    for season in all_data['Season'].unique():
        season_data = all_data[all_data['Season'] == season]
        season_teams = pd.concat([season_data['HomeTeam'], season_data['AwayTeam']]).dropna().unique()
        season_teams = [str(team) for team in season_teams]  # Ensure all team names are strings
        teams_stats = []

        for team in season_teams:
            home_matches = season_data[season_data['HomeTeam'] == team]
            away_matches = season_data[season_data['AwayTeam'] == team]

            stats = {
                'TeamId': next((team_id for team_id, info in team_data_map.items() if info["long_name"] == team), None),
                'Team': team,
                'Season': season,
                'MatchesPlayed': len(home_matches) + len(away_matches),
                'Wins': len(home_matches[home_matches['FTR'] == 'H']) + len(away_matches[away_matches['FTR'] == 'A']),
                'Draws': len(home_matches[home_matches['FTR'] == 'D']) + len(away_matches[away_matches['FTR'] == 'D']),
                'Losses': len(home_matches[home_matches['FTR'] == 'A']) + len(away_matches[away_matches['FTR'] == 'H']),
                'Points': home_matches['PointsHome'].sum() + away_matches['PointsAway'].sum(),
                'GoalsScored': home_matches['FTHG'].sum() + away_matches['FTAG'].sum(),  # Add this line
                'GoalsConceded': home_matches['FTAG'].sum() + away_matches['FTHG'].sum(),  # Add this line
                'GoalDifference': (home_matches['FTHG'].sum() + away_matches['FTAG'].sum()) -
                                  (home_matches['FTAG'].sum() + away_matches['FTHG'].sum()),  # Add this line
            }

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
        # Add Rank column based on Points (higher points = lower rank)
        standings_df = standings_df.sort_values(by='Points', ascending=False).reset_index(drop=True)
        standings_df['Rank'] = standings_df.index + 1

        # Reorder columns to place TeamId and Rank as the first columns
        columns_order = ['TeamId', 'Rank'] + [col for col in standings_df.columns if col not in ['TeamId', 'Rank']]
        standings_df = standings_df[columns_order]

        standings_df = standings_df.sort_values(by='Points', ascending=False).reset_index(drop=True)
        standings_path = os.path.join(STANDINGS_DIR, f"EPLStandings{season.replace('/', '-')}.csv")
        standings_df.to_csv(standings_path, index=False)
        print(f"Standings for season {season} saved to {standings_path}")
        standings.append(standings_df)

def createfinaldataset():
    """Create the final dataset with all relevant stats, including rank, relegations, and titles."""
    try:
        # Load yearly standings
        all_files = [os.path.join(STANDINGS_DIR, f) for f in os.listdir(STANDINGS_DIR) if f.endswith(".csv")]
        all_data_frames = []

        for f in all_files:
            print(f"Reading standings file: {f}")
            df = pd.read_csv(f)

            # Ensure TeamId is present
            if 'TeamId' not in df.columns:
                print(f"Warning: 'TeamId' column missing in {f}. Attempting to map TeamId...")
                df['TeamId'] = df['Team'].map(
                    lambda team: next((team_id for team_id, info in team_data_map.items() if info["long_name"] == team), None)
                )

            # Ensure Rank column is present
            if 'Rank' not in df.columns:
                print(f"Error: 'Rank' column missing in {f}. Skipping this file.")
                continue

            # Add Relegations and Titles columns
            df['Relegations'] = (df['Rank'] > 16).astype(int)  # 1 if rank > 16, else 0
            df['Titles'] = (df['Rank'] == 1).astype(int)  # 1 if rank == 1, else 0

            all_data_frames.append(df)

        if not all_data_frames:
            print("No valid standings data found.")
            return

        all_data = pd.concat(all_data_frames, ignore_index=True)

        # Create the final dataset
        final_dataset = []
        for _, row in all_data.iterrows():
            try:
                final_dataset.append({
                    'TeamId': row['TeamId'],
                    'Team': row['Team'],
                    'Season': row['Season'],
                    'Rank': row['Rank'],
                    'MatchesPlayed': row['MatchesPlayed'],
                    'Wins': row['Wins'],
                    'Draws': row['Draws'],
                    'Losses': row['Losses'],
                    'Points': row['Points'],
                    'GoalsScored': row['GoalsScored'],
                    'GoalsConceded': row['GoalsConceded'],
                    'GoalDifference': row['GoalDifference'],
                    'Relegations': row['Relegations'],
                    'Titles': row['Titles'],
                })
            except KeyError as e:
                print(f"Error processing row: {row}. Missing column: {e}")
                continue

        final_df = pd.DataFrame(final_dataset)

        # Save the final dataset
        final_dataset_path = os.path.join(DATA_DIR, "OverallTeamStats.csv")
        final_df.to_csv(final_dataset_path, index=False)
        print(f"Final dataset saved to {final_dataset_path}")

    except Exception as e:
        print(f"Error creating final dataset: {e}")

def updateyearlystandings(season_code):
    """Update yearly standings for a specific season."""
    try:
        # Load the processed season data
        season_file = os.path.join(DATA_DIR, f"EPLS{season_code}.csv")
        if not os.path.exists(season_file):
            print(f"Season file for {season_code} not found. Run download_and_process_season() first.")
            return

        print(f"Updating standings for season {season_code} using file {season_file}")
        df = pd.read_csv(season_file)

        # Extract the season (e.g., "0708" -> "2007/08")
        season = f"20{season_code[:2]}/20{season_code[2:]}"

        # Map points for home and away matches
        df['PointsHome'] = df['FTR'].map({'H': 3, 'D': 1, 'A': 0})
        df['PointsAway'] = df['FTR'].map({'H': 0, 'D': 1, 'A': 3})

        # Calculate standings for the season
        season_teams = pd.concat([df['HomeTeam'], df['AwayTeam']]).dropna().unique()
        season_teams = [str(team) for team in season_teams]  # Ensure all team names are strings
        teams_stats = []

        for team in season_teams:
            home_matches = df[df['HomeTeam'] == team]
            away_matches = df[df['AwayTeam'] == team]

            stats = {
                'TeamId': next((team_id for team_id, info in team_data_map.items() if info["long_name"] == team), None),
                'Team': team,
                'Season': season,
                'MatchesPlayed': len(home_matches) + len(away_matches),
                'Wins': len(home_matches[home_matches['FTR'] == 'H']) + len(away_matches[away_matches['FTR'] == 'A']),
                'Draws': len(home_matches[home_matches['FTR'] == 'D']) + len(away_matches[away_matches['FTR'] == 'D']),
                'Losses': len(home_matches[home_matches['FTR'] == 'A']) + len(away_matches[away_matches['FTR'] == 'H']),
                'Points': home_matches['PointsHome'].sum() + away_matches['PointsAway'].sum(),
                'GoalsScored': home_matches['FTHG'].sum() + away_matches['FTAG'].sum(),
                'GoalsConceded': home_matches['FTAG'].sum() + away_matches['FTHG'].sum(),
                'GoalDifference': (home_matches['FTHG'].sum() + away_matches['FTAG'].sum()) -
                                  (home_matches['FTAG'].sum() + away_matches['FTHG'].sum()),
            }

            # Add per-game and total stats for the requested columns
            for col in ['HS', 'AS', 'HST', 'AST', 'HC', 'AC', 'HF', 'AF', 'HY', 'AY', 'HR', 'AR']:
                stats[f"Total{col}"] = home_matches[col].sum() + away_matches[col].sum()
                stats[f"PerGame{col}"] = stats[f"Total{col}"] / stats['MatchesPlayed'] if stats['MatchesPlayed'] > 0 else 0

            teams_stats.append(stats)

        standings_df = pd.DataFrame(teams_stats)

        # Skip empty DataFrames
        if standings_df.empty:
            print(f"No data found for season {season}")
            return

        # Add Rank column based on Points (higher points = lower rank)
        standings_df = standings_df.sort_values(by='Points', ascending=False).reset_index(drop=True)
        standings_df['Rank'] = standings_df.index + 1

        # Reorder columns to place TeamId and Rank as the first columns
        columns_order = ['TeamId', 'Rank'] + [col for col in standings_df.columns if col not in ['TeamId', 'Rank']]
        standings_df = standings_df[columns_order]
        
        standings_df = standings_df.sort_values(by='Points', ascending=False).reset_index(drop=True)
        standings_path = os.path.join(STANDINGS_DIR, f"EPLStandings{season.replace('/', '-')}.csv")
        standings_df.to_csv(standings_path, index=False)
        print(f"Standings for season {season} saved to {standings_path}")
    except Exception as e:
        print(f"Error updating yearly standings for season {season_code}: {e}")
        
pullalldata()