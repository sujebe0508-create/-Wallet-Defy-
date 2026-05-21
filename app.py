import streamlit as st
import time
import random
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
# ----------------- 페이지 설정 -----------------
# ── 페이지 설정 ──
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
    h1, h2, h3 { color: #0F2042 !important; font-weight: 700; }
    .stButton>button {
        background-color: #0F2042;
        color: #FFFFFF !important;
        border-radius: 6px;
        border: none;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        background-color: #0F2042; color: #FFFFFF !important;
        border-radius: 6px; border: none; padding: 0.5rem 1.5rem;
        font-weight: 600; transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #1A3668;
        transform: translateY(-1px);
    }
    .stButton>button:hover { background-color: #1A3668; transform: translateY(-1px); }
    .fact-box {
        background-color: #F8FAFC;
        border-left: 5px solid #0F2042;
        padding: 1.5rem;
        border-radius: 0 8px 8px 0;
        margin-top: 1rem;
        margin-bottom: 1rem;
        background-color: #F8FAFC; border-left: 5px solid #0F2042;
        padding: 1.5rem; border-radius: 0 8px 8px 0;
        margin-top: 1rem; margin-bottom: 1rem;
    }
    /* 위험도 배경 애니메이션 */
    @keyframes dangerPulse {
        0%   { background-color: var(--bg-start); }
        50%  { background-color: var(--bg-end); }
        100% { background-color: var(--bg-start); }
    }
    .danger-bg {
        animation: dangerPulse 2s ease-in-out infinite;
        padding: 1.2rem 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        font-size: 1.1rem;
        font-weight: 700;
        text-align: center;
        transition: all 0.5s ease;
        padding: 1.2rem 1.5rem; border-radius: 12px; margin-bottom: 1rem;
        font-size: 1.1rem; font-weight: 700; text-align: center;
    }
    /* 이유 작성 박스 */
    .reason-box {
        background: linear-gradient(135deg, #fff8f8, #fff0f0);
        border: 2px solid #D32F2F;
        border-radius: 12px;
        padding: 1.5rem;
        margin-top: 1rem;
        border: 2px solid #D32F2F; border-radius: 12px; padding: 1.5rem; margin-top: 1rem;
    }
    .char-counter {
        font-size: 0.85rem;
        text-align: right;
        margin-top: 0.3rem;
    }
    .char-ok  { color: #388E3C; font-size: 0.9rem; text-align: right; margin-top: 4px; font-weight: 600; }
    .char-no  { color: #E65100; font-size: 0.9rem; text-align: right; margin-top: 4px; }
    .char-nil { color: #999;    font-size: 0.9rem; text-align: right; margin-top: 4px; }
    </style>
""", unsafe_allow_html=True)
# ----------------- 세션 상태 초기화 -----------------
# ── 세션 상태 초기화 ──
if 'history' not in st.session_state:
    st.session_state['history'] = []
if 'result' not in st.session_state:
    st.session_state['result'] = None   # 분석 결과 저장 → 재실행돼도 유지
# ----------------- 앱 타이틀 -----------------
# ── 타이틀 ──
st.title("💸 Defy.ai : 행동경제학 기반 과소비 방어 시스템")
st.markdown("단순한 잔소리가 아닙니다. **행동경제학(Behavioral Economics)** 이론과 **데이터 시각화**를 통해 당신의 비합리적 소비 욕구를 심층 분석합니다.")
st.write("---")
# ----------------- 사이드바 설정 -----------------
# ── 사이드바 ──
with st.sidebar:
    st.header("⚙️ 나의 재무 & 노동 메트릭스")
    hourly_wage = st.number_input("나의 시급 (원)", min_value=9000, max_value=100000, value=10030, step=10)
    hourly_wage    = st.number_input("나의 시급 (원)", min_value=9000, max_value=100000, value=10030, step=10)
    monthly_budget = st.number_input("이번 달 여유 예산 (원)", min_value=10000, max_value=5000000, value=500000, step=10000)
    st.caption("💡 입력된 데이터는 기회비용 및 예산 타격도 산출 모델에 사용됩니다.")
# ----------------- 탭 구성 -----------------
# ── 탭 ──
tab1, tab2, tab3 = st.tabs(["🛒 실시간 소비 심사", "📈 기회비용 & 자산 분석", "📂 나의 위험 행동 로그"])
# ════════════════════════════════════════
# TAB 1
# ════════════════════════════════════════
with tab1:
    st.markdown("### 🔍 구매 예정 물품 정보 입력")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        item_name = st.text_input("물건 이름", placeholder="예: 무선 헤드폰, 배달 야식 등")
    with col2:
        item_price = st.number_input("가격 (원)", min_value=0, value=150000, step=1000)
        
    category = st.selectbox("물품 카테고리 (행동 편향 분석용)", ["전자기기/장비", "패션/의류", "야식/배달음식", "콘텐츠/구독", "기타 충동구매"])
    
    category = st.selectbox(
        "물품 카테고리 (행동 편향 분석용)",
        ["전자기기/장비", "패션/의류", "야식/배달음식", "콘텐츠/구독", "기타 충동구매"]
    )
    st.write("")
    # ── 분석 버튼 (클릭 시 결과를 session_state에 저장) ──
    if st.button("🚨 AI 심층 분석 및 팩트폭격 가동"):
        if not item_name or item_price <= 0:
            st.warning("제대로 된 물건 이름과 가격을 입력해주세요.")
        else:
            with st.spinner("🧠 행동 패턴 토큰화 및 신경망 가중치 계산 중..."):
                time.sleep(1.5)
                st.toast("기회비용 시뮬레이션 완료", icon="✅")
                
            # 데이터 계산
            required_hours = item_price / hourly_wage
            st.toast("기회비용 시뮬레이션 완료", icon="✅")
            required_hours    = item_price / hourly_wage
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
            danger_score      = min(99, int((budget_impact_pct * 0.6) + random.randint(20, 40)))
            future_value      = item_price * (1.08 ** 10)
            if category in ("전자기기/장비", "패션/의류"):
                theory = "디드로 효과 (Diderot Effect)"
                desc   = "새로운 물건을 구매하면 그에 맞춰 다른 물건들까지 연쇄적으로 구매하게 되는 현상입니다. 이 물건을 사면, 어울리는 케이스나 다른 액세서리를 추가로 사게 될 확률이 87%입니다."
            elif category == "야식/배달음식":
                theory = "**현재 편향 (Hyperbolic Discounting)**"
                desc = "미래의 더 큰 보상(건강, 자산)보다 당장의 작은 보상(도파민, 포만감)을 비합리적으로 과대평가하는 심리적 오류입니다."
                theory = "현재 편향 (Hyperbolic Discounting)"
                desc   = "미래의 더 큰 보상(건강, 자산)보다 당장의 작은 보상(도파민, 포만감)을 비합리적으로 과대평가하는 심리적 오류입니다."
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
                theory = "심적 회계 (Mental Accounting)"
                desc   = "돈의 출처나 용도에 따라 주관적인 꼬리표를 붙여 비합리적으로 소비하는 현상입니다. '어차피 남는 돈'이라는 생각은 자산 증식의 가장 큰 적입니다."
            if category == "야식/배달음식":
                values = [min(100, budget_impact_pct), 95, 80, 10, 90]
                radar_v = [min(100, budget_impact_pct), 95, 80, 10, 90]
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
            
            # ── 위험도 배경색 애니메이션 (danger_score 기반) ──
            # 위험도에 따라 색상 강도 결정
            if danger_score >= 90:
                bg_start = "rgba(255,200,200,0.6)"
                bg_end   = "rgba(220,50,50,0.45)"
                label_color = "#B71C1C"
                level_text = "🔴 CRITICAL — 지금 당장 뒤로가기를 누르십시오"
            elif danger_score >= 75:
                bg_start = "rgba(255,220,180,0.5)"
                bg_end   = "rgba(230,100,30,0.4)"
                label_color = "#E65100"
                level_text = "🟠 HIGH RISK — 위험 신호가 감지되었습니다"
            else:
                bg_start = "rgba(255,245,180,0.5)"
                bg_end   = "rgba(220,180,30,0.35)"
                label_color = "#F57F17"
                level_text = "🟡 MODERATE — 재고해 보십시오"
                radar_v = [min(100, budget_impact_pct),
                           random.randint(60, 90), random.randint(50, 90),
                           random.randint(30, 80), random.randint(50, 80)]
            st.markdown(
                f"""<div class='danger-bg'
                    style='--bg-start:{bg_start}; --bg-end:{bg_end}; color:{label_color};'>
                    {level_text}<br>
                    <span style='font-size:0.85rem; font-weight:400;'>
                    AI 위험도 {danger_score}% · 예산 타격 {budget_impact_pct:.1f}% · 노동 {required_hours:.1f}시간 소모
                    </span>
                </div>""",
                unsafe_allow_html=True
            # 결과 저장
            st.session_state['result'] = dict(
                item_name=item_name, item_price=item_price, category=category,
                required_hours=required_hours, budget_impact_pct=budget_impact_pct,
                danger_score=danger_score, future_value=future_value,
                theory=theory, desc=desc, radar_v=radar_v,
            )
            st.session_state['history'].append({
                "시간": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "물품": item_name, "가격": item_price,
                "카테고리": category, "위험도": danger_score,
            })
            # 이전 이유 텍스트 초기화
            st.session_state['purchase_reason'] = ""
            # ── 강제 냉각 조치 ──
            st.write("---")
            st.markdown("#### ⏳ 강제 냉각 시스템 활성화")
            st.info("비합리적 뇌 회로를 차단하기 위해 10초간 구매 확정을 보류합니다.")
            
            placeholder = st.empty()
            for seconds in range(10, 0, -1):
                placeholder.metric(label="이성이 돌아오기까지", value=f"{seconds}초")
            # 냉각 타이머
            ph = st.empty()
            for s in range(10, 0, -1):
                ph.metric("⏳ 이성이 돌아오기까지", f"{s}초")
                time.sleep(1)
            placeholder.success("🔓 냉각 종료.")
            ph.success("🔓 냉각 종료.")
            # ── 300자 구매 이유 강제 작성 ──
            st.write("---")
            st.markdown("#### ✍️ 최후 관문: 구매 정당화 진술서")
    # ── 결과 렌더링 (session_state 기반 → 텍스트 입력 후 재실행돼도 사라지지 않음) ──
    if st.session_state['result']:
        r  = st.session_state['result']
        ds = r['danger_score']
        st.markdown("### 💀 행동경제학 기반 진단 보고서")
        st.error(f"📈 종합 과소비 위험도: {ds}%")
        st.progress(ds / 100)
        mc1, mc2, mc3 = st.columns(3)
        mc1.metric("요구되는 순수 노동 시간", f"{r['required_hours']:.1f} 시간", "- 휴식 제외")
        mc2.metric("월 예산 타격도", f"{r['budget_impact_pct']:.1f}%", f"- {r['item_price']:,}원 차감")
        mc3.metric("10년 후 기회비용 손실액", f"{int(r['future_value']):,} 원",
                   "S&P500 8% 복리 가정", delta_color="inverse")
        st.markdown("#### 🧠 AI 심리 오류 진단")
        st.markdown(f"""
        <div class="fact-box">
            <p>⚠️ 현재 당신은 <b>{r['theory']}</b>에 빠져있을 가능성이 높습니다.</p>
            <p>{r['desc']}</p>
            <p style='color:#D32F2F; font-weight:bold;'>단순히 {r['item_price']:,}원을 쓰는 것이 아니라,
            {hourly_wage:,}원짜리 당신의 소중한 생명 {r['required_hours']:.1f}시간을 이 물건과 교환하는 것입니다.</p>
        </div>""", unsafe_allow_html=True)
        st.markdown("#### 📊 심층 리스크 프로파일링")
        radar_cats = ['재정적 타격도', '감정적 소비 확률', '대체재 존재 여부', '유지비용 리스크', '후회 가능성']
        fig_radar  = go.Figure(data=go.Scatterpolar(
            r=r['radar_v'] + [r['radar_v'][0]],
            theta=radar_cats + [radar_cats[0]],
            fill='toself', line_color='#0F2042'
        ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=False, margin=dict(l=40, r=40, t=20, b=20), height=350
        )
        st.plotly_chart(fig_radar, use_container_width=True)
        # 위험도 배너
        if ds >= 90:
            bg_s, bg_e, lc = "rgba(255,200,200,0.6)", "rgba(220,50,50,0.45)", "#B71C1C"
            lt = "🔴 CRITICAL — 지금 당장 뒤로가기를 누르십시오"
        elif ds >= 75:
            bg_s, bg_e, lc = "rgba(255,220,180,0.5)", "rgba(230,100,30,0.4)", "#E65100"
            lt = "🟠 HIGH RISK — 위험 신호가 감지되었습니다"
        else:
            bg_s, bg_e, lc = "rgba(255,245,180,0.5)", "rgba(220,180,30,0.35)", "#F57F17"
            lt = "🟡 MODERATE — 재고해 보십시오"
        st.markdown(f"""
        <div class='danger-bg' style='--bg-start:{bg_s}; --bg-end:{bg_e}; color:{lc};'>
            {lt}<br>
            <span style='font-size:0.85rem; font-weight:400;'>
            AI 위험도 {ds}% · 예산 타격 {r['budget_impact_pct']:.1f}% · 노동 {r['required_hours']:.1f}시간 소모
            </span>
        </div>""", unsafe_allow_html=True)
        # ── 300자 강제 입력 (버튼 바깥에 있어서 입력해도 화면 유지됨) ──
        st.write("---")
        st.markdown("#### ✍️ 최후 관문: 구매 정당화 진술서")
        st.markdown("""
        <div class='reason-box'>
            <b>🚨 마지막 저지선입니다.</b><br>
            진단 결과에도 불구하고 구매를 강행하려면,
            <b>이 물건이 당신의 삶에 반드시 필요한 이유를 최소 300자 이상</b> 작성하십시오.<br>
            <span style='color:#888; font-size:0.85rem;'>
            이 과정은 '정당화의 고통(Justification Friction)'을 통해 충동 구매를 억제하는
            행동경제학적 개입 장치입니다.</span>
        </div>""", unsafe_allow_html=True)
        reason = st.text_area(
            "구매 이유 (최소 300자)",
            key="purchase_reason",
            height=160,
            placeholder="이 물건이 나의 삶에 반드시 필요한 이유를 구체적으로 서술하십시오..."
        )
        char_count      = len(reason)
        remaining_chars = max(0, 300 - char_count)
        if char_count == 0:
            st.markdown("<p class='char-nil'>0 / 300자</p>", unsafe_allow_html=True)
        elif remaining_chars > 0:
            st.markdown(
                """<div class='reason-box'>
                <b>🚨 마지막 저지선입니다.</b><br>
                진단 결과에도 불구하고 구매를 강행하려면,
                <b>이 물건이 당신의 삶에 반드시 필요한 이유를 최소 300자 이상</b> 작성하십시오.<br>
                <span style='color:#888; font-size:0.85rem;'>이 과정은 '정당화의 고통(Justification Friction)'을 통해 충동 구매를 억제하는
                행동경제학적 개입 장치입니다.</span>
                </div>""",
                unsafe_allow_html=True
            )
                f"<p class='char-no'>{char_count} / 300자 &nbsp;—&nbsp; 아직 <b>{remaining_chars}자</b> 더 써야 합니다.</p>",
                unsafe_allow_html=True)
        else:
            st.markdown(
                f"<p class='char-ok'>✅ {char_count}자 작성 완료 — 구매 버튼이 활성화되었습니다.</p>",
                unsafe_allow_html=True)
            reason_key = f"reason_{len(st.session_state['history'])}"
            reason = st.text_area(
                "구매 이유 (최소 300자)",
                key=reason_key,
                height=160,
                placeholder="이 물건이 나의 삶에 반드시 필요한 이유를 구체적으로 서술하십시오..."
        st.write("")
        if char_count >= 300:
            if st.button("💳 그래도 구매하겠습니다 (최종 확인)"):
                st.balloons()
                st.warning("⚠️ 구매를 진행하셨군요. 후회는 없으시길 바랍니다. 이 결정이 기록에 남았습니다.")
        else:
            st.button(
                "💳 그래도 구매하겠습니다 (최종 확인)", disabled=True,
                help=f"구매 이유를 {remaining_chars}자 더 작성해야 활성화됩니다."
            )
            char_count = len(reason)
            remaining_chars = max(0, 300 - char_count)
            if char_count == 0:
                st.markdown(
                    "<div class='char-counter' style='color:#999;'>0 / 300자</div>",
                    unsafe_allow_html=True
                )
            elif remaining_chars > 0:
                st.markdown(
                    f"<div class='char-counter' style='color:#E65100;'>{char_count} / 300자 — 아직 {remaining_chars}자 더 써야 합니다.</div>",
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"<div class='char-counter' style='color:#388E3C;'>✅ {char_count}자 작성 완료</div>",
                    unsafe_allow_html=True
                )
            if char_count >= 300:
                if st.button("💳 그래도 구매하겠습니다 (최종 확인)"):
                    st.balloons()
                    st.warning("⚠️ 구매를 진행하셨군요. 후회는 없으시길 바랍니다. 이 결정이 기록에 남았습니다.")
            else:
                st.button("💳 그래도 구매하겠습니다 (최종 확인)", disabled=True,
                          help=f"구매 이유를 {300 - char_count}자 더 작성해야 활성화됩니다.")
# ════════════════════════════════════════
# TAB 2
# ════════════════════════════════════════
with tab2:
    st.markdown("### 📈 기회비용 시뮬레이터")
    st.write("만약 이 돈들을 소비하지 않고 **연 8% 수익률의 인덱스 펀드**에 투자했다면?")
    if len(st.session_state['history']) == 0:
        st.info("먼저 '실시간 소비 심사' 탭에서 분석을 진행해주세요.")
    else:
        total_spent = sum([item['가격'] for item in st.session_state['history']])
        years = list(range(1, 21))
        total_spent   = sum(item['가격'] for item in st.session_state['history'])
        years         = list(range(1, 21))
        future_values = [total_spent * (1.08 ** y) for y in years]
        df_fv = pd.DataFrame({"투자 기간 (년)": years, "예상 자산 가치 (원)": future_values})
        fig_line = px.line(df_fv, x="투자 기간 (년)", y="예상 자산 가치 (원)", markers=True,
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    # ── 30년 충동구매 습관 손실 시뮬레이션 ──
    # ── 30년 노동 손실 시뮬레이션 ──
    st.write("---")
    st.markdown("### 💀 30년 노동 손실 시뮬레이션")
    st.markdown(
        "충동구매가 **습관**이 되면 어떻게 될까요? "
        "매달 이 금액을 소비하는 시나리오 vs 투자하는 시나리오를 비교합니다."
    )
    st.markdown("충동구매가 **습관**이 되면 어떻게 될까요? 매달 이 금액을 소비하는 시나리오 vs 투자하는 시나리오를 비교합니다.")
    # 입력
    sim_col1, sim_col2 = st.columns(2)
    with sim_col1:
        last_price = st.session_state['history'][-1]['가격'] if st.session_state['history'] else 150000
        last_price     = st.session_state['history'][-1]['가격'] if st.session_state['history'] else 150000
        monthly_impulse = st.number_input(
            "월 충동구매 예상액 (원)",
            min_value=10000, max_value=2000000,
            "월 충동구매 예상액 (원)", min_value=10000, max_value=2000000,
            value=int(last_price), step=10000,
            help="마지막으로 분석한 물건 가격이 기본값으로 설정됩니다."
        )
    with sim_col2:
        annual_return = st.slider("가정 연 수익률 (%)", min_value=4, max_value=12, value=8)
    months = list(range(0, 361))  # 0~360개월 (30년)
    months           = list(range(0, 361))
    cumulative_spend = [monthly_impulse * m for m in months]
    # 복리 투자 시뮬레이션 (월 복리)
    monthly_rate = annual_return / 100 / 12
    invest_value = [0.0]
    monthly_rate     = annual_return / 100 / 12
    invest_value     = [0.0]
    for _ in range(360):
        invest_value.append(invest_value[-1] * (1 + monthly_rate) + monthly_impulse)
    df_sim = pd.DataFrame({
        "기간 (개월)": months,
        "💸 소비만 했을 경우 (원금 누적)": cumulative_spend,
        "📈 투자했을 경우 (복리 가치)": invest_value,
    })
    final_invest = invest_value[-1]
    final_spend  = cumulative_spend[-1]
    gap          = final_invest - final_spend
    fig_30 = go.Figure()
    fig_30.add_trace(go.Scatter(
        x=df_sim["기간 (개월)"] / 12,
        y=df_sim["💸 소비만 했을 경우 (원금 누적)"],
        x=[m / 12 for m in months], y=cumulative_spend,
        name="💸 소비만 했을 경우",
        line=dict(color="#D32F2F", width=3),
        fill='tozeroy',
        fillcolor='rgba(211,47,47,0.08)'
        fill='tozeroy', fillcolor='rgba(211,47,47,0.08)'
    ))
    fig_30.add_trace(go.Scatter(
        x=df_sim["기간 (개월)"] / 12,
        y=df_sim["📈 투자했을 경우 (복리 가치)"],
        x=[m / 12 for m in months], y=invest_value,
        name="📈 투자했을 경우",
        line=dict(color="#1A3668", width=3),
        fill='tozeroy',
        fillcolor='rgba(26,54,104,0.08)'
        fill='tozeroy', fillcolor='rgba(26,54,104,0.08)'
    ))
    final_invest = invest_value[-1]
    final_spend  = cumulative_spend[-1]
    gap = final_invest - final_spend
    # 30년 시점 annotation
    fig_30.add_annotation(
        x=30, y=final_invest,
        text=f"📈 {int(final_invest/1e8):.1f}억원",
        showarrow=True, arrowhead=2,
        font=dict(size=13, color="#1A3668"),
        bgcolor="rgba(255,255,255,0.85)"
    )
    fig_30.add_annotation(
        x=30, y=final_spend,
        text=f"💸 {int(final_spend/1e8):.1f}억원",
        showarrow=True, arrowhead=2, ay=40,
        font=dict(size=13, color="#D32F2F"),
        bgcolor="rgba(255,255,255,0.85)"
    )
    fig_30.add_annotation(x=30, y=final_invest,
        text=f"📈 {final_invest/1e8:.1f}억원", showarrow=True, arrowhead=2,
        font=dict(size=13, color="#1A3668"), bgcolor="rgba(255,255,255,0.85)")
    fig_30.add_annotation(x=30, y=final_spend,
        text=f"💸 {final_spend/1e8:.1f}억원", showarrow=True, arrowhead=2, ay=40,
        font=dict(size=13, color="#D32F2F"), bgcolor="rgba(255,255,255,0.85)")
    fig_30.update_layout(
        title=f"30년 후 격차: {int(gap/1e8):.1f}억원 ({int(gap/1e4):,}만원)",
        xaxis_title="경과 연수",
        yaxis_title="금액 (원)",
        title=f"30년 후 격차: {gap/1e8:.1f}억원 ({int(gap/1e4):,}만원)",
        xaxis_title="경과 연수", yaxis_title="금액 (원)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=420,
        margin=dict(l=20, r=20, t=60, b=20)
        height=420, margin=dict(l=20, r=20, t=60, b=20)
    )
    st.plotly_chart(fig_30, use_container_width=True)
    # 충격 요약 카드
    labor_years = final_spend / (hourly_wage * 8 * 250)  # 연 250일 근무 가정
    r1, r2, r3 = st.columns(3)
    r1.metric("30년간 총 소비액", f"{int(final_spend/1e4):,}만원", "습관적 충동구매 누적")
    r2.metric("같은 돈 투자 시 자산", f"{int(final_invest/1e8):.2f}억원", f"연 {annual_return}% 복리")
    labor_years = final_spend / (hourly_wage * 8 * 250)
    r1, r2, r3  = st.columns(3)
    r1.metric("30년간 총 소비액",    f"{int(final_spend/1e4):,}만원",     "습관적 충동구매 누적")
    r2.metric("같은 돈 투자 시 자산", f"{final_invest/1e8:.2f}억원",       f"연 {annual_return}% 복리")
    r3.metric("소비액의 총 노동 환산", f"{labor_years:.1f}년 치 연봉",
              f"시급 {hourly_wage:,}원 기준", delta_color="inverse")
    st.error(
        f"📌 **핵심 메시지:** 매달 {monthly_impulse:,}원의 충동구매 습관은 "
        f"30년 후 **{int(gap/1e8):.1f}억원의 기회비용**으로 돌아옵니다. "
        f"30년 후 **{gap/1e8:.1f}억원의 기회비용**으로 돌아옵니다. "
        f"이것은 단순한 숫자가 아니라, 미래의 당신이 일하지 않아도 될 **{labor_years:.1f}년**입니다."
    )
# ════════════════════════════════════════
# TAB 3
# ════════════════════════════════════════
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
            st.session_state['result']  = None
            st.rerun()
# ----------------- 하단 푸터 -----------------
# ── 푸터 ──
st.write("")
st.write("")
st.caption("© 2026 Defy.ai - 한국외대 기계학습 프로젝트 (Simulated)")

