from functs.remove_hits import remove_hits
import json
import random

# Load the units and their attributes from a JSON file
with open('static/units.json', 'r') as f:
    units = json.load(f)


# Function to simulate a single round of battle
def simulate_battle(attacking_units, defending_units, attacking_battleship_hits, defending_battleship_hits,
                    battle_type):
    # Initialize hit counters for both sides
    attack_hits = 0
    defense_hits = 0
    attack_aircraft_hits = 0
    defense_aircraft_hits = 0
    attack_naval_hits = 0
    defense_naval_hits = 0
    attack_sub_hits = 0
    attack_sub_sneak_hits = 0
    defense_sub_hits = 0

    # Check if either side has destroyers, which affect submarine attacks
    attacking_destroyers = attacking_units.get("Destroyer", 0) > 0
    defending_destroyers = defending_units.get("Destroyer", 0) > 0

    # Calculate paired infantry and artillery for attacking side (artillery boosts infantry attack value)
    num_infantry = attacking_units.get("Infantry", 0)
    num_artillery = attacking_units.get("Artillery", 0)
    paired_infantry = min(num_infantry, num_artillery)  # Paired infantry
    unpaired_infantry = num_infantry - paired_infantry  # Unpaired infantry

    # Roll for each attacking unit to determine hits
    for unit, count in attacking_units.items():
        for _ in range(count):
            if unit == "Infantry" and paired_infantry > 0:
                attack_value = 2  # Boosted infantry attack value due to artillery
                paired_infantry -= 1
            else:
                attack_value = units[unit]["attack"]

            roll = random.randint(1, 6)  # Roll a die (1-6)
            if roll <= attack_value:  # Check if the roll is a hit
                if unit in ["Fighter", "Bomber"]:
                    attack_aircraft_hits += 1
                    attack_hits += 1
                elif unit in ["Destroyer", "Carrier", "Cruiser", "Battleship"]:
                    attack_naval_hits += 1
                    attack_hits += 1
                elif unit == "Submarine":
                    # Check if defending side has no destroyers for sneak attack
                    if defending_units.get("Destroyer", 0) == 0:
                        attack_sub_sneak_hits += 1
                        defending_units = remove_hits(defending_units, 1, ignore_aircraft=True)
                    else:
                        attack_sub_hits += 1
                        attack_hits += 1
                else:
                    attack_hits += 1

    # Roll for each defending unit to determine hits
    for unit, count in defending_units.items():
        if unit == "AA":
            continue  # Skip AA units during defense rolls
        for _ in range(count):
            defense_value = units[unit]["defense"]
            roll = random.randint(1, 6)  # Roll a die (1-6)
            if roll <= defense_value:  # Check if the roll is a hit
                if unit in ["Fighter", "Bomber"]:
                    defense_aircraft_hits += 1
                elif unit in ["Destroyer", "Carrier", "Cruiser", "Battleship"]:
                    defense_naval_hits += 1
                elif unit == "Submarine":
                    defense_sub_hits += 1
                defense_hits += 1

    # Calculate remaining units after hits, factoring in battleship's extra hit capability

    # Adjust defense hits based on extra attacking battleship hits
    if attacking_battleship_hits > 0:
        if defense_hits - attacking_battleship_hits >= 0:
            defense_hits -= attacking_battleship_hits
            attacking_battleship_hits = 0
        else:
            defense_hits = 0
            attacking_battleship_hits -= defense_hits

    # Adjust attack hits based on extra defending battleship hits
    if defending_battleship_hits > 0:
        if attack_hits - defending_battleship_hits >= 0:
            attack_hits -= defending_battleship_hits
            defending_battleship_hits = 0
        else:
            attack_hits = 0
            defending_battleship_hits -= attack_hits

    # Remove hits from the battle based on battle type (sea or land/amphibious)
    if battle_type == 'sea':
        # Handling sea battles
        if defending_destroyers:
            remaining_attacking_units = remove_hits(attacking_units, defense_hits)
        else:
            remaining_attacking_units = remove_hits(attacking_units, defense_naval_hits)
            remaining_attacking_units = remove_hits(remaining_attacking_units, defense_sub_hits, ignore_aircraft=True)
            remaining_attacking_units = remove_hits(remaining_attacking_units, defense_aircraft_hits, ignore_subs=True)

        if attacking_destroyers:
            remaining_defending_units = remove_hits(defending_units, attack_hits)
        else:
            remaining_defending_units = remove_hits(defending_units, attack_naval_hits)
            remaining_defending_units = remove_hits(remaining_defending_units, attack_sub_hits, ignore_aircraft=True)
            remaining_defending_units = remove_hits(remaining_defending_units, attack_aircraft_hits, ignore_subs=True)
    else:
        # Handling land and amphibious battles
        remaining_attacking_units = remove_hits(attacking_units, defense_hits)
        remaining_defending_units = remove_hits(defending_units, attack_hits)

    # Return the number of hits, remaining units, and battleship hits for both sides
    return attack_hits, defense_hits, remaining_attacking_units, remaining_defending_units, attacking_battleship_hits, defending_battleship_hits
