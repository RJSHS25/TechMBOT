import streamlit as st
from utils.search_engine import render_search_page

st.title("🔎 PO Invoice Search")

tab1, = st.tabs(["PO Search Engine"])

with tab1:
    render_search_page(
        title="PO Search Engine",
        csv_file="PO_data.csv",
        page_name="PO Search"
    )
