# app.py
# 로또 분석기 Streamlit 메인 앱

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
sys.path.append(".")

from analyzer.stats import (
    load_data, get_frequency, get_odd_even_ratio,
    get_range_distribution, get_sum_stats, get_hot_cold
)
from simulator.monte_carlo import run_all_strategies

# 페이지 설정
st.set_page_config(
    page_title="로또 분석기",
    page_icon="🎱",
    layout="wide"
)

st.title("🎱 로또 번호 분석기")
st.caption("통계 분석 + 몬테카를로 시뮬레이터 | 모든 전략은 결국 손해입니다.")

# 데이터 로드
@st.cache_data
def get_df():
    return load_data()

df = get_df()
st.sidebar.success(f"✅ 데이터 로드 완료: {len(df)}회차")

# 탭 구성
tab1, tab2 = st.tabs(["📊 통계 분석", "🎲 시뮬레이터"])

# ===========================
# 탭 1: 통계 분석
# ===========================
with tab1:
    st.header("📊 통계 분석")

    # 번호별 출현 빈도
    st.subheader("번호별 출현 빈도")
    freq = get_frequency(df)
    fig_freq = px.bar(
        x=freq.index,
        y=freq.values,
        labels={"x": "번호", "y": "출현 횟수"},
        color=freq.values,
        color_continuous_scale="Blues"
    )
    fig_freq.update_layout(showlegend=False, coloraxis_showscale=False)
    st.plotly_chart(fig_freq, use_container_width=True)

    col1, col2 = st.columns(2)

    # 홀짝 비율
    with col1:
        st.subheader("홀짝 비율")
        ratio = get_odd_even_ratio(df)
        fig_ratio = px.pie(
            values=ratio.values,
            names=ratio.index,
            hole=0.4
        )
        st.plotly_chart(fig_ratio, use_container_width=True)

    # 구간별 분포
    with col2:
        st.subheader("구간별 분포")
        dist = get_range_distribution(df)
        fig_dist = px.bar(
            x=dist.index,
            y=dist.values,
            labels={"x": "구간", "y": "출현 횟수"},
            color=dist.values,
            color_continuous_scale="Greens"
        )
        fig_dist.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig_dist, use_container_width=True)

    # 합계 통계
    st.subheader("회차별 당첨번호 합계 분포")
    sums, stats = get_sum_stats(df)
    col3, col4, col5, col6 = st.columns(4)
    col3.metric("평균", f"{stats['평균']}")
    col4.metric("최솟값", f"{stats['최솟값']}")
    col5.metric("최댓값", f"{stats['최댓값']}")
    col6.metric("표준편차", f"{stats['표준편차']}")

    fig_hist = px.histogram(
        sums,
        nbins=40,
        labels={"value": "합계", "count": "빈도"},
        color_discrete_sequence=["#636EFA"]
    )
    st.plotly_chart(fig_hist, use_container_width=True)

    # 핫/콜드 번호
    st.subheader("최근 50회차 핫/콜드 번호")
    hot, cold = get_hot_cold(df)
    col7, col8 = st.columns(2)

    with col7:
        st.markdown("🔥 **핫 번호 (자주 나온 번호)**")
        hot_df = pd.DataFrame({"번호": hot.index, "출현횟수": hot.values})
        st.dataframe(hot_df, hide_index=True, use_container_width=True)

    with col8:
        st.markdown("❄️ **콜드 번호 (안 나온 번호)**")
        cold_df = pd.DataFrame({"번호": cold.index, "출현횟수": cold.values})
        st.dataframe(cold_df, hide_index=True, use_container_width=True)

# ===========================
# 탭 2: 시뮬레이터
# ===========================
with tab2:
    st.header("🎲 몬테카를로 시뮬레이터")
    st.info("어떤 전략을 써도 로또는 기댓값이 마이너스입니다. 데이터로 확인해보세요.")

    # 시뮬레이션 설정
    weeks = st.slider("시뮬레이션 회차 수 (주)", min_value=10, max_value=1000, value=100, step=10)

    if st.button("▶ 시뮬레이션 실행", type="primary"):
        with st.spinner("시뮬레이션 중..."):
            results = run_all_strategies(weeks=weeks, df_history=df)

        # 결과 요약 테이블
        st.subheader("전략별 결과 요약")
        summary = []
        for r in results:
            summary.append({
                "전략": r["전략"],
                "총 투자": f"{r['총투자']:,}원",
                "총 당첨": f"{r['총당첨']:,}원",
                "순 손익": f"{r['순손익']:,}원",
                "수익률": f"{r['수익률']}%"
            })
        st.dataframe(pd.DataFrame(summary), hide_index=True, use_container_width=True)

        # 누적 손익 차트
        st.subheader("전략별 누적 손익 추이")
        fig_sim = go.Figure()
        colors = {"random": "#636EFA", "hot": "#EF553B", "cold": "#00CC96", "fixed": "#FFA15A"}

        for r in results:
            fig_sim.add_trace(go.Scatter(
                y=r["누적손익"],
                name=r["전략"],
                mode="lines",
                line=dict(color=colors[r["전략"]], width=2)
            ))

        fig_sim.update_layout(
            xaxis_title="회차",
            yaxis_title="누적 손익 (원)",
            hovermode="x unified"
        )
        fig_sim.add_hline(y=0, line_dash="dash", line_color="gray", annotation_text="손익분기점")
        st.plotly_chart(fig_sim, use_container_width=True)

        # 당첨 현황
        st.subheader("당첨 현황")
        prize_data = []
        for r in results:
            for grade, count in r["당첨현황"].items():
                prize_data.append({"전략": r["전략"], "등수": grade, "횟수": count})

        prize_df = pd.DataFrame(prize_data)
        fig_prize = px.bar(
            prize_df[prize_df["등수"] != "꽝"],
            x="등수", y="횟수", color="전략",
            barmode="group"
        )
        st.plotly_chart(fig_prize, use_container_width=True)