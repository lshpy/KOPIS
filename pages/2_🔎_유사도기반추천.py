import streamlit as st
import numpy as np
import pandas as pd
from utils import load_data
from sklearn.metrics.pairwise import cosine_similarity

st.title("🔎 유사도 기반 공연장 추천")

df = load_data()

concert_id = st.text_input("🎤 내한 가수의 공연ID를 입력하세요:")
if concert_id:
    row = df[df["공연ID(mt20Id)"] == concert_id]
    if not row.empty:
        vec = row.iloc[0]["공연벡터"]
        if isinstance(vec, str):
            vec = np.array([eval(vec)])
        else:
            vec = np.array([vec])

        mat = np.stack(df["공연장벡터"].values)
        sims = cosine_similarity(vec, mat)[0]
        df["유사도"] = sims
        top = df.sort_values("유사도", ascending=False).head(5)

        st.subheader("🎯 추천 공연장 TOP 5")
        st.dataframe(top[["공연시설명", "주소", "유사도"]])
    else:
        st.warning("해당 ID의 공연이 존재하지 않습니다.")
