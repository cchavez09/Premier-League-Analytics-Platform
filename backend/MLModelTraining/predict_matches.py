import pandas as pd
import numpy as np
from pathlib import Path
import joblib
from typing import Dict, Tuple, Optional


class CrossSeasonMatchPredictor:
    # Final variables for data and model paths
    BASE_DIR = Path(__file__).parent.parent.parent
    DATA_DIR = BASE_DIR / "data" / "files" / "StandardizedSeasonMatches"
    MODEL_DIR = BASE_DIR / "data" / "files" / "MLModels"
    MODEL_NAME = "historical_ensemble.pkl"
    SCALER_NAME = "historical_scaler.pkl"
    FEATURES_NAME = "historical_features.pkl"

    def __init__(self):
        """Initialize the predictor with model and team mapping"""
        # Load model components using final variables
        self.model = joblib.load(self.MODEL_DIR / self.MODEL_NAME)
        self.scaler = joblib.load(self.MODEL_DIR / self.SCALER_NAME)
        self.feature_names = joblib.load(self.MODEL_DIR / self.FEATURES_NAME)

        # Team data mapping
        self.team_data_map = {
            1: {"long_name": "Arsenal", "short_name": "Arsenal", "stadium": "Emirates Stadium, London"},
            2: {"long_name": "Aston Villa", "short_name": "Aston Villa", "stadium": "Villa Park, Birmingham"},
            3: {"long_name": "Birmingham", "short_name": "Birmingham", "stadium": "St Andrew's, Birmingham"},
            4: {"long_name": "Blackburn Rovers", "short_name": "Blackburn", "stadium": "Ewood Park, Blackburn"},
            5: {"long_name": "Blackpool", "short_name": "Blackpool", "stadium": "Bloomfield Road, Blackpool"},
            6: {"long_name": "Bolton Wanderers", "short_name": "Bolton", "stadium": "University of Bolton Stadium"},
            7: {"long_name": "Bournemouth", "short_name": "Bournemouth", "stadium": "Vitality Stadium, Bournemouth"},
            8: {"long_name": "Brentford", "short_name": "Brentford", "stadium": "Gtech Community Stadium, London"},
            9: {"long_name": "Brighton", "short_name": "Brighton", "stadium": "Amex Stadium, Brighton"},
            10: {"long_name": "Burnley", "short_name": "Burnley", "stadium": "Turf Moor, Burnley"},
            11: {"long_name": "Cardiff City", "short_name": "Cardiff", "stadium": "Cardiff City Stadium, Cardiff"},
            12: {"long_name": "Charlton Athletic", "short_name": "Charlton", "stadium": "The Valley, London"},
            13: {"long_name": "Chelsea", "short_name": "Chelsea", "stadium": "Stamford Bridge, London"},
            14: {"long_name": "Crystal Palace", "short_name": "Crystal Palace", "stadium": "Selhurst Park, London"},
            15: {"long_name": "Derby County", "short_name": "Derby", "stadium": "Pride Park, Derby"},
            16: {"long_name": "Everton", "short_name": "Everton", "stadium": "Goodison Park, Liverpool"},
            17: {"long_name": "Fulham", "short_name": "Fulham", "stadium": "Craven Cottage, London"},
            18: {"long_name": "Huddersfield Town", "short_name": "Huddersfield", "stadium": "John Smith's Stadium, Huddersfield"},
            19: {"long_name": "Hull City", "short_name": "Hull", "stadium": "MKM Stadium, Hull"},
            20: {"long_name": "Ipswich Town", "short_name": "Ipswich", "stadium": "Portman Road, Ipswich"},
            21: {"long_name": "Leeds United", "short_name": "Leeds", "stadium": "Elland Road, Leeds"},
            22: {"long_name": "Leicester City", "short_name": "Leicester", "stadium": "King Power Stadium, Leicester"},
            23: {"long_name": "Liverpool", "short_name": "Liverpool", "stadium": "Anfield, Liverpool"},
            24: {"long_name": "Luton Town", "short_name": "Luton", "stadium": "Kenilworth Road, Luton"},
            25: {"long_name": "Manchester City", "short_name": "Man City", "stadium": "Etihad Stadium, Manchester"},
            26: {"long_name": "Manchester United", "short_name": "Man United", "stadium": "Old Trafford, Manchester"},
            27: {"long_name": "Middlesbrough", "short_name": "Middlesbrough", "stadium": "Riverside Stadium, Middlesbrough"},
            28: {"long_name": "Newcastle United", "short_name": "Newcastle", "stadium": "St James' Park, Newcastle"},
            29: {"long_name": "Norwich City", "short_name": "Norwich", "stadium": "Carrow Road, Norwich"},
            30: {"long_name": "Nottingham Forest", "short_name": "Nott'm Forest", "stadium": "City Ground, Nottingham"},
            31: {"long_name": "Portsmouth", "short_name": "Portsmouth", "stadium": "Fratton Park, Portsmouth"},
            32: {"long_name": "Queens Park Rangers", "short_name": "QPR", "stadium": "Loftus Road, London"},
            33: {"long_name": "Reading", "short_name": "Reading", "stadium": "Select Car Leasing Stadium, Reading"},
            34: {"long_name": "Sheffield United", "short_name": "Sheffield United", "stadium": "Bramall Lane, Sheffield"},
            35: {"long_name": "Southampton", "short_name": "Southampton", "stadium": "St Mary's Stadium, Southampton"},
            36: {"long_name": "Stoke City", "short_name": "Stoke", "stadium": "bet365 Stadium, Stoke-on-Trent"},
            37: {"long_name": "Sunderland", "short_name": "Sunderland", "stadium": "Stadium of Light, Sunderland"},
            38: {"long_name": "Swansea City", "short_name": "Swansea", "stadium": "Liberty Stadium, Swansea"},
            39: {"long_name": "Tottenham Hotspur", "short_name": "Tottenham", "stadium": "Tottenham Hotspur Stadium, London"},
            40: {"long_name": "Watford", "short_name": "Watford", "stadium": "Vicarage Road, Watford"},
            41: {"long_name": "West Bromwich Albion", "short_name": "West Brom", "stadium": "The Hawthorns, West Bromwich"},
            42: {"long_name": "West Ham United", "short_name": "West Ham", "stadium": "London Stadium, London"},
            43: {"long_name": "Wigan Athletic", "short_name": "Wigan", "stadium": "DW Stadium, Wigan"},
            44: {"long_name": "Wolverhampton Wanderers", "short_name": "Wolves", "stadium": "Molineux Stadium, Wolverhampton"},
        }

        # Create reverse mappings for team name lookup
        self.short_name_to_id = {info["short_name"]: team_id for team_id, info in self.team_data_map.items()}
        self.long_name_to_id = {info["long_name"]: team_id for team_id, info in self.team_data_map.items()}

        # Cache for loaded season data
        self.season_cache = {}

    def _get_team_name(self, team_identifier: str) -> str:
        """Get standardized team name from various identifiers"""
        # Check if it's already a valid short name
        if team_identifier in self.short_name_to_id:
            return team_identifier

        # Check if it's a long name
        if team_identifier in self.long_name_to_id:
            team_id = self.long_name_to_id[team_identifier]
            return self.team_data_map[team_id]["short_name"]

        # If not found, return as-is (will be handled in team lookup)
        return team_identifier

    def _load_season_data(self, season: str) -> pd.DataFrame:
        """Load season data from CSV file, using cache if available"""
        if season in self.season_cache:
            return self.season_cache[season]
        if '/' in season:
            years = season.split('/')
            season_code = years[0][-2:] + years[1][-2:]
        else:
            season_code = season
        # Construct file path based on season format
        season_file = self.DATA_DIR / f"EPLS{season_code}.csv"

        if not season_file.exists():
            raise FileNotFoundError(f"Season file not found: {season_file}")

        # Load the CSV with proper column names
        df = pd.read_csv(season_file)

        # Ensure required columns exist
        required_cols = ['homeTeamID', 'awayTeamID', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns in {season_file}: {missing_cols}")

        # Map team IDs to team names if needed
        if 'homeTeamID' in df.columns and 'HomeTeam' not in df.columns:
            df['HomeTeam'] = df['homeTeamID'].map(lambda x: self.team_data_map.get(x, {}).get('short_name', ''))

        if 'awayTeamID' in df.columns and 'AwayTeam' not in df.columns:
            df['AwayTeam'] = df['awayTeamID'].map(lambda x: self.team_data_map.get(x, {}).get('short_name', ''))

        # Cache the loaded data
        self.season_cache[season] = df
        return df

    def _compute_team_stats_for_season(self, team: str, season: str) -> Dict:
        """Compute statistics for a specific team in a specific season"""
        # Get standardized team name
        team_name = self._get_team_name(team)

        # Load season data
        season_data = self._load_season_data(season)

        # Filter matches for this team
        home_games = season_data[season_data['HomeTeam'] == team_name].copy()
        away_games = season_data[season_data['AwayTeam'] == team_name].copy()

        # Calculate statistics
        return self._calculate_team_season_stats(home_games, away_games)

    def _calculate_team_season_stats(self, home_games: pd.DataFrame, away_games: pd.DataFrame) -> Dict:
        """Calculate comprehensive team statistics from home and away games"""
        total_games = len(home_games) + len(away_games)

        if total_games == 0:
            return self._get_default_stats()

        # Goals
        goals_scored = home_games['FTHG'].sum() + away_games['FTAG'].sum()
        goals_conceded = home_games['FTAG'].sum() + away_games['FTHG'].sum()

        # Wins/Draws/Losses
        home_wins = len(home_games[home_games['FTR'] == 'H'])
        away_wins = len(away_games[away_games['FTR'] == 'A'])
        home_draws = len(home_games[home_games['FTR'] == 'D'])
        away_draws = len(away_games[away_games['FTR'] == 'D'])

        wins = home_wins + away_wins
        draws = home_draws + away_draws
        losses = total_games - wins - draws

        # Shots statistics
        shots = (home_games['HS'].sum() + away_games['AS'].sum()) if 'HS' in home_games.columns else 0
        shots_on_target = (home_games['HST'].sum() + away_games['AST'].sum()) if 'HST' in home_games.columns else 0
        shots_conceded = (home_games['AS'].sum() + away_games['HS'].sum()) if 'AS' in home_games.columns else 0
        shots_on_target_conceded = (home_games['AST'].sum() + away_games['HST'].sum()) if 'AST' in home_games.columns else 0

        # Fouls and cards
        fouls = (home_games['HF'].sum() + away_games['AF'].sum()) if 'HF' in home_games.columns else 0
        fouls_won = (home_games['AF'].sum() + away_games['HF'].sum()) if 'AF' in home_games.columns else 0
        yellow_cards = (home_games['HY'].sum() + away_games['AY'].sum()) if 'HY' in home_games.columns else 0
        red_cards = (home_games['HR'].sum() + away_games['AR'].sum()) if 'HR' in home_games.columns else 0

        # Corners
        corners = (home_games['HC'].sum() + away_games['AC'].sum()) if 'HC' in home_games.columns else 0
        corners_conceded = (home_games['AC'].sum() + away_games['HC'].sum()) if 'AC' in home_games.columns else 0

        return {
            'avg_goals_scored': goals_scored / total_games,
            'avg_goals_conceded': goals_conceded / total_games,
            'avg_shots': shots / total_games,
            'avg_shots_on_target': shots_on_target / total_games,
            'avg_shots_conceded': shots_conceded / total_games,
            'avg_shots_on_target_conceded': shots_on_target_conceded / total_games,
            'avg_fouls': fouls / total_games,
            'avg_fouls_won': fouls_won / total_games,
            'avg_corners': corners / total_games,
            'avg_corners_conceded': corners_conceded / total_games,
            'avg_yellow_cards': yellow_cards / total_games,
            'avg_red_cards': red_cards / total_games,
            'win_rate': wins / total_games,
            'draw_rate': draws / total_games,
            'loss_rate': losses / total_games,
        }

    def _get_default_stats(self) -> Dict:
        """Return default statistics when no data is available"""
        return {
            'avg_goals_scored': 1.5,
            'avg_goals_conceded': 1.5,
            'avg_shots': 12.0,
            'avg_shots_on_target': 4.0,
            'avg_shots_conceded': 12.0,
            'avg_shots_on_target_conceded': 4.0,
            'avg_fouls': 11.0,
            'avg_fouls_won': 11.0,
            'avg_corners': 5.0,
            'avg_corners_conceded': 5.0,
            'avg_yellow_cards': 1.8,
            'avg_red_cards': 0.1,
            'win_rate': 0.33,
            'draw_rate': 0.33,
            'loss_rate': 0.34,
        }

    def _get_h2h_stats(self, home_team: str, away_team: str) -> Tuple[int, int]:
        """Get head-to-head statistics between two teams across all cached data"""
        home_team_name = self._get_team_name(home_team)
        away_team_name = self._get_team_name(away_team)

        all_h2h_matches = []

        # Check all cached seasons
        for season, season_data in self.season_cache.items():
            h2h = season_data[
                ((season_data['HomeTeam'] == home_team_name) & (season_data['AwayTeam'] == away_team_name)) |
                ((season_data['HomeTeam'] == away_team_name) & (season_data['AwayTeam'] == home_team_name))
                ]

            if len(h2h) > 0:
                all_h2h_matches.append(h2h)

        if len(all_h2h_matches) == 0:
            return 2, 2  # Default neutral values

        # Combine all h2h matches
        h2h = pd.concat(all_h2h_matches, ignore_index=True)

        # Count wins
        home_wins = 0
        away_wins = 0

        for _, match in h2h.iterrows():
            match_home = match['HomeTeam']
            match_result = match['FTR']

            if match_home == home_team_name:
                if match_result == 'H':
                    home_wins += 1
                elif match_result == 'A':
                    away_wins += 1
            else:  # match_home == away_team_name
                if match_result == 'H':
                    away_wins += 1
                elif match_result == 'A':
                    home_wins += 1

        return home_wins, away_wins

    def _prepare_features(self, home_stats: Dict, away_stats: Dict, home_h2h: int, away_h2h: int) -> np.ndarray:
        """Prepare feature vector for prediction"""
        # First, let's see what features the model expects
        #print(f"Model expects these features: {self.feature_names}")

        # Build features dictionary with all possible features
        features = {
            'home_avg_goals_scored': home_stats['avg_goals_scored'],
            'home_avg_goals_conceded': home_stats['avg_goals_conceded'],
            'home_avg_shots': home_stats['avg_shots'],
            'home_avg_shots_on_target': home_stats['avg_shots_on_target'],
            'home_avg_shots_conceded': home_stats['avg_shots_conceded'],
            'home_avg_shots_on_target_conceded': home_stats['avg_shots_on_target_conceded'],
            'home_avg_fouls': home_stats['avg_fouls'],
            'home_avg_fouls_won': home_stats['avg_fouls_won'],
            'home_avg_corners': home_stats['avg_corners'],
            'home_avg_corners_conceded': home_stats['avg_corners_conceded'],
            'home_avg_yellow_cards': home_stats['avg_yellow_cards'],
            'home_avg_red_cards': home_stats['avg_red_cards'],
            'home_win_rate': home_stats['win_rate'],
            'home_draw_rate': home_stats['draw_rate'],
            'home_loss_rate': home_stats['loss_rate'],

            'away_avg_goals_scored': away_stats['avg_goals_scored'],
            'away_avg_goals_conceded': away_stats['avg_goals_conceded'],
            'away_avg_shots': away_stats['avg_shots'],
            'away_avg_shots_on_target': away_stats['avg_shots_on_target'],
            'away_avg_shots_conceded': away_stats['avg_shots_conceded'],
            'away_avg_shots_on_target_conceded': away_stats['avg_shots_on_target_conceded'],
            'away_avg_fouls': away_stats['avg_fouls'],
            'away_avg_fouls_won': away_stats['avg_fouls_won'],
            'away_avg_corners': away_stats['avg_corners'],
            'away_avg_corners_conceded': away_stats['avg_corners_conceded'],
            'away_avg_yellow_cards': away_stats['avg_yellow_cards'],
            'away_avg_red_cards': away_stats['avg_red_cards'],
            'away_win_rate': away_stats['win_rate'],
            'away_draw_rate': away_stats['draw_rate'],
            'away_loss_rate': away_stats['loss_rate'],

            'home_h2h_wins': home_h2h,
            'away_h2h_wins': away_h2h,

            # Calculate derived features that the model might expect
            'home_scoring_strength': home_stats['avg_goals_scored'] / (home_stats['avg_goals_conceded'] + 0.1),
            'away_scoring_strength': away_stats['avg_goals_scored'] / (away_stats['avg_goals_conceded'] + 0.1),
            'home_defensive_strength': home_stats['avg_goals_conceded'] / (home_stats['avg_goals_scored'] + 0.1),
            'away_defensive_strength': away_stats['avg_goals_conceded'] / (away_stats['avg_goals_scored'] + 0.1),
            'home_shot_accuracy': home_stats['avg_shots_on_target'] / (home_stats['avg_shots'] + 0.1),
            'away_shot_accuracy': away_stats['avg_shots_on_target'] / (away_stats['avg_shots'] + 0.1),
            'home_discipline': home_stats['avg_yellow_cards'] + home_stats['avg_red_cards'] * 3,
            'away_discipline': away_stats['avg_yellow_cards'] + away_stats['avg_red_cards'] * 3,
        }

        # Create feature vector in the same order as training, using only features that exist
        try:
            feature_vector = np.array([features.get(name, 0.0) for name in self.feature_names]).reshape(1, -1)
            return self.scaler.transform(feature_vector)
        except KeyError as e:
            missing_feature = str(e).strip("'")
            raise ValueError(f"Missing feature '{missing_feature}'. Available features: {list(features.keys())}")

    def predict_match(self, home_team: str, away_team: str, home_season: str, away_season: str) -> Dict:
        """Predict match outcome using team statistics from their respective seasons"""
        try:
            # Compute team statistics from their respective seasons
            home_stats = self._compute_team_stats_for_season(home_team, home_season)
            away_stats = self._compute_team_stats_for_season(away_team, away_season)

            # Get head-to-head statistics
            home_h2h, away_h2h = self._get_h2h_stats(home_team, away_team)

            # Prepare features and make prediction
            features = self._prepare_features(home_stats, away_stats, home_h2h, away_h2h)
            prediction = self.model.predict(features)[0]
            probabilities = self.model.predict_proba(features)[0]

            # Map prediction to outcome
            outcome_map = {0: 'away_win', 1: 'draw', 2: 'home_win'}
            predicted_outcome = outcome_map[prediction]

            return {
                'home_team': self._get_team_name(home_team),
                'away_team': self._get_team_name(away_team),
                'home_season': home_season,
                'away_season': away_season,
                'prediction': predicted_outcome,
                'probabilities': {
                    'home_win': float(probabilities[2]),
                    'draw': float(probabilities[1]),
                    'away_win': float(probabilities[0])
                }
            }

        except Exception as e:
            raise ValueError(f"Error predicting match: {str(e)}")


if __name__ == "__main__":
    import sys
    import json

    if len(sys.argv) == 5:
        home_team = sys.argv[1]
        away_team = sys.argv[2]
        home_season = sys.argv[3]
        away_season = sys.argv[4]

        try:
            predictor = CrossSeasonMatchPredictor()
            result = predictor.predict_match(
                home_team=home_team,
                away_team=away_team,
                home_season=home_season,
                away_season=away_season
            )
            # Output as JSON for Node.js to parse
            print(json.dumps(result))
        except Exception as e:
            print(json.dumps({"error": str(e)}), file=sys.stderr)
            sys.exit(1)