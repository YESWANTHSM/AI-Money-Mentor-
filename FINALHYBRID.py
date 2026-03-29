import streamlit as st
import matplotlib.pyplot as plt

# ------------------ OPTIONAL AI SETUP ------------------
try:
    from openai import OpenAI
    client = OpenAI()   # uses env variable if available
    AI_AVAILABLE = True
except:
    AI_AVAILABLE = False

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="AI Money Mentor", layout="wide")

# ------------------ TITLE ------------------
st.markdown("<h1 style='text-align:center;'>💸 AI Money Mentor</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>🚀 Predict • Plan • Achieve Your Financial Goals</p>", unsafe_allow_html=True)

st.markdown("---")

# ------------------ INPUT ------------------
col1, col2 = st.columns(2)

with col1:
    income = st.number_input("💵 Monthly Income (₹)", min_value=0, value=0, step=1000)
    goal = st.text_input("🎯 Financial Goal")
    goal_price = st.number_input("💰 Goal Amount (₹)", min_value=0, value=0, step=1000)

with col2:
    expenses = st.number_input("🧾 Monthly Expenses (₹)", min_value=0, value=0, step=1000)
    risk = st.selectbox("⚖️ Risk Level", ["Low", "Medium", "High"])

# ------------------ AI FUNCTION ------------------
def get_ai_response(prompt, fallback_type):
    if AI_AVAILABLE:
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except:
            pass  # fallback if API fails

    # -------- FALLBACK --------
    if fallback_type == "plan":
        return f"""
✔ Save ₹{int(income * 0.3)} monthly  
✔ Follow 50-30-20 rule  
✔ Start SIP investment  
✔ Build emergency fund  
"""
    elif fallback_type == "insights":
        return f"""
- Savings rate: {int((income-expenses)/income*100)}%  
- Expenses are {(expenses/income)*100:.1f}% of income  
- Financial health is moderate  
"""
    else:
        return """
1. Reduce unnecessary expenses  
2. Increase savings gradually  
3. Invest monthly  
4. Track spending weekly  
"""

# ------------------ BUTTON ------------------
if st.button("🚀 Analyze My Finances"):

    savings = income - expenses

    if savings <= 0:
        st.error("❌ Expenses exceed income!")
    else:
        months_needed = int((goal_price / savings) + 0.99)

        st.markdown("---")

        # METRICS
        col3, col4, col5 = st.columns(3)
        col3.metric("💰 Savings", f"₹{savings}")
        col4.metric("📅 Goal Time", f"{months_needed} months")
        score = int((savings / income) * 100)
        col5.metric("📊 Score", f"{score}/100")

        # EXTRA MONEY
        if months_needed * savings > goal_price:
            extra = months_needed * savings - goal_price
            st.info(f"💡 Extra savings after goal: ₹{extra}")

        st.markdown("---")

        # GRAPH
        st.subheader("📈 Savings Growth")
        months = list(range(1, months_needed + 1))
        growth = [savings * m for m in months]

        fig, ax = plt.subplots(figsize=(5, 3))
        ax.plot(months, growth)
        ax.set_xlabel("Months")
        ax.set_ylabel("Savings (₹)")
        ax.set_title("Savings Over Time")

        st.pyplot(fig)

        st.markdown("---")

        # AI PLAN
        st.subheader("📊 AI Financial Plan")
        plan = get_ai_response("Create financial plan", "plan")
        st.success(plan)

        # AI INSIGHTS
        st.subheader("🧠 Insights")
        insights = get_ai_response("Analyze finances", "insights")
        st.info(insights)

        # AI ACTIONS
        st.subheader("⚡ Action Steps")
        actions = get_ai_response("Give actions", "actions")
        st.warning(actions)

        # STATUS
        if AI_AVAILABLE:
            st.caption("🤖 AI Mode Active")
        else:
            st.caption("⚡ Smart Fallback Mode (No API Required)")
