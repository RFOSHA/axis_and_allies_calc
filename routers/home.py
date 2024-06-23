from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
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
        request.session["save_battles"] = saved_battles
        return JSONResponse(status_code=200, content={"message": "Battle deleted successfully"})
    else:
        return JSONResponse(status_code=404, content={"message": "Battle not found"})