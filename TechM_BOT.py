import streamlit as st

st.set_page_config(layout="wide")

# ===============================
# 🎥 HEADER VIDEO
# ===============================
st.title("🗺️ Maps Knowledge Portal")

st.markdown("### Learn, Navigate, and Explore Mapping Concepts")

st.video("https://www.youtube.com/watch?v=hA_-MkU0Nfw")

st.markdown("---")

# ===============================
# 🧭 DOMAIN SELECTION CARDS
# ===============================
st.markdown("## 🚀 Choose Your Domain")

col1, col2, col3 = st.columns(3)

# 🛣️ LINEAR
with col1:
    st.image("images/linear.png", use_container_width=True)
    st.markdown("### 🛣️ Linear (Lanes)")
    st.markdown("Explore line mapping, boundaries, and attributes")

    if st.button("Go to Linear", key="linear_btn"):
        st.switch_page("pages/1_Linear.py")

# 🔷 POLYGON
with col2:
    st.image("images/polygon.png", use_container_width=True)
    st.markdown("### 🔷 Polygon")
    st.markdown("Understand area mapping and geometry rules")

    if st.button("Go to Polygon", key="polygon_btn"):
        st.switch_page("pages/2_Polygon.py")

# 🚦 SIGNALS
with col3:
    st.image("images/signals.png", use_container_width=True)
    st.markdown("### 🚦 Signals")
    st.markdown("Traffic signals, logic, and configurations")

    if st.button("Go to Signals", key="signals_btn"):
        st.switch_page("pages/3_Signals.py")
