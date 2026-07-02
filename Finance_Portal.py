import streamlit as st

st.set_page_config(
    page_title="Finance Portal",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 Finance Dashboard")

st.subheader("Welcome 👋")

st.write("This portal provides quick access to:")

st.markdown("""
- 🚚 Supplier Onboarding
- 📄 PO / Invoice Search
- 📦 Material Master
- 📚 Knowledge Repository
- 📊 Analytics
""")

st.write("Use the left sidebar to open each module.")

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
