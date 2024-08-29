import plotly.express as px
import plotly.io as pio
from collections import defaultdict

# Function to plot round results, save as HTML, and return HTML content for each round
def plot_round_results(df, filename_prefix, num_simulations):
    rounds = df['Round'].unique()  # Get the unique round numbers from the DataFrame
    plot_htmls = defaultdict(list)  # Dictionary to store HTML content for each round

    # Iterate over each round
    for round_num in rounds:
        filename = str(f"{filename_prefix}_{round_num}.html")  # Create filename for HTML output
        round_df = df[df['Round'] == round_num]  # Filter the DataFrame for the current round

        # Sort the DataFrame by 'Value' in descending order and reset the index
        round_df = round_df.sort_values(by='Value', ascending=False).reset_index(drop=True)

        # Convert 'Count' to percentage of total simulations and round to 2 decimal places
        round_df['Percentage'] = ((round_df['Count'] / num_simulations) * 100).round(2)

        # Create a horizontal bar plot using Plotly Express
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

        # Customize the appearance of the plot
        fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')  # Format and position text
        fig.update_layout(
            showlegend=False,  # Hide the legend
            plot_bgcolor='#4e4e4d',  # Set plot background color
            paper_bgcolor='#4e4e4d',  # Set paper background color
            font=dict(color='#e7e7e7')  # Set font color
        )
        fig.update_xaxes(range=[0, 100])  # Ensure x-axis extends to 100%

        # Save the plot as an HTML file
        pio.write_html(fig, file=filename, full_html=False, include_plotlyjs='cdn')

        # Collect the HTML content for the current round
        plot_htmls[round_num].append(pio.to_html(fig, full_html=False, include_plotlyjs='cdn'))

    return plot_htmls  # Return the dictionary containing HTML content for each round
