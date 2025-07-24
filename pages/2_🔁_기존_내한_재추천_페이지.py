import streamlit as st
import pandas as pd
import numpy as np
from utils.recommend_utils import compute_capacity_similarity
from sklearn.metrics.pairwise import cosine_similarity

st.title("🔁 기존 내한 공연 재추천")

# 데이터 불러오기
df = pd.read_excel("data/최종_적합성분석결과.xlsx")
df = df[df["공연장벡터"].notna()]
df["공연벡터"] = df["공연벡터"].apply(eval)
df["공연장벡터"] = df["공연장벡터"].apply(eval)

venue_df = pd.read_excel("data/공연시설DB.xlsx")
df = df.merge(venue_df[["공연시설ID", "객석 수", "시설특성", "레스토랑", "카페", "편의점", 
                        "장애시설-경사로", "장애시설-엘리베이터", "주소"]],
              on="공연시설ID", how="left")

# 추천 함수 (간단히 포함)
def recommend_alternative_venues(perf_row, df, weights=[0.5,0.3,0.2], alpha=0.7, top_k=5):
    perf_vec = np.array(perf_row["공연벡터"]) * np.array(weights)
    perf_capacity = perf_row["객석 수"]

    candidates = df[(df["적합성"] == "적합") & (df["공연시설ID"] != perf_row["공연시설ID"])]
    candidates["공연장벡터"] = candidates["공연장벡터"].apply(lambda x: np.array(x) * np.array(weights))
    candidates["유사도"] = candidates["공연장벡터"].apply(lambda v: cosine_similarity([perf_vec], [v])[0][0])
    candidates["객석수유사도"] = candidates["객석 수"].apply(lambda c: compute_capacity_similarity(perf_capacity, c))
    candidates["종합유사도"] = alpha * candidates["유사도"] + (1 - alpha) * candidates["객석수유사도"]

    return candidates.sort_values("종합유사도", ascending=False).head(top_k)

# UI
target_title = st.selectbox("🎫 공연명을 선택하세요", df["공연명"].unique())
if target_title:
    perf_row = df[df["공연명"] == target_title].iloc[0]
    if perf_row["적합성"] == "적합":
        st.info("✅ 이 공연은 이미 적합한 공연장에서 진행되었습니다.")
    else:
        st.warning("⚠️ 부적합 공연입니다. 대체 공연장을 추천합니다.")
        results = recommend_alternative_venues(perf_row, df)
        st.dataframe(results[[
            "공연시설명(fcltynm)", "공연시설ID", "유사도", "객석수유사도", "종합유사도",
            "객석 수", "레스토랑", "카페", "편의점", "장애시설-경사로", "장애시설-엘리베이터", "주소"
        ]])
