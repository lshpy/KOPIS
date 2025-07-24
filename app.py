import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# 데이터 불러오기
@st.cache_data
def load_data():
    final = pd.read_excel("data/최종.xlsx")
    facility = pd.read_excel("data/공연시설DB.xlsx")
    concert = pd.read_excel("data/내한공연DB.xlsx")

    final["공연벡터"] = final["공연벡터"].apply(eval)
    final["공연장벡터"] = final["공연장벡터"].apply(eval)

    merged = pd.merge(final, facility, on="공연시설ID", how="left")
    merged = pd.merge(merged, concert, on="공연ID(mt20Id)", how="left")
    return merged

df = load_data()
