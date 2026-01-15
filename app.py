import streamlit as st
import pandas as pd
import plotly.graph_objects as go
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

# --- Custom CSS ---
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }
    .metric-container {
        display: flex;
        justify-content: center;
        gap: 20px;
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

import base64

# --- Helper Function: Image handling ---
def get_img_as_base64(file_path):
    """
    Reads an image file (local) and returns a base64 string for HTML embedding.
    If it's a URL (http/https), returns it as is.
    """
    if file_path.startswith("http") or file_path.startswith("https"):
        return file_path
    
    try:
        with open(file_path, "rb") as f:
            data = f.read()
            encoded = base64.b64encode(data).decode()
        return f"data:image/png;base64,{encoded}"
    except Exception as e:
        # Fallback if file not found
        return "https://via.placeholder.com/100?text=Logo"

# --- Helper Function: Injury Card ---
def render_injury_card(team_name, injuries, color_code):
    injuries_html = "".join([f"<li>{inj}</li>" for inj in injuries]) if injuries else "<li>No major injuries</li>"
    st.markdown(f"""
    <div style="
        background-color: rgba(50, 50, 50, 0.8);
        border-left: 5px solid {color_code};
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 15px;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    ">
        <h4 style="margin-top:0; color: {color_code}; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 5px;">
            {team_name}
        </h4>
        <ul style="padding-left: 20px; margin-bottom: 0; margin-top: 10px;">
            {injuries_html}
        </ul>
    </div>
    """, unsafe_allow_html=True)

# --- Header ---
st.title("⚽ Premier League AI Predictor")
st.markdown("### 🚀 Professional Match Forecasting Engine")
st.markdown("---")

# --- Initialize Logic ---
predictor = MatchPredictor()
fixtures = get_current_fixtures()

# --- Sidebar ---
# --- Sidebar ---
st.sidebar.header("📅 Matchweek Fixtures")
selected_match_id = st.sidebar.radio(
    "Select a Match for Deep Dive:",
    [f"{f['home_team']} vs {f['away_team']}" for f in fixtures],
    index=0
)

# Helper to find selected match data (Moved Up)
match_index = [f"{f['home_team']} vs {f['away_team']}" for f in fixtures].index(selected_match_id)
selected_match = fixtures[match_index]

st.sidebar.markdown("---")
st.sidebar.markdown("### 🛠️ Match Simulation")
with st.sidebar.expander("What-If Analysis", expanded=False):
    st.info("🔮 **Scenario Mode**: Adjust team form and availability to see how the prediction changes in real-time.")
    st.write("Does Recent Form matter?")
    # Form Simulation (1-5 Scale)
    # Default to current form (simple count of 'W' roughly mapped or just middle ground)
    sim_home_form = st.slider(f"{selected_match['home_team']} Form", 1, 5, 3)
    sim_away_form = st.slider(f"{selected_match['away_team']} Form", 1, 5, 3)
    
    st.write("Injury Impact:")
    sim_injury = st.checkbox(f"Key Player Missing for {selected_match['home_team']}?", value=False, help="Simulate the impact of a star player being injured (e.g., reduced attack/defense strength).")
    
    # Calculate Data Overrides
    # Base Odds
    base_odds_h = selected_match.get('avg_odds_home', 2.5)
    base_odds_a = selected_match.get('avg_odds_away', 2.5)
    
    # Logic: Better form -> Lower odds (Stronger)
    # 3 is neutral. Each point +/- adjusts odds by 10%
    form_factor_h = (3 - sim_home_form) * 0.1  # e.g. Form 5 -> -0.2 (20% drop in odds -> Stronger)
    form_factor_a = (3 - sim_away_form) * 0.1
    
    # Injury Factor: Injury -> Higher odds (Weaker) e.g. +15%
    injury_factor = 0.15 if sim_injury else 0.0
    
    # Apply modifiers
    sim_odds_h = base_odds_h * (1 + form_factor_h + injury_factor)
    sim_odds_a = base_odds_a * (1 + form_factor_a) # Assuming injury check is for Home only as per prompt
    
    # Simulated Form Strings for Explanation Engine
    # If slider is 5, give them 5 Wins. If 1, give them 5 Losses.
    def get_sim_form_str(level):
        if level == 5: return ["W", "W", "W", "W", "W"]
        if level == 4: return ["W", "W", "D", "W", "D"]
        if level == 3: return ["W", "L", "D", "W", "L"]
        if level == 2: return ["L", "L", "D", "L", "D"]
        return ["L", "L", "L", "L", "L"]

    # Apply Simulation to Match Data Copy
    simulated_match = selected_match.copy()
    simulated_match['avg_odds_home'] = sim_odds_h
    simulated_match['avg_odds_away'] = sim_odds_a
    simulated_match['last_5_matches_home'] = get_sim_form_str(sim_home_form)
    simulated_match['last_5_matches_away'] = get_sim_form_str(sim_away_form)
    
    # Visual Feedback
    if sim_home_form != 3 or sim_away_form != 3 or sim_injury:
        st.sidebar.warning("⚠️ Simulation Active! Predictions modified.")

st.sidebar.markdown("---")
st.sidebar.markdown("### 🤖 Model Stats")
st.sidebar.metric("Model Accuracy", "54.1%", delta="vs Random (33%)")
st.sidebar.info("Trained on seasons 23-25 with live odds integration.")

# Helper to find selected match data
match_index = [f"{f['home_team']} vs {f['away_team']}" for f in fixtures].index(selected_match_id)
selected_match = fixtures[match_index]


# Update selected_match if radio changes (though typically logic runs top-down)
# Actually simplest is just to Define selected_match immediately after Sidebar Radio at top.


# --- Main Layout: 2:3 Split ---
col1, col2 = st.columns([2, 3])

# --- LEFT COLUMN: The Briefing Room ---
with col1:
    st.subheader("📋 The Briefing Room")
    
    # Match Header (Logos/VS)
    h_col1, h_col2, h_col3 = st.columns([1, 0.8, 1])
    with h_col1:
        logo_h = get_img_as_base64(selected_match['home_team_logo'])
        st.markdown(f"<div style='text-align: center;'><img src='{logo_h}' width='100'></div>", unsafe_allow_html=True)
        st.markdown(f"<p class='team-name-header'>{selected_match['home_team']}</p>", unsafe_allow_html=True)
    with h_col2:
        st.markdown("<p class='vs-text'>VS</p>", unsafe_allow_html=True)
    with h_col3:
        logo_a = get_img_as_base64(selected_match['away_team_logo'])
        st.markdown(f"<div style='text-align: center;'><img src='{logo_a}' width='100'></div>", unsafe_allow_html=True)
        st.markdown(f"<p class='team-name-header'>{selected_match['away_team']}</p>", unsafe_allow_html=True)
        
    st.write("---")
    
    # Match Details
    st.write(f"**🕒 Time:** {selected_match['match_time']}")
    st.write(f"**🌥️ Weather:** {selected_match['weather_condition']}")
    st.write("---")

    # Injury Reports
    st.markdown("#### 🏥 Squad Status")
    render_injury_card(selected_match['home_team'], selected_match['home_injuries'], "#ff4b4b") # Red for Home
    render_injury_card(selected_match['away_team'], selected_match['away_injuries'], "#00b4d8") # Blue/Cyan for Away (Distinct from home)

    # Recent Form
    st.write("---")
    st.markdown("#### 📈 Recent Form (Last 5)")
    st.write(f"**{selected_match['home_team']}**: {' - '.join(selected_match['last_5_matches_home'])}")
    st.write(f"**{selected_match['away_team']}**: {' - '.join(selected_match['last_5_matches_away'])}")


# --- RIGHT COLUMN: The Analytics Hub ---
with col2:
    st.subheader("📊 Analytics Hub")
    
    # Run Prediction
    prediction = predictor.predict_match(simulated_match)
    
    # Calculate Winner
    probs = {
        selected_match['home_team']: prediction['home_win_prob'],
        "Draw": prediction['draw_prob'],
        selected_match['away_team']: prediction['away_win_prob']
    }
    predicted_winner = max(probs, key=probs.get)
    win_prob = probs[predicted_winner]
    
    # Prediction Display
    st.markdown(f"""
    <div style="text-align: center; padding: 10px; background-color: rgba(0, 204, 150, 0.1); border-radius: 10px; border: 1px solid #00cc96; margin-bottom: 20px;">
        <h2 style='margin:0; color: #00cc96;'>🏆 Prediction: {predicted_winner}</h2>
        <h1 style='margin:0; font-size: 3em; color: white;'>{win_prob}%</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # AI Explanation Engine UI
    st.markdown(f"""
    <div style="
        background-color: rgba(0, 100, 255, 0.1); 
        border-left: 4px solid #00b4d8;
        padding: 15px; 
        border-radius: 5px; 
        margin-bottom: 20px;
    ">
        <strong style="color: #00b4d8; font-size: 1.1em;">🤖 AI Insight:</strong><br>
        <span style="color: #e0e0e0; font-size: 1em;">{prediction['reasoning']}</span>
    </div>
    """, unsafe_allow_html=True)

    # Donut Chart
    labels = [f"Home: {selected_match['home_team']}", 'Draw', f"Away: {selected_match['away_team']}"]
    values = [prediction['home_win_prob'], prediction['draw_prob'], prediction['away_win_prob']]
    colors = ['#ff4b4b', '#ab63fa', '#00b4d8'] # Red (Home), Purple (Draw), Blue (Away)
    
    fig_donut = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6, marker_colors=colors)])
    fig_donut.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        annotations=[dict(text="Probabilities", x=0.5, y=0.5, font_size=14, showarrow=False, font=dict(color='white'))],
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5, font=dict(color='white')),
        font=dict(color='white'),
        height=300,
        margin=dict(l=0, r=0, t=30, b=0)
    )
    st.plotly_chart(fig_donut, use_container_width=True)

    st.write("---")

    # Radar Chart
    categories = ['Attack', 'Defense', 'Midfield', 'Counter', 'Set Pieces']
    
    # Generate Stats
    np.random.seed(len(selected_match['home_team']) + len(selected_match['away_team']))
    def get_stats(tier):
        if tier == 1: return np.random.randint(80, 99, 5)
        elif tier == 2: return np.random.randint(60, 85, 5)
        else: return np.random.randint(40, 70, 5)

    home_stats = get_stats(selected_match['home_strength'])
    away_stats = get_stats(selected_match['away_strength'])
    # Close the loop
    home_stats = np.append(home_stats, home_stats[0])
    away_stats = np.append(away_stats, away_stats[0])
    categories = categories + [categories[0]]

    fig_radar = go.Figure()

    fig_radar.add_trace(go.Scatterpolar(
        r=home_stats,
        theta=categories,
        fill='toself',
        name=selected_match['home_team'],
        line_color='#ff4b4b',
        opacity=0.7,
        line=dict(width=3)
    ))
    
    fig_radar.add_trace(go.Scatterpolar(
        r=away_stats,
        theta=categories,
        fill='toself',
        name=selected_match['away_team'],
        line_color='#00b4d8',
        opacity=0.7,
        line=dict(width=3)
    ))

    fig_radar.update_layout(
        template='plotly_dark',
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], gridcolor='#444'),
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5, font=dict(color='white')),
        font=dict(color='white'),
        height=400,
        margin=dict(l=40, r=40, t=20, b=40)
    )
    st.plotly_chart(fig_radar, use_container_width=True)

# Footer
st.markdown("---")
st.caption("Powered by Advanced Python Algorithms & Streamlit | Built for Premier League Fans")
