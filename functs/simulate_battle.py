from functs.remove_hits import remove_hits
import json
import random

# Define the units and their attributes
with open('static/units.json', 'r') as f:
    units = json.load(f)

# Function to simulate a battle round
def simulate_battle(attacking_units, defending_units, attacking_battleship_hits, defending_battleship_hits):
    attack_hits = 0
    defense_hits = 0

    # Calculate paired infantry and artillery
    num_infantry = attacking_units.get("Infantry", 0)
    num_artillery = attacking_units.get("Artillery", 0)
    paired_infantry = min(num_infantry, num_artillery)
    unpaired_infantry = num_infantry - paired_infantry

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

    # Calculate remaining units after hits factoring in battleship extra hit
    # Reducing the defense hits based on extra attacking battleship hits
    if attacking_battleship_hits > 0:
        if defense_hits - attacking_battleship_hits >= 0:
            defense_hits = defense_hits - attacking_battleship_hits
            attacking_battleship_hits = 0

        else:
            defense_hits = 0
            attacking_battleship_hits = attacking_battleship_hits - defense_hits

    # Reducing the attack hits based on extra defender battleship hits
    if defending_battleship_hits > 0:
        if attack_hits - defending_battleship_hits >= 0:
            attack_hits = attack_hits - defending_battleship_hits
            defending_battleship_hits = 0
        else:
            attack_hits = 0
            defending_battleship_hits = defending_battleship_hits - attack_hits

    # Remove hits from the battle
    remaining_attacking_units = remove_hits(attacking_units, defense_hits)
    remaining_defending_units = remove_hits(defending_units, attack_hits)

    return attack_hits, defense_hits, remaining_attacking_units, remaining_defending_units, attacking_battleship_hits, defending_battleship_hits