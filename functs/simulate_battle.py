from functs.remove_hits import remove_hits
import json
import random

# Define the units and their attributes
with open('static/units.json', 'r') as f:
    units = json.load(f)

# Function to simulate a battle round
def simulate_battle(attacking_units, defending_units):
    attack_hits = 0
    defense_hits = 0

    # Calculate paired infantry and artillery
    num_infantry = attacking_units.get("Infantry", 0)
    num_artillery = attacking_units.get("Artillery", 0)
    paired_infantry = min(num_infantry, num_artillery)
    unpaired_infantry = num_infantry - paired_infantry

    #Roll for amphibious bombardment
    # num_attack_infantry = attacking_units.get("Infantry", 0)
    # num_attack_artillery = attacking_units.get("Artillery", 0)
    # num_attack_tank = attacking_units.get("Tank", 0)
    # num_attack_cruiser = attacking_units.get("Cruiser", 0)
    # num_attack_battleship = attacking_units.get("Battleship", 0)
    # num_attacking_land_units = num_attack_infantry + num_attack_artillery + num_attack_tank
    # num_attacking_naval_units = num_attack_cruiser + num_attack_battleship
    #
    # if num_attacking_land_units > 0 and num_attacking_naval_units > 0:
    #     bombardment_units = {key: value for key, value in attacking_units.items() if key in ["Cruiser", "Battleship"]}
    #     for unit, count in bombardment_units.items():
    #         attack_value = units[unit]["attack"]
    #         roll = random.randint(1, 6)
    #         if roll <= attack_value:
    #             attack_hits += 1

    # Roll for each attacking unit
    for unit, count in attacking_units.items():
        for _ in range(count):
            if unit == "Infantry" and paired_infantry > 0:
                attack_value = 2
                paired_infantry -= 1
            else:
                attack_value = units[unit]["attack"]
            roll = random.randint(1, 6)
            if roll <= attack_value:
                attack_hits += 1

    # Roll for each defending unit
    for unit, count in defending_units.items():
        if unit == "AA":
            continue #Skip AA units
        for _ in range(count):
            defense_value = units[unit]["defense"]
            roll = random.randint(1, 6)
            if roll <= defense_value:
                defense_hits += 1

    # Calculate remaining units after hits
    remaining_attacking_units = remove_hits(attacking_units, defense_hits)
    remaining_defending_units = remove_hits(defending_units, attack_hits)

    return attack_hits, defense_hits, remaining_attacking_units, remaining_defending_units