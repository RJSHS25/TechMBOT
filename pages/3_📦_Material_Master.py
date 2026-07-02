import streamlit as st
from utils.search_engine import render_search_page

st.title("📦 Material Master")

tab1, tab2 = st.tabs([
    "Material Master Search Engine",
    "PR Creation SAP"
])

with tab1:
    render_search_page(
        title="Material Master",
        csv_file="data.csv",
        page_name="Material Master"
    )

with tab2:
    st.write("Coming Soon...")
