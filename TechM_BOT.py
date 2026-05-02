import streamlit as st

st.set_page_config(layout="wide")

st.title("🗺️ Maps Knowledge Portal")

st.markdown("### Select a domain")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🛣️ Linear"):
        st.switch_page("pages/1_Linear.py")

with col2:
    if st.button("🔷 Polygon"):
        st.switch_page("pages/2_Polygon.py")

with col3:
    if st.button("🚦 Signals"):
        st.switch_page("pages/3_Signals.py")
