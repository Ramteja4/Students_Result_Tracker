import pandas as pd
import dash
from dash import html, dcc
import plotly.express as px

dash.register_page(__name__, path='/', name="𝐻𝑜𝓂𝑒 🏡")

####################### LOAD DATASET #############################
student_marks_df = pd.read_csv("student_marks.csv")

# Filter out non-numeric columns and 'Total' column for average calculation
numeric_columns = student_marks_df.select_dtypes(include=['number']).columns.drop(['Total', 'Rollno', 'index'])
pass_marks = 14
pass_all_subjects = student_marks_df[numeric_columns].apply(lambda row: all(row >= pass_marks), axis=1).sum()
pass_count = (student_marks_df[numeric_columns] >= pass_marks).sum()
fail_count = (student_marks_df[numeric_columns] < pass_marks).sum()

####################### PIE CHART ###############################
average_marks = student_marks_df[numeric_columns].mean()
pie_chart = px.pie(values=average_marks, names=average_marks.index, title="Average Marks")

####################### BAR GRAPH (AVERAGE MARKS) ###############################
average_bar_graph = px.bar(x=average_marks.index, y=average_marks, title="Average Marks", labels={'x': 'Subject', 'y': 'Average Mark'})

# Add a green line for pass marks (14) to the bar graph
average_bar_graph.add_shape(
    type="line",
    x0=-0.5,  # Start at the first subject
    y0=pass_marks,  # Pass marks
    x1=len(average_marks) - 0.5,  # End at the last subject
    y1=pass_marks,  # Pass marks
    line=dict(color="Green", width=2, dash="dash")
)

####################### PAGE LAYOUT #############################
layout = html.Div(children=[
    html.Div(children=[
        html.H2("Student Marks Overview"),
        html.P("Average Marks of Each Subject:"),
        dcc.Graph(figure=pie_chart),
        dcc.Graph(figure=average_bar_graph),
        html.Hr(),
        html.H2("Pass and Fail Count in Each Subject"),
        html.Ul(children=[
            html.Li(f"{subject}: Pass {pass_count[subject]}, Fail {fail_count[subject]}") for subject in pass_count.index
        ])
    ]),
    html.Hr(),
    html.H2(f"Number of Students Passing All Subjects: {pass_all_subjects}", className="text-center")
], className="bg-light p-4 m-2")  # Bootstrap
