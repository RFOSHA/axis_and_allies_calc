from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import plotly.express as px
import pandas as pd
from collections import defaultdict
import json

# Initialize FastAPI application
app = FastAPI()

# Initialize Jinja2 templates with the directory "templates"
templates = Jinja2Templates(directory="templates")

# Load units data from JSON file located in the "static" directory
with open('static/units.json', 'r') as f:
    units_data = json.load(f)


# Helper function to format the key (unit and count) into a readable and truncated string
def format_key(key, max_length=30):
    if not key or all(not unit for unit in key):
        return 'None'  # Return 'None' if key is empty or has no units
    formatted_key = ', '.join([f"{unit} {num}" for unit, num in key])

    # Truncate the formatted key if it exceeds the maximum length
    if len(formatted_key) > max_length:
        return formatted_key[:max_length] + '...'  # Add ellipsis if truncated
    return formatted_key


# Function to calculate the cumulative value based on unit counts
def calculate_cumulative_value(units_count):
    total_value = 0
    for unit, num in units_count:
        total_value += units_data[unit]["ipc"] * num  # Multiply unit's IPC (a metric) by its count
    return total_value


# Function to plot results using Plotly and return the plot as HTML
def plot_results(units_count, title):
    units_dict = defaultdict(int)  # Initialize a dictionary to hold unit counts
    for units, count in units_count.items():
        units_dict[units] += count  # Aggregate counts for each unit combination

    labels = []  # List to store formatted unit names
    values = []  # List to store the percentage of each unit combination
    cumulative_values = []  # List to store cumulative values based on the unit counts

    total_count = sum(units_dict.values())  # Calculate the total count of all units

    # Populate the labels, values, and cumulative_values lists
    for units, count in units_dict.items():
        labels.append(format_key(units))  # Format and add the key (units) to labels
        values.append((count / total_count) * 100)  # Convert count to percentage and add to values
        cumulative_values.append(calculate_cumulative_value(units))  # Calculate and add cumulative value

    # Create a DataFrame from the collected data
    df = pd.DataFrame({'Units': labels, 'Percentage': values, 'CumulativeValue': cumulative_values})
    df = df.sort_values(by='CumulativeValue', ascending=False)  # Sort DataFrame by cumulative value

    # Generate a horizontal bar plot using Plotly Express
    fig = px.bar(df, x='Percentage', y='Units', orientation='h', title=title, text='Percentage')

    # Customize plot appearance
    fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside',
                      marker_color='#F4A460')  # Format text and color
    fig.update_layout(
        yaxis=dict(autorange="reversed"),  # Reverse y-axis order
        showlegend=False,  # Hide the legend
        plot_bgcolor='#4e4e4d',  # Set plot background color
        paper_bgcolor='#4e4e4d',  # Set paper background color
        font=dict(color='#e7e7e7')  # Set font color
    )
    fig.update_xaxes(range=[0, 120])  # Ensure x-axis extends beyond 100% to accommodate labels

    # Return the plot as an HTML string without full HTML document and including Plotly.js CDN
    return fig.to_html(full_html=False, include_plotlyjs='cdn')
