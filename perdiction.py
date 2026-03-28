import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import math  # ✅ for correct rounding

# LOAD API KEY
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# PAGE CONFIG
st.set_page_config(page_title="AI Money Mentor", page_icon="💰", layout="wide")

# UI STYLE
st.markdown("""
<style>
body { background-color: #0E1117; }
h1, h2, h3 { color: #00FFAA; }

.stButton>button {
    background-color: #00FFAA;
    color: black;
    border-radius: 10px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# SIDEBAR
st.sidebar.title("💰 AI Money Mentor")
st.sidebar.info("Smart Financial Planner")

# TITLE
st.title("💰 AI Money Mentor")
st.caption("🚀 Predict • Plan • Achieve Your Goals")

st.markdown("---")

# INPUT
col1, col2 = st.columns(2)

with col1:
    income = st.number_input("💵 Monthly Income (₹)", min_value=0)
    goal = st.text_input("🎯 Financial Goal")
    goal_price = st.number_input("💰 Goal Amount (₹)", min_value=0)

with col2:
    expenses = st.number_input("💸 Monthly Expenses (₹)", min_value=0)
    risk = st.selectbox("⚖️ Risk Level", ["Low", "Medium", "High"])

# SCORE FUNCTION
def calculate_score(income, expenses):
    if income == 0:
        return 0
    savings = income - expenses
    ratio = savings / income

    score = 50
    if ratio > 0.3:
        score += 30
    elif ratio > 0.1:
        score += 15
    else:
        score -= 10

    if expenses > income:
        score -= 20

    return max(0, min(100, score))

# AI + FALLBACK
def get_ai_response(prompt):
    try:
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a financial advisor."},
                {"role": "user", "content": prompt}
            ]
        )
        return {"type": "ai", "content": res.choices[0].message.content}

    except:
        if "plan" in prompt.lower():
            return {
                "type": "fallback",
                "title": "📊 Plan",
                "points": [
                    "Follow 50-30-20 rule",
                    f"Save ₹{int(income*0.2)} monthly",
                    "Invest in SIP"
                ]
            }
        elif "analyze" in prompt.lower():
            return {
                "type": "fallback",
                "title": "🧠 Insights",
                "points": [
                    f"Expenses ₹{expenses} can be reduced",
                    "Savings need improvement",
                    "Plan is moderate risk"
                ]
            }
        else:
            return {
                "type": "fallback",
                "title": "⚡ Actions",
                "points": [
                    f"Save ₹{int(income*0.3)} monthly",
                    "Reduce expenses 10–15%",
                    f"Emergency fund ₹{expenses*3}"
                ]
            }

# DISPLAY FUNCTION
def display_response(res):
    if res["type"] == "ai":
        st.success("🤖 AI Generated Advice")
        st.write(res["content"])
    else:
        st.warning("⚠️ Smart Fallback Mode")
        st.markdown(f"### {res['title']}")
        for p in res["points"]:
            st.markdown(f"- {p}")

# BUTTON ACTION
if st.button("🚀 Analyze My Finances"):

    if income == 0 or expenses == 0 or goal == "" or goal_price == 0:
        st.warning("Please fill all fields")
    else:
        savings = income - expenses
        score = calculate_score(income, expenses)

        # SUMMARY
        c1, c2, c3 = st.columns(3)
        c1.metric("💰 Income", f"₹{income}")
        c2.metric("💸 Expenses", f"₹{expenses}")
        c3.metric("💵 Savings", f"₹{savings}")

        # SCORE
        st.subheader("💯 Financial Score")
        st.progress(score / 100)
        st.write(f"{score}/100")

        # GRAPH
        st.subheader("📊 Financial Breakdown")
        fig, ax = plt.subplots(figsize=(4,3))
        ax.bar(["Income", "Expenses", "Savings"], [income, expenses, savings])
        st.pyplot(fig)

        # 🎯 GOAL PREDICTION (FIXED LOGIC)
        st.subheader("🎯 Goal Prediction")

        if savings <= 0:
            st.error("❌ No savings available to achieve goal")
            months_needed = 0
        else:
            estimated_months = goal_price / savings
            months_needed = math.ceil(estimated_months)  # ✅ FIXED

            st.write(f"💰 Monthly Savings: ₹{savings}")
            st.write(f"⏱️ Estimated Time: {months_needed} months")

            # ✅ EXTRA MONEY LOGIC
            if months_needed * savings > goal_price:
                extra = months_needed * savings - goal_price
                st.info(f"💡 You will have ₹{extra} extra after reaching your goal")

            # STATUS
            if months_needed <= 6:
                st.success("🚀 Fast achievement possible")
            elif months_needed <= 12:
                st.warning("⚠️ Moderate timeline")
            else:
                st.error("❗ Slow — improve savings or invest")

        # AI PROFILE
        profile = f"""
Income: {income}
Expenses: {expenses}
Goal: {goal}
Goal Amount: {goal_price}
Savings: {savings}
Time Required: {months_needed} months
Risk: {risk}
"""

        # AI CALLS
        plan = get_ai_response(f"Create financial plan for {profile}")
        insights = get_ai_response(f"Analyze financial condition: {profile}")
        actions = get_ai_response(f"Suggest actions to reach goal faster: {profile}")

        # TABS
        t1, t2, t3 = st.tabs(["📊 Plan", "🧠 Insights", "⚡ Actions"])

        with t1:
            display_response(plan)

        with t2:
            display_response(insights)

        with t3:
            display_response(actions)

        # DOWNLOAD
        report = f"""
Income: ₹{income}
Expenses: ₹{expenses}
Savings: ₹{savings}
Goal: ₹{goal_price}
Time Required: {months_needed} months

PLAN:
{plan}

INSIGHTS:
{insights}

ACTIONS:
{actions}
"""
        st.download_button("📄 Download Report", report)
