import streamlit as st
import pandas as pd
import os

def get_combined_matches(df, search_text):
    # your matching logic here
    return df

def log_usage(page_name, search_text):
    # your logging logic here
    pass

def render_search_page(title, csv_file, page_name):
    st.subheader(title)

    if os.path.exists(csv_file):
        df = pd.read_csv(csv_file)
    else:
        st.error(f"{csv_file} not found")
        return

    search_text = st.text_input("Search")

    if search_text:
        results = get_combined_matches(df, search_text)
        log_usage(page_name, search_text)
        st.dataframe(results, use_container_width=True)
    else:
        st.dataframe(df, use_container_width=True)
