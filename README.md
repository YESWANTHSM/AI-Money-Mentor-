# 💰 AI Money Mentor

🚀 Predict • Plan • Achieve Your Financial Goals

AI Money Mentor is an intelligent financial planning system that helps users analyze their income, expenses, and goals to generate personalized financial advice using AI.

---

## 🧠 Problem Statement

Many individuals struggle with:
- Poor financial planning
- Lack of savings discipline
- No clear roadmap to achieve financial goals

Existing solutions are either too complex or not personalized.

---

## 💡 Solution

AI Money Mentor provides:
- 📊 Financial analysis (income, expenses, savings)
- 🎯 Goal prediction (time required to achieve goal)
- 🤖 AI-powered financial advice
- ⚡ Actionable recommendations
- 🛡️ Fallback system when AI is unavailable

---

## ✨ Key Features

- 💰 Monthly savings calculation
- ⏱️ Goal time prediction (auto-calculated)
- 📈 Financial score (0–100)
- 📊 Visual charts for better understanding
- 🤖 AI-generated Plan, Insights, Actions
- 🛡️ Smart fallback system (works without API)
- 💡 Extra savings prediction

---

## 🏗️ Architecture (Multi-Agent System)

The system uses multiple agents:

- Input Agent → Collects user data  
- Analysis Agent → Calculates savings & score  
- Goal Prediction Engine → Estimates time to reach goal  
- Planning Agent → Generates financial plan  
- Insight Agent → Analyzes financial condition  
- Action Agent → Suggests steps  
- Fallback Agent → Ensures reliability when AI fails  

---

## 🔄 Workflow

User Input → Analysis → Goal Prediction → AI Advice → Fallback (if needed) → Output

---

## 🛠️ Tech Stack

- **Python**
- **Streamlit** (UI)
- **OpenAI API** (AI responses)
- **Matplotlib** (charts)
- **dotenv** (API key management)

---

## ⚙️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/your-username/ai-money-mentor.git
cd ai-money-mentor
