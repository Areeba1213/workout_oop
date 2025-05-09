from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def export_plan_to_pdf(plan, filename="workout_plan.pdf"):
    c = canvas.Canvas(filename, pagesize=letter)
    c.setFont("Helvetica", 12)
    c.drawString(100, 750, f"Workout Plan for {plan.user}")
    c.drawString(100, 730, f"Goal: {plan.goal}")
    y = 700
    for exercise in plan.exercises:
        details = exercise.get_details()
        c.drawString(100, y, f"{details['Name']} ({details['Muscle Group']}): {details['Sets']} sets x {details['Reps']} reps")
        y -= 20
    c.save()
    return filename