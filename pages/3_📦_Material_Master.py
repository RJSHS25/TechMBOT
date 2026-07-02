import streamlit as st
from utils import render_search_page

st.title("📦 Material Master")

tab1, tab2 = st.tabs([
    "Material Search Engine",
    "PR Creation in SAP"
])

with tab1:
    render_search_page(
        title="Material Search Engine",
        csv_file="Finance_data.csv",
        page_name="Material Master"
    )

with tab2:
    st.subheader("PR Creation in SAP")
    st.info("Add PR Creation SAP content here.")
