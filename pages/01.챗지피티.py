import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="국가별 인구 분포 대시보드", layout="wide")

st.title("🌍 국가별 인구 분포 대시보드")

# 데이터 로드
df = px.data.gapminder()

# 사이드바 필터
st.sidebar.header("🔎 필터")

year = st.sidebar.slider(
    "연도 선택",
    int(df["year"].min()),
    int(df["year"].max()),
    2007
)

continent = st.sidebar.multiselect(
    "대륙 선택",
    options=df["continent"].unique(),
    default=df["continent"].unique()
)

# 데이터 필터링
filtered_df = df[(df["year"] == year) & (df["continent"].isin(continent))]

# -------------------------------
# 🌍 1. 세계 지도
# -------------------------------
st.subheader("🌍 세계 인구 지도")

fig_map = px.choropleth(
    filtered_df,
    locations="iso_alpha",
    color="pop",
    hover_name="country",
    color_continuous_scale="Viridis",
    title=f"{year}년 국가별 인구"
)

st.plotly_chart(fig_map, use_container_width=True)

# -------------------------------
# 📊 2. TOP 10 국가
# -------------------------------
st.subheader("📊 인구 TOP 10 국가")

top10 = filtered_df.sort_values(by="pop", ascending=False).head(10)

fig_bar = px.bar(
    top10,
    x="country",
    y="pop",
    color="continent",
    title="인구 상위 10개 국가"
)

st.plotly_chart(fig_bar, use_container_width=True)

# -------------------------------
# 📈 3. 연도별 변화
# -------------------------------
st.subheader("📈 인구 변화 추이")

country_list = st.multiselect(
    "국가 선택",
    options=df["country"].unique(),
    default=["Korea, Rep.", "United States", "China"]
)

trend_df = df[df["country"].isin(country_list)]

fig_line = px.line(
    trend_df,
    x="year",
    y="pop",
    color="country",
    markers=True,
    title="국가별 인구 변화"
)

st.plotly_chart(fig_line, use_container_width=True)

# -------------------------------
# 📌 KPI
# -------------------------------
st.subheader("📌 요약")

col1, col2, col3 = st.columns(3)

col1.metric("총 국가 수", len(filtered_df["country"].unique()))
col2.metric("총 인구", f"{filtered_df['pop'].sum():,}")
col3.metric("평균 인구", f"{int(filtered_df['pop'].mean()):,}")
