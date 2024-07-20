import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

def plot_round_results(df, filename_prefix):
    # print("THIS IS THE DATAFRAME THAT IS PASSED INTO THE FUNCTION")
    # print(df)
    round_df = pd.DataFrame()
    # print("THIS IS THE FRESH ROUND_DF")
    # print(round_df)
    rounds = df['Round'].unique()
    # print("THIS IS THE # OF ROUNDS")
    # print(rounds)

    for round_num in rounds:
        filename = str(f"{filename_prefix}_{round_num}.png")
        round_df = df[df['Round'] == round_num]
        #round_df = round_df.sort_values(by='Count', ascending=False)
        # print(f"THIS IS THE DATAFRAME FOR ROUND {round_num}")
        # print(round_df)


        plt.figure(figsize=(10, 6))
        sns.barplot(x='Count', y='Units', data=round_df, palette='muted', hue='Units', legend=False)
        plt.title(f'Count by Units for Round {round_num}')
        plt.xticks(rotation=90)
        plt.tight_layout()

        # Save the figure
        plt.savefig(filename)
        plt.close()

