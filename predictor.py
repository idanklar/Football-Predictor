import pickle
import pandas as pd
import numpy as np
import os

class MatchPredictor:
    def __init__(self):
        self.model = None
        self.encoder = None
        self.load_model()

    def load_model(self):
        try:
            with open('football_model.pkl', 'rb') as f:
                self.model = pickle.load(f)
            with open('encoder.pkl', 'rb') as f:
                self.encoder = pickle.load(f)
            print("Model and Encoder loaded successfully.")
        except FileNotFoundError:
            print("Model files not found. Please run train_model.py first.")

    def get_team_code(self, team_name):
        if not self.encoder:
            return None
        
        try:
            return self.encoder.transform([team_name])[0]
        except ValueError:
            # Handle mismatch (e.g., "Man Utd" vs "Manchester United")
            # Simple heuristic fallback or try to find close match
            # For now, let's try some common mappings
            mappings = {
                "Manchester United": "Man United",
                "Manchester City": "Man City",
                "Tottenham": "Tottenham",
                "West Ham": "West Ham",
                "Nottingham Forest": "Nott'm Forest",
                "Luton Town": "Luton",
                "Sheffield United": "Sheffield United",
                "Wolverhampton Wanderers": "Wolves",
                "Brighton": "Brighton",
                "Newcastle United": "Newcastle",
                "Bournemouth": "Bournemouth",
                "Brentford": "Brentford",
                "Crystal Palace": "Crystal Palace",
                "Fulham": "Fulham",
                "Aston Villa": "Aston Villa",
                "Everton": "Everton"
            }
            if team_name in mappings:
                try:
                    return self.encoder.transform([mappings[team_name]])[0]
                except ValueError:
                    pass
            
            # If still fails, try to find substrings?
            # Creating a dummy code or handling gracefully
            print(f"Warning: Team '{team_name}' not found in encoder.")
            return None

    def predict_match(self, match_data):
        """
        Predicts match outcome using Random Forest model.
        Input: match_data dict
        Output: Probabilities and reasoning.
        """
        if not self.model or not self.encoder:
            return {
                "home_win_prob": 33.3,
                "draw_prob": 33.3,
                "away_win_prob": 33.3,
                "reasoning": "Model not loaded. Using equal probabilities."
            }

        home_team = match_data['home_team']
        away_team = match_data['away_team']

        home_code = self.get_team_code(home_team)
        away_code = self.get_team_code(away_team)

        if home_code is None or away_code is None:
            # Fallback logic if teams not found
            return self._fallback_prediction(match_data)

        # Prepare input for model: Team Codes + Market Odds
        odds_h = match_data.get('avg_odds_home', 2.0)
        odds_d = match_data.get('avg_odds_draw', 3.0)
        odds_a = match_data.get('avg_odds_away', 3.0)
        
        input_data = pd.DataFrame([[home_code, away_code, odds_h, odds_d, odds_a]], 
                                  columns=['HomeTeam_Code', 'AwayTeam_Code', 'AvgH', 'AvgD', 'AvgA'])
        
        # Get probabilities [Away, Draw, Home] -> FTR is 0(A), 1(D), 2(H)
        # Check classes_ attribute to be sure
        probs = self.model.predict_proba(input_data)[0]
        
        # Map probabilities to outcomes based on class order
        classes = self.model.classes_ # Expected [0, 1, 2]
        
        p_away = 0
        p_draw = 0
        p_home = 0
        
        for cls, prob in zip(classes, probs):
            if cls == 0: p_away = prob
            elif cls == 1: p_draw = prob
            elif cls == 2: p_home = prob

        # Convert to percentage
        p_home = round(p_home * 100, 1)
        p_draw = round(p_draw * 100, 1)
        p_away = round(p_away * 100, 1)

        # Generate Reasoning
        reasoning = self._generate_reasoning(match_data, p_home, p_draw, p_away)

        return {
            "home_win_prob": p_home,
            "draw_prob": p_draw,
            "away_win_prob": p_away,
            "reasoning": reasoning
        }

    def _fallback_prediction(self, match_data):
        # Fallback to simple logic if ML model fails for specific teams
        return {
            "home_win_prob": 40.0,
            "draw_prob": 30.0,
            "away_win_prob": 30.0,
            "reasoning": "Team name mismatch in historical database. Defaulting to Home Advantage."
        }

    def _generate_reasoning(self, match_data, p_home, p_draw, p_away):
        reasoning = []
        
        if p_home > 50:
            reasoning.append(f"AI Model strongly favors {match_data['home_team']} based on historical data.")
        elif p_away > 50:
            reasoning.append(f"Historical trends indicate a likely win for {match_data['away_team']}.")
        elif p_home > p_away:
            reasoning.append(f"{match_data['home_team']} has a slight edge.")
        else:
            reasoning.append("Model predicts a very balanced game.")
            
        home_injuries = len(match_data['home_injuries'])
        away_injuries = len(match_data['away_injuries'])
        
        if home_injuries > 2:
            reasoning.append(f"However, {match_data['home_team']} has injury concerns.")
        if away_injuries > 2:
            reasoning.append(f"{match_data['away_team']} is missing key players.")

        if match_data['last_5_matches_home'].count('W') >= 3:
            reasoning.append(f"{match_data['home_team']} is in good form.")
        elif match_data['last_5_matches_home'].count('L') >= 3:
             reasoning.append(f"{match_data['home_team']} has been struggling recently.")
            
        return " ".join(reasoning)
