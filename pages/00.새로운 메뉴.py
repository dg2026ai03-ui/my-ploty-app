import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

# 페이지 설정
st.set_page_config(page_title="멋진 데이터 시각화", layout="wide")

st.title("📊 Streamlit & Plotly 시각화 대시보드")
st.markdown("데이터를 분석하고 아름다운 차트로 시각화합니다.")

# --- 데이터 준비 (이 부분을 실제 데이터로 교체하면 됩니다) ---
@st.cache_data
def load_data():
    # 예시: 최근 30일간의 랜덤 데이터
    df = pd.DataFrame({
        "날짜": pd.date_range(start="2024-01-01", periods=30),
        "매출": np.random.randint(100, 500, size=30),
        "방문자": np.random.randint(1000, 5000, size=30),
        "카테고리": np.random.choice(['A', 'B', 'C'], size=30)
    })
    return df

df = load_data()

# --- 사이드바 필터 ---
st.sidebar.header("필터 설정")
selected_category = st.sidebar.multiselect("카테고리 선택", options=df["카테고리"].unique(), default=df["카테고리"].unique())
filtered_df = df[df["카테고리"].isin(selected_category)]

# --- 시각화 레이아웃 ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 시계열 매출 추이")
    fig1 = px.line(filtered_df, x="날짜", y="매출", color="카테고리", markers=True,
                  template="plotly_dark") # 어두운 테마로 멋지게 설정
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("📊 카테고리별 방문자 합계")
    fig2 = px.bar(filtered_df, x="카테고리", y="방문자", color="카테고리",
                 text_auto='.2s', template="plotly_white")
    st.plotly_chart(fig2, use_container_width=True)

# 데이터 테이블 보여주기
with st.expander("데이터 원본 보기"):
    st.write(filtered_df)
