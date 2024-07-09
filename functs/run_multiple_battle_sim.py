from functs.run_battle_simulation import run_battle_simulation
from collections import defaultdict

# Function to run multiple battle simulations and capture remaining units
def run_multiple_battle_sims(attacking_units, defending_units, num_of_simulations):
    attacker_win_count = 0
    defender_win_count = 0
    ties = 0
    attacker_remaining_units_count = defaultdict(int)
    defender_remaining_units_count = defaultdict(int)

    for _ in range(num_of_simulations):
        outcome, remaining_attacking_units, remaining_defending_units = run_battle_simulation(attacking_units.copy(),
                                                                                              defending_units.copy())

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

    return attacker_win_count, defender_win_count, ties, attacker_remaining_units_count, defender_remaining_units_count
