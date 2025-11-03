from orchestrator_agent import OrchestratorAgent
from assessment_agent import AssessmentAgent
from nutrition_agent import NutritionAgent
from exercise_agent import ExerciseAgent
from motivation_agent import MotivationAgent

# Create agents (Gemini models don’t need start/stop threads for most)
assessor = AssessmentAgent()
nutrition = NutritionAgent()
exercise = ExerciseAgent()
motivation = MotivationAgent()

# Orchestrator (connects all agents)
orchestrator = OrchestratorAgent()
orchestrator.start(assessor, nutrition, exercise, motivation)

# 🧍‍♀️ Example user profile
profile = {
    "name": "Poorna",
    "age": 21,
    "weight": 74,
    "height": 165,
    "goal": "gain muscle",
    "days": 5,
    "equipment": "basic dumbbells"
}

# Generate full plan
plan = orchestrator.buildplan("user123", profile)

# 🖨️ Display result
print("\n📋 Assessment:")
print(plan["assessment"])

print("\n🥗 Nutrition Plan:")
print(plan["nutrition"])

print("\n💪 Workout Plan:")
print(plan["exercise"])

print("\n💬 Motivation:")
print(plan["motivation"])
