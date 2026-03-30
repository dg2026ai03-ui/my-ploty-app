import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🌍 세계 인구 & 사회 통계",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,300&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #F4F1EB;
}
.stApp { background-color: #F4F1EB; }

/* ── Header ── */
.dash-header {
    background: linear-gradient(135deg, #0D2B1F 0%, #1B4332 55%, #2D6A4F 100%);
    border-radius: 24px;
    padding: 2.8rem 3.5rem;
    margin-bottom: 1.8rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 8px 32px rgba(27,67,50,0.25);
}
.dash-header::after {
    content: "";
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse at 80% 50%, rgba(116,198,157,0.15) 0%, transparent 65%);
}
.dash-header h1 {
    font-family: 'DM Serif Display', serif;
    color: #D8F3DC;
    font-size: 2.6rem;
    margin: 0 0 0.35rem 0;
    letter-spacing: -0.8px;
    position: relative; z-index: 1;
}
.dash-header p {
    color: #95D5B2;
    font-size: 0.95rem;
    margin: 0;
    font-weight: 300;
    letter-spacing: 0.3px;
    position: relative; z-index: 1;
}
.dash-header .badge {
    display: inline-block;
    background: rgba(116,198,157,0.2);
    border: 1px solid rgba(116,198,157,0.4);
    color: #74C69D;
    border-radius: 20px;
    padding: 0.2rem 0.8rem;
    font-size: 0.75rem;
    font-weight: 500;
    margin-top: 0.7rem;
    letter-spacing: 0.5px;
    position: relative; z-index: 1;
}

/* ── Tab nav ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background: #fff;
    border-radius: 14px;
    padding: 5px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.06);
    margin-bottom: 1.2rem;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px;
    padding: 0.5rem 1.4rem;
    font-weight: 500;
    font-size: 0.88rem;
    color: #666;
    border: none;
}
.stTabs [aria-selected="true"] {
    background: #1B4332 !important;
    color: #D8F3DC !important;
}

/* ── KPI cards ── */
.kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-bottom: 1.6rem; }
.kpi-card {
    background: #fff;
    border-radius: 18px;
    padding: 1.4rem 1.6rem 1.2rem;
    box-shadow: 0 2px 14px rgba(0,0,0,0.055);
    border-top: 4px solid;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s, box-shadow 0.2s;
}
.kpi-card:hover { transform: translateY(-4px); box-shadow: 0 8px 24px rgba(0,0,0,0.1); }
.kpi-card::after {
    content: attr(data-icon);
    position: absolute;
    right: 1rem; bottom: 0.6rem;
    font-size: 2.8rem;
    opacity: 0.08;
}
.kpi-card.c1 { border-color: #1B4332; }
.kpi-card.c2 { border-color: #4895EF; }
.kpi-card.c3 { border-color: #F4A261; }
.kpi-card.c4 { border-color: #E76F51; }
.kpi-label { font-size: 0.73rem; color: #999; font-weight: 600; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 0.3rem; }
.kpi-value { font-size: 2rem; font-weight: 700; color: #111; line-height: 1.15; }
.kpi-sub { font-size: 0.8rem; margin-top: 0.35rem; font-weight: 500; }
.kpi-sub.up   { color: #2D6A4F; }
.kpi-sub.down { color: #E76F51; }

/* ── Section titles ── */
.sec-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.25rem;
    color: #0D2B1F;
    margin: 0 0 0.5rem 0;
    padding-bottom: 0.45rem;
    border-bottom: 2px solid #D8F3DC;
}
.chart-caption {
    font-size: 0.78rem;
    color: #aaa;
    margin-top: -0.2rem;
    margin-bottom: 0.5rem;
    font-style: italic;
}

/* ── Insight box ── */
.insight-box {
    background: linear-gradient(135deg, #F0FAF4 0%, #E8F5EC 100%);
    border-left: 4px solid #40916C;
    border-radius: 0 12px 12px 0;
    padding: 0.9rem 1.2rem;
    margin: 0.6rem 0 1.2rem 0;
    font-size: 0.86rem;
    color: #1B4332;
    line-height: 1.6;
}
.insight-box strong { color: #0D2B1F; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #fff;
    border-right: 1px solid #EAE6DD;
}
.sidebar-section {
    background: #F4F1EB;
    border-radius: 12px;
    padding: 0.9rem 1rem;
    margin-bottom: 1rem;
}

/* ── Footer ── */
.dash-footer {
    text-align: center;
    color: #bbb;
    font-size: 0.78rem;
    margin-top: 3rem;
    padding: 1.2rem 0;
    border-top: 1px solid #EAE6DD;
}
</style>
""", unsafe_allow_html=True)

# ── Palette & layout helpers ──────────────────────────────────────────────────
CONT_COLOR = {
    "아시아":      "#1B4332",
    "아프리카":    "#F4A261",
    "유럽":        "#4895EF",
    "북아메리카":  "#E76F51",
    "남아메리카":  "#74C69D",
    "오세아니아":  "#A7C957",
}
BASE = dict(plot_bgcolor="#fff", paper_bgcolor="#fff", font_family="DM Sans", margin=dict(l=8, r=8, t=36, b=8))
GRID  = dict(showgrid=True,  gridcolor="#F2EFEA", gridwidth=1)
NOGRID = dict(showgrid=False)

# ── Data ─────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    years = list(range(1960, 2024, 5))
    continents = list(CONT_COLOR.keys())

    # 인구 추이
    pop_raw = {
        "아시아":      [1.70,2.10,2.56,3.07,3.55,3.93,4.30,4.63,4.96,5.23,5.42,5.52,5.61],
        "아프리카":    [0.28,0.35,0.44,0.55,0.68,0.84,1.02,1.23,1.45,1.68,1.93,2.14,2.30],
        "유럽":        [0.60,0.66,0.72,0.75,0.72,0.72,0.73,0.73,0.73,0.74,0.74,0.74,0.74],
        "북아메리카":  [0.28,0.33,0.38,0.44,0.49,0.53,0.57,0.60,0.63,0.66,0.68,0.70,0.71],
        "남아메리카":  [0.15,0.19,0.24,0.30,0.35,0.41,0.46,0.51,0.55,0.59,0.63,0.66,0.68],
        "오세아니아":  [0.016,0.019,0.022,0.026,0.029,0.032,0.035,0.038,0.041,0.044,0.046,0.047,0.048],
    }
    rows = []
    for i, y in enumerate(years):
        for c in continents:
            rows.append({"연도": y, "대륙": c, "인구(십억)": pop_raw[c][i]})
    df_pop = pd.DataFrame(rows)

    # 국가별 데이터
    countries = {
        "대한민국":   (35000,83.5,"아시아",52,"KOR"),
        "일본":       (42000,84.3,"아시아",125,"JPN"),
        "중국":       (13000,77.4,"아시아",1412,"CHN"),
        "인도":       (2500, 70.8,"아시아",1400,"IND"),
        "인도네시아": (4700, 71.7,"아시아",275,"IDN"),
        "파키스탄":   (1500, 67.2,"아시아",230,"PAK"),
        "방글라데시": (2400, 72.6,"아시아",170,"BGD"),
        "베트남":     (3800, 73.6,"아시아",97,"VNM"),
        "태국":       (7900, 78.7,"아시아",70,"THA"),
        "미국":       (65000,79.1,"북아메리카",335,"USA"),
        "캐나다":     (52000,82.7,"북아메리카",38,"CAN"),
        "멕시코":     (10500,75.1,"북아메리카",130,"MEX"),
        "독일":       (51000,81.3,"유럽",83,"DEU"),
        "프랑스":     (44000,82.5,"유럽",68,"FRA"),
        "영국":       (45000,81.8,"유럽",67,"GBR"),
        "이탈리아":   (35000,83.4,"유럽",60,"ITA"),
        "스페인":     (32000,83.6,"유럽",47,"ESP"),
        "폴란드":     (18000,76.9,"유럽",38,"POL"),
        "브라질":     (9000, 75.9,"남아메리카",215,"BRA"),
        "아르헨티나": (13000,76.7,"남아메리카",45,"ARG"),
        "콜롬비아":   (6800, 77.3,"남아메리카",51,"COL"),
        "나이지리아": (2100, 55.2,"아프리카",220,"NGA"),
        "에티오피아": (950,  67.8,"아프리카",120,"ETH"),
        "이집트":     (4200, 72.0,"아프리카",104,"EGY"),
        "남아프리카": (6200, 64.9,"아프리카",60,"ZAF"),
        "케냐":       (2100, 67.5,"아프리카",55,"KEN"),
        "호주":       (57000,83.9,"오세아니아",26,"AUS"),
        "뉴질랜드":   (46000,82.3,"오세아니아",5,"NZL"),
    }
    df_gdp = pd.DataFrame([
        {"국가":k,"1인당GDP":v[0],"기대수명":v[1],"대륙":v[2],"인구(백만)":v[3],"ISO":v[4]}
        for k,v in countries.items()
    ])

    # 연령 구조
    age_groups = ["0-9세","10-19세","20-29세","30-39세","40-49세","50-59세","60-69세","70세+"]
    df_age = pd.DataFrame({
        "연령대": age_groups,
        "대한민국(%)": [8.2,9.4,11.8,13.2,16.1,16.8,13.4,11.1],
        "세계 평균(%)": [17.5,16.2,15.3,13.5,11.8,10.2,8.5,7.0],
        "일본(%)":      [7.8,9.1,11.0,12.4,12.8,15.2,16.0,15.7],
    })

    # 파이
    df_pie = pd.DataFrame({
        "대륙": continents,
        "인구(십억)": [5.61,2.30,0.74,0.71,0.68,0.048],
    })

    # 도시화율
    df_urban = pd.DataFrame({
        "연도": years,
        "세계 평균": [33,35,37,39,41,43,45,47,49,51,53,55,57],
        "아시아":    [22,24,26,28,30,33,37,40,44,48,51,53,55],
        "아프리카":  [18,21,24,28,32,35,38,38,40,43,44,45,46],
        "유럽":      [58,61,64,67,69,71,72,73,73,74,75,75,75],
        "북아메리카":[67,69,71,73,74,75,76,77,78,79,80,81,82],
    })

    # 출생률 히트맵
    hm_countries = ["대한민국","일본","중국","인도","독일","프랑스","미국","브라질","나이지리아","에티오피아","호주","캐나다"]
    np.random.seed(7)
    hm_years = list(range(1990, 2024, 5))
    birth_base = {
        "대한민국":9,"일본":9,"중국":12,"인도":25,"독일":10,"프랑스":13,
        "미국":15,"브라질":18,"나이지리아":40,"에티오피아":38,"호주":14,"캐나다":13
    }
    hm_rows = []
    for c in hm_countries:
        for i, y in enumerate(hm_years):
            val = max(5, birth_base[c] - i * 0.6 + np.random.uniform(-0.5, 0.5))
            hm_rows.append({"국가": c, "연도": y, "출생률(‰)": round(val, 1)})
    df_heatmap = pd.DataFrame(hm_rows)

    # 트리맵
    df_tree = pd.DataFrame([
        {"국가":k,"대륙":v[2],"인구(백만)":v[3],"기대수명":v[1],"1인당GDP":v[0]}
        for k,v in countries.items()
    ])

    # 합계출산율
    fertility_countries = ["대한민국","일본","중국","인도","미국","독일","브라질","나이지리아"]
    fertility_base = {"대한민국":4.5,"일본":2.0,"중국":5.7,"인도":5.9,"미국":3.7,"독일":2.5,"브라질":6.0,"나이지리아":6.8}
    fertility_end  = {"대한민국":0.72,"일본":1.20,"중국":1.09,"인도":2.0,"미국":1.66,"독일":1.46,"브라질":1.65,"나이지리아":5.1}
    f_years = list(range(1960, 2024, 4))
    np.random.seed(42)
    f_rows = []
    for c in fertility_countries:
        vals = np.linspace(fertility_base[c], fertility_end[c], len(f_years))
        vals += np.random.uniform(-0.05, 0.05, len(f_years))
        for y, v in zip(f_years, vals):
            f_rows.append({"연도": y, "국가": c, "합계출산율": round(max(0.5, v), 2)})
    df_fertility = pd.DataFrame(f_rows)

    return df_pop, df_gdp, df_age, df_pie, df_urban, df_heatmap, df_tree, df_fertility

df_pop, df_gdp, df_age, df_pie, df_urban, df_heatmap, df_tree, df_fertility = load_data()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🔧 필터 & 설정")

    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    selected_continents = st.multiselect(
        "📍 대륙 선택",
        options=list(CONT_COLOR.keys()),
        default=["아시아","아프리카","유럽","북아메리카"],
    )
    year_range = st.slider("📅 연도 범위", 1960, 2023, (1975, 2023), step=5)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    bubble_x    = st.selectbox("버블차트 X축", ["1인당GDP","기대수명","인구(백만)"], index=0)
    bubble_y    = st.selectbox("버블차트 Y축", ["기대수명","1인당GDP","인구(백만)"], index=0)
    bubble_size = st.selectbox("버블 크기 기준", ["인구(백만)","1인당GDP","기대수명"], index=0)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    tree_metric = st.radio("🌳 트리맵 색상", ["기대수명","1인당GDP"], index=0)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.caption("📦 UN World Population Prospects 기반 샘플 데이터")

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="dash-header">
    <h1>세계 인구 & 사회 통계</h1>
    <p>Global Population & Social Statistics Dashboard · 1960–2023</p>
    <span class="badge">📊 SAMPLE DATA · UN WPP 기반</span>
</div>
""", unsafe_allow_html=True)

# ── KPI ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="kpi-grid">
    <div class="kpi-card c1" data-icon="🌍">
        <div class="kpi-label">세계 총 인구</div>
        <div class="kpi-value">80.4억</div>
        <div class="kpi-sub up">↑ 1960년 대비 +3.1배</div>
    </div>
    <div class="kpi-card c2" data-icon="❤️">
        <div class="kpi-label">평균 기대수명</div>
        <div class="kpi-value">73.4세</div>
        <div class="kpi-sub up">↑ 1960년 대비 +20.1세</div>
    </div>
    <div class="kpi-card c3" data-icon="🏙️">
        <div class="kpi-label">세계 도시화율</div>
        <div class="kpi-value">57%</div>
        <div class="kpi-sub up">↑ 1960년 33% → 현재</div>
    </div>
    <div class="kpi-card c4" data-icon="👶">
        <div class="kpi-label">합계출산율</div>
        <div class="kpi-value">2.31명</div>
        <div class="kpi-sub down">↓ 1960년 4.97 → 현재</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 인구 & 도시화",
    "🔬 국가 비교",
    "👥 연령 & 출산",
    "🗺️ 분포 시각화",
])

# ═══════════ TAB 1 ════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="sec-title">📈 대륙별 인구 추이</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-caption">사이드바에서 대륙·연도 범위를 조정하세요</div>', unsafe_allow_html=True)

    df_f = df_pop[df_pop["대륙"].isin(selected_continents) & df_pop["연도"].between(*year_range)]
    fig_line = px.line(df_f, x="연도", y="인구(십억)", color="대륙",
                       markers=True, color_discrete_map=CONT_COLOR,
                       labels={"인구(십억)":"인구 (십억 명)","연도":""})
    fig_line.update_traces(line_width=2.8, marker_size=7, marker_line_width=2, marker_line_color="white")
    fig_line.update_layout(**BASE, height=380, hovermode="x unified",
        legend=dict(orientation="h", y=1.08, x=0, font_size=12, bgcolor="rgba(0,0,0,0)"),
        xaxis={**NOGRID,"tickfont":{"size":12}},
        yaxis={**GRID,"tickfont":{"size":12},"ticksuffix":"B"})
    st.plotly_chart(fig_line, use_container_width=True)

    st.markdown('<div class="insight-box">💡 <strong>인사이트:</strong> 아프리카의 인구 증가 속도가 최근 가장 가파릅니다. 2050년에는 아프리카 인구가 25억을 넘어설 것으로 전망됩니다. 유럽은 1990년대부터 정체 상태입니다.</div>', unsafe_allow_html=True)

    st.markdown('<div class="sec-title">🏙️ 대륙별 도시화율 추이</div>', unsafe_allow_html=True)
    df_u = df_urban[df_urban["연도"].between(*year_range)]
    urban_cols   = ["세계 평균","아시아","아프리카","유럽","북아메리카"]
    urban_colors = ["#111","#1B4332","#F4A261","#4895EF","#E76F51"]
    fig_urban = go.Figure()
    for col, color in zip(urban_cols, urban_colors):
        is_avg = col == "세계 평균"
        fig_urban.add_trace(go.Scatter(
            x=df_u["연도"], y=df_u[col], name=col, mode="lines+markers",
            line=dict(color=color, width=3.5 if is_avg else 2, dash="dot" if is_avg else "solid"),
            marker=dict(size=6 if is_avg else 5, symbol="diamond" if is_avg else "circle"),
            fill="tozeroy" if is_avg else "none",
            fillcolor="rgba(17,17,17,0.04)" if is_avg else None,
        ))
    fig_urban.update_layout(**BASE, height=340, hovermode="x unified",
        legend=dict(orientation="h", y=1.08, x=0, font_size=12, bgcolor="rgba(0,0,0,0)"),
        xaxis={**NOGRID,"tickfont":{"size":12}},
        yaxis={**GRID,"tickfont":{"size":12},"ticksuffix":"%","range":[0,100]})
    st.plotly_chart(fig_urban, use_container_width=True)

# ═══════════ TAB 2 ════════════════════════════════════════════════════════════
with tab2:
    col_a, col_b = st.columns(2, gap="medium")

    with col_a:
        st.markdown('<div class="sec-title">🔵 국가 버블 차트</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="chart-caption">X: {bubble_x} · Y: {bubble_y} · 크기: {bubble_size} — 사이드바에서 축을 바꿔보세요</div>', unsafe_allow_html=True)
        axis_fmt = {"1인당GDP":"1인당 GDP (USD)","기대수명":"기대수명 (세)","인구(백만)":"인구 (백만 명)"}
        fig_bubble = px.scatter(df_gdp, x=bubble_x, y=bubble_y, size=bubble_size,
                                color="대륙", hover_name="국가",
                                color_discrete_map=CONT_COLOR, size_max=60,
                                labels={bubble_x:axis_fmt[bubble_x], bubble_y:axis_fmt[bubble_y]})
        fig_bubble.update_traces(marker_opacity=0.78, marker_line_width=2, marker_line_color="white")
        fig_bubble.update_layout(**BASE, height=420,
            legend=dict(orientation="h", y=1.08, x=0, font_size=12, bgcolor="rgba(0,0,0,0)"),
            xaxis={**GRID,"tickformat":"$,.0f" if "GDP" in bubble_x else ",","tickfont":{"size":11}},
            yaxis={**GRID,"tickfont":{"size":12}})
        st.plotly_chart(fig_bubble, use_container_width=True)

    with col_b:
        st.markdown('<div class="sec-title">📊 기대수명 TOP 15</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-caption">기대수명 기준 내림차순 정렬</div>', unsafe_allow_html=True)
        df_top = df_gdp.nlargest(15, "기대수명").sort_values("기대수명")
        fig_hbar = go.Figure(go.Bar(
            x=df_top["기대수명"], y=df_top["국가"], orientation="h",
            marker=dict(
                color=df_top["기대수명"],
                colorscale=[[0,"#D8F3DC"],[0.5,"#40916C"],[1,"#0D2B1F"]],
                showscale=True,
                colorbar=dict(thickness=12, len=0.7, tickfont_size=10),
            ),
            text=df_top["기대수명"].apply(lambda x: f"{x}세"),
            textposition="outside", textfont_size=11,
        ))
        fig_hbar.update_layout(**BASE, height=420,
            xaxis={**GRID,"range":[55,90],"ticksuffix":"세","tickfont":{"size":11}},
            yaxis={**NOGRID,"tickfont":{"size":11}})
        st.plotly_chart(fig_hbar, use_container_width=True)

    st.markdown('<div class="sec-title">🌡️ 국가별 출생률 히트맵 (‰)</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-caption">색이 진할수록 출생률이 높음 · 1990–2023년</div>', unsafe_allow_html=True)
    pivot = df_heatmap.pivot(index="국가", columns="연도", values="출생률(‰)")
    fig_hm = go.Figure(go.Heatmap(
        z=pivot.values,
        x=[str(y) for y in pivot.columns],
        y=pivot.index.tolist(),
        colorscale=[[0,"#F7F5F0"],[0.3,"#95D5B2"],[0.7,"#2D6A4F"],[1,"#0D2B1F"]],
        showscale=True,
        hovertemplate="<b>%{y}</b><br>%{x}년: %{z}‰<extra></extra>",
        colorbar=dict(thickness=14, len=0.9, tickfont_size=10, title="‰"),
    ))
    fig_hm.update_layout(**BASE, height=360,
        xaxis=dict(title="", tickfont_size=11),
        yaxis=dict(tickfont_size=11, autorange="reversed"))
    st.plotly_chart(fig_hm, use_container_width=True)

    st.markdown('<div class="insight-box">💡 <strong>인사이트:</strong> 나이지리아·에티오피아는 출생률 40‰ 수준을 유지하는 반면, 대한민국·일본은 30년 새 절반 이하로 감소했습니다.</div>', unsafe_allow_html=True)

# ═══════════ TAB 3 ════════════════════════════════════════════════════════════
with tab3:
    col_c, col_d = st.columns([1.1, 0.9], gap="medium")

    with col_c:
        st.markdown('<div class="sec-title">👥 연령대별 인구 구조</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-caption">대한민국 vs 세계 평균 vs 일본</div>', unsafe_allow_html=True)
        fig_age = go.Figure()
        for col_name, color, label in [
            ("대한민국(%)","#1B4332","대한민국"),
            ("세계 평균(%)","#74C69D","세계 평균"),
            ("일본(%)","#4895EF","일본"),
        ]:
            fig_age.add_trace(go.Bar(
                name=label, x=df_age["연령대"], y=df_age[col_name],
                marker_color=color, marker_line_color="white", marker_line_width=1.5,
                text=df_age[col_name].apply(lambda v: f"{v}%"),
                textposition="outside", textfont_size=10,
            ))
        fig_age.update_layout(**BASE, barmode="group", height=400, hovermode="x unified",
            legend=dict(orientation="h", y=1.08, x=0, font_size=12, bgcolor="rgba(0,0,0,0)"),
            xaxis={**NOGRID,"tickfont":{"size":11}},
            yaxis={**GRID,"ticksuffix":"%","tickfont":{"size":11}})
        st.plotly_chart(fig_age, use_container_width=True)

    with col_d:
        st.markdown('<div class="sec-title">🥧 대륙별 인구 비중 (2023)</div>', unsafe_allow_html=True)
        fig_pie = px.pie(df_pie, values="인구(십억)", names="대륙",
                         color="대륙", color_discrete_map=CONT_COLOR, hole=0.48)
        fig_pie.update_traces(
            textfont_size=12, textfont_family="DM Sans",
            marker_line_color="white", marker_line_width=3,
            pull=[0.05 if c=="아시아" else 0 for c in df_pie["대륙"]],
        )
        fig_pie.update_layout(**BASE, height=310,
            legend=dict(font_size=12, orientation="v", bgcolor="rgba(0,0,0,0)"),
            annotations=[dict(text="80.4억", x=0.5, y=0.5,
                              font_size=20, font_color="#0D2B1F",
                              font_family="DM Serif Display", showarrow=False)])
        st.plotly_chart(fig_pie, use_container_width=True)
        st.markdown('<div class="insight-box" style="margin-top:0.4rem;">💡 아시아가 세계 인구의 <strong>70%</strong>를 차지. 아프리카는 28.6%로 2위입니다.</div>', unsafe_allow_html=True)

    st.markdown('<div class="sec-title">👶 국가별 합계출산율 추이</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-caption">여성 1인당 평균 출생아 수 · 대체출산율 기준선: 2.1명</div>', unsafe_allow_html=True)

    fertility_countries_sel = st.multiselect(
        "국가 선택",
        options=df_fertility["국가"].unique().tolist(),
        default=["대한민국","일본","인도","나이지리아","미국","독일"],
    )
    fp = ["#1B4332","#40916C","#74C69D","#4895EF","#E76F51","#F4A261","#A7C957","#9B5DE5"]
    fig_fert = go.Figure()
    fig_fert.add_hline(y=2.1, line_dash="dash", line_color="#E76F51", line_width=1.5,
                       annotation_text="대체출산율 2.1", annotation_position="right",
                       annotation_font_size=11, annotation_font_color="#E76F51")
    df_fert_f = df_fertility[
        df_fertility["국가"].isin(fertility_countries_sel) &
        df_fertility["연도"].between(*year_range)
    ]
    for i, country in enumerate(fertility_countries_sel):
        df_c = df_fert_f[df_fert_f["국가"] == country]
        fig_fert.add_trace(go.Scatter(
            x=df_c["연도"], y=df_c["합계출산율"], name=country,
            mode="lines+markers",
            line=dict(color=fp[i % len(fp)], width=2.5),
            marker=dict(size=5),
        ))
    fig_fert.update_layout(**BASE, height=370, hovermode="x unified",
        legend=dict(orientation="h", y=1.08, x=0, font_size=12, bgcolor="rgba(0,0,0,0)"),
        xaxis={**NOGRID,"tickfont":{"size":12}},
        yaxis={**GRID,"ticksuffix":"명","tickfont":{"size":12}})
    st.plotly_chart(fig_fert, use_container_width=True)

    st.markdown('<div class="insight-box">💡 <strong>인사이트:</strong> 대한민국의 합계출산율은 2023년 <strong>0.72명</strong>으로 세계 최저 수준입니다. 인구 유지에 필요한 대체출산율(2.1명)의 1/3 수준입니다.</div>', unsafe_allow_html=True)

# ═══════════ TAB 4 ════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="sec-title">🌳 국가별 인구 트리맵</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="chart-caption">박스 크기: 인구 · 색상: {tree_metric} — 사이드바에서 색상 기준 변경 가능</div>', unsafe_allow_html=True)

    fig_tree = px.treemap(
        df_tree,
        path=[px.Constant("세계"), "대륙", "국가"],
        values="인구(백만)",
        color=tree_metric,
        color_continuous_scale=[[0,"#D8F3DC"],[0.45,"#40916C"],[1,"#0D2B1F"]],
        range_color=[df_tree[tree_metric].min(), df_tree[tree_metric].max()],
        hover_data={"1인당GDP":":,.0f","기대수명":":.1f","인구(백만)":":.0f"},
    )
    fig_tree.update_traces(
        textfont_size=12,
        marker_line_color="white", marker_line_width=2,
        hovertemplate="<b>%{label}</b><br>인구: %{value:.0f}백만<br>" + f"{tree_metric}: %{{color:.1f}}<extra></extra>",
    )
    fig_tree.update_layout(**BASE, height=480,
        coloraxis_colorbar=dict(thickness=14, len=0.8, tickfont_size=10,
                                title=dict(text=tree_metric, font_size=11)))
    st.plotly_chart(fig_tree, use_container_width=True)

    st.markdown('<div class="sec-title">🗺️ 세계 기대수명 지도</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-caption">색이 진할수록 기대수명이 높음 · 마우스를 올려 상세 정보 확인</div>', unsafe_allow_html=True)

    fig_map = px.choropleth(
        df_gdp, locations="ISO", color="기대수명", hover_name="국가",
        hover_data={"1인당GDP":":,.0f","인구(백만)":":.0f","ISO":False},
        color_continuous_scale=[[0,"#F4F1EB"],[0.2,"#D8F3DC"],[0.5,"#52B788"],[0.8,"#1B4332"],[1,"#0D2B1F"]],
        range_color=[55, 86],
        labels={"기대수명":"기대수명 (세)"},
    )
    fig_map.update_geos(
        showcoastlines=True, coastlinecolor="#ccc",
        showland=True, landcolor="#F4F1EB",
        showocean=True, oceancolor="#EAF4FB",
        showcountries=True, countrycolor="#ddd",
        projection_type="natural earth",
        bgcolor="#fff",
    )
    fig_map.update_layout(**BASE, height=440,
        coloraxis_colorbar=dict(thickness=14, len=0.7, tickfont_size=10,
                                title=dict(text="기대수명", font_size=11)))
    st.plotly_chart(fig_map, use_container_width=True)

    st.markdown('<div class="insight-box">💡 <strong>인사이트:</strong> 선진국일수록 기대수명 80세 이상이 뚜렷합니다. 사하라 이남 아프리카는 여전히 60세 미만이 많으며, 의료 인프라 격차가 주요 원인입니다.</div>', unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="dash-footer">
    🌍 세계 인구 & 사회 통계 대시보드 &nbsp;·&nbsp; 샘플 데이터 (UN WPP 기반) &nbsp;·&nbsp; Made with Streamlit & Plotly
</div>
""", unsafe_allow_html=True)
