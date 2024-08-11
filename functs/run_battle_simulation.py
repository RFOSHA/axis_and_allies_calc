import pandas as pd
from functs.simulate_battle import simulate_battle
from functs.remove_hits import remove_hits
import random
import json

# Define the units and their attributes
with open('static/units.json', 'r') as f:
    units = json.load(f)

def calculate_total_ipc(unit_counts):
    total_ipc = 0
    for unit, count in unit_counts.items():
        if unit in units:
            total_ipc += units[unit]['ipc'] * count
    return total_ipc

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
def run_battle_simulation(attacking_units, defending_units, battle_type):
    print("In Run Battle Simulation")
    print(f"attacking_units: {attacking_units}")
    print(f"defending_units: {defending_units}")
    print(f"battle_type: {battle_type}")

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
    num_attacking_naval_bomb_units = num_attack_cruiser + num_attack_battleship


    if num_attacking_land_units > 0 and num_attacking_naval_bomb_units > 0:
        bombardment_units = {key: value for key, value in attacking_units.items() if key in ["Cruiser", "Battleship"]}
        for unit, count in bombardment_units.items():
            for _ in range(count):
                attack_value = units[unit]["attack"]
                roll = random.randint(1, 6)
                if roll <= attack_value:
                    naval_bomb_hits += 1

        attacking_units = {key: value for key, value in attacking_units.items() if key not in ["Cruiser", "Battleship"]}

    # Setting battleship capital hits for sea battles only
    if num_attacking_land_units == 0 and num_attacking_naval_bomb_units > 0:
        attacking_battleship_hits = attacking_units['Battleship']
        defending_battleship_hits = defending_units['Battleship']
    else:
        attacking_battleship_hits = 0
        defending_battleship_hits = 0

    #main battle module
    while sum(attacking_units.values()) > 0 and sum(defending_units.values()) > 0:
        battle_round += 1
        print(f"Main battle module - round: {battle_round}")
        attack_hits, defense_hits, attacking_units, defending_units, attacking_battleship_hits, defending_battleship_hits = simulate_battle(attacking_units, defending_units, attacking_battleship_hits, defending_battleship_hits, battle_type)

        if battle_round == 1:
            defending_units = remove_hits(defending_units, naval_bomb_hits)

        attacking_units_cumulative_value = calculate_total_ipc(attacking_units)
        defending_units_cumulative_value = calculate_total_ipc(defending_units)

        # Filter out keys with 0 values
        filtered_attacking_units = remove_zero_values_and_convert_to_string(attacking_units)
        filtered_defending_units = remove_zero_values_and_convert_to_string(defending_units)

        # Record the current state of the units
        battle_history_attacking.append({'Round': battle_round, 'Units': filtered_attacking_units, 'Count': 1, 'Value': attacking_units_cumulative_value})
        battle_history_defending.append({'Round': battle_round, 'Units': filtered_defending_units, 'Count': 1, 'Value': defending_units_cumulative_value})
        print(f"Main battle module - battle_history_attacking: {battle_history_attacking}")
        print(f"Main battle module - battle_history_defending: {battle_history_defending}")

        # Assess if it is an sub on aircraft situation and if so then force a tie
        num_attacking_subs = attacking_units.get("Submarine", 0)
        num_defending_subs = defending_units.get("Submarine", 0)
        num_attacking_aircraft = attacking_units.get("Fighter", 0) + attacking_units.get("Bomber", 0)
        num_defending_aircraft = defending_units.get("Fighter", 0) + defending_units.get("Bomber", 0)
        num_attacking_nonsub_ships = attacking_units.get("Destroyer", 0) + attacking_units.get("Cruiser",
            0) + attacking_units.get("Carrier", 0) + attacking_units.get("Battleship", 0)
        num_defending_nonsub_ships = defending_units.get("Destroyer", 0) + defending_units.get("Cruiser",
            0) + defending_units.get("Carrier", 0) + defending_units.get("Battleship", 0)

        if (num_defending_nonsub_ships == 0 and num_attacking_nonsub_ships == 0 and num_attacking_subs > 0 and num_defending_subs == 0 and num_defending_aircraft > 0) or \
                (num_defending_nonsub_ships == 0 and num_attacking_nonsub_ships == 0 and num_defending_subs > 0 and num_attacking_subs == 0 and num_attacking_aircraft > 0):
            print(f"ROUND: {battle_round}    TIE")
            outcome = "tie"
            df_attacking_rounds = pd.DataFrame(battle_history_attacking)
            df_defending_rounds = pd.DataFrame(battle_history_defending)
            return outcome, attacking_units, defending_units, df_attacking_rounds, df_defending_rounds

    df_attacking_rounds = pd.DataFrame(battle_history_attacking)

    df_defending_rounds = pd.DataFrame(battle_history_defending)

    if sum(attacking_units.values()) == 0 and sum(defending_units.values()) == 0:
        outcome = "tie"
    elif sum(attacking_units.values()) == 0:
        outcome = "defender win"
    else:
        outcome = "attacker win"

    return outcome, attacking_units, defending_units, df_attacking_rounds, df_defending_rounds

