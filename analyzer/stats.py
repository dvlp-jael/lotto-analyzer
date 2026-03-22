# analyzer/stats.py
# 로또 통계 분석 모듈

import pandas as pd
import numpy as np

LOCAL_PATH = "data/lotto_numbers.csv"

def load_data():
    """로컬 CSV 데이터 로드"""
    df = pd.read_csv(LOCAL_PATH, encoding="utf-8-sig")
    return df

def get_frequency(df):
    """번호별 출현 빈도 계산"""
    # 1~6번 컬럼만 추출
    number_cols = ["1번", "2번", "3번", "4번", "5번", "6번"]
    all_numbers = df[number_cols].values.flatten()

    # 1~45 전체 번호 빈도 계산
    freq = pd.Series(all_numbers).value_counts().sort_index()

    # 1~45 전체 채우기 (안나온 번호도 0으로)
    freq = freq.reindex(range(1, 46), fill_value=0)
    return freq

def get_odd_even_ratio(df):
    """홀짝 비율 분석"""
    number_cols = ["1번", "2번", "3번", "4번", "5번", "6번"]
    results = []

    for _, row in df[number_cols].iterrows():
        numbers = row.values
        odd = sum(1 for n in numbers if n % 2 != 0)
        even = 6 - odd
        results.append(f"{odd}홀{even}짝")

    ratio = pd.Series(results).value_counts()
    return ratio

def get_range_distribution(df):
    """구간별 분포 분석 (1-9, 10-19, 20-29, 30-39, 40-45)"""
    number_cols = ["1번", "2번", "3번", "4번", "5번", "6번"]
    all_numbers = df[number_cols].values.flatten()

    bins = [0, 9, 19, 29, 39, 45]
    labels = ["1~9", "10~19", "20~29", "30~39", "40~45"]
    dist = pd.cut(all_numbers, bins=bins, labels=labels)
    return dist.value_counts().sort_index()

def get_sum_stats(df):
    """회차별 당첨번호 합계 통계"""
    number_cols = ["1번", "2번", "3번", "4번", "5번", "6번"]
    df["합계"] = df[number_cols].sum(axis=1)

    stats = {
        "평균": round(df["합계"].mean(), 1),
        "최솟값": int(df["합계"].min()),
        "최댓값": int(df["합계"].max()),
        "표준편차": round(df["합계"].std(), 1)
    }
    return df["합계"], stats

def get_hot_cold(df, recent_n=50):
    """최근 N회차 핫/콜드 번호"""
    number_cols = ["1번", "2번", "3번", "4번", "5번", "6번"]
    recent = df.tail(recent_n)
    all_numbers = recent[number_cols].values.flatten()

    freq = pd.Series(all_numbers).value_counts().sort_index()
    freq = freq.reindex(range(1, 46), fill_value=0)

    hot = freq.nlargest(5)
    cold = freq.nsmallest(5)
    return hot, cold

if __name__ == "__main__":
    # 테스트 실행
    df = load_data()
    print(f"데이터 로드: {len(df)}회차\n")

    freq = get_frequency(df)
    print("=== 번호별 출현 빈도 (상위 10개) ===")
    print(freq.nlargest(10))

    ratio = get_odd_even_ratio(df)
    print("\n=== 홀짝 비율 ===")
    print(ratio.head(5))

    dist = get_range_distribution(df)
    print("\n=== 구간별 분포 ===")
    print(dist)

    _, stats = get_sum_stats(df)
    print("\n=== 합계 통계 ===")
    print(stats)

    hot, cold = get_hot_cold(df)
    print("\n=== 최근 50회차 핫 번호 ===")
    print(hot)
    print("\n=== 최근 50회차 콜드 번호 ===")
    print(cold)