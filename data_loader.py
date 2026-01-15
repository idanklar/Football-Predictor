from datetime import datetime, timedelta

def get_current_fixtures():
    """
    Returns a list of mock Premier League fixtures for the upcoming matchweek.
    Each fixture is a dictionary containing match details.
    """
    today = datetime.now()
    
    fixtures = [
        {
            "id": 1,
            "home_team": "Arsenal",
            "away_team": "Tottenham",
            "match_time": (today + timedelta(days=2)).strftime("%Y-%m-%d 15:00:00"),
            "weather_condition": "Rainy",
            "home_injuries": ["Gabriel Jesus", "Thomas Partey"],
            "away_injuries": ["James Maddison", "Micky van de Ven"],
            "last_5_matches_home": ["W", "W", "D", "W", "L"],
            "last_5_matches_away": ["L", "D", "W", "W", "W"],
            "home_strength": 1, # Tier 1
            "away_strength": 1,  # Tier 1
            "home_team_logo": "https://upload.wikimedia.org/wikipedia/en/5/53/Arsenal_FC.svg",
            "away_team_logo": "https://upload.wikimedia.org/wikipedia/en/b/b4/Tottenham_Hotspur.svg"
        },
        {
            "id": 2,
            "home_team": "Liverpool",
            "away_team": "Luton Town",
            "match_time": (today + timedelta(days=2)).strftime("%Y-%m-%d 17:30:00"),
            "weather_condition": "Clear",
            "home_injuries": ["Thiago Alcantara"],
            "away_injuries": [],
            "last_5_matches_home": ["W", "D", "W", "W", "W"],
            "last_5_matches_away": ["L", "L", "L", "D", "W"],
            "home_strength": 1,
            "away_strength": 3,
            "home_team_logo": "https://upload.wikimedia.org/wikipedia/en/0/0c/Liverpool_FC.svg",
            "away_team_logo": "https://upload.wikimedia.org/wikipedia/en/9/9d/Luton_Town_logo.svg"
        },
        {
            "id": 3,
            "home_team": "Manchester City",
            "away_team": "Chelsea",
            "match_time": (today + timedelta(days=3)).strftime("%Y-%m-%d 14:00:00"),
            "weather_condition": "Cloudy",
            "home_injuries": ["Kevin De Bruyne"],
            "away_injuries": ["Reece James", "Ben Chilwell", "Christopher Nkunku"],
            "last_5_matches_home": ["W", "W", "W", "W", "W"],
            "last_5_matches_away": ["W", "L", "W", "L", "D"],
            "home_strength": 1,
            "away_strength": 2,
            "home_team_logo": "https://upload.wikimedia.org/wikipedia/en/e/eb/Manchester_City_FC_badge.svg",
            "away_team_logo": "https://upload.wikimedia.org/wikipedia/en/c/cc/Chelsea_FC.svg"
        },
        {
            "id": 4,
            "home_team": "Aston Villa",
            "away_team": "Manchester United",
            "match_time": (today + timedelta(days=3)).strftime("%Y-%m-%d 16:30:00"),
            "weather_condition": "Clear",
            "home_injuries": ["Tyrone Mings", "Emiliano Buendia"],
            "away_injuries": ["Lisandro Martinez", "Luke Shaw"],
            "last_5_matches_home": ["W", "L", "W", "D", "W"],
            "last_5_matches_away": ["W", "W", "W", "D", "L"],
            "home_strength": 2,
            "away_strength": 1, # Historically/Strength-wise treated as 1 or 2
            "home_team_logo": "https://upload.wikimedia.org/wikipedia/en/f/f9/Aston_Villa_FC_crest_%282016%29.svg",
            "away_team_logo": "https://upload.wikimedia.org/wikipedia/en/7/7a/Manchester_United_FC_crest.svg"
        },
        {
            "id": 5,
            "home_team": "Brighton",
            "away_team": "West Ham",
            "match_time": (today + timedelta(days=4)).strftime("%Y-%m-%d 20:00:00"),
            "weather_condition": "Windy",
            "home_injuries": ["Kaoru Mitoma", "Solly March"],
            "away_injuries": ["Lucas Paqueta"],
            "last_5_matches_home": ["D", "L", "W", "D", "L"],
            "last_5_matches_away": ["W", "D", "L", "D", "W"],
            "home_strength": 2,
            "away_strength": 2,
            "home_team_logo": "https://upload.wikimedia.org/wikipedia/en/f/fd/Brighton_%26_Hove_Albion_logo.svg",
            "away_team_logo": "https://upload.wikimedia.org/wikipedia/en/c/c2/West_Ham_United_FC_logo.svg"
        }
    ]
    return fixtures
