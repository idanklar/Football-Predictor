# ⚽ Premier League AI Predictor

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red)
![ML](https://img.shields.io/badge/AI-Scikit--Learn-orange)
![License](https://img.shields.io/badge/License-MIT-green)

> **A professional-grade match forecasting engine driven by Machine Learning.**

<!-- ![App Screenshot](assets/demo.png) -->
*(Screenshot placeholder)*

## 🚀 Overview

The **Premier League AI Predictor** is not just a statistics dashboard—it is a decision-support system fueled by historical data. Unlike simple probability apps, this project utilizes a **Random Forest Classifier** trained on real-world match data (2023–2025 seasons) to predict outcomes with statistical significance.

The system achieves an accuracy of **~54%**, significantly outperforming the random baseline for football matches (~33%), providing users with data-driven insights, real-time injury tracking, and tactical comparisons.

## ✨ Key Features

### 🧠 Advanced Machine Learning
* **Algorithm:** Random Forest Classifier (`sklearn.ensemble`).
* **Training Data:** Trained on 1,000+ historical matches from official CSV datasets.
* **Dynamic Encoding:** Automatically encodes team names and calculates form metrics.
* **FPL Integration:** Fetches real-time team strength data (Attack, Defence, Overall) from the official Fantasy Premier League API to enhance predictive accuracy.

### 🔮 What-If Analysis (Simulation Mode)
* **Scenario Modeling:** Interactive sidebar tools allow users to modify team form and player availability.
* **Real-Time Impact:** Instantly visualizes how a "Key Player Missing" or a sudden drop in form affects the win probability.
* **Tactical Override:** Allows users to test their own hypotheses against the AI's baseline prediction.

### 🤖 AI Insight Engine
* **Narrative Generation:** The system doesn't just give numbers; it explains *why*.
* **Contextual Analysis:** Cross-references statistical probability, FPL strength metrics, and simulated scenarios to generate human-readable commentary (e.g., *"Man City's attack (Rated 1350) is expected to overwhelm Burnley's defense"*).

### 📊 Professional Dashboard UI
* **"Briefing Room" Layout:** A split-screen design separating match context (Left) from predictive analytics (Right).
* **Interactive Visuals:**
    * **Donut Chart:** Real-time win/draw/loss probabilities.
    * **Radar Chart (Spider Plot):** Tactical comparison of team attributes (Attack, Defense, Creativity, etc.).
* **Live Simulation:** Simulates real-world factors like Weather conditions 🌧️ and Injury reports 🚑.

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **Machine Learning:** Scikit-Learn, Joblib, NumPy
* **Data Processing:** Pandas
* **Visualization:** Plotly Graph Objects (Interactive), Streamlit
* **Version Control:** Git & GitHub

## 📂 Project Structure

```bash
football-predictor/
│
├── app.py               # Main Application (Streamlit UI)
├── predictor.py         # Inference Engine & AI Explanation Logic
├── train_model.py       # ML Training Script (Generates the .pkl model)
├── data_loader.py       # Data Simulation (Fixtures, Weather, Injuries)
├── football_model.pkl   # The Trained Brain (Binary)
├── encoder.pkl          # Label Encoder for Team Names
├── season23.csv         # Historical Training Data
├── season24.csv         # Historical Training Data
└── requirements.txt     # Python Dependencies
```

## ⚡ How to Run Locally

### 1. Clone the Repository
```bash
git clone https://github.com/idanklar/Football-Predictor.git
cd Football-Predictor
```

### 2. Set Up Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```
 
 
### 4. Train the Model (Optional)
The repo comes with a pre-trained model, but you can retrain it on new data:

```bash
python train_model.py
```

### 5. Launch the App

```bash
streamlit run app.py
```

## 📈 Performance
The model is evaluated using accuracy scores on a test split of the historical data.

*   **Current Accuracy**: 54.12%
*   **Baseline (Random Guess)**: 33.33%

*Note: Football is highly stochastic; accuracy above 50% is considered strong for simple match outcome models.*

## 📜 License
Distributed under the MIT License. See LICENSE for more information.

---
*Built by Idan Klar*
