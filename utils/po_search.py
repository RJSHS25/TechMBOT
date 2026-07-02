def render_po_search(title, csv_file, page_name):
    st.subheader(title)

    if not os.path.exists(csv_file):
        st.error(f"{csv_file} not found")
        return

    df = pd.read_csv(csv_file, sep=None, engine="python")
    df.columns = df.columns.str.strip()

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

    missing = [c for c in required_columns if c not in df.columns]

    if missing:
        st.error(f"Missing columns: {missing}")
        return

    search_text = st.text_input(
        "Search by PO Number or Invoice Number"
    )

    if not search_text:
        st.info("Enter a PO Number or Invoice Number.")
        return

    search_text = search_text.strip()

    result = df[
        (df["PO#"].astype(str) == search_text) |
        (df["Invoice #"].astype(str) == search_text)
    ]

    if result.empty:
        st.warning(
            "No records found. Please verify the PO Number or Invoice Number."
        )
    else:
        st.dataframe(
            result[required_columns],
            use_container_width=True
        )
