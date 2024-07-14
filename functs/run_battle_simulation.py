import pandas as pd
from functs.simulate_battle import simulate_battle

def remove_zero_values_and_convert_to_string(input_dict):
    """
    Removes keys with a value of 0 from the dictionary and converts the result to a string.
    Returns 'None' if the filtered dictionary is empty.

    Parameters:
    input_dict (dict): The dictionary to be processed.

    Returns:
    str: A string representation of the filtered dictionary or 'None' if empty.
    """
    filtered_dict = {key: value for key, value in input_dict.items() if value != 0}
    if not filtered_dict:
        return 'None'
    result_string = ', '.join(f"{key} {value}" for key, value in filtered_dict.items())
    return result_string

# Function to run the full battle simulation until one side has no units left
def run_battle_simulation(attacking_units, defending_units):

    #Store the round by round stats
    battle_history_attacking = []
    battle_history_defending = []
    battle_round = 0

    while sum(attacking_units.values()) > 0 and sum(defending_units.values()) > 0:
        battle_round += 1
        attack_hits, defense_hits, attacking_units, defending_units = simulate_battle(attacking_units, defending_units)

        # Filter out keys with 0 values
        filtered_attacking_units = remove_zero_values_and_convert_to_string(attacking_units)
        filtered_defending_units = remove_zero_values_and_convert_to_string(defending_units)

        # Record the current state of the units
        battle_history_attacking.append({'Round': battle_round, 'Units': filtered_attacking_units, 'Count': 1})
        battle_history_defending.append({'Round': battle_round, 'Units': filtered_defending_units, 'Count': 1})

    df_attacking_rounds = pd.DataFrame(battle_history_attacking)

    df_defending_rounds = pd.DataFrame(battle_history_defending)

    if sum(attacking_units.values()) == 0 and sum(defending_units.values()) == 0:
        outcome = "tie"
    elif sum(attacking_units.values()) == 0:
        outcome = "defender win"
    else:
        outcome = "attacker win"

    # print(battle_round)
    # print(battle_history_attacking)
    # print(attacking_units)

    return outcome, attacking_units, defending_units, df_attacking_rounds, df_defending_rounds






# Record the current state of the units
# attacking_units_round = str(f"attacking_units_{battle_round}")
# defending_units_round = str(f"defending_units_{battle_round}")
#
# battle_history.append({
#     'round': battle_round,
#     attacking_units_round: attacking_units.copy(),
#     defending_units_round: defending_units.copy()
# })