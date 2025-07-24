import streamlit as st
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from utils import load_data

st.title("🔎 유사도 기반 공연장 추천")
df = load_data()

concert_id = st.text_input("추천 기준 공연ID 입력")

if concert_id:
    row = df[df["공연ID(mt20Id)"] == concert_id]
    if not row.empty:
        vec = np.array([eval(row.iloc[0]["공연벡터"])])
        mat = np.stack(df["공연벡터"].values)
        sims = cosine_similarity(vec, mat)[0]
        top_k = sims.argsort()[-5:][::-1]

        for i in top_k:
            r = df.iloc[i]
            st.markdown(f"🎵 **{r['공연명']}** → **{r['공연시설명(fcltynm)']}** (유사도: {sims[i]:.3f})")
