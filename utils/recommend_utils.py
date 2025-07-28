import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# 객석 수 유사도 함수
def compute_capacity_similarity(cap1, cap2):
    try:
        if cap1 <= 0 or cap2 <= 0:
            return 0.0
        return min(cap1, cap2) / max(cap1, cap2)
    except:
        return 0.0

# 공연장 추천 함수
def recommend_venues(perf_vector, df, weights=[0.5, 0.3, 0.2], alpha=0.7):
    """
    perf_vector: [티켓가, 장르점수, 검색량] 형태의 신규 공연 벡터
    df: 공연장 데이터프레임 (공연장벡터 + 객석 수 포함)
    weights: 각 성분별 가중치
    alpha: 종합 유사도 계산 시 벡터 유사도 비중
    """
    perf_vec = np.array(perf_vector) * np.array(weights)

    # 공연장 벡터 유사도 계산
    df["공연장벡터"] = df["공연장벡터"].apply(lambda x: np.array(x) * np.array(weights))
    df["유사도"] = df["공연장벡터"].apply(lambda v: cosine_similarity([perf_vec], [v])[0][0])

    # 객석 수 유사도 계산
    target_capacity = perf_vector[0] * 200000  # 역정규화된 객석 수 기준 (티켓가 기준과 맞춰짐)
    df["객석수유사도"] = df["객석 수"].apply(lambda c: compute_capacity_similarity(target_capacity, c))

    # 종합 유사도
    df["종합유사도"] = alpha * df["유사도"] + (1 - alpha) * df["객석수유사도"]

    # 정렬 후 반환
    result = df.sort_values("종합유사도", ascending=False).reset_index(drop=True)
    return result
