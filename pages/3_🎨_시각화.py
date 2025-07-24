import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from utils import load_data

st.title("🎨 공연벡터 시각화 (PCA)")

df = load_data()
X = np.stack(df["공연벡터"].values)
pca = PCA(n_components=2)
X_2d = pca.fit_transform(X)

plt.figure(figsize=(8,6))
sns.scatterplot(x=X_2d[:,0], y=X_2d[:,1])
plt.title("PCA 시각화")
st.pyplot(plt)
