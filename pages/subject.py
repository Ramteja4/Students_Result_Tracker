import pandas as pd
import dash
from dash import dcc, html, callback
from dash.dependencies import Input, Output

# Register the page
dash.register_page(__name__, path='/subject', name="𝓢𝓾𝓫𝓳𝓮𝓬𝓽 📚")

####################### DATASET #############################
# Load the dataset
try:
    student_marks_df = pd.read_csv("student_marks.csv")
except FileNotFoundError:
    raise Exception("The file 'student_marks.csv' was not found.")

####################### ANALYZE FAILURES #########################
# Threshold for passing marks
pass_marks = 14

# Identify failed subjects for each student
failed_students = student_marks_df.melt(id_vars=["Rollno"], 
                                        value_vars=["Maths","Physics","Chemistry","English","Biology","Economics","History","Civics"],
                                        var_name="Subject", 
                                        value_name="Score")
failed_students = failed_students[failed_students["Score"] < pass_marks]

####################### WIDGETS #############################
# Define the dropdown options
subjects = ["Maths","Physics","Chemistry","English","Biology","Economics","History","Civics"]
subject_dropdown = dcc.Dropdown(id="subject", options=[{'label': subject, 'value': subject} for subject in subjects], value=subjects[0], clearable=False)

####################### PAGE LAYOUT #############################
# Define the layout of the page
layout = html.Div(children=[
    html.Br(),
    html.Label("Select Subject"), subject_dropdown,
    html.Div(id="failed_students")
])

####################### CALLBACKS ###############################
# Define the callback to update the list of failed students
@callback(Output("failed_students", "children"), 
          Input("subject", "value"))
def update_failed_students(selected_subject):
    filtered_students = failed_students[failed_students["Subject"] == selected_subject]
    if filtered_students.empty:
        return html.P(f"No students failed in {selected_subject}.")
    else:
        rows = []
        for _, row in filtered_students.iterrows():
            rows.append(html.P(f"Roll No: {row['Rollno']}, Marks: {row['Score']}"))
        return rows
