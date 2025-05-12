
import pandas as pd

class Exercise:
    def __init__(self, name, muscle_group, reps, sets, difficulty="Moderate"):
        self.name = name
        self.muscle_group = muscle_group
        self.reps = reps
        self.sets = sets
        self.difficulty = difficulty

    def get_details(self):
        return {
            "Name": self.name,
            "Muscle Group": self.muscle_group,
            "Reps": self.reps,
            "Sets": self.sets,
            "Difficulty": self.difficulty
        }

    def validate_exercise(self):
        if self.reps <= 0 or self.sets <= 0:
            raise ValueError("Reps and sets must be positive.")
        return True

class WorkoutPlan:
    def __init__(self, user, goal="General Fitness"):
        self.user = user
        self.goal = goal
        self.exercises = []

    def add_exercise(self, exercise):
        if exercise.validate_exercise():
            self.exercises.append(exercise)

    def get_plan_df(self):
        return pd.DataFrame([e.get_details() for e in self.exercises])

    def generate_schedule(self):
        # Simplified: Group exercises by muscle group
        schedule = {}
        for exercise in self.exercises:
            mg = exercise.muscle_group
            if mg not in schedule:
                schedule[mg] = []
            schedule[mg].append(exercise.get_details())
        return schedule

class ProgressTracker:
    def __init__(self, user):
        self.user = user
        self.sessions = []  # List of session dictionaries

    def log_session(self, exercise_name, weight, reps_completed, date):
        session = {
            "Exercise": exercise_name,
            "Weight": weight,
            "Reps Completed": reps_completed,
            "Date": date
        }
        self.sessions.append(session)

    def get_progress_df(self):
        return pd.DataFrame(self.sessions)

    def suggest_adjustments(self, exercise_name):
        df = self.get_progress_df()
        if exercise_name in df["Exercise"].values:
            exercise_data = df[df["Exercise"] == exercise_name]
            avg_reps = exercise_data["Reps Completed"].mean()
            avg_weight = exercise_data["Weight"].mean()
            if avg_reps > 12:  # Simple rule-based suggestion
                return f"Increase weight for {exercise_name} by 5-10% (current avg: {avg_weight:.1f} lbs)."
            elif avg_reps < 8:
                return f"Decrease weight for {exercise_name} by 5-10% (current avg: {avg_weight:.1f} lbs)."
        return f"Maintain current weight for {exercise_name}."
