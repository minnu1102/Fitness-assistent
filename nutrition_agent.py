import google.generativeai as genai
import os, threading, time
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class NutritionAgent:
    def __init__(self):
        self.name = "Nutrition Agent"
        self.data = {}
        self.running = False
        self.thread = None

    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self.run, daemon=True)
            self.thread.start()

    def run(self):
        while self.running:
            time.sleep(0.1)

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()

    def make_meal_plan(self, name, age, weight, height, goal):
        prompt = (
            f"Create a personalized 1-day healthy meal plan for {name}, "
            f"age {age}, weight {weight} kg, height {height} cm. "
            f"Goal: {goal}. Include breakfast, lunch, dinner, and snacks. "
            "Add emojis and keep it simple and realistic."
        )
        try:
            model = genai.GenerativeModel("models/gemini-2.5-flash")
            response = model.generate_content(prompt)
            plan = response.text.strip()
        except Exception as e:
            print("[NutritionAgent] Fallback:", e)
            plan = (
                "🥣 Breakfast: Oats with banana\n"
                "🥗 Lunch: Brown rice & grilled chicken\n"
                "🍲 Dinner: Fish with veggies\n"
                "🍎 Snack: Nuts / yogurt"
            )

        now = datetime.now().strftime("%d/%m/%Y %H:%M")
        record = {"time": now, "plan": plan}
        self.data.setdefault(name, []).append(record)
        return plan
