import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="AI Skill Dashboard", layout="wide")

# -----------------------------
# Sample Skill Framework
# -----------------------------
skills = [
    "Prompt Engineering",
    "Data Analysis",
    "Automation",
    "AI Ethics",
    "Model Understanding",
    "Tool Usage",
    "Problem Solving",
    "Collaboration with AI"
]

# -----------------------------
# Sidebar - User Input
# -----------------------------
st.sidebar.header("AI Skill Self Assessment")
user_name = st.sidebar.text_input("Your Name", "User")

scores = {}
for skill in skills:
    scores[skill] = st.sidebar.slider(skill, 1, 5, 3)

# -----------------------------
# Data Processing
# -----------------------------
df = pd.DataFrame(list(scores.items()), columns=["Skill", "Score"])
avg_score = df["Score"].mean()

# -----------------------------
# Main Dashboard
# -----------------------------
st.title(f"🤖 {user_name}'s AI Skill Dashboard")

col1, col2 = st.columns(2)

# -----------------------------
# Radar Chart
# -----------------------------
with col1:
    st.subheader("Skill Radar")
    angles = np.linspace(0, 2*np.pi, len(skills), endpoint=False).tolist()
    values = df["Score"].tolist()

    angles += angles[:1]
    values += values[:1]

    fig, ax = plt.subplots(figsize=(5,5), subplot_kw=dict(polar=True))
    ax.plot(angles, values)
    ax.fill(angles, values, alpha=0.1)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(skills)
    ax.set_yticks([1,2,3,4,5])

    st.pyplot(fig)

# -----------------------------
# Bar Chart
# -----------------------------
with col2:
    st.subheader("Skill Breakdown")
    fig2, ax2 = plt.subplots()
    ax2.barh(df["Skill"], df["Score"])
    st.pyplot(fig2)

# -----------------------------
# Insight Section
# -----------------------------
st.subheader("📊 Insights")

strong_skills = df[df["Score"] >= 4]["Skill"].tolist()
weak_skills = df[df["Score"] <= 2]["Skill"].tolist()

st.write(f"Average Score: {avg_score:.2f}")

if strong_skills:
    st.success(f"Strong Skills: {', '.join(strong_skills)}")

if weak_skills:
    st.warning(f"Needs Improvement: {', '.join(weak_skills)}")

#
