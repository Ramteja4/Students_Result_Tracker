import os
import pandas as pd
import dash
from dash import dcc, html, callback
from dash.dependencies import Input, Output

# Register the page
dash.register_page(__name__, path='/subject', name="𝓢𝓾𝓫𝓳𝓮𝓬𝓽 📚")

####################### LOAD DATASET #############################
# Compute absolute path to CSV (project root)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
csv_path = os.path.join(BASE_DIR, "student_marks.csv")

# Load the dataset safely
try:
    student_marks_df = pd.read_csv(csv_path)
except FileNotFoundError:
    raise Exception(f"The file 'student_marks.csv' was not found at {csv_path}. "
                    "Make sure it is included in your repository.")

####################### ANALYZE FAILURES #########################
pass_marks = 14

# Identify failed subjects for each student
failed_students = student_marks_df.melt(
    id_vars=["Rollno"], 
    value_vars=["Maths","Physics","Chemistry","English","Biology","Economics","History","Civics"],
    var_name="Subject", 
    value_name="Score"
)
failed_students = failed_students[failed_students["Score"] < pass_marks]

####################### WIDGETS #############################
subjects = ["Maths","Physics","Chemistry","English","Biology","Economics","History","Civics"]
subject_dropdown = dcc.Dropdown(
    id="subject", 
    options=[{'label': subject, 'value': subject} for subject in subjects], 
    value=subjects[0], 
    clearable=False
)

####################### PAGE LAYOUT #############################
layout = html.Div(children=[
    html.Br(),
    html.Label("Select Subject"), subject_dropdown,
    html.Div(id="failed_students")
])

####################### CALLBACKS ###############################
@callback(
    Output("failed_students", "children"), 
    Input("subject", "value")
)
def update_failed_students(selected_subject):
    filtered_students = failed_students[failed_students["Subject"] == selected_subject]
    if filtered_students.empty:
        return html.P(f"No students failed in {selected_subject}.")
    else:
        rows = [html.P(f"Roll No: {row['Rollno']}, Marks: {row['Score']}") for _, row in filtered_students.iterrows()]
        return rows
