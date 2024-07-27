import pandas as pd
from functs.simulate_battle import simulate_battle
from functs.remove_hits import remove_hits
import random
import json

# Define the units and their attributes
with open('static/units.json', 'r') as f:
    units = json.load(f)

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
    anti_air_hits = 0
    naval_bomb_hits = 0

    # Roll for anti-aircraft gun
    num_anti_aircraft = defending_units.get("AA", 0)
    num_fighters = attacking_units.get("Fighter", 0)
    num_bombers = attacking_units.get("Bomber", 0)
    attacking_air_units = {key: attacking_units[key] for key in ["Fighter", "Bomber"]}

    if num_anti_aircraft > 0 and (num_bombers+num_fighters) > 0:
        if (num_anti_aircraft * 3) <= (num_bombers+num_fighters):
            rounds = num_anti_aircraft * 3
        else:
            rounds = (num_bombers+num_fighters)

        for i in range(rounds):
            roll = random.randint(1, 6)
            if roll <= units["AA"]["defense"]:
                anti_air_hits += 1

        remaining_attacking_air_units = remove_hits(attacking_air_units, anti_air_hits)
        attacking_units.update(remaining_attacking_air_units)

    #Roll for amphibious bombardment
    num_attack_infantry = attacking_units.get("Infantry", 0)
    num_attack_artillery = attacking_units.get("Artillery", 0)
    num_attack_tank = attacking_units.get("Tank", 0)
    num_attack_cruiser = attacking_units.get("Cruiser", 0)
    num_attack_battleship = attacking_units.get("Battleship", 0)
    num_attacking_land_units = num_attack_infantry + num_attack_artillery + num_attack_tank
    num_attacking_naval_units = num_attack_cruiser + num_attack_battleship

    if num_attacking_land_units > 0 and num_attacking_naval_units > 0:
        bombardment_units = {key: value for key, value in attacking_units.items() if key in ["Cruiser", "Battleship"]}
        for unit, count in bombardment_units.items():
            for _ in range(count):
                attack_value = units[unit]["attack"]
                roll = random.randint(1, 6)
                if roll <= attack_value:
                    naval_bomb_hits += 1

        attacking_units = {key: value for key, value in attacking_units.items() if key not in ["Cruiser", "Battleship"]}

    #main battle module
    while sum(attacking_units.values()) > 0 and sum(defending_units.values()) > 0:
        battle_round += 1
        attack_hits, defense_hits, attacking_units, defending_units = simulate_battle(attacking_units, defending_units)

        if battle_round == 1:
            defending_units = remove_hits(defending_units, naval_bomb_hits)

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

    return outcome, attacking_units, defending_units, df_attacking_rounds, df_defending_rounds

