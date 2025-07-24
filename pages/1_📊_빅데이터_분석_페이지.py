import streamlit as st
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

st.title("📊 내한 공연 적합성 분석 및 클러스터링")

# 데이터 불러오기
df = pd.read_excel("data/최종.xlsx")
df = df.dropna(subset=["공연벡터"])
df["공연벡터"] = df["공연벡터"].apply(eval)

# 적합성 통계 시각화
st.subheader("✅ 적합성 분석 결과")
st.bar_chart(df["적합성"].value_counts())

st.write("📌 적합 공연 수:", (df["적합성"] == "적합").sum())
st.write("📌 부적합 공연 수:", (df["적합성"] == "부적합").sum())

# 클러스터링
st.subheader("🎨 KMeans 클러스터링 분석")

X = np.vstack(df["공연벡터"])
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)

k = st.slider("클러스터 수 선택", 2, 10, 4)
kmeans = KMeans(n_clusters=k, random_state=42)
clusters = kmeans.fit_predict(X)

df["클러스터"] = clusters

fig, ax = plt.subplots(figsize=(8,6))
sns.scatterplot(x=X_pca[:, 0], y=X_pca[:, 1], hue=clusters, palette="tab10", s=80, ax=ax)
plt.title("PCA 기반 공연 클러스터링")
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.legend(title="클러스터", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
st.pyplot(fig)

if st.checkbox("📋 클러스터별 공연 보기"):
    cluster_id = st.selectbox("🔍 클러스터 선택", sorted(df["클러스터"].unique()))
    st.dataframe(df[df["클러스터"] == cluster_id][["공연명", "공연시설명(fcltynm)", "적합성", "클러스터"]])
