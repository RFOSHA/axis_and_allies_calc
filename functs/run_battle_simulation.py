import pandas as pd
from functs.simulate_battle import simulate_battle
from functs.remove_hits import remove_hits
import random
import json

# Load the units and their attributes from a JSON file
with open('static/units.json', 'r') as f:
    units = json.load(f)

# Function to calculate the total IPC (cost) of all units
def calculate_total_ipc(unit_counts):
    total_ipc = 0
    for unit, count in unit_counts.items():
        if unit in units:  # Ensure the unit is in the units data
            total_ipc += units[unit]['ipc'] * count  # Multiply unit's IPC by its count
    return total_ipc

# Function to remove keys with zero values from a dictionary and convert the result to a string
def remove_zero_values_and_convert_to_string(input_dict):
    # Filter out entries with zero values
    filtered_dict = {key: value for key, value in input_dict.items() if value != 0}
    if not filtered_dict:
        return 'None'  # Return 'None' if the filtered dictionary is empty
    # Convert the filtered dictionary to a string
    result_string = ', '.join(f"{key} {value}" for key, value in filtered_dict.items())
    return result_string

# Function to run the full battle simulation until one side has no units left
def run_battle_simulation(attacking_units, defending_units, battle_type):

    # Store the round-by-round stats
    battle_history_attacking = []
    battle_history_defending = []
    battle_round = 0
    anti_air_hits = 0  # Track the number of hits from anti-aircraft guns
    naval_bomb_hits = 0  # Track the number of hits from naval bombardment

    # Roll for anti-aircraft gun hits
    num_anti_aircraft = defending_units.get("AA", 0)
    num_fighters = attacking_units.get("Fighter", 0)
    num_bombers = attacking_units.get("Bomber", 0)
    attacking_air_units = {key: attacking_units[key] for key in ["Fighter", "Bomber"]}

    if num_anti_aircraft > 0 and (num_bombers + num_fighters) > 0:
        if (num_anti_aircraft * 3) <= (num_bombers + num_fighters):
            rounds = num_anti_aircraft * 3
        else:
            rounds = (num_bombers + num_fighters)

        # Roll dice for each potential anti-aircraft hit
        for i in range(rounds):
            roll = random.randint(1, 6)
            if roll <= units["AA"]["defense"]:
                anti_air_hits += 1

        # Remove the hits from the attacking air units
        remaining_attacking_air_units = remove_hits(attacking_air_units, anti_air_hits)
        attacking_units.update(remaining_attacking_air_units)

    # Roll for amphibious bombardment
    num_attack_infantry = attacking_units.get("Infantry", 0)
    num_attack_artillery = attacking_units.get("Artillery", 0)
    num_attack_tank = attacking_units.get("Tank", 0)
    num_attack_cruiser = attacking_units.get("Cruiser", 0)
    num_attack_battleship = attacking_units.get("Battleship", 0)
    num_attacking_land_units = num_attack_infantry + num_attack_artillery + num_attack_tank
    num_attacking_naval_bomb_units = num_attack_cruiser + num_attack_battleship

    # Perform bombardment if there are attacking land units and naval bombardment units
    if num_attacking_land_units > 0 and num_attacking_naval_bomb_units > 0:
        bombardment_units = {key: value for key, value in attacking_units.items() if key in ["Cruiser", "Battleship"]}
        for unit, count in bombardment_units.items():
            for _ in range(count):
                attack_value = units[unit]["attack"]
                roll = random.randint(1, 6)
                if roll <= attack_value:
                    naval_bomb_hits += 1

        # Remove bombardment units after the attack
        attacking_units = {key: value for key, value in attacking_units.items() if key not in ["Cruiser", "Battleship"]}

    # Setting battleship capital hits for sea battles only
    if num_attacking_land_units == 0 and num_attacking_naval_bomb_units > 0:
        attacking_battleship_hits = attacking_units['Battleship']
        defending_battleship_hits = defending_units['Battleship']
    else:
        attacking_battleship_hits = 0
        defending_battleship_hits = 0

    # Main battle loop: continue until one side has no units left
    while sum(attacking_units.values()) > 0 and sum(defending_units.values()) > 0:
        battle_round += 1
        attack_hits, defense_hits, attacking_units, defending_units, attacking_battleship_hits, defending_battleship_hits = simulate_battle(
            attacking_units, defending_units, attacking_battleship_hits, defending_battleship_hits, battle_type)

        # Apply naval bombardment hits in the first round
        if battle_round == 1:
            defending_units = remove_hits(defending_units, naval_bomb_hits)

        # Calculate the cumulative IPC value for both sides
        attacking_units_cumulative_value = calculate_total_ipc(attacking_units)
        defending_units_cumulative_value = calculate_total_ipc(defending_units)

        # Filter out keys with 0 values and convert to strings
        filtered_attacking_units = remove_zero_values_and_convert_to_string(attacking_units)
        filtered_defending_units = remove_zero_values_and_convert_to_string(defending_units)

        # Record the current state of the units for both sides
        battle_history_attacking.append({'Round': battle_round, 'Units': filtered_attacking_units, 'Count': 1, 'Value': attacking_units_cumulative_value})
        battle_history_defending.append({'Round': battle_round, 'Units': filtered_defending_units, 'Count': 1, 'Value': defending_units_cumulative_value})

        # Assess if it's a submarine vs aircraft situation and force a tie if necessary
        num_attacking_subs = attacking_units.get("Submarine", 0)
        num_defending_subs = defending_units.get("Submarine", 0)
        num_attacking_aircraft = attacking_units.get("Fighter", 0) + attacking_units.get("Bomber", 0)
        num_defending_aircraft = defending_units.get("Fighter", 0) + defending_units.get("Bomber", 0)
        num_attacking_nonsub_ships = attacking_units.get("Destroyer", 0) + attacking_units.get("Cruiser", 0) + attacking_units.get("Carrier", 0) + attacking_units.get("Battleship", 0)
        num_defending_nonsub_ships = defending_units.get("Destroyer", 0) + defending_units.get("Cruiser", 0) + defending_units.get("Carrier", 0) + defending_units.get("Battleship", 0)

        # If the conditions for a tie (subs vs. aircraft with no non-sub ships) are met, return a tie
        if (num_defending_nonsub_ships == 0 and num_attacking_nonsub_ships == 0 and num_attacking_subs > 0 and num_defending_subs == 0 and num_defending_aircraft > 0) or \
                (num_defending_nonsub_ships == 0 and num_attacking_nonsub_ships == 0 and num_defending_subs > 0 and num_attacking_subs == 0 and num_attacking_aircraft > 0):
            outcome = "tie"
            df_attacking_rounds = pd.DataFrame(battle_history_attacking)
            df_defending_rounds = pd.DataFrame(battle_history_defending)
            return outcome, attacking_units, defending_units, df_attacking_rounds, df_defending_rounds

    # Convert battle history lists to DataFrames
    df_attacking_rounds = pd.DataFrame(battle_history_attacking)
    df_defending_rounds = pd.DataFrame(battle_history_defending)

    # Determine the outcome of the battle
    if sum(attacking_units.values()) == 0 and sum(defending_units.values()) == 0:
        outcome = "tie"
    elif sum(attacking_units.values()) == 0:
        outcome = "defender win"
    else:
        outcome = "attacker win"

    # Return the final outcome, remaining units, and the battle history DataFrames
    return outcome, attacking_units, defending_units, df_attacking_rounds, df_defending_rounds
