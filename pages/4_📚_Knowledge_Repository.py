import streamlit as st

st.title("📚 Knowledge Repository")

tab1, tab2 = st.tabs(["SOPs", "Process Maps"])

with tab1:
    st.subheader("SOPs")
    st.info("Add SOP links/files here.")

with tab2:
    st.subheader("Process Maps")
    st.info("Add process map links/files here.")
