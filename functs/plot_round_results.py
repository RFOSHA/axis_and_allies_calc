import pandas as pd
import plotly.express as px
import plotly.io as pio
from collections import defaultdict

def plot_round_results(df, filename_prefix, num_simulations):
    rounds = df['Round'].unique()
    plot_htmls = defaultdict(list)

    for round_num in rounds:
        filename = str(f"{filename_prefix}_{round_num}.html")
        round_df = df[df['Round'] == round_num]

        # Sort the DataFrame by Value in descending order
        round_df = round_df.sort_values(by='Value', ascending=False).reset_index(drop=True)

        round_df['Percentage'] = ((round_df['Count'] / num_simulations) * 100).round(2)  # Convert to percentage

        fig = px.bar(
            round_df,
            x='Percentage',
            y='Units',
            orientation='h',
            title=f'Count by Units for Round {round_num}',
            text='Percentage',
            color='Units',
            color_discrete_sequence=['#F4A460']  # Set bar color
        )

        fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
        fig.update_layout(
            showlegend=False,
            plot_bgcolor='#4e4e4d',
            paper_bgcolor='#4e4e4d',
            font=dict(color='white')
        )
        fig.update_xaxes(range=[0, 100])  # Ensure x-axis goes to 100%

        # Save the figure as an HTML file
        pio.write_html(fig, file=filename, full_html=False, include_plotlyjs='cdn')

        # Collect the HTML content
        plot_htmls[round_num].append(pio.to_html(fig, full_html=False, include_plotlyjs='cdn'))

    return plot_htmls

