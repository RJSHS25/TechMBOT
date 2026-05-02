import streamlit as st
import pandas as pd
from fuzzywuzzy import fuzz

# 📄 Load data
@st.cache_data
def load_data():
    return pd.read_csv("knowledge_base.csv")

df = load_data()

# 🧠 Title
st.title("🗺️ Maps Knowledge Explorer")

# ===============================
# 🔍 SEARCH (your existing logic improved)
# ===============================
st.subheader("🔍 Search")

user_input = st.text_input("Ask anything (e.g. boundary, polygon rules...)")

matched_row = None

if user_input:
    matches = []
    for _, row in df.iterrows():
        text = f"{row['Topic']} {row['Description']}"
        score = fuzz.partial_ratio(user_input.lower(), text.lower())
        matches.append((row, score))

    best_match = sorted(matches, key=lambda x: x[1], reverse=True)[0]

    if best_match[1] > 50:
        matched_row = best_match[0]
    else:
        st.warning("No strong match found. Try navigation below.")

# ===============================
# 🧭 NAVIGATION (NEW FEATURE)
# ===============================
st.subheader("🧭 Browse Knowledge")

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

if not matched_row:
    matched_row = topic_df[topic_df["Topic"] == topic].iloc[0]

# ===============================
# 📄 DISPLAY SECTION
# ===============================
if matched_row is not None:
    st.markdown("---")

    st.success(f"### 📌 {matched_row['Topic']}")

    st.markdown(f"**📝 Description:** {matched_row['Description']}")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📊 Attributes")
        st.markdown(matched_row.get("Attributes", ""))

    with col2:
        st.markdown("### ⚙️ Specifications")
        st.markdown(matched_row.get("Specifications", ""))

    # 🖼️ Images
    images = str(matched_row.get("Images", "")).split(",")

    if images and images[0]:
        st.markdown("### 🖼️ Reference Images")
        for img in images:
            try:
                st.image(img.strip(), use_container_width=True)
            except:
                st.warning(f"Image not found: {img}")

    # 📌 PCIR
    if matched_row.get("PCIR"):
        st.info(f"📌 PCIR: {matched_row['PCIR']}")

    # 🛠️ Freshdesk
    if matched_row.get("Freshdesk"):
        st.info(f"🛠️ Freshdesk: {matched_row['Freshdesk']}")