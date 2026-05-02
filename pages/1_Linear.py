import streamlit as st
from utils.common import load_data, sidebar_navigation, render_content, log_usage, show_analytics

st.set_page_config(layout="wide")

df = load_data()

# Filter
df = df[df["Category"] == "Linear"]

search_result, topic_df, topic = sidebar_navigation(df)

if search_result is not None:
    selected_row = search_result
else:
    selected_row = topic_df[topic_df["Topic"] == topic].iloc[0]

render_content(selected_row)
log_usage(selected_row)
show_analytics()
