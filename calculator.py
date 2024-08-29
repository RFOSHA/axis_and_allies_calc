from fastapi import FastAPI, Request, Form, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import json
from starlette.middleware.sessions import SessionMiddleware
from routers import home, simulate

# Load the units and their attributes from a JSON file
with open('static/units.json', 'r') as f:
    units = json.load(f)

# Create the FastAPI app instance
app = FastAPI()

# Set up Jinja2 templates, specifying the directory where HTML templates are stored
templates = Jinja2Templates(directory="templates")

# Mount the "static" directory to serve static files like CSS, JavaScript, and images
app.mount("/static", StaticFiles(directory="static"), name="static")

# Add session middleware to enable session management (e.g., storing saved battles in user sessions)
app.add_middleware(SessionMiddleware, secret_key='!secret')  # Replace '!secret' with a real secret key in production

# Create a router for handling routes, which will allow us to modularize the application
router = APIRouter()

# Include routers from other modules (home and simulate), which handle different parts of the application
app.include_router(home.router)
app.include_router(simulate.router)
