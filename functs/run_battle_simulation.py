from functs.simulate_battle import simulate_battle

# Function to run the full battle simulation until one side has no units left
def run_battle_simulation(attacking_units, defending_units):
    while sum(attacking_units.values()) > 0 and sum(defending_units.values()) > 0:
        attack_hits, defense_hits, attacking_units, defending_units = simulate_battle(attacking_units, defending_units)

    if sum(attacking_units.values()) == 0 and sum(defending_units.values()) == 0:
        outcome = "tie"
    elif sum(attacking_units.values()) == 0:
        outcome = "defender win"
    else:
        outcome = "attacker win"

    return outcome, attacking_units, defending_units