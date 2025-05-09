import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from models import Exercise, WorkoutPlan, ProgressTracker

# Inject custom CSS
st.markdown("""
<style>
/* Global styles */
body {
    font-family: 'Arial', sans-serif;
    background-color: #f4f7fa;
    color: #333;
}

/* Main container */
.stApp {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
    background-color: #ffffff;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* Title and headers */
h1 {
    color: #2c3e50;
    text-align: center;
    font-size: 2.5em;
    margin-bottom: 20px;
}
h2 {
    color: #34495e;
    font-size: 1.8em;
    border-bottom: 2px solid #3498db;
    padding-bottom: 5px;
}

/* Sidebar */
.sidebar .sidebar-content {
    background-color: #2c3e65;
    color: #ecf0f1;
    padding: 20px;
    border-radius: 10px;
}
.sidebar .stRadio > div > label {
    color: #ecf0f1;
    font-size: 1.1em;
    padding: 10px;
    border-radius: 5px;
    transition: background-color 0.3s;
}
.sidebar .stRadio > div > label:hover {
    background-color: #34495e;
}

/* Forms */
.stForm {
    background-color: #ecf0f1;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
.stTextInput > div > input,
.stNumberInput > div > input,
.stSelectbox > div > select {
    border: 1px solid #27ae60;
    border-radius: 5px;
    padding: 8px;
    font-size: 1em;
}
.stFormSubmitButton > button {
    background-color: #27ae60;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    font-size: 1em;
    cursor: pointer;
    transition: background-color 0.3s;
}
.stFormSubmitButton > button:hover {
    background-color: #2980b9;
}

/* Tables */
.stDataFrame {
    border: 1px solid #ddd;
    border-radius: 5px;
    overflow: hidden;
}
.stDataFrame table {
    width: 100%;
    border-collapse: collapse;
}
.stDataFrame th, .stDataFrame td {
    padding: 10px;
    text-align: left;
    border-bottom: 1px solid #ddd;
}
.stDataFrame tr:hover {
    background-color: #f1f3f5;
}

/* Buttons */
.stButton > button {
    background-color: #e74c3c;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    font-size: 1em;
    cursor: pointer;
    transition: background-color 0.3s;
}
.stButton > button:hover {
    background-color: #c0392b;
}

/* Plotly charts */
.plotly-graph-div {
    border: 1px solid #ddd;
    border-radius: 5px;
    padding: 10px;
    background-color: #fff;
}

/* Responsive design */
@media (max-width: 768px) {
    .stApp {
        padding: 10px;
    }
    h1 {
        font-size: 2em;
    }
    h2 {
        font-size: 1.5em;
    }
    .stForm {
        padding: 10px;
    }
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "plan" not in st.session_state:
    st.session_state.plan = WorkoutPlan(user="User")
if "tracker" not in st.session_state:
    st.session_state.tracker = ProgressTracker(user="User")

# Streamlit App
st.title("Custom Workout Planner & Progress Tracker")

# Sidebar for navigation
st.sidebar.title("Menu")
page = st.sidebar.radio("Select Page", ["Create Exercise", "View Plan", "Log Session", "Track Progress"])

# Page 1: Create Exercise
if page == "Create Exercise":
    st.header("Add New Exercise")
    with st.form("exercise_form"):
        name = st.text_input("Exercise Name", placeholder="e.g., Bench Press")
        muscle_group = st.selectbox("Muscle Group", ["Chest", "Back", "Legs", "Arms", "Core"])
        reps = st.number_input("Reps", min_value=1, step=1, value=10)
        sets = st.number_input("Sets", min_value=1, step=1, value=3)
        difficulty = st.selectbox("Difficulty", ["Easy", "Moderate", "Hard"])
        submit = st.form_submit_button("Add Exercise")

    if submit:
        try:
            exercise = Exercise(name, muscle_group, reps, sets, difficulty)
            st.session_state.plan.add_exercise(exercise)
            st.success(f"Added {name} to your workout plan!")
        except ValueError as e:
            st.error(str(e))

# Page 2: View Plan
elif page == "View Plan":
    st.header("Your Workout Plan")
    df = st.session_state.plan.get_plan_df()
    if not df.empty:
        st.dataframe(df)
        st.subheader("Schedule by Muscle Group")
        schedule = st.session_state.plan.generate_schedule()
        for muscle_group, exercises in schedule.items():
            st.write(f"**{muscle_group}**")
            st.table(exercises)
    else:
        st.info("No exercises added yet. Go to 'Create Exercise' to start.")

# Page 3: Log Session
elif page == "Log Session":
    st.header("Log Workout Session")
    with st.form("session_form"):
        exercise_name = st.text_input("Exercise Name")
        weight = st.number_input("Weight (lbs)", min_value=0.0, step=0.1)
        reps_completed = st.number_input("Reps Completed", min_value=0, step=1)
        date = st.date_input("Date", value=datetime.now())
        submit = st.form_submit_button("Log Session")

    if submit:
        st.session_state.tracker.log_session(exercise_name, weight, reps_completed, date)
        st.success(f"Logged session for {exercise_name}!")

# Page 4: Track Progress
elif page == "Track Progress":
    st.header("Progress Tracker")
    df = st.session_state.tracker.get_progress_df()
    if not df.empty:
        st.dataframe(df)
        # Plot progress for selected exercise
        exercise = st.selectbox("Select Exercise for Visualization", df["Exercise"].unique())
        exercise_data = df[df["Exercise"] == exercise]
        fig = px.line(exercise_data, x="Date", y="Weight", title=f"Weight Progress for {exercise}",
                      markers=True)
        st.plotly_chart(fig)
        # Show suggestion
        suggestion = st.session_state.tracker.suggest_adjustments(exercise)
        st.write("**Suggestion**: ", suggestion)
    else:
        st.info("No sessions logged yet. Go to 'Log Session' to start.")