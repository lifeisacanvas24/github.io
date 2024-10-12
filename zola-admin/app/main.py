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

logging.basicConfig(level=logging.INFO)
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Example async context manager for lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()  # Initialize the database connection or other startup tasks
    yield  # This is where the app runs
    # Cleanup can be done here if necessary

# Async context manager for database session
@asynccontextmanager
async def get_db_session():
    db = next(get_db())
    try:
        yield db
    finally:
        db.close()

app = FastAPI(lifespan=lifespan)

app.include_router(admin_router.router, prefix="/admin", tags=["admin"])
app.include_router(user_router.router, prefix="/admin", tags=["users"])

# Middleware to add user information to the request
class AddUserMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        async with get_db_session() as db:
            try:
                user_id = get_user_id_from_cookie(request.cookies.get("user_id"))
                if user_id:
                    request.state.user = await get_current_user(db=db, user_id=user_id)
                    logging.info(f"User ID retrieved from cookie: {user_id}")
                    if request.state.user:
                        logging.info(f"User retrieved: {request.state.user.username}")
                else:
                    request.state.user = None
            except HTTPException as e:
                logging.error(f"HTTPException in middleware: {e.detail}")
                request.state.user = None
            except Exception as e:
                logging.error(f"Error in middleware: {e}")
                request.state.user = None

        response = await call_next(request)
        return response

# Add middleware to the app
app.add_middleware(AddUserMiddleware)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Admin Dashboard"}

@app.get("/admin/")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "user": request.state.user})

@app.post("/login/")
async def login(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = authenticate_user(username, password, db)
    if not user:
        logging.warning(f"Failed login attempt for user: {username}")
        return templates.TemplateResponse("login.html", {
            "request": request, "error": "Invalid credentials, please try again."
        })

    # Set the user in cookie and redirect to the dashboard
    response = RedirectResponse(url="/dashboard/", status_code=302)
    response.set_cookie(key="user_id", value=str(user.id), httponly=True, secure=False, samesite="Lax")
    return response

@app.get("/dashboard/")
async def dashboard(request: Request):
    if not request.state.user:
        return RedirectResponse(url="/admin/")

    # Log current user info
    logging.info(f"Current user: {request.state.user.username}")

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user": request.state.user  # Pass user context
    })

@app.get("/logout/")
async def logout():
    response = RedirectResponse(url="/logout-confirmation/")
    response.delete_cookie("user_id")  # Remove the user_id cookie
    return response

@app.get("/logout-confirmation/", response_class=HTMLResponse)
async def logout_confirmation(request: Request):
    return templates.TemplateResponse("logout_confirmation.html", {
        "request": request,
        "user": request.state.user  # Pass the user object to the template
    })
