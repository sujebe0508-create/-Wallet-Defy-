import streamlit as st
import time
import random
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ----------------- 페이지 설정 -----------------
st.set_page_config(page_title="Defy.ai - AI 행동경제학 소비 진단", page_icon="💸", layout="wide")

st.markdown("""
    <style>
    /* 메인 헤더 및 제목 스타일링 */
    h1, h2, h3, .stSubheader {
        color: #0F2042 !important;
        font-family: 'Pretendard', -apple-system, sans-serif;
        font-weight: 700;
    }
    /* 버튼 스타일 */
    .stButton>button {
        background-color: #0F2042;
        color: #FFFFFF !important;
        border-radius: 6px;
        border: none;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #1A3668;
        transform: translateY(-1px);
    }
    .fact-box {
        background-color: #F8FAFC;
        border-left: 5px solid #0F2042;
        padding: 1.5rem;
        border-radius: 0 8px 8px 0;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------- 세션 상태 초기화 -----------------
if 'history' not in st.session_state:
    st.session_state['history'] = []

# ----------------- 앱 타이틀 -----------------
st.title("💸 Defy.ai : 행동경제학 기반 과소비 방어 시스템")
st.markdown("단순한 잔소리가 아닙니다. **행동경제학(Behavioral Economics)** 이론과 **데이터 시각화**를 통해 당신의 비합리적 소비 욕구를 심층 분석합니다.")
st.write("---")

# ----------------- 사이드바 설정 -----------------
with st.sidebar:
    st.header("⚙️ 나의 재무 & 노동 메트릭스")
    hourly_wage = st.number_input("나의 시급 (원)", min_value=9000, max_value=100000, value=10030, step=10)
    monthly_budget = st.number_input("이번 달 여유 예산 (원)", min_value=10000, max_value=5000000, value=500000, step=10000)
    st.caption("💡 입력된 데이터는 기회비용 및 예산 타격도 산출 모델에 사용됩니다.")

# ----------------- 탭 구성 -----------------
tab1, tab2, tab3 = st.tabs(["🛒 실시간 소비 심사", "📈 기회비용 & 자산 분석", "📂 나의 위험 행동 로그"])

with tab1:
    st.markdown("### 🔍 구매 예정 물품 정보 입력")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        item_name = st.text_input("물건 이름", placeholder="예: 무선 헤드폰, 배달 야식 등")
    with col2:
        item_price = st.number_input("가격 (원)", min_value=0, value=150000, step=1000)
        
    category = st.selectbox("물품 카테고리 (행동 편향 분석용)", ["전자기기/장비", "패션/의류", "야식/배달음식", "콘텐츠/구독", "기타 충동구매"])
    
    st.write("")
    if st.button("🚨 AI 심층 분석 및 팩트폭격 가동"):
        if not item_name or item_price <= 0:
            st.warning("제대로 된 물건 이름과 가격을 입력해주세요.")
        else:
            with st.spinner("🧠 행동 패턴 토큰화 및 신경망 가중치 계산 중..."):
                time.sleep(1.5)
                st.toast("기회비용 시뮬레이션 완료", icon="✅")
                
            # 데이터 계산
            required_hours = item_price / hourly_wage
            budget_impact_pct = (item_price / monthly_budget) * 100 if monthly_budget > 0 else 100
            
            # 위험도 계산 로직 (시뮬레이션)
            danger_score = min(99, int((budget_impact_pct * 0.6) + random.randint(20, 40)))
            
            # 로그 저장
            st.session_state['history'].append({
                "시간": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "물품": item_name,
                "가격": item_price,
                "카테고리": category,
                "위험도": danger_score
            })
            
            st.markdown("### 💀 행동경제학 기반 진단 보고서")
            st.error(f"📈 종합 과소비 위험도: {danger_score}%")
            st.progress(danger_score / 100)
            
            # 메트릭스 출력
            mcol1, mcol2, mcol3 = st.columns(3)
            mcol1.metric("요구되는 순수 노동 시간", f"{required_hours:.1f} 시간", "- 휴식 제외")
            mcol2.metric("월 예산 타격도", f"{budget_impact_pct:.1f}%", f"- {item_price:,}원 차감")
            
            # S&P500 기회비용 (10년, 연 8% 수익률 가정)
            future_value = item_price * (1.08 ** 10)
            mcol3.metric("10년 후 기회비용 손실액", f"{int(future_value):,} 원", "S&P500 8% 복리 가정", delta_color="inverse")
            
            # 행동경제학 분석
            st.markdown("#### 🧠 AI 심리 오류 진단")
            if category == "전자기기/장비" or category == "패션/의류":
                theory = "**디드로 효과 (Diderot Effect)**"
                desc = "새로운 물건을 구매하면 그에 맞춰 다른 물건들까지 연쇄적으로 구매하게 되는 현상입니다. 이 물건을 사면, 어울리는 케이스나 다른 액세서리를 추가로 사게 될 확률이 87%입니다."
            elif category == "야식/배달음식":
                theory = "**현재 편향 (Hyperbolic Discounting)**"
                desc = "미래의 더 큰 보상(건강, 자산)보다 당장의 작은 보상(도파민, 포만감)을 비합리적으로 과대평가하는 심리적 오류입니다."
            else:
                theory = "**심적 회계 (Mental Accounting)**"
                desc = "돈의 출처나 용도에 따라 주관적인 꼬리표를 붙여 비합리적으로 소비하는 현상입니다. '어차피 남는 돈'이라는 생각은 자산 증식의 가장 큰 적입니다."
                
            st.markdown(f"""
            <div class="fact-box">
                <p>⚠️ 현재 당신은 <b>{theory}</b>에 빠져있을 가능성이 높습니다.</p>
                <p>{desc}</p>
                <p style='color: #D32F2F; font-weight: bold;'>단순히 {item_price:,}원을 쓰는 것이 아니라, {hourly_wage:,}원짜리 당신의 소중한 생명 {required_hours:.1f}시간을 이 물건과 교환하는 것입니다.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # 레이더 차트 (AI 분석 시뮬레이션)
            st.markdown("#### 📊 심층 리스크 프로파일링")
            categories = ['재정적 타격도', '감정적 소비 확률', '대체재 존재 여부', '유지비용 리스크', '후회 가능성']
            
            # 카테고리별 약간의 가중치
            if category == "야식/배달음식":
                values = [min(100, budget_impact_pct), 95, 80, 10, 90]
            else:
                values = [min(100, budget_impact_pct), random.randint(60, 90), random.randint(50, 90), random.randint(30, 80), random.randint(50, 80)]
                
            fig_radar = go.Figure(data=go.Scatterpolar(
                r=values + [values[0]],
                theta=categories + [categories[0]],
                fill='toself',
                line_color='#0F2042'
            ))
            fig_radar.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                showlegend=False,
                margin=dict(l=40, r=40, t=20, b=20),
                height=350
            )
            st.plotly_chart(fig_radar, use_container_width=True)
            
            # 강제 냉각 조치
            st.write("---")
            st.markdown("#### ⏳ 강제 냉각 시스템 활성화")
            st.info("비합리적 뇌 회로를 차단하기 위해 10초간 구매 확정을 보류합니다.")
            
            placeholder = st.empty()
            for seconds in range(10, 0, -1):
                placeholder.metric(label="이성이 돌아오기까지", value=f"{seconds}초")
                time.sleep(1)
            placeholder.success("🔓 냉각 종료. 진단 결과를 보고도 사야겠다면, 사십시오.")

with tab2:
    st.markdown("### 📈 기회비용 시뮬레이터")
    st.write("만약 이 돈들을 소비하지 않고 **연 8% 수익률의 인덱스 펀드**에 투자했다면?")
    
    if len(st.session_state['history']) == 0:
        st.info("먼저 '실시간 소비 심사' 탭에서 분석을 진행해주세요.")
    else:
        # 지금까지 누적된 소비액
        total_spent = sum([item['가격'] for item in st.session_state['history']])
        
        years = list(range(1, 21)) # 1년~20년
        future_values = [total_spent * (1.08 ** y) for y in years]
        
        df_fv = pd.DataFrame({
            "투자 기간 (년)": years,
            "예상 자산 가치 (원)": future_values
        })
        
        fig_line = px.line(df_fv, x="투자 기간 (년)", y="예상 자산 가치 (원)", markers=True,
                           title=f"현재 소비 누적액 {total_spent:,}원의 복리 마법",
                           color_discrete_sequence=['#1A3668'])
        st.plotly_chart(fig_line, use_container_width=True)
        
        # 예산 파이 차트
        st.markdown("### 🍩 현재 예산 타격도")
        remaining_budget = max(0, monthly_budget - total_spent)
        
        fig_pie = px.pie(
            values=[total_spent, remaining_budget], 
            names=['총 지출(심사 내역)', '남은 예산'],
            hole=0.4,
            color_discrete_sequence=['#D32F2F', '#4CAF50']
        )
        st.plotly_chart(fig_pie, use_container_width=True)

with tab3:
    st.markdown("### 📂 나의 위험 행동 로그")
    st.write("이번 접속 동안 분석된 소비 심사 내역입니다. 데이터가 쌓일수록 스스로의 패턴을 객관화할 수 있습니다.")
    
    if len(st.session_state['history']) == 0:
        st.write("아직 분석된 내역이 없습니다.")
    else:
        df_history = pd.DataFrame(st.session_state['history'])
        st.dataframe(df_history, use_container_width=True)
        
        if st.button("🗑️ 로그 초기화"):
            st.session_state['history'] = []
            st.rerun()

# ----------------- 하단 푸터 -----------------
st.write("")
st.write("")
st.caption("© 2026 Defy.ai - 한구외대 기계학습 프로젝트 (Simulated)")
