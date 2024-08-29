import json

# Load the units and their attributes from a JSON file
with open('static/units.json', 'r') as f:
    units = json.load(f)


# Function to remove hits from units based on the lowest IPC (cost) first
def remove_hits(units_count, hits, ignore_subs=False, ignore_aircraft=False):
    # Create a copy of the units_count dictionary to avoid modifying the original
    remaining_units = units_count.copy()

    # Sort units by their IPC (cost) in ascending order
    sorted_units = sorted(remaining_units.keys(), key=lambda unit: units[unit]["ipc"])

    # Apply the specified number of hits
    for _ in range(hits):
        for unit in sorted_units:
            # Skip submarines if ignore_subs is True
            if unit == 'Submarine' and ignore_subs:
                continue
            # Skip aircraft (Fighter and Bomber) if ignore_aircraft is True
            elif unit in ["Fighter", "Bomber"] and ignore_aircraft:
                continue
            # If the current unit is available (count > 0), reduce its count by 1
            elif remaining_units[unit] > 0:
                remaining_units[unit] -= 1
                break  # Break out of the loop once a hit is applied

    # Return the updated units_count dictionary after applying the hits
    return remaining_units
