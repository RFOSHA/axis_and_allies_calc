import random
from collections import defaultdict

# Define the units and their attributes
units = {
    "Infantry": {"attack": 1, "defense": 2, "ipc": 3},
    "Artillery": {"attack": 2, "defense": 2, "ipc": 4},
    "Tank": {"attack": 3, "defense": 3, "ipc": 5},
    "Fighter": {"attack": 3, "defense": 4, "ipc": 10},
    "Bomber": {"attack": 4, "defense": 1, "ipc": 12},
    "Submarine": {"attack": 2, "defense": 1, "ipc": 6},
    "Destroyer": {"attack": 2, "defense": 2, "ipc": 8},
    "Cruiser": {"attack": 3, "defense": 3, "ipc": 12},
    "Aircraft Carrier": {"attack": 1, "defense": 2, "ipc": 14},
    "Battleship": {"attack": 4, "defense": 4, "ipc": 20},
    "Anti-Aircraft": {"attack": 0, "defense": 1, "ipc": 5},
}

# Function to remove hits from units with the lowest IPC cost first
def remove_hits(units_count, hits):
    remaining_units = units_count.copy()
    sorted_units = sorted(remaining_units.keys(), key=lambda unit: units[unit]["ipc"])

    for _ in range(hits):
        for unit in sorted_units:
            if remaining_units[unit] > 0:
                remaining_units[unit] -= 1
                break

    return remaining_units

# Function to simulate a battle round
def simulate_battle(attacking_units, defending_units):
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
            # print(unit, attack_value, roll)
            if roll <= attack_value:
                attack_hits += 1

    # Roll for each defending unit
    for unit, count in defending_units.items():
        for _ in range(count):
            defense_value = units[unit]["defense"]
            roll = random.randint(1, 6)
            # print(unit, defense_value, roll)
            if roll <= defense_value:
                defense_hits += 1

    # Calculate remaining units after hits
    remaining_attacking_units = remove_hits(attacking_units, defense_hits)
    remaining_defending_units = remove_hits(defending_units, attack_hits)

    return attack_hits, defense_hits, remaining_attacking_units, remaining_defending_units

# Function to run the full battle simulation until one side has no units left
def run_battle_simulation(attacking_units, defending_units):
    round_number = 1
    initial_attacking_units = attacking_units.copy()
    initial_defending_units = defending_units.copy()

    while sum(attacking_units.values()) > 0 and sum(defending_units.values()) > 0:
        print(f"Round {round_number}:")
        print(f"Start of round attacking units: {attacking_units}")
        print(f"Start of round defending units: {defending_units}")
        attack_hits, defense_hits, attacking_units, defending_units = simulate_battle(attacking_units, defending_units)
        print(f"Attacker hits: {attack_hits}")
        print(f"Defender hits: {defense_hits}")
        print(f"Remaining attacking units: {attacking_units}")
        print(f"Remaining defending units: {defending_units}")
        print()
        round_number += 1

    if sum(attacking_units.values()) == 0 and sum(defending_units.values()) == 0:
        print("Tie: all attacking and defending units destroyed")
        outcome = "tie"
    elif sum(attacking_units.values()) == 0:
        print(f"Defender wins! Remaining units: {defending_units}")
        outcome = "defender win"
    else:
        print(f"Attacker wins! Remaining units: {attacking_units}")
        outcome = "attacker win"

    return outcome, attacking_units, defending_units

def run_multiple_battle_sims(attacking_units, defending_units, num_of_simulations):
    simulation_num = 1
    attacker_win_count = 0
    defender_win_count = 0
    ties = 0
    attacker_remaining_units_count = defaultdict(int)
    defender_remaining_units_count = defaultdict(int)

    while simulation_num <= num_of_simulations:
        print(f"Simulation {simulation_num}")
        simulation_num += 1

        outcome, remaining_attacking_units, remaining_defending_units = run_battle_simulation(attacking_units, defending_units)
        if outcome == "tie":
            ties += 1
        elif outcome == "defender win":
            defender_win_count += 1
            # print(remaining_defending_units)
            # print(remaining_defending_units.items())
            defender_remaining_units_count[tuple(remaining_defending_units.items())] += 1
            attacker_remaining_units_count[tuple(remaining_attacking_units.items())] += 1
        else:
            attacker_win_count += 1
            # print(remaining_attacking_units)
            # print(remaining_attacking_units.items())
            attacker_remaining_units_count[tuple(remaining_attacking_units.items())] += 1
            defender_remaining_units_count[tuple(remaining_defending_units.items())] += 1

    print(f"Number of attacker wins: {attacker_win_count}")
    print(f"Number of defender wins: {defender_win_count}")
    print(f"Number of ties: {ties}")

    print("Attacker remaining units after each win:")
    for units, count in attacker_remaining_units_count.items():
        print(dict(units), count)

    print("Defender remaining units after each win:")
    for units, count in defender_remaining_units_count.items():
        print(dict(units), count)



# Example usage
attack_infantry = 2
attack_artillery = 1
attack_tank = 0
attack_fighter = 0
attack_bomber = 0
attack_submarine = 0
attack_destroyer = 0
attack_cruiser = 0
attack_aircraft_carrier = 0
attack_battleship = 0

defense_infantry = 2
defense_artillery = 0
defense_tank = 0
defense_fighter = 0
defense_bomber = 0
defense_submarine = 0
defense_destroyer = 0
defense_cruiser = 0
defense_aircraft_carrier = 0
defense_battleship = 0

number_of_simulations = 10

attacking_units = {"Infantry": attack_infantry,
                   "Tank": attack_tank,
                   "Artillery": attack_artillery,
                   "Fighter": attack_fighter,
                   "Bomber": attack_bomber,
                   "Submarine": attack_submarine,
                   "Destroyer": attack_destroyer,
                   "Cruiser": attack_cruiser,
                   "Aircraft Carrier": attack_aircraft_carrier,
                   "Battleship": attack_battleship}

defending_units = {"Infantry": defense_infantry,
                   "Tank": defense_tank,
                   "Artillery": defense_artillery,
                   "Fighter": defense_fighter,
                   "Bomber": defense_bomber,
                   "Submarine": defense_submarine,
                   "Destroyer": defense_destroyer,
                   "Cruiser": defense_cruiser,
                   "Aircraft Carrier": defense_aircraft_carrier,
                   "Battleship": defense_battleship}

run_multiple_battle_sims(attacking_units, defending_units, number_of_simulations)

# attack_hits, defense_hits, remaining_attacking_units, remaining_defending_units = simulate_battle(attacking_units, defending_units)
# print(f"Attacker hits: {attack_hits}")
# print(f"Defender hits: {defense_hits}")
# print(f"Remaining attacking units: {remaining_attacking_units}")
# print(f"Remaining defending units: {remaining_defending_units}")
