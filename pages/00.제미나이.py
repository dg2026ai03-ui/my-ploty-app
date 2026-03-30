import streamlit as st
import plotly.express as px
import pandas as pd

# 페이지 설정
st.set_page_config(page_title="세계 인구 분포 대시보드", layout="wide")

# 데이터 로드 (Plotly 내장 세계 통계 데이터)
@st.cache_data
def load_data():
    df = px.data.gapminder()
    # 가장 최근 데이터 연도 확인
    latest_year = df['year'].max()
    return df, latest_year

df, max_year = load_data()

# --- 사이드바 설정 ---
st.sidebar.header("🌍 설정")
year = st.sidebar.slider("연도 선택", 
                         min_value=int(df['year'].min()), 
                         max_value=int(max_year), 
                         value=int(max_year), 
                         step=5)

continents = st.sidebar.multiselect("대륙 선택", 
                                    options=df['continent'].unique(), 
                                    default=df['continent'].unique())

# 데이터 필터링
filtered_df = df[(df['year'] == year) & (df['continent'].isin(continents))]

# --- 메인 화면 ---
st.title(f"📊 {year}년 국가별 인구 분포")
st.markdown(f"현재 선택된 연도와 대륙에 따른 전 세계 인구 현황입니다.")

# 레이아웃 나누기
col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("🗺️ 세계 인구 지도")
    # 지도 시각화
    fig_map = px.choropleth(filtered_df, 
                            locations="iso_alpha",
                            color="pop", 
                            hover_name="country",
                            color_continuous_scale=px.colors.sequential.Plasma,
                            title=f"{year}년 글로벌 인구 밀도",
                            labels={'pop':'인구 수'})
    
    fig_map.update_layout(margin={"r":0,"t":40,"l":0,"b":0}, height=500)
    st.plotly_chart(fig_map, use_container_width=True)

with col2:
    st.subheader("🔝 인구 상위 국가 (TOP 10)")
    # 상위 10개국 추출
    top_10 = filtered_df.nlargest(10, 'pop')
    
    fig_bar = px.bar(top_10, 
                     x='pop', 
                     y='country', 
                     orientation='h',
                     color='pop',
                     color_continuous_scale='Viridis',
                     text_auto='.2s',
                     title=f"{year}년 인구 상위 10개국")
    
    fig_bar.update_layout(yaxis={'categoryorder':'total ascending'}, height=500)
    st.plotly_chart(fig_bar, use_container_width=True)
