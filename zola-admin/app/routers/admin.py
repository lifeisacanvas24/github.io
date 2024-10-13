from fastapi import APIRouter, Depends, Request, Form, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.models import UserCreate  # Updated import from models.py
from app.crud import create_user
import logging

router = APIRouter()

@router.get("/users/create-user/", response_class=HTMLResponse)
async def create_user_page(request: Request):
    return templates.TemplateResponse("create_user.html", {"request": request})

@router.post("/users/create-user/", response_model=None)  # Disable response model
async def create_user_route(
    request: Request,
    user: UserCreate,  # Using Pydantic model
    db: Session = Depends(get_db)
):
    try:
        created_user = create_user(db=db, user=user)  # Create the user
    except Exception as e:
        logging.error(f"Error creating user: {str(e)}")
        raise HTTPException(status_code=400, detail="User creation failed.")

        return RedirectResponse(url="/admin/", status_code=302)
