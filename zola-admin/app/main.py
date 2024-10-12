#app/main.py
from fastapi import FastAPI, Depends, Request, Form, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.auth import authenticate_user, get_current_user
from app.crud import create_user
from app.init_db import init_db
import logging
from app.routers import user as user_router
from app.routers import admin as admin_router
from app.database import Base, engine
from app.dependencies import get_db
from fastapi.staticfiles import StaticFiles

logging.basicConfig(level=logging.INFO)
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

app = FastAPI()

app.include_router(admin_router.router, prefix="/admin", tags=["admin"])
app.include_router(user_router.router, prefix="/admin", tags=["users"])

@app.middleware("http")
async def add_user_to_request(request: Request, call_next):
    try:
        request.state.user = await get_current_user(request)
    except HTTPException:
        request.state.user = None

    response = await call_next(request)
    return response

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

@app.on_event("startup")
def on_startup():
    init_db()

Base.metadata.create_all(bind=engine)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Admin Dashboard"}

@app.get("/admin/")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "user": request.state.user})

@app.post("/login/")
def login(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = authenticate_user(username, password, db)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    response = RedirectResponse(url="/dashboard/", status_code=302)
    response.set_cookie(key="username", value=user.username)
    return response

@app.get("/dashboard/")
def dashboard(request: Request):
    if not request.state.user:
        return RedirectResponse(url="/admin/")
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/logout/")
def logout():
    response = RedirectResponse(url="/logout-confirmation/")
    response.delete_cookie("username")
    return response

@app.get("/logout-confirmation/", response_class=HTMLResponse)
async def logout_confirmation(request: Request):
    return templates.TemplateResponse("logout_confirmation.html", {"request": request})
