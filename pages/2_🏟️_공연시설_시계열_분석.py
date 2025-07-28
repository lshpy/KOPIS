import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from prophet import Prophet
from prophet.plot import plot_plotly
import plotly.graph_objs as go

st.set_page_config(layout="wide")
st.title("🏟️ 공연시설 시계열 분석 및 내한 시기 예측")

# 데이터 파일 경로
file_path = "data/KOPIS_공연시설_피벗_요약.xlsx"

# 시트 리스트 (공연건수, 상연횟수, 총티켓판매수)
sheet_options = {
    "공연건수": "공연건수",
    "상연횟수": "상연횟수",
    "총티켓판매수": "총티켓판매수"
}

selected_sheet = st.selectbox("📈 분석 항목 선택", list(sheet_options.values()))
df = pd.read_excel(file_path, sheet_name=selected_sheet)
df = df.dropna(how="all", subset=df.columns[1:]).fillna(0)

# 공연시설 선택
selected_venue = st.selectbox("🎪 분석할 공연시설", df["공연시설명"].unique())

# 시계열 데이터 변환
venue_data = df[df["공연시설명"] == selected_venue].set_index("공연시설명").T
venue_data.columns = [selected_venue]
venue_data.index.name = "월"
venue_data.reset_index(inplace=True)

# 📊 원시 시계열 그래프 출력
st.subheader(f"📉 {selected_venue}의 월별 {selected_sheet} 변화 추이")
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(venue_data["월"], venue_data[selected_venue], marker='o')
plt.xticks(rotation=45)
plt.xlabel("월")
plt.ylabel(selected_sheet)
plt.grid(True)
st.pyplot(fig)

# 📌 통계 요약
st.subheader("📌 통계 요약")
col1, col2, col3 = st.columns(3)
col1.metric("평균", f"{venue_data[selected_venue].mean():.1f}")
col2.metric("최대", f"{venue_data[selected_venue].max():.0f}")
col3.metric("최소", f"{venue_data[selected_venue].min():.0f}")

# 🏆 전체 랭킹
st.subheader("🏆 평균 기준 전체 공연시설 랭킹")
df["평균"] = df.iloc[:, 1:].mean(axis=1)
top_n = st.slider("Top-N 시설 수", 5, 30, 10)
top_ranked = df.sort_values(by="평균", ascending=False)[["공연시설명", "평균"]].head(top_n)
st.dataframe(top_ranked.reset_index(drop=True))

# 📈 Prophet 기반 향후 12개월 예측
st.subheader("🔮 향후 1년 예측 및 내한 시기 추천")

# Prophet 데이터 준비
df_prophet = venue_data[["월", selected_venue]].copy()
df_prophet.columns = ["ds", "y"]
try:
    df_prophet["ds"] = pd.to_datetime(df_prophet["ds"])
except Exception as e:
    st.error("❌ 날짜 형식이 올바르지 않습니다. '월'은 yyyy-mm 형식이어야 합니다.")
    st.stop()

# Prophet 예측
model = Prophet(yearly_seasonality=True, weekly_seasonality=False, daily_seasonality=False)
model.fit(df_prophet)
future = model.make_future_dataframe(periods=12, freq="M")
forecast = model.predict(future)

# 예측 그래프
st.markdown("#### ▶ 예측 시계열 그래프")
fig2 = plot_plotly(model, forecast)
st.plotly_chart(fig2, use_container_width=True)

# 추천 월 추출
future_forecast = forecast[forecast["ds"] > df_prophet["ds"].max()]
future_forecast["월"] = future_forecast["ds"].dt.strftime("%Y-%m")
top_months = future_forecast.sort_values("yhat", ascending=False).head(3)[["월", "yhat"]]

# 결과 출력
st.markdown("#### 🏅 예측 기준 내한 공연 적합 추천 시기 (Top 3)")
st.dataframe(top_months.rename(columns={"yhat": f"{selected_sheet} 예측값"}).reset_index(drop=True))
