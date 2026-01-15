# ⚽ Premier League Match Predictor

A professional-grade AI forecasting tool for Premier League matches, built with **Python**, **Streamlit**, and **Scikit-Learn**.

## 🚀 How it Works
The application uses a **Random Forest Classifier** trained on historical Premier League data (Seasons 23-25) to predict match outcomes.

**Key Features:**
*   **Machine Learning Model:** Trained on `HomeTeam`, `AwayTeam`, and **Market Betting Odds** to leverage "Wisdom of the Crowd".
*   **Real-Time Form:** Displays the actual last 5 match results for each team based on historical data.
*   **Visualizations:** Interactive Radar Charts and Donut Charts powered by Plotly.
*   **Insight Engine:** Explains *why* a team is favored (e.g., "AI Model strongly favors Man City based on historical data" or "Home advantage provides an edge").

## ✨ Features
- **Interactive Dashboard:** "Briefing Room" for match stats vs "Analytics Hub" for predictions.
- **AI Predictions**: Real-time probability calculation for Home Win / Draw / Away Win.
- **Deep-Dive Visuals**: 
    - Donut Charts for win probabilities.
    - **Radar Charts** comparing teams on tactical attributes.
    - **Injury Cards**: Custom coded UI for player availability.
- **Dark Mode UI**: Sleek, modern interface.

## 🛠️ Installation

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd "Football Predictor"
    ```

2.  **Create a Virtual Environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Train the Model** (Required first time):
    ```bash
    python3 train_model.py
    ```

5.  **Run the App**:
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
