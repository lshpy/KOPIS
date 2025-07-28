import streamlit as st

# ✅ 페이지 설정 (무조건 가장 먼저 위치해야 함)
st.set_page_config(
    page_title="KOPIS 내한공연 추천 시스템",
    layout="wide",
    page_icon="🎭"
)

# ✅ 한글 폰트 설정 (Nanum Gothic for Hugging Face Spaces)
import matplotlib.font_manager as fm
font_dirs = ['/usr/share/fonts/truetype/nanum/']
font_files = fm.findSystemFonts(fontpaths=font_dirs)
for font_file in font_files:
    fm.fontManager.addfont(font_file)
st.markdown("<style>html, body, [class*='css']  { font-family: 'NanumGothic', sans-serif; }</style>", unsafe_allow_html=True)

# ✅ 제목 및 소개
st.title("🎭 KOPIS 기반 내한 공연장 추천 및 분석 대시보드")
st.markdown("""
#### 👋 환영합니다!
이 앱은 **공연예술통합전산망(KOPIS)** 데이터를 기반으로,  
**내한 공연에 적합한 공연장을 분석하고 추천**하는 목적의 **빅데이터 기반 분석 시스템**입니다.

---

### 📌 주요 기능
1. **공연 데이터 분석**  
    - 공연장 유형 및 벡터 클러스터링  
    - 트렌드 및 수익성 분석

2. **공연장 추천 시스템**  
    - 기존 부적합 공연에 대한 재추천  
    - 신규 내한 공연에 대한 최적 공연장 추천

3. **지도 기반 시각화**  
    - 추천된 공연장 위치를 지도 위에서 확인 가능

---

### 🗂️ 좌측 메뉴에서 페이지를 선택해주세요!
- `📊 빅데이터 분석 페이지`: 클러스터링, PCA, 공연장 벡터 시각화
- `🏟️ 공연시설 시계열 분석`: 공연시설별 시간 흐름 및 수요 분석
- `🔁 기존 내한 재추천 페이지`: 기존 공연 중 부적합 공연의 대체 공연장 추천
- `🆕 신규 공연장 추천 페이지`: 신규 공연 벡터 입력 후 적합한 공연장 자동 추천
""")

# ✅ 하단 크레딧
st.markdown("---")
st.markdown("""
📌 **데이터 출처**: KOPIS 공연예술통합전산망  
👨‍💻 **개발자**: 고려대학교 이승현  
📅 **공모전 제출용 버전**
""")
