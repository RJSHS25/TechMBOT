import streamlit as st
import pandas as pd
import os

st.set_page_config(layout="wide")

st.title("📊 Analytics Dashboard")

# ===============================
# 📄 LOAD DATA
# ===============================
if not os.path.exists("usage_logs.csv"):
    st.warning("No usage data available yet")
    st.stop()

df = pd.read_csv("usage_logs.csv")

# Convert timestamp
df["Timestamp"] = pd.to_datetime(df["Timestamp"])

# ===============================
# 📊 TOP METRICS
# ===============================
col1, col2, col3 = st.columns(3)

col1.metric("Total Searches", len(df))
col2.metric("Unique Topics", df["Topic"].nunique())
col3.metric("Active Users", df["User"].nunique())

st.markdown("---")

# ===============================
# 🔥 TOP TOPICS
# ===============================
st.subheader("🔥 Most Viewed Topics")

top_topics = df["Topic"].value_counts().head(10)

st.bar_chart(top_topics)

# ===============================
# 👤 USER ACTIVITY
# ===============================
st.subheader("👤 Usage by User")

user_usage = df["User"].value_counts()

st.bar_chart(user_usage)

# ===============================
# 📈 USAGE OVER TIME
# ===============================
st.subheader("📈 Usage Trend")

df["Date"] = df["Timestamp"].dt.date
trend = df.groupby("Date").size()

st.line_chart(trend)

# ===============================
# 🗺️ HEATMAP (DAY vs HOUR)
# ===============================
st.subheader("🗺️ Usage Heatmap")

df["Hour"] = df["Timestamp"].dt.hour
df["Day"] = df["Timestamp"].dt.day_name()

heatmap = df.pivot_table(
    index="Day",
    columns="Hour",
    values="Topic",
    aggfunc="count"
).fillna(0)

st.dataframe(heatmap)
