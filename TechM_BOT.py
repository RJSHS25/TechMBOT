import streamlit as st
import pandas as pd
import os

st.set_page_config(layout="wide")

# ===============================
# 📄 LOAD DATA (GLOBAL)
# ===============================
@st.cache_data
def load_data():
    return pd.read_csv("knowledge_base.csv")

df = load_data()

# ===============================
# 🧠 HEADER
# ===============================
st.title("🗺️ Maps Knowledge Portal")
st.markdown("### Learn, Navigate, and Explore Mapping Concepts")

# ===============================
# 🔍 GLOBAL SEARCH (HOME)
# ===============================
st.markdown("## 🔍 Search Knowledge")

search_input = st.text_input("Type to search (e.g. boundary, signal...)")

if search_input:
    filtered = df[df["Topic"].str.contains(search_input, case=False, na=False)]

    if not filtered.empty:
        selected_topic = st.selectbox("Suggestions", filtered["Topic"].unique())

        selected_row = filtered[filtered["Topic"] == selected_topic].iloc[0]

        # 🚀 Redirect based on category
        category = selected_row["Category"]

        if st.button("Go to Result"):
            if category == "Linear":
                st.switch_page("pages/1_Linear.py")
            elif category == "Polygon":
                st.switch_page("pages/2_Polygon.py")
            elif category == "Signals":
                st.switch_page("pages/3_Signals.py")
    else:
        st.warning("No results found")

st.markdown("---")

# ===============================
# 🎥 VIDEO (CONTROLLED SIZE)
# ===============================
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.video("https://www.youtube.com/watch?v=hA_-MkU0Nfw")

st.markdown("---")

# ===============================
# 🧭 DOMAIN CARDS
# ===============================
st.markdown("## 🚀 Choose Your Domain")

col1, col2, col3 = st.columns(3)

# 🛣️ LINEAR
with col1:
    img_path = os.path.join(os.getcwd(), "images/linear.png")

    if os.path.exists(img_path):
        st.image(img_path, use_container_width=True)
    else:
        st.warning("Linear image missing")

    st.markdown("### 🛣️ Linear")
    st.markdown("Explore line mapping and boundaries")

    if st.button("Go to Linear", key="linear"):
        st.switch_page("pages/1_Linear.py")

# 🔷 POLYGON
with col2:
    img_path = os.path.join(os.getcwd(), "images/polygon.png")

    if os.path.exists(img_path):
        st.image(img_path, use_container_width=True)
    else:
        st.warning("Polygon image missing")

    st.markdown("### 🔷 Polygon")
    st.markdown("Area mapping and geometry")

    if st.button("Go to Polygon", key="polygon"):
        st.switch_page("pages/2_Polygon.py")

# 🚦 SIGNALS
with col3:
    img_path = os.path.join(os.getcwd(), "images/signals.png")

    if os.path.exists(img_path):
        st.image(img_path, use_container_width=True)
    else:
        st.warning("Signals image missing")

    st.markdown("### 🚦 Signals")
    st.markdown("Traffic signal configurations")

    if st.button("Go to Signals", key="signals"):
        st.switch_page("pages/3_Signals.py")
