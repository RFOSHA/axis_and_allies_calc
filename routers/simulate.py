from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from functs.run_multiple_battle_sim import run_multiple_battle_sims
from functs.plot_results import plot_results
from functs.plot_round_results import plot_round_results
import shutil
import os
from functs.resolved_in_previous_round import resolved_in_previous_round

templates = Jinja2Templates(directory="templates")

router = APIRouter()

# Formatting for outputs
def format_key(key):
    return ', '.join([f"{unit} {num}" for unit, num in key])

# Retrieving image paths to be sent to the results.html file
def get_image_paths(directory):
    return [os.path.join(directory, filename) for filename in os.listdir(directory) if filename.endswith(('png', 'jpg', 'jpeg', 'gif'))]

# Add the custom filter to the Jinja2 environment
templates.env.filters['format_key'] = format_key

@router.post("/simulate", response_class=HTMLResponse)
async def simulate_battle_endpoint(request: Request,
                                   battle_type: str = Form(...),
                                   attack_infantry: int = Form(0),
                                   attack_artillery: int = Form(0),
                                   attack_tank: int = Form(0),
                                   attack_fighter: int = Form(0),
                                   attack_bomber: int = Form(0),
                                   attack_submarine: int = Form(0),
                                   attack_destroyer: int = Form(0),
                                   attack_cruiser: int = Form(0),
                                   attack_carrier: int = Form(0),
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
                                   defense_carrier: int = Form(0),
                                   defense_battleship: int = Form(0),
                                   defense_aa: int = Form(0),
                                   number_of_simulations: int = Form(1000)):

    # Assigning the attacking units variable
    attacking_units = {
        "Infantry": attack_infantry,
        "Artillery": attack_artillery,
        "Tank": attack_tank,
        "Fighter": attack_fighter,
        "Bomber": attack_bomber,
        "Submarine": attack_submarine,
        "Destroyer": attack_destroyer,
        "Cruiser": attack_cruiser,
        "Carrier": attack_carrier,
        "Battleship": attack_battleship,
        "AA": attack_aa
    }

    # Assigning the defending units variable
    defending_units = {
        "Infantry": defense_infantry,
        "Artillery": defense_artillery,
        "Tank": defense_tank,
        "Fighter": defense_fighter,
        "Bomber": defense_bomber,
        "Submarine": defense_submarine,
        "Destroyer": defense_destroyer,
        "Cruiser": defense_cruiser,
        "Carrier": defense_carrier,
        "Battleship": defense_battleship,
        "AA": defense_aa
    }

    # Store the initial attacking and defending units and removing up the units that do not have any count
    initial_attacking_units = {unit: count for unit, count in attacking_units.items() if count > 0}
    initial_defending_units = {unit: count for unit, count in defending_units.items() if count > 0}

    # Running the battle simulations and storing results
    attacker_win_count, defender_win_count, ties, attacker_remaining_units_count, defender_remaining_units_count, battle_history_attacking_df, battle_history_defending_df = run_multiple_battle_sims(
        attacking_units, defending_units, number_of_simulations, battle_type)

    # Filter out attacking units with a quantity of 0
    filtered_attacker_remaining_units_count = {}

    # Loop to filter out the attacking units that are not present to clean up presentation on the graph
    for key_tuple, value in attacker_remaining_units_count.items():
        # Create a new tuple with items where the value is not zero
        new_key_tuple = tuple(item for item in key_tuple if item[1] != 0)
        # Add to the new dictionary
        filtered_attacker_remaining_units_count[new_key_tuple] = value

    # Filter out defending units with a quantity of 0
    filtered_defender_remaining_units_count = {}

    # Loop to filter out the defending units that are not present to clean up presentation on the graph
    for key_tuple, value in defender_remaining_units_count.items():
        # Create a new tuple with items where the value is not zero
        new_key_tuple = tuple(item for item in key_tuple if item[1] != 0)
        # Add to the new dictionary
        filtered_defender_remaining_units_count[new_key_tuple] = value

    #Set path for plots
    shutil.rmtree('static/attacker_rxr')
    os.makedirs('static/attacker_rxr')
    shutil.rmtree('static/defender_rxr')
    os.makedirs('static/defender_rxr')
    attacker_plot_html = plot_results(filtered_attacker_remaining_units_count, "Attacker Remaining Units Distribution")
    defender_plot_html = plot_results(filtered_defender_remaining_units_count, "Defender Remaining Units Distribution")
    attacker_rxr_plot_path = "static/attacker_rxr/attacker_rxr_plot"
    defender_rxr_plot_path = "static/defender_rxr/defender_rxr_plot"

    # Calculate the number of outcomes that were already resolved in a prior round
    battle_history_attacking_df = resolved_in_previous_round(battle_history_attacking_df, number_of_simulations)
    battle_history_defending_df = resolved_in_previous_round(battle_history_defending_df, number_of_simulations)

    # Create plots for the round by round outcomes
    attacker_round_plots = plot_round_results(battle_history_attacking_df, attacker_rxr_plot_path, number_of_simulations)
    defender_round_plots = plot_round_results(battle_history_defending_df, defender_rxr_plot_path, number_of_simulations)

    # Calculate win percentage to display at the top of the results page
    attacker_win_percentage = round((attacker_win_count / number_of_simulations) * 100, 2)
    defender_win_percentage = round((defender_win_count / number_of_simulations) * 100, 2)
    tie_percentage = round((ties / number_of_simulations) * 100, 2)

    # Form data to send back to the index.html after clicking the Simulate Another Battle button
    form_data = {
        "battle_type": battle_type,
        "attack_infantry": attack_infantry,
        "attack_artillery": attack_artillery,
        "attack_tank": attack_tank,
        "attack_fighter": attack_fighter,
        "attack_bomber": attack_bomber,
        "attack_submarine": attack_submarine,
        "attack_destroyer": attack_destroyer,
        "attack_cruiser": attack_cruiser,
        "attack_carrier": attack_carrier,
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
        "defense_carrier": defense_carrier,
        "defense_battleship": defense_battleship,
        "defense_aa": defense_aa,
        "number_of_simulations": number_of_simulations
    }

    # Return statement for the page that includes all variables to be used by jinja
    return templates.TemplateResponse("result.html", {
        "request": request,
        "attacker_win_count": attacker_win_count,
        "attacker_win_percentage": attacker_win_percentage,
        "defender_win_count": defender_win_count,
        "defender_win_percentage": defender_win_percentage,
        "ties": ties,
        "tie_percentage": tie_percentage,
        "attacker_remaining_units_count": dict(filtered_attacker_remaining_units_count),
        "defender_remaining_units_count": dict(filtered_defender_remaining_units_count),
        "attacker_plot_html": attacker_plot_html,
        "defender_plot_html": defender_plot_html,
        "initial_attacking_units": initial_attacking_units,
        "initial_defending_units": initial_defending_units,
        "form_data": form_data,
        "attacker_round_plots": attacker_round_plots,
        "defender_round_plots": defender_round_plots
    })