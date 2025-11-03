# streamlit_app.py
import streamlit as st
import threading
import time

from assessment_agent import AssessmentAgent
from nutrition_agent import NutritionAgent
from exercise_agent import ExerciseAgent
from motivation_agent import MotivationAgent
from orchestrator_agent import OrchestratorAgent

# ---------------------- PAGE CONFIG ----------------------
st.set_page_config(page_title="🏋️‍♀️ Fitness Helper", page_icon="💪", layout="wide")

# ---------------------- STYLES ----------------------
st.markdown("""
    <style>
    body { background-color: #0b0c10; color: #f8f9fa; }
    .main-title { text-align:center; color:#ff7b00; font-size:48px; font-weight:bold; margin-top:-30px; }
    .sub-title { text-align:center; font-size:18px; color:#ccc; margin-bottom:40px; }
    .day-card { background-color:#1f2833; padding:20px; border-radius:15px; margin-bottom:15px; box-shadow:0 4px 12px rgba(255,123,0,0.2); }
    .section-title { color:#ff7b00; font-size:22px; font-weight:bold; margin-top:20px; margin-bottom:10px; }
    .plan-text { color:#e5e5e5; line-height:1.6; white-space: pre-wrap; }
    </style>
""", unsafe_allow_html=True)

# ---------------------- HEADER ----------------------
st.markdown("<div class='main-title'>🏋️‍♂️ Fitness Helper</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Your AI-powered multi-agent fitness planner 💡</div>", unsafe_allow_html=True)

# ---------------------- INPUT FORM ----------------------
with st.form("fitness_form"):
    name = st.text_input("👤 Name", placeholder="Enter your name")
    age = st.number_input("🎂 Age", min_value=10, max_value=100, value=21)
    weight = st.number_input("⚖️ Weight (kg)", min_value=20, max_value=250, value=60)
    height = st.number_input("📏 Height (cm)", min_value=100, max_value=240, value=165)
    goal = st.selectbox("🎯 Fitness Goal", ["lose weight", "gain muscle", "get fit"])
    days = st.slider("📅 Workout Days per Week", 1, 7, 6)
    equipment = st.text_input("🏋️‍♀️ Equipment Available", placeholder="e.g., dumbbells, yoga mat, none")
    submitted = st.form_submit_button("🚀 Generate My Plan")

# ---------------------- AGENT INIT ----------------------
agents = {
    'assessment': AssessmentAgent(),
    'nutrition': NutritionAgent(),
    'exercise': ExerciseAgent(),
    'motivation': MotivationAgent(),
    'orchestrator': OrchestratorAgent()
}

# Start agents that have start()
if hasattr(agents['assessment'], 'start'):
    agents['assessment'].start()
if hasattr(agents['nutrition'], 'start'):
    agents['nutrition'].start()
if hasattr(agents['exercise'], 'start'):
    agents['exercise'].start()
if hasattr(agents['motivation'], 'start'):
    agents['motivation'].start()

# Start orchestrator with required agents
if hasattr(agents['orchestrator'], 'start'):
    agents['orchestrator'].start(
        agents['assessment'], agents['nutrition'], agents['exercise'], agents['motivation']
    )

# ---------------------- HELPERS ----------------------
def safe_assess(agent, user_info):
    try:
        # use assess(user_info) as per your agent implementation
        return agent.assess(user_info)
    except Exception as e:
        return {"plan": f"⚠️ Assessment unavailable: {e}"}

def safe_nutrition(agent, name, age, weight, height, goal):
    try:
        return agent.make_meal_plan(name, age, weight, height, goal)
    except Exception as e:
        return f"⚠️ Nutrition unavailable: {e}"

def safe_exercise(agent, userid, name, age, weight, height, goal, days, equipment):
    try:
        return agent.makeplan(userid, name, age, weight, height, goal, days, equipment)
    except Exception as e:
        return f"⚠️ Exercise unavailable: {e}"

def safe_motivation(agent, user_info):
    try:
        # many versions used give_boost(user_info)
        if hasattr(agent, "give_boost"):
            return agent.give_boost(user_info)
        # fallback to motivate_user if that's the method name
        if hasattr(agent, "motivate_user"):
            return agent.motivate_user(user_info.get("name", ""), user_info.get("goal", ""))
        return "⚠️ Motivation agent method not found."
    except Exception as e:
        return f"⚠️ Motivation unavailable: {e}"

# ---------------------- MAIN LOGIC ----------------------
if submitted:
    if not name.strip():
        st.warning("⚠️ Please enter your name first.")
    else:
        with st.spinner("💡 Generating your personalized AI fitness plan..."):
            userid = name.lower().replace(" ", "_")

            # BMI and context
            bmi = round(weight / ((height / 100) ** 2), 1)
            if bmi < 18.5:
                bmi_status = "Underweight"; color = "#3b82f6"
                health_tip = "Focus on gaining healthy weight with high-protein, calorie-dense foods."
                fitness_focus = "strength training and muscle gain"
            elif 18.5 <= bmi < 24.9:
                bmi_status = "Normal"; color = "#10b981"
                health_tip = "Maintain your balance with a mix of cardio and strength workouts."
                fitness_focus = "balanced fitness"
            elif 25 <= bmi < 29.9:
                bmi_status = "Overweight"; color = "#f59e0b"
                health_tip = "Include more cardio and reduce sugar intake to shed fat."
                fitness_focus = "fat loss and endurance"
            else:
                bmi_status = "Obese"; color = "#ef4444"
                health_tip = "Prioritize low-impact workouts and a calorie-controlled diet."
                fitness_focus = "gradual weight loss"

            # banner
            st.markdown(f"""
                <div style="
                    background-color:{color};
                    color:white;
                    padding:16px;
                    border-radius:12px;
                    text-align:center;
                    margin-top:12px;
                    box-shadow:0px 0px 12px rgba(255,255,255,0.04);
                ">
                    <strong>📊 {name}'s Summary</strong><br>
                    BMI: {bmi} ({bmi_status}) — {health_tip}
                </div>
            """, unsafe_allow_html=True)

            # build user_info dict for agents that expect dict
            user_info = {
                "name": name, "age": age, "weight": weight, "height": height,
                "goal": goal, "bmi": bmi, "bmi_status": bmi_status,
                "days": days, "equipment": equipment
            }

            # run agents (sequentially or multithreaded — we'll use threads for speed)
            results = {}

            def run_assess():
                results['assess'] = safe_assess(agents['assessment'], user_info)

            def run_nutri():
                results['nutri'] = safe_nutrition(agents['nutrition'], name, age, weight, height, f"{goal} ({bmi_status})")

            def run_exer():
                results['exer'] = safe_exercise(agents['exercise'], userid, name, age, weight, height,
                                                f"{goal} for {fitness_focus}", days, equipment)

            def run_motiv():
                results['motiv'] = safe_motivation(agents['motivation'], user_info)

            threads = [
                threading.Thread(target=run_assess, daemon=True),
                threading.Thread(target=run_nutri, daemon=True),
                threading.Thread(target=run_exer, daemon=True),
                threading.Thread(target=run_motiv, daemon=True)
            ]
            for t in threads: t.start()

            # small animated progress
            prog = st.progress(0)
            for i in range(10):
                time.sleep(0.08)
                prog.progress((i + 1) * 10)

            for t in threads: t.join()

            # let orchestrator build final plan if available (safe)
            try:
                results['final'] = agents['orchestrator'].buildplan(name, user_info)
            except Exception:
                results['final'] = {"error": "Orchestrator unavailable or buildplan failed."}

        st.success(f"🎉 Personalized dashboard generated for {name} 💪")

        # ---------------------- DISPLAY RESULTS ----------------------
        st.markdown("<div class='section-title'>📋 Assessment</div>", unsafe_allow_html=True)
        # assessment may be dict with 'plan' or string
        assess_text = results.get('assess', {})
        if isinstance(assess_text, dict):
            text = assess_text.get('plan', str(assess_text))
        else:
            text = str(assess_text)
        st.markdown(f"<div class='plan-text'>{text}</div>", unsafe_allow_html=True)

        st.markdown("<div class='section-title'>🥗 Nutrition Plan</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='plan-text'>{results.get('nutri', '⚠️ No nutrition plan available.')}</div>", unsafe_allow_html=True)

        st.markdown("<div class='section-title'>💪 Workout Plan</div>", unsafe_allow_html=True)
        exer_text = results.get('exer', '⚠️ No workout plan available.')
        # If exercise comes as single string with "Day" markers, split into cards
        if isinstance(exer_text, str) and "Day" in exer_text:
            parts = exer_text.split("Day")
            for idx, part in enumerate(parts):
                if idx == 0:
                    intro = part.strip()
                    if intro:
                        st.markdown(f"<div class='plan-text'>{intro}</div>", unsafe_allow_html=True)
                    continue
                day_content = part.strip()
                st.markdown(f"<div class='day-card'><b>📆 Day {idx}</b><br><div class='plan-text'>Day {day_content}</div></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='plan-text'>{exer_text}</div>", unsafe_allow_html=True)

        st.markdown("<div class='section-title'>💬 Motivation</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='plan-text'>{results.get('motiv', '⚠️ No motivation available.')}</div>", unsafe_allow_html=True)
