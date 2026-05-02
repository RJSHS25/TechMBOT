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
selected_row = topic_df[topic_df["Topic"] == topic].iloc[0]

# ===============================
# 🖥️ MAIN 3 COLUMN LAYOUT
# ===============================
left_space, center, right = st.columns([1, 3, 1])

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
