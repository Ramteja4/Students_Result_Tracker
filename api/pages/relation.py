import os
import pandas as pd
import dash
from dash import dcc, html, callback
import plotly.express as px
from dash.dependencies import Input, Output

# Register the page
dash.register_page(__name__, path='/relation', name="𝓒𝓸𝓶𝓹𝓪𝓻𝓲𝓼𝓸𝓷 ⚔️")

####################### LOAD DATASET #############################
# Compute the absolute path to the CSV (project root)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
csv_path = os.path.join(BASE_DIR, "student_marks.csv")

# Load CSV safely
try:
    student_marks_df = pd.read_csv(csv_path)
except FileNotFoundError:
    raise Exception(f"The file 'student_marks.csv' was not found at {csv_path}. "
                    f"Make sure it is included in your repository and deployed.")

####################### BARPLOT FUNCTION ################
def create_barplot(rollno, subject1="Maths", subject2="Physics"):
    """Creates a bar plot comparing scores in two subjects for a given roll number."""
    try:
        student_data = student_marks_df[student_marks_df["Rollno"] == rollno]
        if student_data.empty:
            # Return empty figure with message instead of crashing
            fig = px.bar(title=f"No data found for Rollno {rollno}")
            return fig

        data = {
            "Subject": [subject1, subject2],
            "Mean Score": [student_data.get(subject1, pd.Series([None]))[0],
                           student_data.get(subject2, pd.Series([None]))[0]]
        }
        df = pd.DataFrame(data)

        barplot = px.bar(
            data_frame=df, 
            x="Subject", 
            y="Mean Score", 
            title=f"Comparison of {subject1} and {subject2} Scores for Rollno {rollno}", 
            height=600
        )

        # Add a green line for pass marks (14)
        pass_mark = 14
        barplot.add_shape(
            type="line",
            x0=-0.5,  # Start at first subject
            y0=pass_mark,
            x1=1.5,   # End at second subject
            y1=pass_mark,
            line=dict(color="Green", width=2, dash="dash")
        )

        return barplot

    except KeyError as e:
        fig = px.bar(title=f"One of the subjects {subject1} or {subject2} does not exist in the dataset.")
        return fig

####################### WIDGETS #############################
columns = ["Maths","Physics","Chemistry","English","Biology","Economics","History","Civics"]
rollnos = student_marks_df["Rollno"].unique() if not student_marks_df.empty else []

rollno_dropdown = dcc.Dropdown(
    id="rollno", 
    options=[{'label': str(rollno), 'value': rollno} for rollno in rollnos], 
    value=rollnos[0] if len(rollnos) > 0 else None, 
    clearable=False
)
subject1_dropdown = dcc.Dropdown(
    id="subject1", 
    options=[{'label': col, 'value': col} for col in columns], 
    value="Maths", 
    clearable=False
)
subject2_dropdown = dcc.Dropdown(
    id="subject2", 
    options=[{'label': col, 'value': col} for col in columns], 
    value="Chemistry", 
    clearable=False
)

####################### PAGE LAYOUT #############################
layout = html.Div(
    children=[
        html.Br(),
        html.Label("Rollno"), rollno_dropdown,
        html.Label("Subject 1"), subject1_dropdown, 
        html.Label("Subject 2"), subject2_dropdown,
        dcc.Graph(id="barplot")
    ],
    className="container"
)

####################### CALLBACKS ###############################
@callback(
    Output("barplot", "figure"), 
    [Input("rollno", "value"), Input("subject1", "value"), Input("subject2", "value")]
)
def update_barplot(rollno, subject1, subject2):
    if rollno is None:
        # Return empty figure if no roll numbers exist
        return px.bar(title="No data available.")
    return create_barplot(rollno, subject1, subject2)
