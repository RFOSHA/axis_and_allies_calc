import pandas as pd

def resolved_in_previous_round(battle_history_df, number_of_simulations):
    # List to hold new rows
    new_rows = []

    # Loop through each round starting from Round 2
    for round_number in battle_history_df['Round'].unique()[1:]:
        count_in_round = battle_history_df[battle_history_df['Round'] == round_number]['Count'].sum()
        difference = number_of_simulations - count_in_round

        if difference > 0:
            # Create a new record for the resolved outcomes
            new_record = pd.DataFrame({
                'Round': [round_number],
                'Units': ['RIPR'],
                'Value': [0],
                'Count': [difference]
            })
            new_rows.append(new_record)

    # Concatenate the new rows to the original dataframe
    if new_rows:
        battle_history_df = pd.concat([battle_history_df] + new_rows, ignore_index=True)

    # Sort the DataFrame by Round to maintain order
    battle_history_df = battle_history_df.sort_values(by='Round').reset_index(drop=True)

    return battle_history_df