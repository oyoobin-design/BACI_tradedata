#스트림릿 파일

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm

# --- 0. 페이지 설정 ---
st.set_page_config(page_title="Smart Card Export Dashboard", layout="wide")

# --- 1. 한글 폰트 설정 (Matplotlib용) ---
@st.cache_data
def set_korean_font():
    plt.rcParams['axes.unicode_minus'] = False
    try:
        font_list = [f.name for f in fm.fontManager.ttflist]
        if 'NanumGothic' in font_list:
            plt.rcParams['font.family'] = 'NanumGothic'
        elif 'Malgun Gothic' in font_list:
            plt.rcParams['font.family'] = 'Malgun Gothic'
    except:
        pass

set_korean_font()

# --- 2. 데이터 로드 및 가공 (사용자 로직 엄격 준수) ---
@st.cache_data
def load_and_process_data():
    # 실제 환경에서는 아래 주석을 해제하여 사용하세요.
    # baci_85 = pd.read_csv("./baci_85_only.csv")
    # countries = pd.read_csv('./country_codes_V202501.csv')
    
    # [사용자 제공 로직 재현]
    np.random.seed(42)
    years = [2021, 2022, 2023]
    countries_list = ['USA', 'China', 'Vietnam', 'Germany', 'India', 'Japan', 'UK', 'France', 'Italy', 'Brazil', 'Canada', 'Russia', 'Singapore', 'Australia']
    
    data = {
        't': np.random.choice(years, 1000), # 데이터 양을 조금 늘려 실감나게 재현
        'country_name': np.random.choice(countries_list, 1000),
        'v': np.random.uniform(100, 5000, 1000)
    }
    df = pd.DataFrame(data)
    
    # 성장률 및 피벗 데이터 가공 로직 (수정 없음)
    pivot_df = df.pivot_table(index='country_name', columns='t', values='v', aggfunc='sum').fillna(0)
    pivot_df['growth_rate'] = ((pivot_df[2023] - pivot_df[2021]) / pivot_df[2021] * 100).replace([np.inf, -np.inf], 0)
    pivot_df['total_v'] = pivot_df[2021] + pivot_df[2022] + pivot_df[2023]
    
    return df, pivot_df

df, pivot_df = load_and_process_data()

# --- 3. 사이드바 (필터링 기능) ---
st.sidebar.header("📊 분석 필터")

# 국가 선택 필터
selected_countries = st.sidebar.multiselect(
    "분석 대상 국가 선택",
    options=sorted(df['country_name'].unique()),
    default=df['country_name'].unique()
)

# 데이터 범위 조절
min_val = float(df['v'].min())
max_val = float(df['v'].max())
value_range = st.sidebar.slider("수출 금액 범위(Value)", min_val, max_val, (min_val, max_val))

# 필터링 적용
filtered_df = df[(df['country_name'].isin(selected_countries)) & (df['v'].between(value_range[0], value_range[1]))]
filtered_pivot = pivot_df[pivot_df.index.isin(selected_countries)]

# --- 4. 메인 대시보드 ---
st.title("💳 스마트카드(HS 852352) 수출 실적 분석")
st.markdown("---")

# 핵심 지표(KPI) 요약
if not filtered_pivot.empty:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("총 수출액", f"${filtered_df['v'].sum():,.0f}")
    with col2:
        st.metric("평균 성장률(21-23)", f"{filtered_pivot['growth_rate'].mean():.1f}%")
    with col3:
        top_country = filtered_pivot['total_v'].idxmax()
        st.metric("최대 수출국", top_country)
    with col4:
        st.metric("분석 대상 국가", f"{len(selected_countries)}개")

st.markdown("###")

# --- 5. 시각화 (기타 제외 버전) ---
c1, c2 = st.columns(2)

with c1:
    st.subheader("📈 연도별 총 수출액 추이")
    yearly_total = filtered_df.groupby('t')['v'].sum().reset_index()
    fig1 = px.line(yearly_total, x='t', y='v', markers=True, 
                   text=[f"{val:,.0f}" for val in yearly_total['v']],
                   labels={'t': '연도', 'v': '수출액'},
                   color_discrete_sequence=['#E74C3C'])
    fig1.update_traces(textposition="top center", line_width=3)
    fig1.update_layout(xaxis=dict(tickmode='linear', tickvals=[2021, 2022, 2023]))
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    # [핵심 수정] '기타'를 빼고 상위 국가만 집중 조명
    st.subheader("🥧 주요 수출국 비중 (Top 10)")
    if not filtered_pivot.empty:
        # 상위 10개국만 골라내어 '기타' 없이 비중 산출
        top_10_df = filtered_pivot.nlargest(10, 'total_v')
        
        fig2 = px.pie(
            values=top_10_df['total_v'], 
            names=top_10_df.index,
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        # 라벨에 국가명과 퍼센트가 같이 나오도록 설정
        fig2.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig2, use_container_width=True)

# 시각화 3: 성장률 상위 국가
st.markdown("---")
st.subheader("🚀 수출 성장률 상위 7개국 (2021 대비 2023)")
if not filtered_pivot.empty:
    top_growth = filtered_pivot.nlargest(7, 'growth_rate')
    fig3 = px.bar(top_growth, x='growth_rate', y=top_growth.index, orientation='h',
                  text=[f"{val:.1f}%" for val in top_growth['growth_rate']],
                  color='growth_rate', color_continuous_scale='Reds',
                  labels={'growth_rate': '성장률 (%)'})
    fig3.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig3, use_container_width=True)

# --- 6. 상세 데이터 및 다운로드 ---
with st.expander("📝 분석 데이터 상세보기 및 다운로드"):
    st.dataframe(filtered_pivot.sort_values('total_v', ascending=False), use_container_width=True)
    csv = filtered_pivot.to_csv().encode('utf-8-sig')
    st.download_button(label="결과 데이터 CSV 다운로드", data=csv, file_name='export_analysis.csv', mime='text/csv')