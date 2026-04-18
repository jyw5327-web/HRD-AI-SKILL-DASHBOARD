import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="AI Skill Diagnostic System", layout="wide")

# -----------------------------
# Skill Framework
# -----------------------------
skill_categories = {
    "AI 이해·판단": [
        "AI 원리 이해",
        "AI 한계 인식",
        "과업 적합성 판단"
    ],
    "프롬프트 설계": [
        "프롬프트 구조화",
        "프롬프트 개선",
        "템플릿 활용"
    ],
    "업무 적용": [
        "AI 도구 선택",
        "업무 적용 능력",
        "성과 전환"
    ],
    "책임 있는 활용": [
        "데이터 보호",
        "윤리 인식",
        "위험 판단"
    ],
    "창의·문제해결": [
        "아이디어 생성",
        "혁신 활용",
        "문제 해결"
    ]
}

# -----------------------------
# Sidebar Input
# -----------------------------
st.sidebar.title("AI 역량 진단")
user_name = st.sidebar.text_input("이름", "사용자")

responses = {}

st.sidebar.markdown("---")
st.sidebar.write("각 문항을 1~5점으로 평가하세요")

for category, items in skill_categories.items():
    st.sidebar.subheader(category)
    for item in items:
        key = f"{category}_{item}"
        responses[key] = st.sidebar.slider(item, 1, 5, 3)

# -----------------------------
# Data Processing
# -----------------------------
data = []
for key, score in responses.items():
    category, item = key.split("_")
    data.append([category, item, score])

df = pd.DataFrame(data, columns=["Category", "Item", "Score"])
category_avg = df.groupby("Category")["Score"].mean().reset_index()

# -----------------------------
# Main UI
# -----------------------------
st.title(f"🤖 {user_name}님의 AI 역량 대시보드")

col1, col2 = st.columns(2)

# Radar Chart (Plotly)
with col1:
    st.subheader("역량 레이더 차트")
    fig = px.line_polar(category_avg, r="Score", theta="Category", line_close=True)
    st.plotly_chart(fig)

# Bar Chart
with col2:
    st.subheader("영역별 점수")
    fig2 = px.bar(category_avg, x="Category", y="Score")
    st.plotly_chart(fig2)

# -----------------------------
# Insights
# -----------------------------
st.subheader("📊 진단 결과")

avg_score = df["Score"].mean()
st.write(f"전체 평균 점수: {avg_score:.2f}")

strong = category_avg[category_avg["Score"] >= 4]["Category"].tolist()
weak = category_avg[category_avg["Score"] <= 2.5]["Category"].tolist()

if strong:
    st.success(f"강점 영역: {', '.join(strong)}")

if weak:
    st.warning(f"보완 필요 영역: {', '.join(weak)}")

# -----------------------------
# Recommendation Logic
# -----------------------------
st.subheader("🧠 맞춤 추천")

recommendations = {
    "AI 이해·판단": "AI 기본 개념 및 한계 학습 필요",
    "프롬프트 설계": "구조화된 프롬프트 템플릿 연습",
    "업무 적용": "실제 업무에 AI 적용 시도",
    "책임 있는 활용": "윤리 및 데이터 보호 교육 필요",
    "창의·문제해결": "AI 기반 아이디어 생성 연습"
}

for cat in weak:
    st.write(f"- {cat}: {recommendations[cat]}")

# -----------------------------
# User Typing (HRD Insight)
# -----------------------------
st.subheader("👤 활용 유형 분석")

if avg_score >= 4:
    st.success("고성과 AI 활용자 (확산 및 리더 후보)")
elif avg_score >= 3:
    st.info("일반 활용자 (교육 강화 대상)")
else:
    st.warning("기초 역량 강화 필요")

# -----------------------------
# Save Results
# -----------------------------
if st.button("결과 저장"):
    df.to_csv(f"{user_name}_AI_진단결과.csv", index=False)
    st.success("저장 완료")
