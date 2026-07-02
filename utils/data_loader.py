import pandas as pd
import os
import streamlit as st

@st.cache_data
def load_data(file_name, empty_message):
    if os.path.exists(file_name):
        df = pd.read_csv(file_name)
    else:
        df = pd.DataFrame(columns=["Topic", "Description"])
        df.loc[0] = ["Sample", empty_message]

    if "Question" in df.columns:
        df.rename(
            columns={
                "Question":"Topic",
                "Answer":"Description"
            },
            inplace=True
        )

    return df
