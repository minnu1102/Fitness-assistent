import google.generativeai as genai
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class MotivationAgent:
    def __init__(self):
        self.name = "Motivation Agent"
        self.data = {}

    def start(self):
        print(f"[{self.name}] Ready to motivate users! 🚀")

    def give_motivation(self, name, goal):
        """
        Generate a motivational message based on the user's goal.
        """
        try:
            prompt = (
                f"You are a fitness motivator. Write a short, uplifting message for {name} "
                f"who is working towards {goal}. Keep it personal, friendly, and inspiring! 💪🔥"
            )

            response = genai.GenerativeModel("gemini-2.5-flash").generate_content(prompt)
            motivation_text = response.text.strip()

        except Exception as e:
            print("[MotivationAgent] Fallback:", e)
            motivation_text = (
                f"Keep pushing, {name}! Every small effort brings you closer to your {goal}! 🌟"
            )

        # Record the motivation entry
        now = datetime.now().strftime("%d/%m/%Y %H:%M")
        record = {"time": now, "motivation": motivation_text}
        self.data.setdefault(name, []).append(record)

        return motivation_text
