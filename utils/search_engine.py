import streamlit as st
import pandas as pd
import os
from difflib import get_close_matches

def render_search_page(title, csv_file, page_name):
    st.subheader(title)

    if not os.path.exists(csv_file):
        st.error(f"{csv_file} not found")
        return

    df = pd.read_csv(csv_file, sep=None, engine="python")
    df.columns = df.columns.str.strip()

    required_columns = [
        "Material Code",
        "Material Description",
        "GL Account",
        "Valuation Class"
    ]

    search_text = st.text_input(
        "Search by Material Description, Material Code, GL Account, or Valuation Class"
    )

    if not search_text:
        st.info("Enter material name, material code, GL account, or valuation class to search.")
        return

    search_text = search_text.strip()

    # Convert searchable columns to text
    for col in required_columns:
        df[col] = df[col].astype(str).str.strip()

    # 1. Exact match in any column
    exact_match = df[
        (df["Material Description"].str.lower() == search_text.lower()) |
        (df["Material Code"] == search_text) |
        (df["GL Account"] == search_text) |
        (df["Valuation Class"] == search_text)
    ]

    if not exact_match.empty:
        st.dataframe(exact_match[required_columns], use_container_width=True)
        return

    # 2. Partial match in any column
    partial_match = df[
        df["Material Description"].str.lower().str.contains(search_text.lower(), na=False) |
        df["Material Code"].str.contains(search_text, na=False) |
        df["GL Account"].str.contains(search_text, na=False) |
        df["Valuation Class"].str.contains(search_text, na=False)
    ]

    if not partial_match.empty:
        st.info("We found matching materials. Please select the correct one.")

        selected_material = st.selectbox(
            "Is this what you are looking for?",
            partial_match["Material Description"].tolist()
        )

        selected_row = partial_match[
            partial_match["Material Description"] == selected_material
        ]

        st.dataframe(selected_row[required_columns], use_container_width=True)
        return

    # 3. Nearest match only for material description
    descriptions = df["Material Description"].tolist()

    nearest_matches = get_close_matches(
        search_text,
        descriptions,
        n=5,
        cutoff=0.3
    )

    if nearest_matches:
        st.info("We found similar materials. Please confirm the correct one.")

        selected_material = st.selectbox(
            "Is this what you are looking for?",
            nearest_matches
        )

        selected_row = df[
            df["Material Description"] == selected_material
        ]

        st.dataframe(selected_row[required_columns], use_container_width=True)

    else:
        st.warning(
            "No close match found. Try searching with a shorter or different keyword, "
            "for example: Laptop, Pen, Printer, Cable, material code, GL account, or valuation class."
        )
