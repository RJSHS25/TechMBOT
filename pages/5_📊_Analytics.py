import streamlit as st
import pandas as pd
import os

st.title("📊 Usage Analytics")

log_file = "usage_logs.csv"

if not os.path.exists(log_file):
    st.info("No usage logs found yet.")
    st.stop()

df_logs = pd.read_csv(log_file)
df_logs.columns = df_logs.columns.str.strip()

if df_logs.empty:
    st.info("No usage data available yet.")
    st.stop()

st.subheader("Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Total Searches", len(df_logs))

if "Page" in df_logs.columns:
    most_used_page = df_logs["Page"].mode()[0]
    col2.metric("Most Used Page", most_used_page)
else:
    col2.metric("Most Used Page", "N/A")

if "Search Text" in df_logs.columns:
    unique_searches = df_logs["Search Text"].nunique()
    col3.metric("Unique Searches", unique_searches)
else:
    col3.metric("Unique Searches", "N/A")

st.divider()

st.subheader("Recent Searches")
st.dataframe(
    df_logs.tail(10).sort_index(ascending=False),
    use_container_width=True,
    hide_index=True
)

if "Page" in df_logs.columns:
    st.divider()
    st.subheader("Page-wise Usage")

    page_usage = (
        df_logs["Page"]
        .value_counts()
        .reset_index()
    )

    page_usage.columns = ["Page", "Search Count"]

    st.bar_chart(
        page_usage,
        x="Page",
        y="Search Count"
    )

if "Search Text" in df_logs.columns:
    st.divider()
    st.subheader("Top Search Terms")

    top_searches = (
        df_logs["Search Text"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    top_searches.columns = ["Search Text", "Count"]

    st.dataframe(
        top_searches,
        use_container_width=True,
        hide_index=True
    )
