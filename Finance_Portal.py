import streamlit as st

st.set_page_config(page_title="Finance Dashboard", layout="wide")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔐 TechM Portal Login")
    email = st.text_input("Enter Email:")

    if st.button("Login"):
        if "@" in email:
            st.session_state.authenticated = True
            st.session_state.user_email = email
            st.rerun()
        else:
            st.error("Please enter a valid email.")

    st.stop()

st.title("🏠 Finance Dashboard")

st.markdown(f"""
### Welcome **{st.session_state.user_email}** 👋

This portal provides quick access to:

- 🚚 Supplier Onboarding
- 📄 PO / Invoice Search
- 📦 Material Master
- 📚 Knowledge Repository
- 📊 Analytics

Use the left sidebar to open each module.
""")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.page_link("pages/1_👥_Supplier_Onboarding.py", label="📦 Open Material Master")
    st.page_link("pages/2_🔎_PO_Invoice_Search.py", label="🚚 Open Supplier Onboarding")

with col2:
    st.page_link("pages/3_📦_Material_Master.py", label="📄 Open PO / Invoice Search")
    st.page_link("pages/4_📚_Knowledge_Repository.py", label="📚 Open Knowledge Repository")
    st.page_link("pages/5_📊_Analytics.py", label="📊 Open Analytics")
