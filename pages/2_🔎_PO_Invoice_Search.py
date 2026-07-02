import streamlit as st
from utils.render_po_search import render_po_search

st.title("🔎 PO Invoice Search")

tab1, = st.tabs(["PO Search Engine"])

with tab1:
    render_po_search(
        title="PO Search Engine",
        csv_file="PO_data.csv",
        page_name="PO Search"
    )
