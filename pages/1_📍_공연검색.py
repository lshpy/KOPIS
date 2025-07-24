import streamlit as st
from utils import load_data

st.title("📍 공연 검색")
df = load_data()

query = st.text_input("공연ID 또는 공연명 입력")

if query:
    row = df[(df["공연ID(mt20Id)"] == query) | (df["공연명"].str.contains(query))]
    if not row.empty:
        r = row.iloc[0]
        st.subheader(f"🎵 {r['공연명']}")
        st.markdown(f"""
        **장르**: {r['장르']}  
        **출연진**: {r['출연진']}  
        **공연장**: {r['공연시설명(fcltynm)']}  
        **주소**: {r['주소']}  
        **객석 수**: {r['객석 수']}  
        **티켓**: {r['티켓가격']}
        """)
    else:
        st.warning("공연을 찾을 수 없습니다.")
