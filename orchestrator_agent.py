from datetime import datetime

class OrchestratorAgent:
    def start(self, assessor, nutrition, exercise, motivation):
        """Link all agents together when orchestrator starts"""
        self.assessor = assessor
        self.nutrition = nutrition
        self.exercise = exercise
        self.motivation = motivation
        self.data = {}

    def buildplan(self, userid, profile):
        """Build a complete personalized fitness plan"""
        try:
            # Extract user details
            name = profile.get("name", "User")
            age = profile.get("age", 0)
            weight = profile.get("weight", 0)
            height = profile.get("height", 0)
            goal = profile.get("goal", "general fitness")
            days = profile.get("days", 5)
            equipment = profile.get("equipment", "bodyweight only")

            # 🧠 1️⃣ ASSESSMENT
            try:
                assessment = self.assessor.assess_user(name, age, weight, height, goal)
            except Exception as e:
                print("[Orchestrator] Assessment failed:", e)
                assessment = f"⚠️ Assessment unavailable: {e}"

            # 🥗 2️⃣ NUTRITION PLAN
            try:
                nutrition = self.nutrition.make_meal_plan(name, age, weight, height, goal)
            except Exception as e:
                print("[Orchestrator] Nutrition failed:", e)
                nutrition = f"⚠️ Nutrition unavailable: {e}"

            # 💪 3️⃣ EXERCISE PLAN
            try:
                exercise = self.exercise.makeplan(userid, name, age, weight, height, goal, days, equipment)
            except Exception as e:
                print("[Orchestrator] Exercise failed:", e)
                exercise = f"⚠️ Exercise unavailable: {e}"

            # 💬 4️⃣ MOTIVATION MESSAGE
            try:
                motivation = self.motivation.give_motivation(name, goal)
            except Exception as e:
                print("[Orchestrator] Motivation failed:", e)
                motivation = f"⚠️ Motivation unavailable: {e}"

            # 🕒 TIMESTAMP
            when = datetime.now().strftime("%d/%m/%Y %H:%M")

            # 📦 COMBINE EVERYTHING
            plan = {
                "when": when,
                "assessment": assessment,
                "nutrition": nutrition,
                "exercise": exercise,
                "motivation": motivation
            }

            # 🧾 SAVE USER HISTORY
            self.data.setdefault(userid, []).append(plan)
            return plan

        except Exception as e:
            print("[Orchestrator] Unexpected error:", e)
            return {"error": f"Unexpected error: {e}"}

    def gethistory(self, userid):
        """Return previous plans for a user"""
        return self.data.get(userid, [])
