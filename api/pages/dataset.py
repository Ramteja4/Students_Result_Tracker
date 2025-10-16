import pandas as pd
import dash
from dash import html,dash_table

dash.register_page(__name__, path='/dataset', name="𝒟𝒶𝓉𝒶𝓈𝑒𝓉 📋")


student_df = pd.read_csv("student_marks.csv")

# Display data
layout = html.Div(children=[
    html.Br(),
    dash_table.DataTable(
        data=student_df.to_dict('records'),
        page_size=20
    ),
])
