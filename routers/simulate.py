from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from functs.run_multiple_battle_sim import run_multiple_battle_sims
from functs.plot_results import plot_results
from collections import defaultdict

templates = Jinja2Templates(directory="templates")

router = APIRouter()

def format_key(key):
    return ', '.join([f"{unit} {num}" for unit, num in key])

# Add the custom filter to the Jinja2 environment
templates.env.filters['format_key'] = format_key

@router.post("/simulate", response_class=HTMLResponse)
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
                                   attack_aa: int = Form(0),
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
                                   defense_aa: int = Form(0),
                                   number_of_simulations: int = Form(1000)):
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
        "Battleship": attack_battleship,
        "AA": attack_aa
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
        "Battleship": defense_battleship,
        "AA": defense_aa
    }

    print(defending_units)
    print(defense_aa)

    initial_attacking_units = {unit: count for unit, count in attacking_units.items() if count > 0}
    initial_defending_units = {unit: count for unit, count in defending_units.items() if count > 0}

    attacker_win_count, defender_win_count, ties, attacker_remaining_units_count, defender_remaining_units_count = run_multiple_battle_sims(
        attacking_units, defending_units, number_of_simulations)

    # Filter out units with a quantity of 0
    filtered_attacker_remaining_units_count = {}

    for key_tuple, value in attacker_remaining_units_count.items():
        # Create a new tuple with items where the value is not zero
        new_key_tuple = tuple(item for item in key_tuple if item[1] != 0)
        # Add to the new dictionary
        filtered_attacker_remaining_units_count[new_key_tuple] = value

    filtered_defender_remaining_units_count = {}

    for key_tuple, value in defender_remaining_units_count.items():
        # Create a new tuple with items where the value is not zero
        new_key_tuple = tuple(item for item in key_tuple if item[1] != 0)
        # Add to the new dictionary
        filtered_defender_remaining_units_count[new_key_tuple] = value

    # Iterate through the dictionary
    list_defender_remaining_units_count = [] = []
    for key, value in filtered_defender_remaining_units_count.items():
        # Create a string for the current key
        print(key, value)
        key_str = ', '.join([f"{unit} {num}" for unit, num in key])
        # Append the formatted string to the list
        list_defender_remaining_units_count.append(f"{key_str}: {value}")

    # Join the formatted components into a single string
    # str_defender_remaining_units_count = ', '.join(list_defender_remaining_units_count)

    attacker_plot_path = "static/attacker_plot.png"
    defender_plot_path = "static/defender_plot.png"

    plot_results(filtered_attacker_remaining_units_count, "Attacker Remaining Units Distribution", attacker_plot_path)
    plot_results(filtered_defender_remaining_units_count, "Defender Remaining Units Distribution", defender_plot_path)

    form_data = {
        "attack_infantry": attack_infantry,
        "attack_artillery": attack_artillery,
        "attack_tank": attack_tank,
        "attack_fighter": attack_fighter,
        "attack_bomber": attack_bomber,
        "attack_submarine": attack_submarine,
        "attack_destroyer": attack_destroyer,
        "attack_cruiser": attack_cruiser,
        "attack_aircraft_carrier": attack_aircraft_carrier,
        "attack_battleship": attack_battleship,
        "attack_aa": attack_aa,
        "defense_infantry": defense_infantry,
        "defense_artillery": defense_artillery,
        "defense_tank": defense_tank,
        "defense_fighter": defense_fighter,
        "defense_bomber": defense_bomber,
        "defense_submarine": defense_submarine,
        "defense_destroyer": defense_destroyer,
        "defense_cruiser": defense_cruiser,
        "defense_aircraft_carrier": defense_aircraft_carrier,
        "defense_battleship": defense_battleship,
        "defense_aa": defense_aa,
        "number_of_simulations": number_of_simulations
    }

    return templates.TemplateResponse("result.html", {
        "request": request,
        "attacker_win_count": attacker_win_count,
        "defender_win_count": defender_win_count,
        "ties": ties,
        "attacker_remaining_units_count": dict(filtered_attacker_remaining_units_count),
        "defender_remaining_units_count": dict(filtered_defender_remaining_units_count),
        "attacker_plot_path": "/" + attacker_plot_path,
        "defender_plot_path": "/" + defender_plot_path,
        "initial_attacking_units": initial_attacking_units,
        "initial_defending_units": initial_defending_units,
        "form_data": form_data
    })