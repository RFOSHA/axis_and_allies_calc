from fastapi import FastAPI, Request, Form, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from collections import defaultdict
import random
import matplotlib.pyplot as plt
import os
import json
from functs.run_multiple_battle_sim import run_multiple_battle_sims
from functs.plot_results import plot_results
from routers import home, simulate

# Define the units and their attributes
with open('static/units.json', 'r') as f:
    units = json.load(f)

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

router = APIRouter()

app.include_router(home.router)
app.include_router(simulate.router)


