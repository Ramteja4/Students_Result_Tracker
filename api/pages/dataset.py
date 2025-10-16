import os
import pandas as pd
import dash
from dash import html, dash_table

# Register the page
dash.register_page(__name__, path='/dataset', name="𝒟𝒶𝓉𝒶𝓈𝑒𝓉 📋")

####################### LOAD DATASET #############################
# Compute absolute path to CSV (project root)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
csv_path = os.path.join(BASE_DIR, "student_marks.csv")

# Load CSV safely
try:
    student_df = pd.read_csv(csv_path)
except FileNotFoundError:
    raise Exception(f"The file 'student_marks.csv' was not found at {csv_path}. "
                    f"Make sure it is included in your repository.")

####################### PAGE LAYOUT #############################
layout = html.Div(children=[
    html.Br(),
    dash_table.DataTable(
        data=student_df.to_dict('records'),
        page_size=20,
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'center'},
        style_header={'fontWeight': 'bold'}
    ),
])
