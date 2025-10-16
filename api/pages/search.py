import pandas as pd
import dash
from dash import dcc, html, callback
import plotly.express as px
from dash.dependencies import Input, Output

dash.register_page(__name__, path='/search', name="𝓢𝓮𝓪𝓻𝓬𝓱 🔍")

####################### LOAD DATASET #############################
student_marks_df = pd.read_csv("student_marks.csv")

####################### BAR PLOT #################################
def create_student_barplot(Rollno):
    student_data = student_marks_df[student_marks_df['Rollno'] == Rollno]
    if student_data.empty:
        return px.bar(title="Student not found")

    student_data = student_data.melt(id_vars=["Rollno"], 
                                     value_vars=["Maths","Physics","Chemistry","English","Biology","Economics","History","Civics"],
                                     var_name="Subject", 
                                     value_name="Score")
    fig = px.bar(student_data, x="Subject", y="Score", title=f"Scores for Rollno {Rollno}", height=600)

    # Add a green line for pass marks (35)
    fig.add_shape(
        type="line",
        x0=-0.5,  # Start at the first subject
        y0=35,    # Pass marks
        x1=len(student_data['Subject']) - 0.5,  # End at the last subject
        y1=35,    # Pass marks
        line=dict(color="Green", width=2, dash="dash")
    )

    # Identify and highlight failed subjects
    failed_subjects = student_data[student_data['Score'] < 35]
    if not failed_subjects.empty:
        annotations = [
            dict(
                x=row['Subject'], 
                y=row['Score'], 
                text=row['Subject'], 
                showarrow=True, 
                arrowhead=2, 
                ax=20, 
                ay=-30, 
                font=dict(color='red')
            ) 
            for _, row in failed_subjects.iterrows()
        ]
        fig.update_layout(annotations=annotations)

        # Add text for failed subjects
        failed_subjects_text = ", ".join(failed_subjects['Subject'])
        fail_info = f"Failed Subjects: {failed_subjects_text}"
        fig.add_annotation(text=fail_info, xref="paper", yref="paper", x=1.05, y=1.05, showarrow=False, font=dict(size=12, color="red"), align="left")

    return fig

####################### PAGE LAYOUT #############################
layout = html.Div(children=[
    html.H1("Search Student Scores by Roll Number", className="text-center my-4"),
    dcc.Input(id="Rollno_input", type="number", placeholder="Enter roll number", className="form-control", min=1251, max=1272),
    html.Br(),
    dcc.Graph(id="student_barplot")
], className="container")

####################### CALLBACKS ###############################
@callback(Output("student_barplot", "figure"), 
          [Input("Rollno_input", "value")])
def update_student_barplot(Rollno):
    if Rollno is None:
        return px.bar(title="Enter a roll number to view scores")
    return create_student_barplot(Rollno)
