import streamlit as st
import pandas as pd
import os
from datetime import datetime

@st.cache_data
def load_data():
    return pd.read_csv("knowledge_base.csv")

def sidebar_navigation(df):
    st.sidebar.title("🧭 Navigation")

    # 🔍 Search
    st.sidebar.markdown("## 🔍 Search")
    search_input = st.sidebar.text_input("Search topic...", key="search_input")

    search_result = None

    if search_input:
        filtered = df[df["Topic"].str.contains(search_input, case=False, na=False)]

        if not filtered.empty:
            topic_search = st.sidebar.selectbox(
                "Suggestions",
                filtered["Topic"].unique(),
                key="search_suggestions"
            )
            search_result = filtered[filtered["Topic"] == topic_search].iloc[0]

    st.sidebar.markdown("---")

    subcategory = st.sidebar.selectbox(
        "SubCategory",
        df["SubCategory"].unique(),
        key="subcategory_select"
    )

    topic_df = df[df["SubCategory"] == subcategory]

    topic = st.sidebar.selectbox(
        "Topic",
        topic_df["Topic"].unique(),
        key="topic_select"
    )

    return search_result, topic_df, topic


def render_content(selected_row):
    center, right = st.columns([4, 1])

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

        # Images
        images = str(selected_row.get("Images", "")).split(",")

        if images and images[0]:
            st.markdown("### 🖼️ Reference Images")

            cols = st.columns(3)

            for i, img in enumerate(images):
                img_path = os.path.join(os.getcwd(), img.strip())

                if os.path.exists(img_path):
                    with cols[i % 3]:
                        st.markdown("""
                        <div style="border:1px solid #ddd;padding:10px;border-radius:8px;text-align:center;">
                        """, unsafe_allow_html=True)

                        st.image(img_path, use_container_width=True)

                        st.markdown(f"<small>{img}</small></div>", unsafe_allow_html=True)
                else:
                    st.error(f"❌ Not found: {img}")

    with right:
        st.markdown("## 📌 Details")

        if selected_row.get("PCIR"):
            st.success(f"📌 PCIR\n\n{selected_row['PCIR']}")

        if selected_row.get("Freshdesk"):
            st.info(f"🛠️ Freshdesk\n\n{selected_row['Freshdesk']}")


def log_usage(selected_row):
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


def show_analytics():
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
