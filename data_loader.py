from datetime import datetime, timedelta

def get_current_fixtures():
    """
    Returns a list of mock Premier League fixtures for the upcoming matchweek.
    Each fixture is a dictionary containing match details.
    """
    
    # Matchweek 22 Fixtures
    fixtures = [
        {
            "id": 1,
            "home_team": "Manchester United",
            "away_team": "Manchester City",
            "match_time": "2026-01-17 14:30:00",
            "weather_condition": "Rainy 🌧️",
            "home_injuries": ["Luke Shaw (Muscle)", "Mason Mount (Calf)"],
            "away_injuries": ["Kevin De Bruyne (Rest)", "Rodri (Suspended)"],
            "last_5_matches_home": ["L", "W", "D", "D", "D"], # Man Utd Form (Real Data)
            "last_5_matches_away": ["W", "W", "D", "D", "D"], # Man City Form (Real Data)
            "home_team_logo": "https://upload.wikimedia.org/wikipedia/en/thumb/7/7a/Manchester_United_FC_crest.svg/1200px-Manchester_United_FC_crest.svg.png",
            "away_team_logo": "https://upload.wikimedia.org/wikipedia/en/thumb/e/eb/Manchester_City_FC_badge.svg/1200px-Manchester_City_FC_badge.svg.png",
            "home_strength": 2, # Tier 2
            "away_strength": 1,  # Tier 1
            "avg_odds_home": 3.40,
            "avg_odds_draw": 3.10,
            "avg_odds_away": 1.60
        },
        {
            "id": 2,
            "home_team": "Tottenham",
            "away_team": "West Ham",
            "match_time": "2026-01-17 17:00:00",
            "weather_condition": "Cloudy ☁️",
            "home_injuries": ["Maddison (Ankle)", "Van de Ven (Hamstring)"],
            "away_injuries": ["Antonio (Knee)", "Paqueta (Calf)"],
            "last_5_matches_home": ["L", "W", "D", "D", "L"], # Tottenham Form
            "last_5_matches_away": ["L", "L", "D", "L", "L"], # West Ham Form
            "home_team_logo": "https://upload.wikimedia.org/wikipedia/en/thumb/b/b4/Tottenham_Hotspur.svg/1200px-Tottenham_Hotspur.svg.png",
            "away_team_logo": "https://upload.wikimedia.org/wikipedia/en/thumb/c/c2/West_Ham_United_FC_logo.svg/1200px-West_Ham_United_FC_logo.svg.png",
            "home_strength": 2,
            "away_strength": 2,
            "avg_odds_home": 1.80,
            "avg_odds_draw": 3.40,
            "avg_odds_away": 4.10
        },
        {
            "id": 3,
            "home_team": "Nottingham Forest",
            "away_team": "Arsenal",
            "match_time": "2026-01-17 19:30:00",
            "weather_condition": "Cold Night ❄️",
            "home_injuries": ["Awoniyi (Groin)"],
            "away_injuries": ["Timber (Knee)", "Partey (Thigh)"],
            "last_5_matches_home": ["L", "L", "L", "L", "W"], # Nottingham Forest Form
            "last_5_matches_away": ["W", "W", "W", "W", "D"], # Arsenal Form
            "home_team_logo": "https://upload.wikimedia.org/wikipedia/en/thumb/d/d2/Nottingham_Forest_gridiron.svg/1200px-Nottingham_Forest_gridiron.svg.png", # Using Gridiron logo variation as fallback or standard one but PNG
            "away_team_logo": "https://upload.wikimedia.org/wikipedia/en/thumb/5/53/Arsenal_FC.svg/1200px-Arsenal_FC.svg.png",
            "home_strength": 3,
            "away_strength": 1,
            "avg_odds_home": 6.50,
            "avg_odds_draw": 4.20,
            "avg_odds_away": 1.45
        },
        {
            "id": 4,
            "home_team": "Liverpool",
            "away_team": "Burnley",
            "match_time": "2026-01-17 17:00:00",
            "weather_condition": "Windy 💨",
            "home_injuries": ["Alisson (Hamstring)", "Jota (Knee)"],
            "away_injuries": ["Foster (Illness)"],
            "last_5_matches_home": ["W", "W", "D", "D", "D"], # Liverpool Form
            "last_5_matches_away": ["D", "D", "L", "L", "D"], # Burnley Form
            "home_team_logo": "https://upload.wikimedia.org/wikipedia/en/thumb/0/0c/Liverpool_FC.svg/1200px-Liverpool_FC.svg.png",
            "away_team_logo": "https://upload.wikimedia.org/wikipedia/en/thumb/6/62/Burnley_F.C._Logo.svg/1200px-Burnley_F.C._Logo.svg.png",
            "home_strength": 1,
            "away_strength": 3,
            "avg_odds_home": 1.15,
            "avg_odds_draw": 7.50,
            "avg_odds_away": 16.00
        }
    ]
    return fixtures
