import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np
from data_loader import get_current_fixtures
from predictor import MatchPredictor

# --- Page Configuration ---
st.set_page_config(
    page_title="Premier League Predictor",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for "Wow" Factor ---
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }
    .match-card {
        background-color: #262730;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #41424b;
        margin-bottom: 10px;
        transition: transform 0.2s;
    }
    .match-card:hover {
        transform: scale(1.02);
        border-color: #ff4b4b;
    }
    .injury-card {
        background-color: #333333;
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .injury-title {
        font-weight: bold;
        margin-bottom: 5px;
        display: block;
        font-size: 1.1em;
    }
    .home-injury { color: #FF4B4B; } /* Bright Red */
    .away-injury { color: #FFD700; } /* Bright Yellow */
    
    .team-logo {
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 100px;
    }
    .vs-text {
        font-size: 2rem;
        font-weight: 900;
        color: #ff4b4b;
        text-align: center;
        margin-top: 20px;
    }
    .team-name-header {
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Header ---
st.title("⚽ Premier League AI Predictor")
st.markdown("### 🚀 Professional Match Forecasting Engine")
st.markdown("---")

# --- Initialize Logic ---
predictor = MatchPredictor()
fixtures = get_current_fixtures()

# --- Sidebar / Dashboard ---
st.sidebar.header("📅 Matchweek Fixtures")
selected_match_id = st.sidebar.radio(
    "Select a Match for Deep Dive:",
    [f"{f['home_team']} vs {f['away_team']}" for f in fixtures],
    index=0
)

# Helper to find selected match data
match_index = [f"{f['home_team']} vs {f['away_team']}" for f in fixtures].index(selected_match_id)
selected_match = fixtures[match_index]

# --- Main Dashboard Area ---
col1, col2 = st.columns([1, 2])

with col1:
    # Logos and Team Names Header
    c1, c2, c3 = st.columns([1, 0.8, 1])
    with c1:
        st.markdown(f"<div style='text-align: center;'><img src='{selected_match['home_team_logo']}' width='100'></div>", unsafe_allow_html=True)
        st.markdown(f"<p class='team-name-header'>{selected_match['home_team']}</p>", unsafe_allow_html=True)
    with c2:
        st.markdown("<p class='vs-text'>VS</p>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div style='text-align: center;'><img src='{selected_match['away_team_logo']}' width='100'></div>", unsafe_allow_html=True)
        st.markdown(f"<p class='team-name-header'>{selected_match['away_team']}</p>", unsafe_allow_html=True)

    st.write("---")
    st.write(f"**Date:** {selected_match['match_time']}")
    st.write(f"**Weather:** {selected_match['weather_condition']}")
    
    st.markdown("#### 🏥 Injury Report")
    
    # Custom HTML Injury Cards
    home_injuries_str = ', '.join(selected_match['home_injuries']) if selected_match['home_injuries'] else 'No major injuries'
    away_injuries_str = ', '.join(selected_match['away_injuries']) if selected_match['away_injuries'] else 'No major injuries'
    
    st.markdown(f"""
    <div class="injury-card">
        <span class="injury-title home-injury">🏠 {selected_match['home_team']} Injuries</span>
        <span style="color: #ddd;">{home_injuries_str}</span>
    </div>
    <div class="injury-card">
        <span class="injury-title away-injury">✈️ {selected_match['away_team']} Injuries</span>
        <span style="color: #ddd;">{away_injuries_str}</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("#### 📈 Recent Form (Last 5)")
    st.write(f"**{selected_match['home_team']}**: {' - '.join(selected_match['last_5_matches_home'])}")
    st.write(f"**{selected_match['away_team']}**: {' - '.join(selected_match['last_5_matches_away'])}")

with col2:
    st.subheader("🤖 AI Prediction Model")
    
    # Run Prediction
    prediction = predictor.predict_match(selected_match)
    
    # Calculate Winner for Display
    probs = {
        selected_match['home_team']: prediction['home_win_prob'],
        "Draw": prediction['draw_prob'],
        selected_match['away_team']: prediction['away_win_prob']
    }
    predicted_winner = max(probs, key=probs.get)
    win_prob = probs[predicted_winner]
    
    st.markdown(f"<h2 style='text-align: center; color: #00cc96;'>🏆 Prediction: {predicted_winner} ({win_prob}%)</h2>", unsafe_allow_html=True)
    
    # Visualization: Donut Chart for Win Probabilities
    labels = [f"Home: {selected_match['home_team']}", 'Draw', f"Away: {selected_match['away_team']}"]
    values = [prediction['home_win_prob'], prediction['draw_prob'], prediction['away_win_prob']]
    colors = ['#00cc96', '#ab63fa', '#ef553b'] # Green, Purple, Redish
    
    fig_donut = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6, marker_colors=colors)])
    fig_donut.update_layout(
        annotations=[dict(text=f"{max(values)}%", x=0.5, y=0.5, font_size=20, showarrow=False)],
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=14),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
    )
    st.plotly_chart(fig_donut, use_container_width=True)

    # Reasoning Text
    st.info(f"💡 **AI Insight:** {prediction['reasoning']}")

# --- Radar Chart Section ---
st.markdown("---")
st.subheader("📊 Tactical Analysis (Radar Chart)")

def create_radar_chart(home_team, away_team, home_strength, away_strength):
    categories = ['Attack', 'Defense', 'Midfield', 'Counter', 'Set Pieces']
    
    # Generate semi-random stats based on strength tier (High tier = high stats)
    # Strength 1 = 80-99, 2 = 60-85, 3 = 40-70
    np.random.seed(len(home_team) + len(away_team)) # Consistent random per match
    
    def get_stats(tier):
        if tier == 1: return np.random.randint(80, 99, 5)
        elif tier == 2: return np.random.randint(60, 85, 5)
        else: return np.random.randint(40, 70, 5)

    home_stats = get_stats(selected_match['home_strength'])
    away_stats = get_stats(selected_match['away_strength'])

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=home_stats,
        theta=categories,
        fill='toself',
        name=home_team,
        line_color='#00cc96',
        opacity=0.7,
        line=dict(width=3)
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=away_stats,
        theta=categories,
        fill='toself',
        name=away_team,
        line_color='#ef553b',
        opacity=0.7,
        line=dict(width=3)
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(color='white', size=10),
                gridcolor='#555'
            ),
            angularaxis=dict(
                tickfont=dict(color='white', size=12, weight='bold'),
                rotation=90,
                direction="clockwise"
            ),
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
    )
    return fig

radar_fig = create_radar_chart(
    selected_match['home_team'], 
    selected_match['away_team'], 
    selected_match['home_strength'], 
    selected_match['away_strength']
)
st.plotly_chart(radar_fig, use_container_width=True)

# Footer
st.markdown("---")
st.caption("Powered by Advanced Python Algorithms & Streamlit | Built for Premier League Fans")
