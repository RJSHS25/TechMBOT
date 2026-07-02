import streamlit as st
import pandas as pd
import os


def render_po_search(title, csv_file, page_name):
    st.subheader(title)

    # Check if file exists
    if not os.path.exists(csv_file):
        st.error(f"{csv_file} not found.")
        return

    # Read CSV
    df = pd.read_csv(csv_file, sep=None, engine="python")
    df.columns = df.columns.str.strip()

    # Required columns
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

    # Validate columns
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        st.error(f"The following columns are missing from the CSV: {missing_columns}")
        return

    # Search box
    search_text = st.text_input(
        "🔍 Search by PO Number or Invoice Number"
    )

    if not search_text:
        st.info("Enter a PO Number or Invoice Number to begin your search.")
        return

    search_text = search_text.strip()

    # Convert searchable columns to string
    df["PO#"] = df["PO#"].astype(str).str.strip()
    df["Invoice #"] = df["Invoice #"].astype(str).str.strip()

    # Exact Match
    result = df[
        (df["PO#"] == search_text) |
        (df["Invoice #"] == search_text)
    ]

    # Partial Match (optional)
    if result.empty:
        result = df[
            df["PO#"].str.contains(search_text, case=False, na=False) |
            df["Invoice #"].str.contains(search_text, case=False, na=False)
        ]

    # Display Results
    if result.empty:
        st.warning(
            "No matching Purchase Order or Invoice was found. Please verify the number and try again."
        )
    else:
        st.success(f"{len(result)} record(s) found.")

        st.dataframe(
            result[required_columns],
            use_container_width=True,
            hide_index=True
        )
