import random

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

    # Roll for each attacking unit
    for unit, count in attacking_units.items():
        for _ in range(count):
            attack_value = units[unit]["attack"]
            roll = random.randint(1, 6)
            if roll <= attack_value:
                attack_hits += 1

    # Roll for each defending unit
    for unit, count in defending_units.items():
        for _ in range(count):
            defense_value = units[unit]["defense"]
            roll = random.randint(1, 6)
            if roll <= defense_value:
                defense_hits += 1

    # Calculate remaining units after hits
    remaining_attacking_units = remove_hits(attacking_units, defense_hits)
    remaining_defending_units = remove_hits(defending_units, attack_hits)

    return attack_hits, defense_hits, remaining_attacking_units, remaining_defending_units

# Example usage
attack_infantry = 0
attack_artillery = 0
attack_tank = 0
attack_fighter = 0
attack_bomber = 4
attack_submarine = 0
attack_destroyer = 0
attack_cruiser = 0
attack_aircraft_carrier = 0
attack_battleship = 0

defense_infantry = 1
defense_artillery = 1
defense_tank = 1
defense_fighter = 1
defense_bomber = 1
defense_submarine = 0
defense_destroyer = 0
defense_cruiser = 0
defense_aircraft_carrier = 0
defense_battleship = 0

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

attack_hits, defense_hits, remaining_attacking_units, remaining_defending_units = simulate_battle(attacking_units, defending_units)
print(f"Attacker hits: {attack_hits}")
print(f"Defender hits: {defense_hits}")
print(f"Remaining attacking units: {remaining_attacking_units}")
print(f"Remaining defending units: {remaining_defending_units}")
