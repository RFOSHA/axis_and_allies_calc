from functs.run_battle_simulation import run_battle_simulation
from collections import defaultdict
import pandas as pd

# Function to run multiple battle simulations and capture remaining units
def run_multiple_battle_sims(attacking_units, defending_units, num_of_simulations):
    attacker_win_count = 0
    defender_win_count = 0
    ties = 0
    attacker_remaining_units_count = defaultdict(int)
    defender_remaining_units_count = defaultdict(int)
    battle_history_attacking_df = pd.DataFrame()
    battle_history_defending_df = pd.DataFrame()

    for _ in range(num_of_simulations):
        outcome, remaining_attacking_units, remaining_defending_units, df_attacking_rounds, df_defending_rounds\
            = run_battle_simulation(attacking_units.copy(), defending_units.copy())

        battle_history_attacking_df = pd.concat([df_attacking_rounds,battle_history_attacking_df], ignore_index=True).groupby(['Round', 'Units']).sum().reset_index()
        battle_history_defending_df = pd.concat([df_defending_rounds,battle_history_defending_df], ignore_index=True).groupby(['Round', 'Units']).sum().reset_index()

        if outcome == "tie":
            ties += 1
            defender_remaining_units_count[tuple(remaining_defending_units.items())] += 1
            attacker_remaining_units_count[tuple(remaining_attacking_units.items())] += 1
        elif outcome == "defender win":
            defender_win_count += 1
            defender_remaining_units_count[tuple(remaining_defending_units.items())] += 1
            attacker_remaining_units_count[tuple(remaining_attacking_units.items())] += 1
        else:
            attacker_win_count += 1
            attacker_remaining_units_count[tuple(remaining_attacking_units.items())] += 1
            defender_remaining_units_count[tuple(remaining_defending_units.items())] += 1

    return attacker_win_count, defender_win_count, ties, attacker_remaining_units_count, defender_remaining_units_count, battle_history_attacking_df, battle_history_defending_df
