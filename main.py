import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🌍 세계 인구 & 사회 통계 대시보드",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        background-color: #F7F5F0;
    }
    .stApp { background-color: #F7F5F0; }

    /* Header */
    .dashboard-header {
        background: linear-gradient(135deg, #1B4332 0%, #2D6A4F 60%, #40916C 100%);
        border-radius: 20px;
        padding: 2.5rem 3rem;
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }
    .dashboard-header::before {
        content: "🌍";
        position: absolute;
        right: 3rem;
        top: 50%;
        transform: translateY(-50%);
        font-size: 7rem;
        opacity: 0.15;
    }
    .dashboard-header h1 {
        font-family: 'DM Serif Display', serif;
        color: #D8F3DC;
        font-size: 2.4rem;
        margin: 0 0 0.4rem 0;
        letter-spacing: -0.5px;
    }
    .dashboard-header p {
        color: #B7E4C7;
        font-size: 1rem;
        margin: 0;
        font-weight: 300;
    }

    /* Metric cards */
    .metric-row { display: flex; gap: 1rem; margin-bottom: 1.5rem; flex-wrap: wrap; }
    .metric-card {
        background: #fff;
        border-radius: 16px;
        padding: 1.4rem 1.6rem;
        flex: 1;
        min-width: 160px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        border-left: 5px solid;
        transition: transform 0.2s;
    }
    .metric-card:hover { transform: translateY(-3px); }
    .metric-card.green  { border-color: #40916C; }
    .metric-card.blue   { border-color: #4895EF; }
    .metric-card.amber  { border-color: #F4A261; }
    .metric-card.rose   { border-color: #E76F51; }
    .metric-label { font-size: 0.78rem; color: #888; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px; }
    .metric-value { font-size: 1.9rem; font-weight: 600; color: #1a1a1a; line-height: 1.2; }
    .metric-sub   { font-size: 0.82rem; color: #40916C; font-weight: 500; margin-top: 2px; }

    /* Section titles */
    .section-title {
        font-family: 'DM Serif Display', serif;
        font-size: 1.35rem;
        color: #1B4332;
        margin: 0.5rem 0 1rem 0;
        padding-bottom: 0.4rem;
        border-bottom: 2px solid #D8F3DC;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #fff;
        border-right: 1px solid #E8E4DC;
    }
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stMultiSelect label,
    section[data-testid="stSidebar"] .stSlider label {
        font-weight: 500;
        color: #1B4332;
    }

    /* Chart wrapper */
    .chart-card {
        background: #fff;
        border-radius: 16px;
        padding: 1.2rem 1.4rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.05);
        margin-bottom: 1.2rem;
    }
    div[data-testid="stPlotlyChart"] { border-radius: 12px; }

    /* Footer */
    .footer { text-align: center; color: #aaa; font-size: 0.8rem; margin-top: 3rem; padding-top: 1rem; border-top: 1px solid #E8E4DC; }
</style>
""", unsafe_allow_html=True)

# ── Sample Data ───────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    # 1) 연도별 대륙 인구 (1960~2023)
    years = list(range(1960, 2024, 5))
    continents = ["아시아", "아프리카", "유럽", "북아메리카", "남아메리카", "오세아니아"]
    pop_data = {
        "아시아":      [1.70, 2.10, 2.56, 3.07, 3.55, 3.93, 4.30, 4.63, 4.96, 5.23, 5.42, 5.52, 5.61],
        "아프리카":    [0.28, 0.35, 0.44, 0.55, 0.68, 0.84, 1.02, 1.23, 1.45, 1.68, 1.93, 2.14, 2.30],
        "유럽":        [0.60, 0.66, 0.72, 0.75, 0.72, 0.72, 0.73, 0.73, 0.73, 0.74, 0.74, 0.74, 0.74],
        "북아메리카":  [0.28, 0.33, 0.38, 0.44, 0.49, 0.53, 0.57, 0.60, 0.63, 0.66, 0.68, 0.70, 0.71],
        "남아메리카":  [0.15, 0.19, 0.24, 0.30, 0.35, 0.41, 0.46, 0.51, 0.55, 0.59, 0.63, 0.66, 0.68],
        "오세아니아":  [0.016, 0.019, 0.022, 0.026, 0.029, 0.032, 0.035, 0.038, 0.041, 0.044, 0.046, 0.047, 0.048],
    }
    rows = []
    for i, y in enumerate(years):
        for c in continents:
            rows.append({"연도": y, "대륙": c, "인구(십억)": pop_data[c][i]})
    df_pop = pd.DataFrame(rows)

    # 2) 국가별 GDP vs 기대수명
    np.random.seed(42)
    countries = {
        "대한민국": (35000, 83.5, "아시아", 52),
        "일본":     (42000, 84.3, "아시아", 125),
        "중국":     (13000, 77.4, "아시아", 1412),
        "인도":     (2500,  70.8, "아시아", 1400),
        "미국":     (65000, 79.1, "북아메리카", 335),
        "캐나다":   (52000, 82.7, "북아메리카", 38),
        "멕시코":   (10500, 75.1, "북아메리카", 130),
        "독일":     (51000, 81.3, "유럽", 83),
        "프랑스":   (44000, 82.5, "유럽", 68),
        "영국":     (45000, 81.8, "유럽", 67),
        "이탈리아": (35000, 83.4, "유럽", 60),
        "스페인":   (32000, 83.6, "유럽", 47),
        "브라질":   (9000,  75.9, "남아메리카", 215),
        "아르헨티나":(13000, 76.7, "남아메리카", 45),
        "나이지리아":(2100,  55.2, "아프리카", 220),
        "에티오피아":(950,   67.8, "아프리카", 120),
        "이집트":   (4200,  72.0, "아프리카", 104),
        "남아프리카":(6200,  64.9, "아프리카", 60),
        "호주":     (57000, 83.9, "오세아니아", 26),
        "뉴질랜드": (46000, 82.3, "오세아니아", 5),
        "인도네시아":(4700,  71.7, "아시아", 275),
        "파키스탄": (1500,  67.2, "아시아", 230),
        "방글라데시":(2400,  72.6, "아시아", 170),
        "베트남":   (3800,  73.6, "아시아", 97),
        "태국":     (7900,  78.7, "아시아", 70),
    }
    df_gdp = pd.DataFrame([
        {"국가": k, "1인당GDP(USD)": v[0], "기대수명(세)": v[1], "대륙": v[2], "인구(백만)": v[3]}
        for k, v in countries.items()
    ])

    # 3) 연령대별 인구 구조 (한국 vs 세계 평균)
    age_groups = ["0-9세", "10-19세", "20-29세", "30-39세", "40-49세", "50-59세", "60-69세", "70세+"]
    df_age = pd.DataFrame({
        "연령대": age_groups,
        "대한민국(%)": [8.2, 9.4, 11.8, 13.2, 16.1, 16.8, 13.4, 11.1],
        "세계 평균(%)": [17.5, 16.2, 15.3, 13.5, 11.8, 10.2, 8.5, 7.0],
    })

    # 4) 대륙별 현재 인구 비중
    df_pie = pd.DataFrame({
        "대륙": continents,
        "인구(십억)": [5.61, 2.30, 0.74, 0.71, 0.68, 0.048],
    })

    # 5) 연도별 도시화율
    df_urban = pd.DataFrame({
        "연도": list(range(1960, 2024, 5)),
        "세계 평균": [33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57],
        "아시아":    [22, 24, 26, 28, 30, 33, 37, 40, 44, 48, 51, 53, 55],
        "아프리카":  [18, 21, 24, 28, 32, 35, 38, 38, 40, 43, 44, 45, 46],
        "유럽":      [58, 61, 64, 67, 69, 71, 72, 73, 73, 74, 75, 75, 75],
        "북아메리카":[67, 69, 71, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82],
    })

    return df_pop, df_gdp, df_age, df_pie, df_urban

df_pop, df_gdp, df_age, df_pie, df_urban = load_data()

# ── Color palette ─────────────────────────────────────────────────────────────
PALETTE = ["#1B4332", "#40916C", "#74C69D", "#4895EF", "#F4A261", "#E76F51", "#A7C957"]
CONT_COLOR = {
    "아시아":     "#1B4332",
    "아프리카":   "#F4A261",
    "유럽":       "#4895EF",
    "북아메리카": "#E76F51",
    "남아메리카": "#74C69D",
    "오세아니아": "#A7C957",
}

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🔧 필터 & 설정")
    st.markdown("---")

    selected_continents = st.multiselect(
        "📍 대륙 선택 (인구 추이)",
        options=list(CONT_COLOR.keys()),
        default=["아시아", "아프리카", "유럽", "북아메리카"],
    )

    year_range = st.slider(
        "📅 연도 범위",
        min_value=1960, max_value=2023,
        value=(1980, 2023), step=5,
    )

    st.markdown("---")
    st.markdown("**💡 차트 설명**")
    st.caption("• **인구 추이** — 대륙별 인구 변화 (선 그래프)")
    st.caption("• **GDP vs 기대수명** — 국가별 버블 차트")
    st.caption("• **연령 구조** — 한국 vs 세계 평균 비교")
    st.caption("• **대륙 비중** — 현재 인구 파이 차트")
    st.caption("• **도시화율** — 대륙별 도시화 추이")
    st.markdown("---")
    st.caption("📦 데이터: UN World Population Prospects 기반 샘플")

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="dashboard-header">
    <h1>세계 인구 & 사회 통계</h1>
    <p>Global Population & Social Statistics Dashboard · 1960–2023</p>
</div>
""", unsafe_allow_html=True)

# ── KPI Cards ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="metric-row">
    <div class="metric-card green">
        <div class="metric-label">세계 총 인구</div>
        <div class="metric-value">80.4억</div>
        <div class="metric-sub">↑ 2023년 기준</div>
    </div>
    <div class="metric-card blue">
        <div class="metric-label">평균 기대수명</div>
        <div class="metric-value">73.4세</div>
        <div class="metric-sub">↑ 1960년 대비 +20세</div>
    </div>
    <div class="metric-card amber">
        <div class="metric-label">세계 도시화율</div>
        <div class="metric-value">57%</div>
        <div class="metric-sub">↑ 1960년 33% → 2023년</div>
    </div>
    <div class="metric-card rose">
        <div class="metric-label">연간 인구 증가</div>
        <div class="metric-value">+6,900만</div>
        <div class="metric-sub">↓ 증가 속도 둔화 중</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Row 1: 인구 추이 & GDP vs 기대수명 ────────────────────────────────────────
col1, col2 = st.columns([1.1, 1], gap="medium")

with col1:
    st.markdown('<div class="section-title">📈 대륙별 인구 추이</div>', unsafe_allow_html=True)
    df_filtered = df_pop[
        (df_pop["대륙"].isin(selected_continents)) &
        (df_pop["연도"] >= year_range[0]) &
        (df_pop["연도"] <= year_range[1])
    ]
    fig_line = px.line(
        df_filtered, x="연도", y="인구(십억)", color="대륙",
        markers=True,
        color_discrete_map=CONT_COLOR,
        labels={"인구(십억)": "인구 (십억 명)", "연도": ""},
    )
    fig_line.update_traces(line_width=2.5, marker_size=6)
    fig_line.update_layout(
        plot_bgcolor="#fff", paper_bgcolor="#fff",
        font_family="DM Sans",
        legend=dict(orientation="h", yanchor="bottom", y=1.01, xanchor="left", x=0, font_size=12),
        margin=dict(l=10, r=10, t=30, b=10),
        hovermode="x unified",
        xaxis=dict(showgrid=False, tickfont_size=12),
        yaxis=dict(showgrid=True, gridcolor="#F0EDE8", tickfont_size=12),
        height=360,
    )
    st.plotly_chart(fig_line, use_container_width=True)

with col2:
    st.markdown('<div class="section-title">🔵 1인당 GDP vs 기대수명</div>', unsafe_allow_html=True)
    fig_bubble = px.scatter(
        df_gdp, x="1인당GDP(USD)", y="기대수명(세)",
        size="인구(백만)", color="대륙",
        hover_name="국가",
        color_discrete_map=CONT_COLOR,
        size_max=55,
        labels={"1인당GDP(USD)": "1인당 GDP (USD)", "기대수명(세)": "기대수명 (세)"},
    )
    fig_bubble.update_traces(marker_opacity=0.75, marker_line_width=1.5, marker_line_color="white")
    fig_bubble.update_layout(
        plot_bgcolor="#fff", paper_bgcolor="#fff",
        font_family="DM Sans",
        legend=dict(orientation="h", yanchor="bottom", y=1.01, xanchor="left", x=0, font_size=12),
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis=dict(showgrid=True, gridcolor="#F0EDE8", tickformat="$,.0f", tickfont_size=11),
        yaxis=dict(showgrid=True, gridcolor="#F0EDE8", tickfont_size=12),
        height=360,
    )
    st.plotly_chart(fig_bubble, use_container_width=True)

# ── Row 2: 연령 구조 & 파이 ───────────────────────────────────────────────────
col3, col4 = st.columns([1.2, 0.8], gap="medium")

with col3:
    st.markdown('<div class="section-title">👥 연령대별 인구 구조 비교</div>', unsafe_allow_html=True)
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        name="대한민국",
        x=df_age["연령대"],
        y=df_age["대한민국(%)"],
        marker_color="#1B4332",
        marker_line_color="white",
        marker_line_width=1.5,
    ))
    fig_bar.add_trace(go.Bar(
        name="세계 평균",
        x=df_age["연령대"],
        y=df_age["세계 평균(%)"],
        marker_color="#74C69D",
        marker_line_color="white",
        marker_line_width=1.5,
    ))
    fig_bar.update_layout(
        barmode="group",
        plot_bgcolor="#fff", paper_bgcolor="#fff",
        font_family="DM Sans",
        legend=dict(orientation="h", yanchor="bottom", y=1.01, xanchor="left", x=0, font_size=12),
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis=dict(showgrid=False, tickfont_size=12),
        yaxis=dict(showgrid=True, gridcolor="#F0EDE8", ticksuffix="%", tickfont_size=12),
        height=320,
        hovermode="x unified",
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with col4:
    st.markdown('<div class="section-title">🌐 대륙별 인구 비중 (2023)</div>', unsafe_allow_html=True)
    fig_pie = px.pie(
        df_pie, values="인구(십억)", names="대륙",
        color="대륙",
        color_discrete_map=CONT_COLOR,
        hole=0.45,
    )
    fig_pie.update_traces(
        textfont_size=12,
        textfont_family="DM Sans",
        marker_line_color="white",
        marker_line_width=2.5,
        pull=[0.04 if c == "아시아" else 0 for c in df_pie["대륙"]],
    )
    fig_pie.update_layout(
        plot_bgcolor="#fff", paper_bgcolor="#fff",
        font_family="DM Sans",
        legend=dict(font_size=12, orientation="v"),
        margin=dict(l=10, r=10, t=20, b=10),
        height=320,
        annotations=[dict(text="80.4억", x=0.5, y=0.5, font_size=18, font_color="#1B4332",
                          font_family="DM Serif Display", showarrow=False)],
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# ── Row 3: 도시화율 (Full width) ──────────────────────────────────────────────
st.markdown('<div class="section-title">🏙️ 대륙별 도시화율 추이</div>', unsafe_allow_html=True)

urban_colors = ["#1B4332", "#40916C", "#F4A261", "#4895EF", "#E76F51"]
fig_area = go.Figure()
urban_cols = ["세계 평균", "아시아", "아프리카", "유럽", "북아메리카"]

for i, col in enumerate(urban_cols):
    df_u = df_urban[(df_urban["연도"] >= year_range[0]) & (df_urban["연도"] <= year_range[1])]
    fig_area.add_trace(go.Scatter(
        x=df_u["연도"], y=df_u[col],
        name=col,
        mode="lines+markers",
        line=dict(color=urban_colors[i], width=2.5 if col == "세계 평균" else 2,
                  dash="dash" if col == "세계 평균" else "solid"),
        marker=dict(size=5),
        fill="tozeroy" if col == "세계 평균" else "none",
        fillcolor="rgba(27,67,50,0.07)" if col == "세계 평균" else None,
    ))

fig_area.update_layout(
    plot_bgcolor="#fff", paper_bgcolor="#fff",
    font_family="DM Sans",
    legend=dict(orientation="h", yanchor="bottom", y=1.01, xanchor="left", x=0, font_size=12),
    margin=dict(l=10, r=10, t=30, b=10),
    xaxis=dict(showgrid=False, tickfont_size=12),
    yaxis=dict(showgrid=True, gridcolor="#F0EDE8", ticksuffix="%", tickfont_size=12, range=[0, 100]),
    height=320,
    hovermode="x unified",
)
st.plotly_chart(fig_area, use_container_width=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    🌍 세계 인구 & 사회 통계 대시보드 · 샘플 데이터 (UN WPP 기반) · Made with Streamlit & Plotly
</div>
""", unsafe_allow_html=True)
