# Function to remove hits from units with the lowest IPC cost first
import json

# Define the units and their attributes
with open('static/units.json', 'r') as f:
    units = json.load(f)

def remove_hits(units_count, hits):
    remaining_units = units_count.copy()
    sorted_units = sorted(remaining_units.keys(), key=lambda unit: units[unit]["ipc"])

    for _ in range(hits):
        for unit in sorted_units:
            if remaining_units[unit] > 0:
                remaining_units[unit] -= 1
                break

    return remaining_units