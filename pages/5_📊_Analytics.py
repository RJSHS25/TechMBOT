import streamlit as st
import pandas as pd
import os

st.title("📊 Usage Analytics")

if os.path.exists("usage_logs.csv"):
    df_logs = pd.read_csv("usage_logs.csv")
    st.dataframe(df_logs, use_container_width=True)
else:
    st.info("No logs found yet.")
