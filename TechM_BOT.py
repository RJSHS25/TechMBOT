import streamlit as st
import pandas as pd

# 📄 Load data
@st.cache_data
def load_data():
    return pd.read_csv("knowledge_base.csv")

df = load_data()

st.set_page_config(layout="wide")

# ===============================
# 🧭 LEFT NAVIGATION PANEL
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
# 📄 GET SELECTED ROW
# ===============================
if search_result is not None:
    selected_row = search_result
else:
    selected_row = topic_df[topic_df["Topic"] == topic].iloc[0]

# ===============================
# 🖥️ MAIN 3 COLUMN LAYOUT
# ===============================
left_space, center, right = st.columns([4, 1])

# ===============================
# 🎯 CENTER CONTENT
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

    # 🖼️ Images
    images = str(selected_row.get("Images", "")).split(",")

    if images and images[0]:
        st.markdown("### 🖼️ Reference Images")
        for img in images:
            try:
                st.image(img.strip(), use_container_width=True)
            except:
                st.warning(f"Image not found: {img}")

# ===============================
# 📌 RIGHT PANEL (PCIR + Freshdesk)
# ===============================
with right:
    st.markdown("## 📌 Details")

    pcir = selected_row.get("PCIR", "")
    if pcir:
        st.success(f"📌 PCIR\n\n{pcir}")

    freshdesk = selected_row.get("Freshdesk", "")
    if freshdesk:
        st.info(f"🛠️ Freshdesk\n\n{freshdesk}")



# ===============================
# 📌 Search
# ===============================


from fuzzywuzzy import fuzz

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
# 📌 Analytics
# ===============================
from datetime import datetime
import os

log_entry = {
    "User": "demo_user",  # replace with login later
    "Topic": selected_row["Topic"],
    "Category": selected_row["Category"],
    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}

log_file = "usage_logs.csv"

pd.DataFrame([log_entry]).to_csv(
    log_file,
    mode='a',
    header=not os.path.exists(log_file),
    index=False
)

st.markdown("---")
st.markdown("## 📊 Analytics")

if os.path.exists("usage_logs.csv"):
    logs = pd.read_csv("usage_logs.csv")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🔥 Most Viewed Topics")
        st.dataframe(logs["Topic"].value_counts().head(5))

    with col2:
        st.markdown("### 👤 Usage by User")
        st.dataframe(logs["User"].value_counts())
