import pandas as pd
import dash
from dash import dcc, html, callback
import plotly.express as px
from dash.dependencies import Input, Output

# Register the page
dash.register_page(__name__, path='/relation', name="𝓒𝓸𝓶𝓹𝓪𝓻𝓲𝓼𝓸𝓷 ⚔️")

####################### LOAD DATASET #############################
# Load the dataset and handle the file not found error
try:
    student_marks_df = pd.read_csv("student_marks.csv")
except FileNotFoundError:
    raise Exception("The file 'student_marks.csv' was not found.")

####################### BARPLOT FUNCTION #############################
def create_barplot(rollno, subject1="Maths", subject2="Physics"):
    """Creates a bar plot comparing scores in two subjects for a given roll number."""
    try:
        student_data = student_marks_df[student_marks_df["Rollno"] == rollno]
        if student_data.empty:
            raise ValueError(f"No data found for Rollno {rollno}.")
        
        data = {
            "Subject": [subject1, subject2],
            "Mean Score": [student_data[subject1].values[0], student_data[subject2].values[0]]
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
            x0=-0.5,  # Start at the first subject
            y0=pass_mark,    # Pass marks
            x1=1.5,  # End at the last subject (2 subjects in total, indexed from 0)
            y1=pass_mark,    # Pass marks
            line=dict(color="Green", width=2, dash="dash")
        )
        
        return barplot
    
    except KeyError as e:
        raise Exception(f"One of the subjects {subject1} or {subject2} does not exist in the dataset. Error: {e}")

####################### WIDGETS #############################
# Define the dropdown options
columns = ["Maths","Physics","Chemistry","English","Biology","Economics","History","Civics"]
rollnos = student_marks_df["Rollno"].unique()

rollno_dropdown = dcc.Dropdown(
    id="rollno", 
    options=[{'label': str(rollno), 'value': rollno} for rollno in rollnos], 
    value=rollnos[0], 
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
# Define the layout of the page
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
# Define the callback to update the barplot
@callback(
    Output("barplot", "figure"), 
    [Input("rollno", "value"), Input("subject1", "value"), Input("subject2", "value")]
)
def update_barplot(rollno, subject1, subject2):
    return create_barplot(rollno, subject1, subject2)
