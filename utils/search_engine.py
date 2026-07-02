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

    search_text = st.text_input("Search Material Description")

    if search_text:
        descriptions = df["Material Description"].astype(str).tolist()

        exact_match = df[
            df["Material Description"].astype(str).str.lower()
            == search_text.lower()
        ]

        if not exact_match.empty:
            st.success("Exact match found")
            st.dataframe(
                exact_match[
                    [
                        "Material Code",
                        "Material Description",
                        "GL Account",
                        "Valuation Class"
                    ]
                ],
                use_container_width=True
            )

        else:
            nearest_matches = get_close_matches(
                search_text,
                descriptions,
                n=5,
                cutoff=0.3
            )

            if nearest_matches:
                st.warning("Exact match not found. Please select nearest match.")

                selected_material = st.selectbox(
                    "Select Material",
                    nearest_matches
                )

                selected_row = df[
                    df["Material Description"] == selected_material
                ]

                st.dataframe(
                    selected_row[
                        [
                            "Material Code",
                            "Material Description",
                            "GL Account",
                            "Valuation Class"
                        ]
                    ],
                    use_container_width=True
                )
            else:
                st.error("No matching material found.")
    else:
        st.info("Enter material name to search.")
