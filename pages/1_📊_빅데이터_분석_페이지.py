import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm

from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity

# ✅ 한글 폰트 설정 (Hugging Face Spaces용 Nanum Gothic)
font_dirs = ['/usr/share/fonts/truetype/nanum/']
font_files = fm.findSystemFonts(fontpaths=font_dirs)
for font_file in font_files:
    fm.fontManager.addfont(font_file)
plt.rc('font', family='NanumGothic')
plt.rcParams['axes.unicode_minus'] = False

# ✅ Streamlit 설정
st.set_page_config(layout="wide")
st.title("🎭 내한 공연 적합성 분석 및 클러스터링")

# ✅ 데이터 로드
@st.cache_data
def load_data():
    df = pd.read_excel("data/최종.xlsx")
    df = df.dropna(subset=["공연벡터", "공연장벡터"])
    df["공연벡터"] = df["공연벡터"].apply(eval)
    df["공연장벡터"] = df["공연장벡터"].apply(eval)
    return df

df = load_data()

# ✅ 유사도 계산
def compute_similarity(row, weights=[0.5, 0.3, 0.2]):
    perf_vec = np.array(row["공연벡터"]) * np.array(weights)
    venue_vec = np.array(row["공연장벡터"]) * np.array(weights)
    sim = cosine_similarity([perf_vec], [venue_vec])[0][0]
    return pd.Series([sim, "적합" if sim >= 0.8 else "부적합"])

df[["유사도", "적합성"]] = df.apply(compute_similarity, axis=1)
df[["대표티켓가", "장르점수", "검색량"]] = df["공연벡터"].apply(lambda x: pd.Series(x[:3]))

# ✅ KMeans 클러스터링
X = np.vstack(df["공연벡터"])
kmeans = KMeans(n_clusters=4, random_state=42)
df["클러스터"] = kmeans.fit_predict(X)

cluster_name_map = {
    0: "주류 인기 콘서트형",
    1: "글로벌 공연형",
    2: "프리미엄 클래식 공연형",
    3: "소극장 실험 공연형"
}
df["클러스터명"] = df["클러스터"].map(cluster_name_map)

# ✅ 설명
with st.expander("📌 분석 기준 설명"):
    st.markdown("""
    - 공연벡터와 공연장벡터의 가중 코사인 유사도로 적합성 판단  
    - 요소 가중치: `티켓가(0.5)`, `장르점수(0.3)`, `검색량(0.2)`  
    - 유사도 0.8 이상이면 **적합**, 아니면 **부적합**  
    - 공연벡터에 대해 KMeans 클러스터링 수행
    """)

# ✅ 적합성 분포 시각화
st.subheader("✅ 적합성 분포")
fig1, ax1 = plt.subplots()
sns.countplot(data=df, x="적합성", palette="Set2", ax=ax1)
st.pyplot(fig1)

col1, col2 = st.columns(2)
col1.metric("적합 공연 수", int((df["적합성"] == "적합").sum()))
col2.metric("부적합 공연 수", int((df["적합성"] == "부적합").sum()))

# ✅ PCA 시각화
st.subheader("🎯 PCA 기반 클러스터 시각화")
X_pca = PCA(n_components=2).fit_transform(X)
fig2, ax2 = plt.subplots(figsize=(10, 6))
colors = sns.color_palette("tab10", len(cluster_name_map))

for i, (cid, name) in enumerate(cluster_name_map.items()):
    mask = df["클러스터"] == cid
    ax2.scatter(X_pca[mask, 0], X_pca[mask, 1], s=40,
                color=colors[i], label=name, alpha=0.7, edgecolor="black")
ax2.legend(title="공연 유형", bbox_to_anchor=(1.01, 1))
ax2.set_title("PCA 기반 공연 유형 분포")
st.pyplot(fig2)

# ✅ 클러스터별 평균 티켓가
st.subheader("🎟️ 클러스터별 평균 티켓가")
avg_price = df.groupby("클러스터명")["대표티켓가"].mean().sort_values()
fig3, ax3 = plt.subplots()
sns.barplot(x=avg_price.values, y=avg_price.index, palette="Spectral", ax=ax3)
ax3.set_xlabel("평균 티켓가 (원)")
ax3.set_title("클러스터별 평균 티켓 가격")
st.pyplot(fig3)

# ✅ 클러스터별 적합성 비율
st.subheader("📊 클러스터별 적합성 비율")
ratio = df.groupby("클러스터명")["적합성"].value_counts(normalize=True).unstack().fillna(0)
fig4, ax4 = plt.subplots(figsize=(8, 5))
ratio.plot(kind="barh", stacked=True, color=["#6BAED6", "#FD8D3C"], ax=ax4)
ax4.set_title("클러스터별 적합/부적합 비율")
ax4.set_xlabel("비율")
ax4.legend(title="적합성", loc="center left", bbox_to_anchor=(1, 0.5))
st.pyplot(fig4)

# ✅ 클러스터 해석 및 공연 목록
st.subheader("📌 클러스터별 해석 및 공연 목록")
for cid, name in cluster_name_map.items():
    st.markdown(f"### 🔹 {name}")
    sub_df = df[df["클러스터"] == cid][["공연명", "대표티켓가", "적합성", "검색량", "장르점수"]]
    st.dataframe(sub_df.reset_index(drop=True), use_container_width=True)
