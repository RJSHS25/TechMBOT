import streamlit as st
import pandas as pd
from fuzzywuzzy import fuzz
from datetime import datetime
import os

st.set_page_config(layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("knowledge_base.csv")

df = load_data()

# ===============================
# 🔍 SEARCH FIRST (FIXED)
# ===============================
st.sidebar.markdown("## 🔍 Search")
search_input = st.sidebar.text_input("Search topic...")

search_result = None

if search_input:
    scores = []
    for _, row in df.iterrows():
        text = f"{row['Topic']} {row['Description']}"
        score = fuzz.partial_ratio(search_input.lower(), text.lower())
        scores.append((row, score))

    best_match = sorted(scores, key=lambda x: x[1], reverse=True)[0]

    if best_match[1] > 50:
        search_result = best_match[0]

# ===============================
# 🧭 NAVIGATION
# ===============================
with st.sidebar:
    st.title("🧭 Navigation")

    project = st.selectbox("Project", df["Project"].unique())

    category = st.selectbox(
        "Category",
        df[df["Project"] == project]["Category"].unique()
    )

    subcategory = st.selectbox(
        "SubCategory",
        df[
            (df["Project"] == project) &
            (df["Category"] == category)
        ]["SubCategory"].unique()
    )

    topic_df = df[
        (df["Project"] == project) &
        (df["Category"] == category) &
        (df["SubCategory"] == subcategory)
    ]

    topic = st.selectbox("Topic", topic_df["Topic"].unique())

# ===============================
# 📄 SELECT ROW
# ===============================
if search_result is not None:
    selected_row = search_result
else:
    selected_row = topic_df[topic_df["Topic"] == topic].iloc[0]

# ===============================
# 🖥️ LAYOUT FIXED
# ===============================
center, right = st.columns([4, 1])

# ===============================
# 🎯 CENTER
# ===============================
with center:
    st.title(f"📌 {selected_row['Topic']}")
    st.markdown(f"**📝 Description:** {selected_row['Description']}")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📊 Attributes")
        st.markdown(selected_row.get("Attributes", ""))

    with col2:
        st.markdown("### ⚙️ Specifications")
        st.markdown(selected_row.get("Specifications", ""))

    images = str(selected_row.get("Images", "")).split(",")

    if images and images[0]:
        st.markdown("### 🖼️ Reference Images")
        for img in images:
            img_path = os.path.join(os.getcwd(), img.strip())
            if os.path.exists(img_path):
                st.image(img_path, use_container_width=True)
            else:
                st.error(f"❌ Image not found: {img_path}")

# ===============================
# 📌 RIGHT PANEL
# ===============================
with right:
    st.markdown("## 📌 Details")

    if selected_row.get("PCIR"):
        st.success(f"📌 PCIR\n\n{selected_row['PCIR']}")

    if selected_row.get("Freshdesk"):
        st.info(f"🛠️ Freshdesk\n\n{selected_row['Freshdesk']}")

# ===============================
# 📊 ANALYTICS FIXED
# ===============================
if "last_topic" not in st.session_state:
    st.session_state.last_topic = None

if st.session_state.last_topic != selected_row["Topic"]:
    log_entry = {
        "User": "demo_user",
        "Topic": selected_row["Topic"],
        "Category": selected_row["Category"],
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    pd.DataFrame([log_entry]).to_csv(
        "usage_logs.csv",
        mode='a',
        header=not os.path.exists("usage_logs.csv"),
        index=False
    )

    st.session_state.last_topic = selected_row["Topic"]

st.markdown("---")
st.markdown("## 📊 Analytics")

if os.path.exists("usage_logs.csv"):
    logs = pd.read_csv("usage_logs.csv")

    col1, col2 = st.columns(2)

    with col1:
        st.dataframe(logs["Topic"].value_counts().head(5))

    with col2:
        st.dataframe(logs["User"].value_counts())
