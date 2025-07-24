import streamlit as st
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from utils import load_data

st.title("🧠 신규 공연벡터 → 공연장 추천")

df = load_data()

vec_input = st.text_input("공연벡터 입력 (예: [0.2, 0.8, 0.0])")

if vec_input:
    try:
        vec = np.array([eval(vec_input)])
        mat = np.stack(df["공연벡터"].values)
        sims = cosine_similarity(vec, mat)[0]
        top_k = sims.argsort()[-5:][::-1]

        for i in top_k:
            r = df.iloc[i]
            st.markdown(f"🎵 **{r['공연명']}** → **{r['공연시설명(fcltynm)']}** (유사도: {sims[i]:.3f})")
    except:
        st.error("올바른 벡터 형식을 입력해주세요.")
