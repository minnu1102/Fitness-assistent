import google.generativeai as genai
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment and configure Gemini
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class AssessmentAgent:
    def __init__(self):
        self.name = "Assessment Agent"
        self.data = {}

    def start(self):
        print(f"[{self.name}] Ready to assess users!")

    def assess(self, profile):
        """
        Assess user based on their age, weight, height, and goal.
        Returns a brief fitness summary and recommended focus area.
        """
        try:
            name = profile.get("name", "User")
            age = profile.get("age", 0)
            weight = profile.get("weight", 0)
            height = profile.get("height", 0)
            goal = profile.get("goal", "general fitness")

            prompt = (
                f"You are a fitness coach. Assess {name}, age {age}, weight {weight} kg, height {height} cm. "
                f"Their goal is {goal}. "
                "Give a short summary with recommended exercise intensity, diet focus, and weekly routine tips. "
                "Keep it conversational and encouraging."
            )

            response = genai.GenerativeModel("gemini-2.5-flash").generate_content(prompt)
            assessment_text = response.text.strip()

        except Exception as e:
            print("[AssessmentAgent] Fallback:", e)
            assessment_text = f"Hi {name}, based on your info, try light to moderate workouts and eat balanced meals 🥗💪"

        # Record assessment
        now = datetime.now().strftime("%d/%m/%Y %H:%M")
        record = {"time": now, "assessment": assessment_text}
        self.data.setdefault(name, []).append(record)

        return assessment_text
