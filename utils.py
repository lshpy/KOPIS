import pandas as pd
import numpy as np
import streamlit as st

@st.cache_data
def load_data():
    final = pd.read_excel("data/최종.xlsx")
    final["공연벡터"] = final["공연벡터"].apply(eval)
    final["공연장벡터"] = final["공연장벡터"].apply(eval)
    facility = pd.read_excel("data/공연시설DB.xlsx")
    concert = pd.read_excel("data/내한공연DB.xlsx")

    df = pd.merge(final, facility, on="공연시설ID", how="left")
    df = pd.merge(df, concert, on="공연ID(mt20Id)", how="left")
    return df
