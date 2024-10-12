#app/routers/admin.py
from fastapi import APIRouter, Depends, Request, HTTPException, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from app.auth import get_current_user
from app.models import User
from app.database import get_db
from app import schemas, crud
from sqlalchemy.orm import Session
from starlette.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")  # Ensure this path is correct

# User Creation Page - GET
@router.get("/users/create-user/", response_class=HTMLResponse)
def create_user_page(request: Request, current_user: User = Depends(get_current_user)):
    if not current_user.is_authenticated:
        return RedirectResponse(url="/admin/")
    return templates.TemplateResponse("create_user.html", {"request": request, "title": "Create User"})

# Create New User - POST
@router.post("/users/create-user-post/")
def create_new_user(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    if not username or not password:
        return templates.TemplateResponse("create_user.html", {"request": request, "error": "Username and password must be provided"})

    new_user_data = schemas.UserCreate(username=username, password=password)
    try:
        db_user = crud.create_user(db, user=new_user_data)
        # After creating the user, redirect to a success page
        return templates.TemplateResponse("create_user_success.html", {"request": request, "username": username})
    except Exception as e:
        return templates.TemplateResponse("create_user.html", {"request": request, "error": str(e)})
