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
    anti_air_hits = 0

    # Calculate paired infantry and artillery
    num_infantry = attacking_units.get("Infantry", 0)
    num_artillery = attacking_units.get("Artillery", 0)
    paired_infantry = min(num_infantry, num_artillery)
    unpaired_infantry = num_infantry - paired_infantry

    # Roll for anti-aircraft gun
    num_anti_aircraft = defending_units.get("AA", 0)
    print(f"Number of antiaircraft: {num_anti_aircraft}")
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
        print(attacking_units)



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