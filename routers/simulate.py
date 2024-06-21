from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from functs.run_multiple_battle_sim import run_multiple_battle_sims
from functs.plot_results import plot_results
from collections import defaultdict

templates = Jinja2Templates(directory="templates")

router = APIRouter()

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

    initial_attacking_units = {unit: count for unit, count in attacking_units.items() if count > 0}
    initial_defending_units = {unit: count for unit, count in defending_units.items() if count > 0}

    attacker_win_count, defender_win_count, ties, attacker_remaining_units_count, defender_remaining_units_count = run_multiple_battle_sims(
        attacking_units, defending_units, number_of_simulations)

    attacker_plot_path = "static/attacker_plot.png"
    defender_plot_path = "static/defender_plot.png"

    plot_results(attacker_remaining_units_count, "Attacker Remaining Units Distribution", attacker_plot_path)
    plot_results(defender_remaining_units_count, "Defender Remaining Units Distribution", defender_plot_path)

    return templates.TemplateResponse("result.html", {
        "request": request,
        "attacker_win_count": attacker_win_count,
        "defender_win_count": defender_win_count,
        "ties": ties,
        "attacker_remaining_units_count": dict(attacker_remaining_units_count),
        "defender_remaining_units_count": dict(defender_remaining_units_count),
        "attacker_plot_path": "/" + attacker_plot_path,
        "defender_plot_path": "/" + defender_plot_path,
        "initial_attacking_units": initial_attacking_units,
        "initial_defending_units": initial_defending_units
    })