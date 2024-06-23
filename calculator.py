from fastapi import FastAPI, Request, Form, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import json
from starlette.middleware.sessions import SessionMiddleware
from routers import home, simulate

# Define the units and their attributes
with open('static/units.json', 'r') as f:
    units = json.load(f)

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Add session middleware to enable storing saved battles
app.add_middleware(SessionMiddleware, secret_key='!secret')

router = APIRouter()

app.include_router(home.router)
app.include_router(simulate.router)


