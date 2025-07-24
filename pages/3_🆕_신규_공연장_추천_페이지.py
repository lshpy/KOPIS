import streamlit as st
import pandas as pd
import numpy as np
import time
import re
from urllib.parse import quote
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from utils.recommend_utils import recommend_venues

# 🎭 장르 점수 맵
genre_score_map = {
    "연극": 0.5,
    "무용(서양/한국무용)": 0.6,
    "대중무용": 0.7,
    "서양음악(클래식)": 0.6,
    "한국음악(국악)": 0.5,
    "대중음악": 0.85,
    "복합": 0.4,
    "서커스/마술": 0.3,
    "뮤지컬": 0.7
}

# 🔍 뉴스 검색량 수집 함수
def get_news_count_by_scroll(query, delay=1.5):
    encoded_query = quote(query)
    url = f"https://search.naver.com/search.naver?where=news&query={encoded_query}"

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)

    driver.get(url)
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    titles = driver.find_elements(By.CSS_SELECTOR, "span.sds-comps-text-type-headline1")
    count = len([t for t in titles if t.text.strip()])
    driver.quit()
    return count

# 💸 티켓가 추출 함수
def extract_first_ticket_price(text):
    match = re.search(r'(\d[\d,]*)', str(text))
    return int(match.group(1).replace(",", "")) if match else None

# 📐 공연 벡터 생성 함수
def create_perf_vector(title, cast, genre, price):
    query = f"{title} {cast}" if cast else title
    count = get_news_count_by_scroll(query)
    st.info(f"🔍 '{query}' 검색 결과 뉴스 기사 수: {count}")

    genre_score = genre_score_map.get(genre, 0.5)
    price_value = extract_first_ticket_price(price)
    price_norm = price_value / 200000 if price_value else 0
    search_norm = count / 500 if count < 500 else 1.0  # 정규화 클립

    return [round(price_norm, 3), round(genre_score, 2), round(search_norm, 3)]

# 🚀 Streamlit 앱 실행 함수
def render():
    st.title("🆕 신규 내한 공연 정보 입력 → 공연장 추천")

    st.subheader("1️⃣ 공연 정보 입력")
    title = st.text_input("공연 제목")
    cast = st.text_input("출연진 (첫 명만 입력해도 됨)")
    genre = st.selectbox("장르 선택", list(genre_score_map.keys()))
    price = st.text_input("대표 티켓가격 (예: 99,000원 또는 숫자만 입력)")

    st.subheader("2️⃣ 유사도 가중치 설정")
    w1 = st.slider("티켓가 가중치", 0.0, 1.0, 0.5)
    w2 = st.slider("장르 가중치", 0.0, 1.0, 0.3)
    w3 = st.slider("검색량 가중치", 0.0, 1.0, 0.2)
    alpha = st.slider("🎯 종합유사도에서 벡터 유사도 비중 (α)", 0.0, 1.0, 0.7)

    if st.button("🚀 벡터 생성 및 추천 실행"):
        if not title or not genre or not price:
            st.error("공연 제목, 장르, 가격은 필수 입력입니다.")
            return

        perf_vector = create_perf_vector(title, cast, genre, price)
        st.success(f"🎯 생성된 공연 벡터: {perf_vector}")

        # 데이터 로드 및 전처리
        df = pd.read_excel("data/최종.xlsx")
        venue_df = pd.read_excel("data/공연시설DB.xlsx")
        df = df[df["공연장벡터"].notna()].copy()
        df["공연장벡터"] = df["공연장벡터"].apply(eval)

        # 객석 수 등 공연장 정보 병합
        df = df.merge(venue_df, on="공연시설ID", how="left")

        # 추천 수행
        results = recommend_venues(perf_vector, df, weights=[w1, w2, w3], alpha=alpha)

        # 결과 출력
        st.subheader("✅ 추천 공연장 리스트 (유사도 기반 상위)")
        st.dataframe(results[[
            "공연시설명", "공연시설ID", "유사도", "객석수유사도", "종합유사도", "객석 수",
            "레스토랑", "카페", "편의점",
            "장애시설-주차장", "장애시설-화장실", "장애시설-경사로", "장애시설-엘리베이터"
        ]].head(10))

# 🟢 이 모듈이 직접 실행될 때만 앱 실행
if __name__ == "__main__":
    render()
