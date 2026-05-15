import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from difflib import get_close_matches
from sklearn.linear_model import LinearRegression
import plotly.express as px
import random

# ==========================================
# KINDRED AI - PREMIUM FIGMA STYLE VERSION
# ==========================================

st.set_page_config(
    page_title="Kindred AI",
    page_icon="✨",
    layout="wide"
)

# ==========================================
# PREMIUM CSS
# ==========================================

st.markdown("""
<style>

/* Global */
.stApp {
    background: linear-gradient(135deg, #0f172a, #111827, #1e293b);
    color: white;
    font-family: 'Poppins', sans-serif;
}

/* Smooth transitions */
* {
    transition: all 0.3s ease;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: rgba(17,24,39,0.95);
    border-right: 1px solid rgba(255,255,255,0.08);
}

/* Cards */
.card {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.12);
    padding: 24px;
    border-radius: 24px;
    backdrop-filter: blur(16px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.35);
    margin-bottom: 20px;
}

/* Card hover */
.card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 40px rgba(99,102,241,0.35);
}

/* Metric boxes */
.metric-box {
    background: linear-gradient(135deg,#6366f1,#06b6d4);
    padding: 28px;
    border-radius: 24px;
    text-align: center;
    color: white;
    box-shadow: 0 10px 30px rgba(0,0,0,0.35);
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg,#4f46e5,#06b6d4);
    color: white;
    border: none;
    border-radius: 14px;
    padding: 12px 24px;
    font-weight: bold;
    width: 100%;
}

/* Button hover */
.stButton > button:hover {
    transform: scale(1.02);
    box-shadow: 0 0 20px rgba(99,102,241,0.6);
}

/* Inputs */
.stTextInput input {
    background-color: rgba(255,255,255,0.08) !important;
    color: white !important;
    border-radius: 14px !important;
}

.stSelectbox div[data-baseweb="select"] {
    background-color: rgba(255,255,255,0.08);
    border-radius: 14px;
}

/* Headers */
h1, h2, h3 {
    color: white;
    font-weight: 700;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border-radius: 18px;
    overflow: hidden;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# LOGIN SYSTEM
# ==========================================

USERS = {
    "Shivani Mohan": "1234",
    "child1": "1111",
    "child2": "2222",
    "admin": "admin"
}

if "auth" not in st.session_state:
    st.session_state.auth = False
    st.session_state.user = None

def login_page():

    st.markdown("""
    <div style='text-align:center;padding-top:80px'>
        <h1>👨‍👩‍👧‍👦 Kindred AI</h1>
        <p>Modern Family Intelligence Platform</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])

    with col2:

        st.markdown("<div class='card'>", unsafe_allow_html=True)

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):

            if username in USERS and USERS[username] == password:
                st.session_state.auth = True
                st.session_state.user = username
                st.rerun()

            else:
                st.error("Invalid credentials")

        st.markdown("</div>", unsafe_allow_html=True)

if not st.session_state.auth:
    login_page()
    st.stop()

# ==========================================
# SESSION STATE
# ==========================================

if "chat" not in st.session_state:
    st.session_state.chat = []

if "mood_log" not in st.session_state:
    st.session_state.mood_log = []

if "grocery_list" not in st.session_state:
    st.session_state.grocery_list = []

if "energy_usage" not in st.session_state:
    st.session_state.energy_usage = [5,6,4,7,8,6,9]

# ==========================================
# ML MODEL
# ==========================================

def energy_model():

    X = np.arange(len(st.session_state.energy_usage)).reshape(-1,1)
    y = np.array(st.session_state.energy_usage)

    model = LinearRegression()
    model.fit(X,y)

    return model

def energy_predict():

    model = energy_model()

    pred = model.predict([[len(st.session_state.energy_usage)]])
    return float(pred[0])

# ==========================================
# AI ENGINE
# ==========================================

kb = {
    "homework":"📚 Break tasks into smaller steps.",
    "stress":"🧘 Take breaks and relax.",
    "energy":"⚡ Turn off unused devices.",
    "family":"❤️ Communication improves bonding."
}

fallback = [
    "🤖 Analyzing family patterns...",
    "🧠 Learning emotional behavior trends...",
    "✨ Generating smart recommendation..."
]

def ai(q):

    q = q.lower()

    match = get_close_matches(
        q,
        list(kb.keys()),
        n=1,
        cutoff=0.3
    )

    if match:
        return kb[match[0]]

    for k in kb:
        if k in q:
            return kb[k]

    return random.choice(fallback)

# ==========================================
# MOOD SCORE
# ==========================================

def mood_score():

    if not st.session_state.mood_log:
        return 50

    mapping = {
        "Happy": 80,
        "Neutral": 50,
        "Stressed": 30,
        "Sad": 20
    }

    return int(np.mean([
        mapping[m[1]]
        for m in st.session_state.mood_log
    ]))

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.markdown(f"""
## 👋 Welcome
### {st.session_state.user}
""")

menu = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "🧠 AI",
        "🚨 Safety",
        "🛒 Grocery",
        "⚡ Energy",
        "😊 Mood",
        "📄 Report"
    ]
)

# ==========================================
# DASHBOARD
# ==========================================

if menu == "🏠 Dashboard":

    st.markdown("""
    <div class='card'>
        <h1>✨ Kindred AI</h1>
        <p>Your intelligent family wellness ecosystem.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(f"""
        <div class='metric-box'>
            <h3>😊 Mood Score</h3>
            <h1>{mood_score()}</h1>
            <p>Family wellness index</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:

        st.markdown(f"""
        <div class='metric-box'>
            <h3>⚡ Energy Forecast</h3>
            <h1>{round(energy_predict(),2)}</h1>
            <p>AI future prediction</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:

        st.markdown(f"""
        <div class='metric-box'>
            <h3>🛒 Grocery Items</h3>
            <h1>{len(st.session_state.grocery_list)}</h1>
            <p>House essentials tracked</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.subheader("📈 Energy Trend Analytics")

    df = pd.DataFrame({
        "Day": list(range(len(st.session_state.energy_usage))),
        "Usage": st.session_state.energy_usage
    })

    fig = px.line(
        df,
        x="Day",
        y="Usage",
        markers=True
    )

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='white'
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# AI ASSISTANT
# ==========================================

elif menu == "🧠 AI":

    st.title("🧠 Smart AI Assistant")

    q = st.text_input("Ask your AI assistant")

    if q:
        st.session_state.chat.append((q, ai(q)))

    for a, b in reversed(st.session_state.chat[-8:]):

        st.markdown(f"""
        <div class='card'>
        <b>👤 You:</b> {a}<br><br>
        <b>🤖 AI:</b> {b}
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# SAFETY
# ==========================================

elif menu == "🚨 Safety":

    st.title("🚨 Safety Center")

    if mood_score() < 40:
        st.error("⚠ Emotional risk detected")

    if energy_predict() > np.mean(st.session_state.energy_usage) + 2:
        st.warning("⚡ High energy usage predicted")

    st.info("💡 AI Suggestion: Schedule family relaxation time.")

    if st.button("Emergency Alert"):
        st.error("🚨 Emergency alert sent")

# ==========================================
# GROCERY
# ==========================================

elif menu == "🛒 Grocery":

    st.title("🛒 Smart Grocery")

    item = st.text_input("Add grocery item")

    if st.button("Add Item") and item:
        st.session_state.grocery_list.append(item)

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    for i, g in enumerate(st.session_state.grocery_list, 1):
        st.write(f"{i}. {g}")

    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# ENERGY
# ==========================================

elif menu == "⚡ Energy":

    st.title("⚡ Energy AI")

    df = pd.DataFrame({
        "Day": list(range(len(st.session_state.energy_usage))),
        "Usage": st.session_state.energy_usage
    })

    fig = px.area(
        df,
        x="Day",
        y="Usage"
    )

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='white'
    )

    st.plotly_chart(fig, use_container_width=True)

    st.success(f"🔮 Predicted Usage: {round(energy_predict(),2)}")

# ==========================================
# MOOD TRACKER
# ==========================================

elif menu == "😊 Mood":

    st.title("😊 Mood Tracker")

    mood = st.selectbox(
        "Select Mood",
        ["Happy","Neutral","Stressed","Sad"]
    )

    if st.button("Log Mood"):

        st.session_state.mood_log.append(
            (
                datetime.now().strftime("%H:%M"),
                mood
            )
        )

    df = pd.DataFrame(
        st.session_state.mood_log,
        columns=["Time","Mood"]
    )

    st.dataframe(df, use_container_width=True)

# ==========================================
# REPORT
# ==========================================

elif menu == "📄 Report":

    st.title("📄 Weekly AI Report")

    if st.button("Generate Report"):

        report = f"""
        FAMILY WELLNESS REPORT

        😊 Mood Score: {mood_score()}

        ⚡ Energy Forecast: {round(energy_predict(),2)}

        🛒 Grocery Items: {len(st.session_state.grocery_list)}

        🤖 AI Analysis:
        Family systems operating normally.
        """

        st.text_area(
            "Generated Report",
            report,
            height=300
        )
