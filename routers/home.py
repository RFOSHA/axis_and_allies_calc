from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import json

# Define the units and their attributes
with open('static/units.json', 'r') as f:
    units = json.load(f)

templates = Jinja2Templates(directory="templates")

router = APIRouter()
@router.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "units": units})