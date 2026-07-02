import streamlit as st
import pandas as pd
import os


def render_po_search(title, csv_file, page_name):
    st.subheader(title)

    if not os.path.exists(csv_file):
        st.error(f"{csv_file} not found.")
        return

    df = pd.read_csv(csv_file, sep=None, engine="python")
    df.columns = df.columns.str.replace("\ufeff", "", regex=False).str.strip()

    required_columns = [
        "PO#",
        "Month",
        "Year",
        "PO Status",
        "Invoice #",
        "PO Value#",
        "Invoice Amount",
        "PO Limit",
        "Delivery Status",
        "Invoice Status"
    ]

    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        st.error(f"Missing columns: {missing_columns}")
        st.write("Columns found:", df.columns.tolist())
        return

    search_text = st.text_input("🔍 Search by PO Number or Invoice Number")

    if not search_text:
        st.info("Enter a PO Number or Invoice Number to begin your search.")
        return

    search_text = search_text.strip()

    df["PO#"] = df["PO#"].astype(str).str.strip()
    df["Invoice #"] = df["Invoice #"].astype(str).str.strip()

    result = df[
        (df["PO#"] == search_text) |
        (df["Invoice #"] == search_text)
    ]

    if result.empty:
        result = df[
            df["PO#"].str.contains(search_text, case=False, na=False) |
            df["Invoice #"].str.contains(search_text, case=False, na=False)
        ]

    if result.empty:
        st.warning("No matching Purchase Order or Invoice found.")
        return

    selected_row = result.iloc[0]

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("PO Number", selected_row["PO#"])
    col2.metric("PO Status", selected_row["PO Status"])
    col3.metric("Invoice Status", selected_row["Invoice Status"])
    col4.metric("Delivery Status", selected_row["Delivery Status"])

    st.divider()

    st.dataframe(
        result[required_columns],
        use_container_width=True,
        hide_index=True
    )
