from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from collections import defaultdict
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

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

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

# Function to run the full battle simulation until one side has no units left
def run_battle_simulation(attacking_units, defending_units):
    while sum(attacking_units.values()) > 0 and sum(defending_units.values()) > 0:
        attack_hits, defense_hits, attacking_units, defending_units = simulate_battle(attacking_units, defending_units)

    if sum(attacking_units.values()) == 0 and sum(defending_units.values()) == 0:
        outcome = "tie"
    elif sum(attacking_units.values()) == 0:
        outcome = "defender win"
    else:
        outcome = "attacker win"

    return outcome, attacking_units, defending_units

# Function to run multiple battle simulations and capture remaining units
def run_multiple_battle_sims(attacking_units, defending_units, num_of_simulations):
    attacker_win_count = 0
    defender_win_count = 0
    ties = 0
    attacker_remaining_units_count = defaultdict(int)
    defender_remaining_units_count = defaultdict(int)

    for _ in range(num_of_simulations):
        outcome, remaining_attacking_units, remaining_defending_units = run_battle_simulation(attacking_units.copy(), defending_units.copy())

        if outcome == "tie":
            ties += 1
        elif outcome == "defender win":
            defender_win_count += 1
            defender_remaining_units_count[tuple(remaining_defending_units.items())] += 1
        else:
            attacker_win_count += 1
            attacker_remaining_units_count[tuple(remaining_attacking_units.items())] += 1

    return attacker_win_count, defender_win_count, ties, attacker_remaining_units_count, defender_remaining_units_count

@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "units": units})

@app.post("/simulate", response_class=HTMLResponse)
async def simulate_battle_endpoint(request: Request,
                                   attack_infantry: int = Form(0),
                                   attack_artillery: int = Form(0),
                                   attack_tank: int = Form(0),
                                   attack_fighter: int = Form(0),
                                   attack_bomber: int = Form(0),
                                   attack_submarine: int = Form(0),
                                   attack_destroyer: int = Form(0),
                                   attack_cruiser: int = Form(0),
                                   attack_aircraft_carrier: int = Form(0),
                                   attack_battleship: int = Form(0),
                                   defense_infantry: int = Form(0),
                                   defense_artillery: int = Form(0),
                                   defense_tank: int = Form(0),
                                   defense_fighter: int = Form(0),
                                   defense_bomber: int = Form(0),
                                   defense_submarine: int = Form(0),
                                   defense_destroyer: int = Form(0),
                                   defense_cruiser: int = Form(0),
                                   defense_aircraft_carrier: int = Form(0),
                                   defense_battleship: int = Form(0),
                                   number_of_simulations: int = Form(1)):

    attacking_units = {
        "Infantry": attack_infantry,
        "Artillery": attack_artillery,
        "Tank": attack_tank,
        "Fighter": attack_fighter,
        "Bomber": attack_bomber,
        "Submarine": attack_submarine,
        "Destroyer": attack_destroyer,
        "Cruiser": attack_cruiser,
        "Aircraft Carrier": attack_aircraft_carrier,
        "Battleship": attack_battleship
    }

    defending_units = {
        "Infantry": defense_infantry,
        "Artillery": defense_artillery,
        "Tank": defense_tank,
        "Fighter": defense_fighter,
        "Bomber": defense_bomber,
        "Submarine": defense_submarine,
        "Destroyer": defense_destroyer,
        "Cruiser": defense_cruiser,
        "Aircraft Carrier": defense_aircraft_carrier,
        "Battleship": defense_battleship
    }

    attacker_win_count, defender_win_count, ties, attacker_remaining_units_count, defender_remaining_units_count = run_multiple_battle_sims(attacking_units, defending_units, number_of_simulations)

    return templates.TemplateResponse("result.html", {
        "request": request,
        "attacker_win_count": attacker_win_count,
        "defender_win_count": defender_win_count,
        "ties": ties,
        "attacker_remaining_units_count": dict(attacker_remaining_units_count),
        "defender_remaining_units_count": dict(defender_remaining_units_count)
    })
