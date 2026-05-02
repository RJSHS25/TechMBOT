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
# 🔍 SEARCH (LIVE SUGGESTIONS)
# ===============================
with st.sidebar:
    st.title("🧭 Navigation")

    # 🔍 Search
    st.markdown("## 🔍 Search")
    search_input = st.text_input("Search topic...", key="search_input")

    search_result = None

    if search_input:
        filtered = df[df["Topic"].str.contains(search_input, case=False, na=False)]

        if not filtered.empty:
            topic_search = st.selectbox(
                "Suggestions",
                filtered["Topic"].unique(),
                key="search_suggestions"
            )
            search_result = filtered[filtered["Topic"] == topic_search].iloc[0]

    st.markdown("---")

    # 🧭 Navigation
    project = st.selectbox(
        "Project",
        df["Project"].unique(),
        key="project_select"
    )

    category = st.selectbox(
        "Category",
        df[df["Project"] == project]["Category"].unique(),
        key="category_select"
    )

    subcategory = st.selectbox(
        "SubCategory",
        df[
            (df["Project"] == project) &
            (df["Category"] == category)
        ]["SubCategory"].unique(),
        key="subcategory_select"
    )

    topic_list = df[
        (df["Project"] == project) &
        (df["Category"] == category) &
        (df["SubCategory"] == subcategory)
    ]["Topic"].unique()

    topic = st.selectbox(
        "Topic",
        topic_list,
        key="topic_select"
    )

# ===============================
# 🧭 SIDEBAR NAVIGATION
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
# 🌳 DECISION TREE
# ===============================
st.markdown("## 🌳 Guided Decision Tree")

category_choice = st.radio(
    "What are you working on?",
    df["Category"].unique()
)

sub_df = df[df["Category"] == category_choice]

subcategory_choice = st.radio(
    "Select sub type",
    sub_df["SubCategory"].unique()
)

topic_df_tree = sub_df[sub_df["SubCategory"] == subcategory_choice]

topic_choice_tree = st.radio(
    "What do you want to know?",
    topic_df_tree["Topic"].unique()
)

tree_selected_row = topic_df_tree[
    topic_df_tree["Topic"] == topic_choice_tree
].iloc[0]

# ===============================
# 📄 FINAL SELECTION LOGIC
# ===============================
if search_result is not None:
    selected_row = search_result
elif tree_selected_row is not None:
    selected_row = tree_selected_row
else:
    selected_row = topic_df[topic_df["Topic"] == topic].iloc[0]

# ===============================
# 🖥️ LAYOUT
# ===============================
center, right = st.columns([4, 1])

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

    # 🖼️ IMAGE GRID WITH BOXES
    images = str(selected_row.get("Images", "")).split(",")

    if images and images[0]:
        st.markdown("### 🖼️ Reference Images")

        cols = st.columns(3)

        for i, img in enumerate(images):
            img_path = os.path.join(os.getcwd(), img.strip())

            if os.path.exists(img_path):
                with cols[i % 3]:
                    st.markdown(f"""
                    <div style="
                        border:1px solid #ddd;
                        padding:10px;
                        border-radius:8px;
                        text-align:center;
                    ">
                    """, unsafe_allow_html=True)

                    st.image(img_path, use_container_width=True)

                    st.markdown(f"<small>{img}</small></div>", unsafe_allow_html=True)
            else:
                st.error(f"❌ Not found: {img}")

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
# 📊 ANALYTICS (FIXED)
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
        st.markdown("### 🔥 Most Viewed Topics")
        st.dataframe(logs["Topic"].value_counts().head(5))

    with col2:
        st.markdown("### 👤 Usage by User")
        st.dataframe(logs["User"].value_counts())
