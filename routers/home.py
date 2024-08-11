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

@router.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    form_data = dict(request.query_params)
    saved_battles = request.session.get("saved_battles", {})
    return templates.TemplateResponse("index.html", {"request": request, "units": units, "form_data": form_data, "saved_battles": saved_battles})

class BattleData(BaseModel):
    name: str
    data: dict

@router.post("/save_battle")
async def save_battle(request: Request, battle: BattleData):
    saved_battles = request.session.get("saved_battles", {})
    saved_battles[battle.name] = battle.data
    request.session["saved_battles"] = saved_battles
    return JSONResponse(status_code=200, content={"message": "Battle saved successfully"})

@router.get("/load_battle")
async def load_battle(request: Request, name: str):
    saved_battles = request.session.get("saved_battles", {})
    battle_data = saved_battles.get(name, {})
    return JSONResponse(status_code=200, content=battle_data)

@router.delete("/delete_battle")
async def delete_battle(request: Request, name: str):
    saved_battles = request.session.get("saved_battles", {})
    if name in saved_battles:
        del saved_battles[name]
        request.session["saved_battles"] = saved_battles
        return JSONResponse(status_code=200, content={"message": "Battle deleted successfully"})
    else:
        return JSONResponse(status_code=404, content={"message": "Battle not found"})

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
        "Carrier": attack_carrier,
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
        "Carrier": defense_carrier,
        "Battleship": defense_battleship,
        "AA": defense_aa
    }

    form_data = dict(request.query_params)
    saved_battles = request.session.get("saved_battles", {})

    attacker_win_count, defender_win_count, ties, attacker_remaining_units_count, defender_remaining_units_count, battle_history_attacking_df, battle_history_defending_df = run_multiple_battle_sims(
        attacking_units, defending_units, number_of_simulations, battle_type)

    return JSONResponse({
        "attacker_win_count": attacker_win_count,
        "defender_win_count": defender_win_count,
        "ties": ties,
    })