from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import plotly.express as px
import pandas as pd
from collections import defaultdict

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def format_key(key):
    if not key or all(not unit for unit in key):
        return 'None'
    return ', '.join([f"{unit} {num}" for unit, num in key])

def plot_results(units_count, title):
    units_dict = defaultdict(int)
    for units, count in units_count.items():
        units_dict[units] += count

    labels = []
    values = []

    total_count = sum(units_dict.values())

    for units, count in units_dict.items():
        labels.append(format_key(units))
        values.append((count / total_count) * 100)  # Convert to percentage

    df = pd.DataFrame({'Units': labels, 'Percentage': values})
    fig = px.bar(df, x='Percentage', y='Units', orientation='h', title=title, text='Percentage')
    fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside', marker_color='#F4A460')
    fig.update_layout(
        yaxis=dict(autorange="reversed"),
        showlegend=False,
        #plot_bgcolor='#4e4e4d',
        #paper_bgcolor='#4e4e4d',
        #font=dict(color='white')
    )
    fig.update_xaxes(range=[0, 120])  # Ensure x-axis goes to 100%

    return fig.to_html(full_html=False, include_plotlyjs='cdn')