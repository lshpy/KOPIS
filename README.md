---
title: KOPIS 공연장 추천 시스템
emoji: 🎭
colorFrom: purple
colorTo: indigo
sdk: streamlit
sdk_version: "1.34.0"
app_file: app.py
pinned: false
---

# 🎭 공연장 추천 시스템 (KOPIS 기반 Big Data Recommender)

본 프로젝트는 공연예술통합전산망(KOPIS) 데이터를 활용하여  
**공연 벡터 → 공연장 벡터** 기반의 추천 시스템을 구현한 Streamlit 웹 애플리케이션입니다.

## 📦 기능 요약

| 기능 | 설명 |
|------|------|
| 📍 공연 검색 | 공연ID 또는 공연명을 입력해 상세 정보 조회 |
| 🔎 유사도 기반 추천 | 기존 공연과 유사한 벡터를 가진 공연장 추천 |
| 🎨 시각화 | 공연벡터 클러스터링 (PCA 기반 시각화) |
| 🧠 신규 벡터 추천 | 직접 입력한 벡터로 Top-N 공연장 추천 |

---

## 🗂️ 폴더 구조

```bash
kopis-recommender/
├── app.py                  # Streamlit 메인 엔트리 포인트
├── utils.py                # 공통 데이터 로딩 및 전처리 함수
├── pages/                  # 개별 기능 페이지
│   ├── 1_📍_공연검색.py
│   ├── 2_🔎_유사도기반추천.py
│   ├── 3_🎨_시각화.py
│   └── 4_🧠_신규벡터추천.py
├── data/                   # 공연 관련 데이터 엑셀 파일
│   ├── 최종.xlsx
│   ├── 공연시설DB.xlsx
│   └── 내한공연DB.xlsx
├── requirements.txt        # 라이브러리 의존성
└── README.md
