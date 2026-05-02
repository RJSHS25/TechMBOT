import streamlit as st
import os

st.set_page_config(layout="wide")

st.title("🗺️ Maps Knowledge Portal")
st.markdown("### Learn, Navigate, and Explore Mapping Concepts")

# 🎥 Smaller centered video
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.video("https://www.youtube.com/watch?v=hA_-MkU0Nfw")

st.markdown("---")

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
