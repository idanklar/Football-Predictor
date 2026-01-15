# ⚽ Premier League Match Predictor

A professional-grade AI forecasting tool for Premier League matches, built with **Python** and **Streamlit**.

## 🚀 How it Works
The application uses a custom weighted scoring algorithm to predict match outcomes:
1.  **Team Strength Tier**: Higher quality squads get a significant boost.
2.  **Home Advantage**: Statistically proven home field advantage (+10% weight).
3.  **Recent Form**: Analysis of the last 5 matches (W/D/L).
4.  **Injury Impact**: Penalties applied for key player absences.
5.  **Weather Conditions**: Contextual display for match day.

## ✨ Features
- **Interactive Dashboard**: Browse upcoming fixtures for the matchweek.
- **AI Predictions**: Real-time probability calculation for Home Win / Draw / Away Win.
- **Deep-Dive Visuals**: 
    - Donut Charts for win probabilities.
    - **Radar Charts** comparing teams on Attack, Defense, Midfield, Counter, and Set Pieces.
- **Explainability**: The AI explains *why* it chose a specific outcome (e.g., "Arsenal favored due to home advantage...").
- **Dark Mode UI**: Sleek, modern interface using custom CSS.

## 🛠️ Installation

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd "Football Predictor"
    ```

2.  **Create a Virtual Environment** (Optional but recommended):
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the App**:
    ```bash
    streamlit run app.py
    ```

## 🐳 Docker Support

To run via Docker:
```bash
docker build -t pl-predictor .
docker run -p 8501:8501 pl-predictor
```

---
*Built for the Modern Football Fan.*
