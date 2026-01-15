import pandas as pd
import glob
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def train():
    # 1. Load Data
    csv_files = glob.glob("*.csv")
    if not csv_files:
        print("No CSV files found!")
        return

    print(f"Loading files: {csv_files}")
    dfs = []
    for f in csv_files:
        try:
            df = pd.read_csv(f)
            dfs.append(df)
        except Exception as e:
            print(f"Error reading {f}: {e}")

    if not dfs:
        return

    full_df = pd.concat(dfs, ignore_index=True)
    
    # 2. Data Cleaning
    # Keep relevant columns
    cols_to_keep = ['HomeTeam', 'AwayTeam', 'FTR', 'AvgH', 'AvgD', 'AvgA']
    # Check if columns exist
    if not all(col in full_df.columns for col in cols_to_keep):
        print(f"Dataset missing required columns. Available: {full_df.columns}")
        return

    df_clean = full_df[cols_to_keep].dropna()

    # 3. Preprocessing
    le = LabelEncoder()
    # Fit encoder on all unique team names (both home and away)
    all_teams = pd.concat([df_clean['HomeTeam'], df_clean['AwayTeam']]).unique()
    le.fit(all_teams)

    df_clean['HomeTeam_Code'] = le.transform(df_clean['HomeTeam'])
    df_clean['AwayTeam_Code'] = le.transform(df_clean['AwayTeam'])

    # Map FTR: H=2, D=1, A=0
    ftr_map = {'H': 2, 'D': 1, 'A': 0}
    # Filter rows with unexpected FTR
    df_clean = df_clean[df_clean['FTR'].isin(ftr_map.keys())]
    df_clean['Result'] = df_clean['FTR'].map(ftr_map)

    # 4. Training
    # We use Team Codes AND Market Odds
    # Market odds are incredibly strong predictors (Wisdom of the Crowd)
    features = ['HomeTeam_Code', 'AwayTeam_Code', 'AvgH', 'AvgD', 'AvgA']
    
    # Drop rows where odds are missing
    df_clean = df_clean.dropna(subset=features)

    X = df_clean[features]
    y = df_clean['Result']

    # Split for validation mainly to print accuracy
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)

    # 5. Evaluation
    preds = rf.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print(f"Model Training Complete. Accuracy: {acc:.4f}")

    # Retrain on full dataset for production? 
    # Usually better to use the one we validated or retrain exactly same params on full data.
    # Let's retrain on full data for maximum knowledge
    rf_full = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_full.fit(X, y)

    # 6. Saving
    with open('football_model.pkl', 'wb') as f:
        pickle.dump(rf_full, f)
    
    with open('encoder.pkl', 'wb') as f:
        pickle.dump(le, f)

    print("Model and Encoder saved successfully.")

if __name__ == "__main__":
    train()
