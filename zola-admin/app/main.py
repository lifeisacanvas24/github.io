# app/main.py
from fastapi.middleware.cors import CORSMiddleware  # Ensure this is included
from fastapi import FastAPI, Depends, Request, Form, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager  # Add this line
import logging

# Import your auth, crud, database, and routers here
from app.auth import authenticate_user, get_current_user, get_user_id_from_cookie
from app.crud import create_user
from app.database import init_db, get_db
from app.routers import user as user_router
from app.routers import admin as admin_router

# Logging configuration
logging.basicConfig(level=logging.INFO)
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Initialize Jinja2 templates
templates = Jinja2Templates(directory="app/templates")

# Create FastAPI app
app = FastAPI()

# Async context manager to handle the lifespan of the app (e.g., database connections)
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()  # Initialize the database on app startup
    yield  # This is where the app runs


# Middleware to log and retrieve user from cookie
@app.middleware("http")
async def dispatch(request: Request, call_next):
    try:
        # Allow access to the login page
        if request.url.path == "/admin/" or request.url.path == "/login/":
            response = await call_next(request)
            return response

        # Attempt to get the user from cookies
        user_id = get_user_id_from_cookie(request.cookies.get("user_id"))
        request.state.user = await get_current_user(get_db(), user_id)

        response = await call_next(request)
        return response
    except Exception as e:
        logging.error(f"Error in middleware: {str(e)}")
        raise HTTPException(status_code=403, detail="Not authenticated")

# Include admin routes
app.include_router(admin_router.router, prefix="/admin", tags=["admin"])
app.include_router(user_router.router, prefix="/users", tags=["users"])

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this as necessary
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (e.g., CSS, JavaScript)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Root route
@app.get("/")
async def read_root():
    return {"message": "Welcome to the Admin Dashboard"}

# Admin login page
@app.get("/admin/")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "title": "Admin Login"})

# Admin login form submission
@app.post("/login/", response_model=None)
async def login(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = authenticate_user(username, password, db)
    if not user:
        logging.warning(f"Failed login attempt for user: {username}")
        return templates.TemplateResponse("login.html", {
            "request": request,
            "title": "Admin Login",
            "error": "Invalid credentials, please try again."
        })

    response = RedirectResponse(url="/dashboard/", status_code=302)
    response.set_cookie(key="user_id", value=str(user.id), httponly=True, secure=False, samesite="Lax")
    logging.info(f"User logged in: {username}, user_id set in cookie.")
    return response

# Admin dashboard page
@app.get("/dashboard/", response_model=None)
async def dashboard(request: Request):
    if request.state.user is None:
        return RedirectResponse(url="/admin/")

    logging.info(f"Current user: {request.state.user.username}")
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user": request.state.user,
        "title": "Admin Dashboard"
    })

# Logout functionality
@app.get("/logout/", response_model=None)
async def logout():
    response = RedirectResponse(url="/logout-confirmation/")
    response.delete_cookie("user_id")
    return response

# Logout confirmation page
@app.get("/logout-confirmation/", response_class=HTMLResponse)
async def logout_confirmation(request: Request):
    return templates.TemplateResponse("logout_confirmation.html", {
        "request": request,
        "title": "Logout Confirmation",
        "user": request.state.user
    })
