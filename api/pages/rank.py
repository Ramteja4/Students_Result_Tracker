import os
import pandas as pd
import dash
from dash import html
import dash_bootstrap_components as dbc

# Register the page
dash.register_page(__name__, path='/rank', name="𝑅� rank 📈")

####################### LOAD DATASET #############################
# Compute absolute path to CSV (project root)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
csv_path = os.path.join(BASE_DIR, "student_marks.csv")

# Load CSV safely
try:
    student_marks_df = pd.read_csv(csv_path)
except FileNotFoundError:
    raise Exception(f"The file 'student_marks.csv' was not found at {csv_path}. "
                    f"Make sure it is included in your repository.")

####################### RANKING #############################
student_marks_df['Rank'] = student_marks_df['Total'].rank(ascending=False, method='dense')
ranked_df = student_marks_df.sort_values(by='Rank')

####################### PAGE LAYOUT #############################
layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Student Ranks based on Total Scores", className="text-center my-4")
        ])
    ]),
    dbc.Row([
        dbc.Col([
            dbc.ListGroup([
                dbc.ListGroupItem(
                    f"Rank {int(row['Rank'])} - Name: {row['Name']} - Rollno: {row['Rollno']}", 
                    className="d-flex justify-content-between align-items-center"
                ) for _, row in ranked_df.iterrows()
            ])
        ], width=6, className="mx-auto")
    ])
], fluid=True, className="p-4")
