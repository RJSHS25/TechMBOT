import streamlit as st

st.title("👥 Supplier Onboarding")

tab1, tab2 = st.tabs([
    "Supplier Onboarding Status",
    "Sample Guide for Questionnaire"
])

with tab1:
    st.subheader("Supplier Onboarding Status")
    st.info("Add Supplier Onboarding Status search here.")

with tab2:
    st.subheader("Sample Guide for Questionnaire")
    st.info("Add questionnaire guide here.")
