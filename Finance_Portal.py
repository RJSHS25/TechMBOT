import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Finance Portal",
    page_icon="🏠",
    layout="wide"
)

# -------------------------------
# LOGIN CHECK
# -------------------------------

def load_allowed_users():
    if os.path.exists("allowed_users.csv"):
        df = pd.read_csv("allowed_users.csv")
        df.columns = df.columns.str.strip().str.lower()
        return df
    return pd.DataFrame(columns=["email"])


def login():
    st.title("🔐 Finance Portal Login")

    email = st.text_input("Enter your email address")

    if st.button("Login"):
        allowed_users = load_allowed_users()

        if "email" not in allowed_users.columns:
            st.error("allowed_users.csv must contain an 'email' column.")
            st.stop()

        allowed_emails = allowed_users["email"].astype(str).str.lower().str.strip().tolist()

        if email.lower().strip() in allowed_emails:
            st.session_state["logged_in"] = True
            st.session_state["user_email"] = email.lower().strip()
            st.rerun()
        else:
            st.error("Access denied. Your email is not authorized.")

    st.stop()


if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login()


# -------------------------------
# FINANCE DASHBOARD
# -------------------------------

st.title("🏠 Finance Dashboard")

st.subheader(f"Welcome {st.session_state.get('user_email', '')} 👋")

st.write("This portal provides quick access to:")

st.markdown("""
- 🚚 Supplier Onboarding
- 📄 PO / Invoice Search
- 📦 Material Master
- 📚 Knowledge Repository
- 📊 Analytics
""")

st.write("Use the left sidebar or the links below to open each module.")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.page_link(
        "pages/3_📦_Material_Master.py",
        label="📦 Open Material Master"
    )

    st.page_link(
        "pages/1_👥_Supplier_Onboarding.py",
        label="🚚 Open Supplier Onboarding"
    )

with col2:
    st.page_link(
        "pages/2_🔎_PO_Invoice_Search.py",
        label="📄 Open PO / Invoice Search"
    )

    st.page_link(
        "pages/4_📚_Knowledge_Repository.py",
        label="📚 Open Knowledge Repository"
    )

    st.page_link(
        "pages/5_📊_Analytics.py",
        label="📊 Open Analytics"
    )

st.divider()

if st.button("Logout"):
    st.session_state["logged_in"] = False
    st.session_state["user_email"] = ""
    st.rerun()
