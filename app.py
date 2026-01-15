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
    .team-name {
        font-size: 1.2rem;
        font-weight: bold;
        color: #ffffff;
    }
    .vs-text {
        font-size: 1rem;
        color: #ff4b4b;
        font-style: italic;
    }
    .metric-container {
        display: flex;
        justify-content: center;
        gap: 20px;
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
    st.subheader("📋 Match Details")
    
    # Logos and Team Names
    c1, c2, c3 = st.columns([1, 0.5, 1])
    with c1:
        st.image(selected_match['home_team_logo'], width=80)
        st.write(f"**{selected_match['home_team']}**")
    with c2:
        st.write("")
        st.write("")
        st.markdown("<h3 style='text-align: center; color: #ff4b4b;'>VS</h3>", unsafe_allow_html=True)
    with c3:
        st.image(selected_match['away_team_logo'], width=80)
        st.write(f"**{selected_match['away_team']}**")

    st.write("---")
    st.write(f"**Date:** {selected_match['match_time']}")
    st.write(f"**Weather:** {selected_match['weather_condition']}")
    
    st.markdown("#### 🏥 Injury Report")
    st.error(f"**{selected_match['home_team']}**: {', '.join(selected_match['home_injuries']) if selected_match['home_injuries'] else 'None'}")
    st.warning(f"**{selected_match['away_team']}**: {', '.join(selected_match['away_injuries']) if selected_match['away_injuries'] else 'None'}")
    
    st.markdown("#### 📈 Recent Form (Last 5)")
    st.write(f"**{selected_match['home_team']}**: {' - '.join(selected_match['last_5_matches_home'])}")
    st.write(f"**{selected_match['away_team']}**: {' - '.join(selected_match['last_5_matches_away'])}")

with col2:
    st.subheader("🤖 AI Prediction Model")
    
    # Run Prediction
    prediction = predictor.predict_match(selected_match)
    
    # Visualization: Donut Chart for Win Probabilities
    labels = ['Home Win', 'Draw', 'Away Win']
    values = [prediction['home_win_prob'], prediction['draw_prob'], prediction['away_win_prob']]
    colors = ['#00cc96', '#ab63fa', '#ef553b'] # Green, Purple, Redish
    
    fig_donut = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6, marker_colors=colors)])
    fig_donut.update_layout(
        title_text=f"Win Probability: {selected_match['home_team']} vs {selected_match['away_team']}",
        annotations=[dict(text=f"{max(values)}%", x=0.5, y=0.5, font_size=20, showarrow=False)],
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
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
        line_color='#00cc96'
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=away_stats,
        theta=categories,
        fill='toself',
        name=away_team,
        line_color='#ef553b'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            ),
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        showlegend=True
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
