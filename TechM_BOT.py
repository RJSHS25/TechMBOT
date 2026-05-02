import streamlit as st
import pandas as pd
import os

st.set_page_config(layout="wide")

# ===============================
# 📄 LOAD DATA
# ===============================
@st.cache_data
def load_data():
    return pd.read_csv("knowledge_base.csv")

df = load_data()

# ===============================
# 🧭 TOP NAV BAR
# ===============================
nav1, nav2 = st.columns([3, 2])

with nav1:
    st.markdown("## 🗺️ Maps Knowledge Portal")

with nav2:
    search_input = st.text_input(
        "🔍 Search",
        placeholder="Search topics...",
        label_visibility="collapsed"
    )

# ===============================
# 🔍 FUZZY SEARCH (SMART SEARCH)
# ===============================
from fuzzywuzzy import fuzz

if search_input:
    matches = []

    for _, row in df.iterrows():
        text = f"{row['Topic']} {row['Description']}"
        score = fuzz.partial_ratio(search_input.lower(), text.lower())
        matches.append((row, score))

    # Sort top 5 matches
    top_matches = sorted(matches, key=lambda x: x[1], reverse=True)[:5]

    # Keep only good matches
    options = [
        f"{m[0]['Category']} → {m[0]['Topic']}"
        for m in top_matches if m[1] > 50
    ]

    if options:
        selected_option = st.selectbox(
            "Results",
            options,
            key="top_search"
        )

        # Extract topic back
        selected_topic = selected_option.split("→")[1].strip()

        selected_row = df[df["Topic"] == selected_topic].iloc[0]
        category = selected_row["Category"]

        if st.button("Open", key="open_result"):
            if category == "Linear":
                st.switch_page("pages/1_Linear.py")
            elif category == "Polygon":
                st.switch_page("pages/2_Polygon.py")
            elif category == "Signals":
                st.switch_page("pages/3_Signals.py")
    else:
        st.caption("No close matches found")

# ===============================
# 🔍 SEARCH LOGIC (COMPACT)
# ===============================
if search_input:
    filtered = df[df["Topic"].str.contains(search_input, case=False, na=False)]

    if not filtered.empty:
        selected_topic = st.selectbox(
            "Results",
            filtered["Topic"].unique(),
            key="top_search"
        )

        selected_row = filtered[filtered["Topic"] == selected_topic].iloc[0]

        category = selected_row["Category"]

        if st.button("Open", key="open_result"):
            if category == "Linear":
                st.switch_page("pages/1_Linear.py")
            elif category == "Polygon":
                st.switch_page("pages/2_Polygon.py")
            elif category == "Signals":
                st.switch_page("pages/3_Signals.py")

    else:
        st.caption("No matches found")

# ===============================
# 🎥 VIDEO (CENTERED SMALL)
# ===============================
st.markdown("---")

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.video("https://www.youtube.com/watch?v=hA_-MkU0Nfw")

# ===============================
# 🧭 DOMAIN CARDS
# ===============================
st.markdown("---")
st.markdown("## 🚀 Choose Your Domain")

col1, col2, col3 = st.columns(3)

# 🛣️ LINEAR
with col1:
    img = os.path.join(os.getcwd(), "images/linear.png")

    if os.path.exists(img):
        st.image(img, use_container_width=True)

    st.markdown("### 🛣️ Linear")
    st.caption("Line mapping, boundaries, attributes")

    if st.button("Open Linear", key="linear_btn"):
        st.switch_page("pages/1_Linear.py")

# 🔷 POLYGON
with col2:
    img = os.path.join(os.getcwd(), "images/polygon.png")

    if os.path.exists(img):
        st.image(img, use_container_width=True)

    st.markdown("### 🔷 Polygon")
    st.caption("Area mapping and geometry")

    if st.button("Open Polygon", key="polygon_btn"):
        st.switch_page("pages/2_Polygon.py")

# 🚦 SIGNALS
with col3:
    img = os.path.join(os.getcwd(), "images/signals.png")

    if os.path.exists(img):
        st.image(img, use_container_width=True)

    st.markdown("### 🚦 Signals")
    st.caption("Traffic signal configurations")

    if st.button("Open Signals", key="signals_btn"):
        st.switch_page("pages/3_Signals.py")
