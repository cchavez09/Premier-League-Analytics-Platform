import requests
import pandas as pd
import os
import time
import json

API_TOKEN = 'ee9c76d4c4d34046ba22762d5802fd09'
BASE_URL = 'https://api.football-data.org/v4/'
HEADERS = {'X-Auth-Token': API_TOKEN}
DATA_DIR = './data/files/'

# Ensure the data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# Hardcoded list of English teams (IDs and names)
english_teams = [
    {'id': 57, 'name': 'Arsenal FC'},
    {'id': 58, 'name': 'Aston Villa FC'},
    {'id': 59, 'name': 'Blackburn Rovers FC'},
    {'id': 60, 'name': 'Bolton Wanderers FC'},
    {'id': 61, 'name': 'Chelsea FC'},
    {'id': 62, 'name': 'Everton FC'},
    {'id': 63, 'name': 'Fulham FC'},
    {'id': 64, 'name': 'Liverpool FC'},
    {'id': 65, 'name': 'Manchester City FC'},
    {'id': 66, 'name': 'Manchester United FC'},
    {'id': 67, 'name': 'Newcastle United FC'},
    {'id': 68, 'name': 'Norwich City FC'},
    {'id': 69, 'name': 'Queens Park Rangers FC'},
    {'id': 70, 'name': 'Stoke City FC'},
    {'id': 71, 'name': 'Sunderland AFC'},
    {'id': 72, 'name': 'Swansea City AFC'},
    {'id': 73, 'name': 'Tottenham Hotspur FC'},
    {'id': 74, 'name': 'West Bromwich Albion FC'},
    {'id': 75, 'name': 'Wigan Athletic FC'},
    {'id': 76, 'name': 'Wolverhampton Wanderers FC'},
    {'id': 322, 'name': 'Hull City AFC'},
    {'id': 325, 'name': 'Portsmouth FC'},
    {'id': 328, 'name': 'Burnley FC'},
    {'id': 332, 'name': 'Birmingham City FC'},
    {'id': 336, 'name': 'Blackpool FC'},
    {'id': 338, 'name': 'Leicester City FC'},
    {'id': 340, 'name': 'Southampton FC'},
    {'id': 341, 'name': 'Leeds United FC'},
    {'id': 342, 'name': 'Derby County FC'},
    {'id': 343, 'name': 'Middlesbrough FC'},
    {'id': 345, 'name': 'Sheffield Wednesday FC'},
    {'id': 346, 'name': 'Watford FC'},
    {'id': 347, 'name': 'AFC Wimbledon'},
    {'id': 348, 'name': 'Charlton Athletic FC'},
    {'id': 349, 'name': 'Ipswich Town FC'},
    {'id': 351, 'name': 'Nottingham Forest FC'},
    {'id': 354, 'name': 'Crystal Palace FC'},
    {'id': 355, 'name': 'Reading FC'},
    {'id': 356, 'name': 'Sheffield United FC'},
    {'id': 357, 'name': 'Barnsley FC'},
    {'id': 361, 'name': 'Rochdale AFC'},
    {'id': 363, 'name': 'Chesterfield FC'},
    {'id': 365, 'name': 'Colchester United FC'},
    {'id': 366, 'name': 'Torquay United FC'},
    {'id': 369, 'name': 'Walsall FC'},
    {'id': 370, 'name': 'Gillingham FC'},
    {'id': 376, 'name': 'Northampton Town FC'},
    {'id': 384, 'name': 'Millwall FC'},
    {'id': 385, 'name': 'Rotherham United FC'},
    {'id': 387, 'name': 'Bristol City FC'},
    {'id': 389, 'name': 'Luton Town FC'},
    {'id': 391, 'name': 'Notts County FC'},
    {'id': 393, 'name': 'Port Vale FC'},
    {'id': 394, 'name': 'Huddersfield Town AFC'},
    {'id': 396, 'name': 'Stockport County FC'},
    {'id': 397, 'name': 'Brighton & Hove Albion FC'},
    {'id': 399, 'name': 'Leyton Orient FC'},
    {'id': 400, 'name': 'Bristol Rovers FC'},
    {'id': 402, 'name': 'Brentford FC'},
    {'id': 409, 'name': 'Milton Keynes Dons FC'},
    {'id': 411, 'name': 'Cheltenham Town FC'},
    {'id': 563, 'name': 'West Ham United FC'},
    {'id': 1044, 'name': 'AFC Bournemouth'},
]

def fetch_data(endpoint):
    """Fetch data from the API."""
    response = requests.get(BASE_URL + endpoint, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data from {endpoint}: {response.status_code}")
        return None

def save_to_csv(data, filename):
    """Save data to a CSV file."""
    df = pd.json_normalize(data)
    df.to_csv(os.path.join(DATA_DIR, filename), index=False)

# Fetch and save individual match data
def fetch_and_save_match_data(match_id):
    """Fetch and save individual match data."""
    match_data = fetch_data(f"matches/{match_id}")
    if match_data:
        # Extract relevant information
        match_info = {
            "match_id": match_data["id"],
            "utcDate": match_data["utcDate"],
            "status": match_data["status"],
            "attendance": match_data.get("attendance", 0),  # Default to 0 if not available
            "venue": match_data.get("venue", "Unknown"),  # Default to "Unknown" if not available
            "home_team": match_data["homeTeam"]["name"],
            "away_team": match_data["awayTeam"]["name"],
            "home_score": match_data["score"]["fullTime"].get("home", 0),  # Default to 0 if not available
            "away_score": match_data["score"]["fullTime"].get("away", 0),  # Default to 0 if not available
            "goals": match_data.get("goals", []),  # Default to an empty list if not available
            "bookings": match_data.get("bookings", []),  # Default to an empty list if not available
            "substitutions": match_data.get("substitutions", []),  # Default to an empty list if not available
            "referees": match_data.get("referees", []),  # Default to an empty list if not available
            "statistics": match_data.get("statistics", {}),  # Default to an empty dictionary if not available
        }
        with open(f"match_{match_id}.json", 'w') as json_file:
            json.dump(match_info, json_file, indent=4)

# Example usage: Fetch and save match data for a specific match ID
match_id = 537848
fetch_and_save_match_data(match_id)

# Fetch and save data for person 38101
# person_id = 38101
# competitions = "PL"

# all_matches = []

# while True:
#     person_matches = fetch_data(f"persons/{person_id}/matches?e=ASSIST")
#     if person_matches and 'matches' in person_matches:
#         all_matches.extend(person_matches['matches'])
#     else:
#         break

# if all_matches:
#     save_to_csv(all_matches, f"person_{person_id}_career_assists.csv")
# Fetch and save data for each English team and year
# for team in english_teams:
#     team_id = team['id']
#     team_name = team['name']
#     total_matches = []
# # Define the date range for the 1979/80 season to the 2025/26 season
# date_from = "2000-08-01"
# date_to = "2026-05-31"

# # Fetch and save data for each English team
# for team in english_teams:
#     team_id = team['id']
#     team_name = team['name']
    
#     # Fetch all matches for the team within the date range
#     matches = fetch_data(f"teams/{team_id}/?matches/?dateFrom={date_from}/?dateTo={date_to}")
#     time.sleep(6)  # Wait 6 seconds between requests
#     if matches and 'matches' in matches:
#         # Save all matches for the team in a single CSV file
#         save_to_csv(matches['matches'], f"{team_name}_all_matches.csv")

#     # Save total matches for the team
#     if total_matches:
#         save_to_csv(total_matches, f"{team_name}_total.csv")
