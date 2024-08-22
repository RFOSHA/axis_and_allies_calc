from functs.remove_hits import remove_hits
import json
import random

# Define the units and their attributes
with open('static/units.json', 'r') as f:
    units = json.load(f)

# Function to simulate a battle round
def simulate_battle(attacking_units, defending_units, attacking_battleship_hits, defending_battleship_hits, battle_type):
    attack_hits = 0
    defense_hits = 0
    attack_aircraft_hits = 0
    defense_aircraft_hits = 0
    attack_naval_hits = 0
    defense_naval_hits = 0
    attack_sub_hits = 0
    attack_sub_sneak_hits = 0
    defense_sub_hits = 0
    print(battle_type)

    # Check for destroyers
    attacking_destroyers = attacking_units.get("Destroyer", 0) > 0
    defending_destroyers = defending_units.get("Destroyer", 0) > 0

    # Calculate paired infantry and artillery
    num_infantry = attacking_units.get("Infantry", 0)
    num_artillery = attacking_units.get("Artillery", 0)
    paired_infantry = min(num_infantry, num_artillery)
    unpaired_infantry = num_infantry - paired_infantry

    # Roll for each attacking unit
    for unit, count in attacking_units.items():
        for _ in range(count):
            print(f"ROLLING ATTACK - UNIT: {unit}")
            if unit == "Infantry" and paired_infantry > 0:
                attack_value = 2
                paired_infantry -= 1
            else:
                attack_value = units[unit]["attack"]
            roll = random.randint(1, 6)
            print(f"ROLLING ATTACK - ROLL: {roll}")
            if roll <= attack_value:
                if unit in ["Fighter", "Bomber"]:
                    attack_aircraft_hits += 1
                    attack_hits += 1
                    print(f"ROLLING ATTACK - Attack Aircraft Hits: {attack_aircraft_hits}")
                elif unit in ["Destroyer", "Carrier", "Cruiser", "Battleship"]:
                    attack_naval_hits += 1
                    attack_hits += 1
                    print(f"ROLLING ATTACK - Attack Naval Hits: {attack_naval_hits}")
                elif unit in ["Submarine"]:

                    if defending_units.get("Destroyer", 0) == 0:

                        attack_sub_sneak_hits += 1
                        print(f"ROLLING SUB SNEAK ATTACK - Attack Sub SNEAK Hits: {attack_sub_sneak_hits}")

                        defending_units = remove_hits(defending_units, 1,
                                                                ignore_aircraft=True)
                        print(f"ROLLING SUB SNEAK ATTACK - New Defending Units: {defending_units}")
                    else:
                        attack_sub_hits += 1
                        attack_hits += 1
                        print(f"ROLLING SUB ATTACK - Attack Sub Hits: {attack_sub_hits}")
                else:
                    attack_hits += 1

                print(f"ROLLING ATTACK - Total Attack Hits: {attack_hits}")

    # Roll for each defending unit
    for unit, count in defending_units.items():
        #print(f"ROLLING DEFENSE - UNIT: {unit}")
        if unit == "AA":
            continue #Skip AA units
        for _ in range(count):
            print(f"ROLLING DEFENSE - UNIT: {unit}")
            defense_value = units[unit]["defense"]
            roll = random.randint(1, 6)
            print(f"ROLLING DEFENSE - ROLL: {roll}")
            if roll <= defense_value:
                if unit in ["Fighter", "Bomber"]:
                    defense_aircraft_hits += 1
                    print(f"ROLLING DEFENSE - Defense Aircraft Hits: {defense_aircraft_hits}")
                elif unit in ["Destroyer", "Carrier", "Cruiser", "Battleship"]:
                    defense_naval_hits += 1
                    print(f"ROLLING DEFENSE - Defense Naval Hits: {defense_naval_hits}")
                elif unit in ["Submarine"]:
                    defense_sub_hits += 1
                    print(f"ROLLING DEFENSE - Defense Sub Hits: {defense_sub_hits}")
                defense_hits += 1
                print(f"ROLLING DEFENSE - Total Defense Hits: {defense_hits}")

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

    print(f"Attack Units Pre Removing Hits: {attacking_units}")
    print(f"Defense Units Pre Removing Hits: {defending_units}")
    print(f"Attack hits - summary: {attack_hits}")
    print(f"Attack aircraft hits - summary: {attack_aircraft_hits}")
    print(f"Attack naval hits - summary: {attack_naval_hits}")
    print(f"Attack sub hits - summary: {attack_sub_hits}")
    print(f"Defense hits - summary: {defense_hits}")
    print(f"Defense aircraft hits - summary: {defense_aircraft_hits}")
    print(f"Defense naval hits - summary: {defense_naval_hits}")
    print(f"Defense sub hits - summary: {defense_sub_hits}")

    # Remove hits from the battle accounting for differences in naval battles
    if battle_type == 'sea':
        print(attacking_destroyers, defending_destroyers)

        if defending_destroyers == True:
            print("Route 1")
            remaining_attacking_units = remove_hits(attacking_units, defense_hits)
        else:
            print("Route 2")
            remaining_attacking_units = remove_hits(attacking_units, defense_naval_hits)
            remaining_attacking_units = remove_hits(remaining_attacking_units, defense_sub_hits, ignore_aircraft=True)
            remaining_attacking_units = remove_hits(remaining_attacking_units, defense_aircraft_hits, ignore_subs=True)

        if attacking_destroyers == True:
            print("Route 3")
            remaining_defending_units = remove_hits(defending_units, attack_hits)
        else:
            print("Route 4")
            remaining_defending_units = remove_hits(defending_units, attack_naval_hits)
            remaining_defending_units = remove_hits(remaining_defending_units, attack_sub_hits, ignore_aircraft=True)
            remaining_defending_units = remove_hits(remaining_defending_units, attack_aircraft_hits, ignore_subs=True)


    else:
        print("Route 5")
        # Land and amphibious battles
        remaining_attacking_units = remove_hits(attacking_units, defense_hits)
        remaining_defending_units = remove_hits(defending_units, attack_hits)

    print(f"Attack Units Post Removing Hits: {remaining_attacking_units}")
    print(f"Defense Units Post Removing Hits: {remaining_defending_units}")

    return attack_hits, defense_hits, remaining_attacking_units, remaining_defending_units, attacking_battleship_hits, defending_battleship_hits