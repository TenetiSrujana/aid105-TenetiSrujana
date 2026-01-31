import streamlit as st
import pandas as pd
from datetime import datetime
import random

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="SchemeAssist AI",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ================= LOAD DATA =================
@st.cache_data
def load_data():
    df = pd.read_csv("src/data/schemes_master.csv", encoding="utf-8-sig")
    df.columns = df.columns.str.strip().str.lower()
    df["deadline"] = pd.to_datetime(df["deadline"])
    return df

df = load_data()

# ================= SESSION =================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ================= STYLES =================
st.markdown("""
<style>
.hero {
    background: linear-gradient(90deg,#0a4c8b,#1e88e5);
    padding:50px;
    border-radius:25px;
    color:white;
}
.stat-box {
    background:white;
    padding:20px;
    border-radius:18px;
    text-align:center;
    box-shadow:0 8px 25px rgba(0,0,0,0.08);
}
.frame {
    background:white;
    padding:35px;
    border-radius:25px;
    margin-top:30px;
}
</style>
""", unsafe_allow_html=True)

# ================= LOGIN =================
if not st.session_state.logged_in:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center;color:#1e88e5;'>🔐 Welcome to <b>SchemeAssist AI</b></h2>", unsafe_allow_html=True)

    name = st.text_input("Full Name")
    age = st.number_input("Age", 10, 100)
    income = st.number_input("Annual Income ₹", 0, 500000, 15000)

    category = st.selectbox(
        "Category",
        sorted(df["category"].unique())
    )

    if st.button("🚀 Enter Dashboard"):
        st.session_state.user = {
            "name": name,
            "age": age,
            "income": income,
            "category": category
        }
        st.session_state.logged_in = True
        st.rerun()

    st.stop()

u = st.session_state.user

# ================= DASHBOARD =================
st.markdown("<div class='frame'>", unsafe_allow_html=True)

st.markdown(f"""
<div class="hero">
  <h1>🏛️ SchemeAssist AI</h1>
  <p>AI-curated schemes for <b>{u['category']}</b></p>
</div>
""", unsafe_allow_html=True)

# FILTERS
income = st.slider("Income ₹", 0, 500000, u["income"])
category = st.selectbox("Category", sorted(df["category"].unique()))

filtered = df[
    (df["min_income"] <= income) &
    (df["max_income"] >= income) &
    (df["category"] == category)
]

filtered = filtered.sort_values(
    by=["deadline", "estimated_benefit"],
    ascending=[True, False]
)

# STATS
c1, c2 = st.columns(2)
c1.markdown(f"<div class='stat-box'><h2>{len(filtered)}</h2><p>Total Schemes</p></div>", unsafe_allow_html=True)
c2.markdown(f"<div class='stat-box'><h2>{category}</h2><p>Category</p></div>", unsafe_allow_html=True)

st.markdown("## 🎯 Recommended Schemes")

for _, s in filtered.iterrows():
    days = (s["deadline"] - datetime.now()).days
    urgency = "HIGH" if days < 30 else "MEDIUM"
    score = random.randint(85, 97)

    st.markdown(f"### 🏷️ {s['scheme_name']}")
    st.write(f"💰 Benefit: ₹{int(s['estimated_benefit']):,}")
    st.write(f"⏰ Deadline: {s['deadline'].strftime('%d %b %Y')}")
    st.write(f"🔥 Urgency: {urgency}")
    st.progress(score)

    st.markdown("---")

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<center>© 2026 SchemeAssist AI</center>", unsafe_allow_html=True)
