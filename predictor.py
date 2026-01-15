
class MatchPredictor:
    def __init__(self):
        pass

    def calculate_form_score(self, last_5):
        """
        Calculates a form score based on the last 5 matches.
        W = 3, D = 1, L = 0.
        Max score = 15.
        Normalized to 0-1 range.
        """
        score = 0
        for result in last_5:
            if result == 'W':
                score += 3
            elif result == 'D':
                score += 1
        return score / 15.0

    def predict_match(self, match_data):
        """
        Predicts the outcome of a match based on weighted factors.
        Returns probabilities for Home Win, Draw, Away Win and a reasoning string.
        """
        home_strength = match_data['home_strength']
        away_strength = match_data['away_strength']
        home_form = self.calculate_form_score(match_data['last_5_matches_home'])
        away_form = self.calculate_form_score(match_data['last_5_matches_away'])
        
        # Base Probability (Strength Tier based)
        # Tier 1 vs Tier 3 -> High favor to Tier 1
        # Tier 1 vs Tier 1 -> Even
        # Invert tier: 1 is best, 3 is worst. Convert to score: 3 (Tier 1), 2 (Tier 2), 1 (Tier 3)
        home_tier_score = 4 - home_strength
        away_tier_score = 4 - away_strength
        
        # Initial Strength Weight
        strength_diff = home_tier_score - away_tier_score
        
        # Base points (out of 100 for simplicity of relative calculation)
        home_points = 35
        away_points = 35
        draw_points = 30
        
        # Apply Strength Diff (Each tier diff shifts 10%)
        home_points += strength_diff * 10
        away_points -= strength_diff * 10
        
        # Home Advantage (+10%)
        home_points += 10
        away_points -= 5 # Draw takes some hit too maybe
        draw_points -= 5
        
        # Form Impact (Up to 10% swing)
        form_diff = home_form - away_form # Range -1 to 1
        home_points += form_diff * 10
        away_points -= form_diff * 10
        
        # Injury Penalty (-5% per injury)
        home_injury_penalty = len(match_data['home_injuries']) * 5
        away_injury_penalty = len(match_data['away_injuries']) * 5
        
        home_points -= home_injury_penalty
        away_points -= away_injury_penalty
        
        # Redistribute lost points from penalties to the opponent and draw
        # Actually, let's just reduce the team's score. Normalization will handle percentages.
        
        # Ensure points don't go negative or too low logic handled by normalization
        home_points = max(5, home_points)
        away_points = max(5, away_points)
        draw_points = max(5, draw_points)
        
        total_points = home_points + away_points + draw_points
        
        p_home = round((home_points / total_points) * 100, 1)
        p_away = round((away_points / total_points) * 100, 1)
        p_draw = round((draw_points / total_points) * 100, 1)
        
        # Reasoning Generation
        reasoning = []
        if home_points > away_points + 10:
            reasoning.append(f"{match_data['home_team']} are strong favorites.")
        elif away_points > home_points + 10:
            reasoning.append(f"{match_data['away_team']} are favored to win.")
        else:
            reasoning.append("This is expected to be a tight contest.")
            
        if strength_diff > 0:
            reasoning.append(f"Higher squad quality for {match_data['home_team']}.")
        elif strength_diff < 0:
             reasoning.append(f"Higher squad quality for {match_data['away_team']}.")
             
        reasoning.append(f"Home advantage applied for {match_data['home_team']}.")
        
        if len(match_data['home_injuries']) > 2:
            reasoning.append(f"Significant injury concerns for {match_data['home_team']} negatively impact their chances.")
            
        if len(match_data['away_injuries']) > 2:
            reasoning.append(f"{match_data['away_team']} are struggling with injuries.")

        if home_form > 0.8:
            reasoning.append(f"{match_data['home_team']} are in excellent form.")
        elif home_form < 0.3:
            reasoning.append(f"{match_data['home_team']} have been in poor form recently.")

        return {
            "home_win_prob": p_home,
            "draw_prob": p_draw,
            "away_win_prob": p_away,
            "reasoning": " ".join(reasoning)
        }
