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

# ================= SAFE STATE COLUMN (CLOUD-PROOF) =================
STATE_COL = None
for col in df.columns:
    if "state" in col:
        STATE_COL = col
        break

if STATE_COL is None:
    st.error("❌ State column not found in CSV")
    st.write("Columns found:", df.columns.tolist())
    st.stop()

# ================= SESSION =================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ================= STYLES =================
st.markdown("""
<style>
body { background:#f4f7fb; }
.hero {
    background: linear-gradient(90deg,#0a4c8b,#1e88e5);
    padding:60px;
    border-radius:30px;
    color:white;
}
.big { font-size:44px; font-weight:800 }
.sub { font-size:18px; opacity:0.9 }
.stat-box {
    background:white;
    padding:22px;
    border-radius:20px;
    text-align:center;
    box-shadow:0 10px 30px rgba(0,0,0,0.08);
}
.frame {
    background:white;
    padding:40px;
    border-radius:30px;
    box-shadow:0 12px 35px rgba(0,0,0,0.08);
    margin-top:40px;
}
</style>
""", unsafe_allow_html=True)

# ================= LOGIN =================
if not st.session_state.logged_in:
    st.markdown("<br><br>", unsafe_allow_html=True)
    _, mid, _ = st.columns([1,2,1])

    with mid:
        st.markdown(
            "<h2 style='text-align:center;color:#1e88e5;'>🔐 Welcome to <b>SchemeAssist AI</b></h2>",
            unsafe_allow_html=True
        )

        name = st.text_input("Full Name")
        age = st.number_input("Age", 10, 100)
        income = st.number_input("Annual Income ₹", 0, 500000, 15000)

        state = st.selectbox(
            "State",
            ["Select your state"] + sorted(df[STATE_COL].dropna().unique())
        )

        category = st.selectbox(
            "Category",
            sorted(df["category"].dropna().unique())
        )

        if st.button("🚀 Enter Dashboard"):
            st.session_state.user = {
                "name": name,
                "age": age,
                "income": income,
                "state": state,
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
  <div class="big">🏛️ SchemeAssist AI</div>
  <div class="sub">Schemes curated for <b>{u['category']}</b> in <b>{u['state']}</b></div>
</div>
""", unsafe_allow_html=True)

# ================= FILTER =================
income = st.number_input("Income ₹", 0, 500000, u["income"])
state = st.selectbox("State", ["ALL"] + sorted(df[STATE_COL].dropna().unique()))
category = st.selectbox("Category", sorted(df["category"].dropna().unique()))

filtered = df[
    (df["min_income"] <= income) &
    (df["max_income"] >= income) &
    (
        (df[STATE_COL] == state) |
        (df[STATE_COL] == "ALL") |
        (state == "ALL")
    ) &
    (df["category"] == category)
]

filtered = filtered.sort_values(by=["deadline", "estimated_benefit"], ascending=[True, False])

st.markdown(f"## 🎯 Recommended Schemes ({len(filtered)})")

for _, s in filtered.iterrows():
    days = (s["deadline"] - datetime.now()).days
    score = random.randint(85, 98)

    st.markdown(f"### 🏷️ {s['scheme_name']}")
    st.write(f"💰 Benefit: ₹{int(s['estimated_benefit']):,}")
    st.write(f"⏳ Deadline: {s['deadline'].strftime('%d %b %Y')}")
    st.progress(score)
    st.markdown("---")

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<center>© 2026 SchemeAssist AI</center>", unsafe_allow_html=True)
