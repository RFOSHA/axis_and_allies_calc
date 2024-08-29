import pandas as pd


# Function to identify outcomes resolved in previous rounds and update the battle history DataFrame
def resolved_in_previous_round(battle_history_df, number_of_simulations):
    # List to hold new rows that will be added to the DataFrame
    new_rows = []

    # Loop through each round starting from Round 2
    for round_number in battle_history_df['Round'].unique()[1:]:
        # Calculate the total count of outcomes in the current round
        count_in_round = battle_history_df[battle_history_df['Round'] == round_number]['Count'].sum()

        # Calculate the difference between total simulations and count in the current round
        difference = number_of_simulations - count_in_round

        # If there are outcomes resolved in previous rounds (difference > 0)
        if difference > 0:
            # Create a new record for the resolved outcomes
            new_record = pd.DataFrame({
                'Round': [round_number],  # The current round number
                'Units': ['RIPR'],  # "RIPR" stands for "Resolved In Previous Round"
                'Value': [0],  # Assign a value of 0 to this record (placeholder)
                'Count': [difference]  # The difference representing resolved outcomes
            })
            new_rows.append(new_record)  # Add the new record to the list of new rows

    # Concatenate the new rows to the original DataFrame if any new rows were added
    if new_rows:
        battle_history_df = pd.concat([battle_history_df] + new_rows, ignore_index=True)

    # Sort the DataFrame by 'Round' to maintain chronological order
    battle_history_df = battle_history_df.sort_values(by='Round').reset_index(drop=True)

    return battle_history_df  # Return the updated DataFrame
