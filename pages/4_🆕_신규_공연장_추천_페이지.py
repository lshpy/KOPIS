import streamlit as st
import pandas as pd
import numpy as np
import re
import folium
from streamlit_folium import st_folium
from utils.recommend_utils import recommend_venues

# ✅ 페이지 설정
st.set_page_config(layout="wide")
st.title("🆕 신규 내한 공연 정보 입력 → 공연장 추천")

# 🎭 장르 점수 맵
genre_score_map = {
    "연극": 0.5, "무용(서양/한국무용)": 0.6, "대중무용": 0.7,
    "서양음악(클래식)": 0.6, "한국음악(국악)": 0.5, "대중음악": 0.85,
    "복합": 0.4, "서커스/마술": 0.3, "뮤지컬": 0.7
}

# 💸 티켓가 정수 추출
def extract_first_ticket_price(text):
    match = re.search(r'(\d[\d,]*)', str(text))
    return int(match.group(1).replace(",", "")) if match else None

# 📐 공연 벡터 생성
def create_perf_vector(title, genre, price, search_score):
    genre_score = genre_score_map.get(genre, 0.5)
    price_value = extract_first_ticket_price(price)
    price_norm = price_value / 200000 if price_value else 0
    return [round(price_norm, 3), round(genre_score, 2), round(search_score, 3)]

# ✅ 1. 공연 정보 입력
st.subheader("1️⃣ 공연 정보 입력")
title = st.text_input("공연 제목")
genre = st.selectbox("장르 선택", list(genre_score_map.keys()))
price = st.text_input("대표 티켓가격 (예: 99,000원 또는 숫자만 입력)")

# ✅ 2. 검색량 수준 선택
st.subheader("2️⃣ 검색량 수준 선택")
search_category = st.selectbox("🔍 뉴스 검색량 등급", ["낮음", "보통", "높음", "매우 높음"])
search_score_map = {"낮음": 0.2, "보통": 0.5, "높음": 0.8, "매우 높음": 1.0}
search_score = search_score_map[search_category]

# ✅ 3. 유사도 가중치 설정
st.subheader("3️⃣ 유사도 가중치 설정")
w1 = st.slider("티켓가 가중치", 0.0, 1.0, 0.5)
w2 = st.slider("장르 가중치", 0.0, 1.0, 0.3)
w3 = st.slider("검색량 가중치", 0.0, 1.0, 0.2)
alpha = st.slider("🎯 종합유사도에서 벡터 유사도 비중 (α)", 0.0, 1.0, 0.7)

# 🚀 실행 버튼
if st.button("🚀 벡터 생성 및 추천 실행"):
    if not title or not genre or not price:
        st.error("공연 제목, 장르, 가격은 필수 입력입니다.")
        st.stop()

    # 공연 벡터 생성 및 저장
    perf_vector = create_perf_vector(title, genre, price, search_score)
    st.session_state["perf_vector"] = perf_vector
    st.session_state["title"] = title
    st.success(f"🎯 생성된 공연 벡터: {perf_vector}")

    try:
        df = pd.read_excel("data/최종.xlsx")
        venue_df = pd.read_excel("data/공연시설DB.xlsx")
    except Exception as e:
        st.error(f"❌ 데이터 파일 로드 오류: {e}")
        st.stop()

    from ast import literal_eval
    df = df[df["공연장벡터"].notna()].copy()
    df["공연장벡터"] = df["공연장벡터"].apply(literal_eval)

    df = df.merge(venue_df[[
        "공연시설ID", "공연시설명", "객석 수", "레스토랑", "카페", "편의점",
        "장애시설-주차장", "장애시설-화장실", "장애시설-경사로", "장애시설-엘리베이터",
        "주소", "위도", "경도"
    ]], on="공연시설ID", how="left")
    df = df.drop_duplicates(subset="공연시설ID")

    results = recommend_venues(perf_vector, df, weights=[w1, w2, w3], alpha=alpha)
    st.session_state["results"] = results.sort_values("종합유사도", ascending=False).head(10)

# 결과 출력 (세션 상태가 존재할 경우)
if "results" in st.session_state and "title" in st.session_state:
    top_results = st.session_state["results"]
    title = st.session_state["title"]

    st.subheader(f"✅ '{title}'에 대한 추천 공연장 리스트 (상위 10곳)")
    st.dataframe(top_results[[
        "공연시설명", "공연시설ID", "유사도", "객석수유사도", "종합유사도", "객석 수",
        "레스토랑", "카페", "편의점",
        "장애시설-주차장", "장애시설-화장실", "장애시설-경사로", "장애시설-엘리베이터", "주소"
    ]])

    st.subheader("📍 추천 공연장 위치 지도")
    map_obj = folium.Map(location=[37.5665, 126.9780], zoom_start=11)
    for _, row in top_results.iterrows():
        if pd.notna(row["위도"]) and pd.notna(row["경도"]):
            folium.Marker(
                location=[row["위도"], row["경도"]],
                popup=f"{row['공연시설명']}<br>{row['주소']}",
                tooltip=row["공연시설명"]
            ).add_to(map_obj)
    st_folium(map_obj, width=900, height=500)

