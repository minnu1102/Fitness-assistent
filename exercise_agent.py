import google.generativeai as genai
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class ExerciseAgent:
    def __init__(self):
        self.name = "Exercise Agent"
        self.data = {}

    def makeplan(self, userid, name, age, weight, height, goal, days, equipment):
        prompt = (
            f"Create a {days}-day workout plan for {name}, "
            f"age {age}, weight {weight} kg, height {height} cm. "
            f"Goal: {goal}. Equipment available: {equipment}. "
            "Add emojis for each exercise and separate each day clearly."
        )
        try:
            model = genai.GenerativeModel("models/gemini-2.5-flash")
            response = model.generate_content(prompt)
            plan = response.text.strip()
        except Exception as e:
            print("[ExerciseAgent] Fallback:", e)
            plan = (
                "💪 **Workout Plan (Fallback)**\n"
                "📆 Day 1: Push-ups, squats, lunges\n"
                "📆 Day 2: Cardio (20 min walk/run)\n"
                "📆 Day 3: Plank + jumping jacks\n"
                "📆 Day 4: Rest 🧘‍♀️\n"
                "📆 Day 5: Dumbbell curls & crunches\n"
                "📆 Day 6: Cardio & stretching\n"
                "📆 Day 7: Rest and hydration 💧"
            )

        now = datetime.now().strftime("%d/%m/%Y %H:%M")
        record = {"time": now, "plan": plan}
        self.data.setdefault(userid, []).append(record)
        return plan
