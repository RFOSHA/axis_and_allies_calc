from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from functs.run_multiple_battle_sim import run_multiple_battle_sims

import json

# Define the units and their attributes
with open('static/units.json', 'r') as f:
    units = json.load(f)

templates = Jinja2Templates(directory="templates")

router = APIRouter()

#Path for index (home) page
@router.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    form_data = dict(request.query_params)
    saved_battles = request.session.get("saved_battles", {})
    return templates.TemplateResponse("index.html", {"request": request, "units": units, "form_data": form_data, "saved_battles": saved_battles})

# Create an object to store saved battle configurations
class BattleData(BaseModel):
    name: str
    data: dict

# New route for Battle Rules page
@router.get("/battle-rules", response_class=HTMLResponse)
async def get_battle_rules(request: Request):
    return templates.TemplateResponse("battle_rules.html", {"request": request})

# Route to save a battle configuration to local storage to be retrieved later
@router.post("/save_battle")
async def save_battle(request: Request, battle: BattleData):
    saved_battles = request.session.get("saved_battles", {})
    saved_battles[battle.name] = battle.data
    request.session["saved_battles"] = saved_battles
    return JSONResponse(status_code=200, content={"message": "Battle saved successfully"})

# Route to retrieve a previously saved battle
@router.get("/load_battle")
async def load_battle(request: Request, name: str):
    saved_battles = request.session.get("saved_battles", {})
    battle_data = saved_battles.get(name, {})
    return JSONResponse(status_code=200, content=battle_data)

# Route to delete a previously saved battle
@router.delete("/delete_battle")
async def delete_battle(request: Request, name: str):
    saved_battles = request.session.get("saved_battles", {})
    if name in saved_battles:
        del saved_battles[name]
        request.session["saved_battles"] = saved_battles
        return JSONResponse(status_code=200, content={"message": "Battle deleted successfully"})
    else:
        return JSONResponse(status_code=404, content={"message": "Battle not found"})

# Route to do a quick simulation that keeps the user on the index.html page
@router.post("/quick_simulate", response_class=HTMLResponse)
async def quick_simulate(request: Request,
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
                         number_of_simulations: int = Form(100)):

# Create the attacking units dictionary from form inputs
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

# Create the defending units dictionary from form inputs
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

    # Running the battle simulations and storing results
    attacker_win_count, defender_win_count, ties, attacker_remaining_units_count, defender_remaining_units_count, battle_history_attacking_df, battle_history_defending_df = run_multiple_battle_sims(
        attacking_units, defending_units, number_of_simulations, battle_type)

    # Calculate win percentage to display at the top of the results page and convert to string to add the % for the JS injection
    attacker_win_percentage = round((attacker_win_count / number_of_simulations) * 100, 2)
    defender_win_percentage = round((defender_win_count / number_of_simulations) * 100, 2)
    tie_percentage = round((ties / number_of_simulations) * 100, 2)

    # Return data for the JS to use to inject updated HTML
    return JSONResponse({
        "attacker_win_percentage": attacker_win_percentage,
        "defender_win_percentage": defender_win_percentage,
        "tie_percentage": tie_percentage,
    })