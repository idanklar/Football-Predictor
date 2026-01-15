import pandas as pd
import glob

def get_last_5_form(team_name):
    # Load all data
    csv_files = sorted(glob.glob("season*.csv")) # Ensure order if possible, though concat handles it
    dfs = []
    for f in csv_files:
        try:
            df = pd.read_csv(f)
            # Convert date to datetime if needed, but for appending, simple concat works if files are chronological
            # The files are named season23, season24, season25.
            dfs.append(df)
        except:
            pass
            
    if not dfs:
        return []

    full_df = pd.concat(dfs, ignore_index=True)
    
    # Filter for the team
    team_matches = full_df[(full_df['HomeTeam'] == team_name) | (full_df['AwayTeam'] == team_name)].copy()
    
    # Get last 5
    last_5 = team_matches.tail(5)
    
    form = []
    for index, row in last_5.iterrows():
        if row['HomeTeam'] == team_name:
            if row['FTR'] == 'H': form.append('W')
            elif row['FTR'] == 'D': form.append('D')
            else: form.append('L')
        else: # Away Team
            if row['FTR'] == 'A': form.append('W')
            elif row['FTR'] == 'D': form.append('D')
            else: form.append('L')
            
    return form

teams = [
    "Man United", "Man City", 
    "Tottenham", "West Ham", 
    "Nott'm Forest", "Arsenal", 
    "Liverpool", "Burnley"
]

print("--- FORM GUIDE ---")
for team in teams:
    form = get_last_5_form(team)
    print(f"{team}: {form}")
