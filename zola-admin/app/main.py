from fastapi import FastAPI, Depends, Request, Form, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.auth import authenticate_user, get_current_user, get_user_id_from_cookie
from app.crud import create_user
from app.init_db import init_db
from app.dependencies import get_db
from app.routers import user as user_router
from app.routers import admin as admin_router
from app.database import Base, engine
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from starlette.middleware.base import BaseHTTPMiddleware
import logging

# Logging configuration
logging.basicConfig(level=logging.INFO)
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()  # Initialize database connection or other startup tasks
    yield  # This is where the app runs

@asynccontextmanager
async def get_db_session():
    """Session generator for database interactions"""
    db = next(get_db())  # Use the get_db() dependency for getting the session
    try:
        yield db
    finally:
        db.close()

app = FastAPI(lifespan=lifespan)

# Include routers
app.include_router(admin_router.router, prefix="/admin", tags=["admin"])
app.include_router(user_router.router, prefix="/users", tags=["users"])

class AddUserMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        async with get_db_session() as db:
            user_id = get_user_id_from_cookie(request.cookies.get("user_id"))
            if user_id:
                try:
                    request.state.user = await get_current_user(db=db, user_id=user_id)  # Use await here
                    logging.info(f"User retrieved: {request.state.user.username}")
                except HTTPException as e:
                    logging.error(f"HTTPException in middleware: {e.detail}")
                    request.state.user = None
            else:
                logging.warning("No user_id cookie found.")
                request.state.user = None

        response = await call_next(request)
        return response

app.add_middleware(AddUserMiddleware)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Admin Dashboard"}

@app.get("/admin/")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "user": request.state.user})

@app.post("/login/", response_model=None)
async def login(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = authenticate_user(username, password, db)
    if not user:
        logging.warning(f"Failed login attempt for user: {username}")
        return templates.TemplateResponse("login.html", {
            "request": request, "error": "Invalid credentials, please try again."
        })

    response = RedirectResponse(url="/dashboard/", status_code=302)
    response.set_cookie(key="user_id", value=str(user.id), httponly=True, secure=False, samesite="Lax")
    return response

@app.get("/dashboard/", response_model=None)
async def dashboard(request: Request):
    if not request.state.user:
        return RedirectResponse(url="/admin/")

    logging.info(f"Current user: {request.state.user.username}")
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user": request.state.user
    })

@app.get("/logout/", response_model=None)
async def logout():
    response = RedirectResponse(url="/logout-confirmation/")
    response.delete_cookie("user_id")
    return response

@app.get("/logout-confirmation/", response_class=HTMLResponse)
async def logout_confirmation(request: Request):
    return templates.TemplateResponse("logout_confirmation.html", {
        "request": request,
        "user": request.state.user
    })
