# app/routers/user.py
from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db
from app.dependencies import get_current_user
from app.models import User

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/users/list")
async def list_users(request: Request, db: Session = Depends(get_db)):
    users = db.query(User).all()
    success_message = "User list retrieved successfully!"
    return templates.TemplateResponse("list_users.html", {"request": request, "users": users, "success_message": success_message})

@router.get("/users/create-user")
def create_user_page(request: Request):
    return templates.TemplateResponse("create_user.html", {"request": request})

@router.post("/users/create-user")
def create_user(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user_data = schemas.UserCreate(username=username, password=password)
    new_user = crud.create_user(db, user_data)
    return RedirectResponse(url="/users/list?success=User%20created%20successfully", status_code=303)

@router.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.delete("/users/delete/{user_id}", response_model=dict)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    crud.delete_user(db, user_id)
    return RedirectResponse(url="/users/list?success=User%20deleted%20successfully", status_code=303)
