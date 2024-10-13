#!/bin/bash

# Create the folder structure
mkdir -p zola-admin/app/routers
mkdir -p zola-admin/static/uploads
mkdir -p zola-admin/app/templates

# Create necessary files
touch zola-admin/app/__init__.py
touch zola-admin/app/database.py
touch zola-admin/app/models.py
touch zola-admin/app/routers/auth.py
touch zola-admin/app/routers/blog.py
touch zola-admin/app/routers/media.py
touch zola-admin/app/routers/seo.py
touch zola-admin/app/routers/comments.py
touch zola-admin/app/routers/subscriptions.py
touch zola-admin/app/routers/products.py
touch zola-admin/.env
touch zola-admin/main.py
touch zola-admin/requirements.txt


# Populate main.py
cat <<EOL > zola-admin/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from app.routers import auth, blog, media, seo, comments, subscriptions, products

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database configuration (modify according to your setup)
register_tortoise(
    app,
    db_url='postgres://username:password@localhost:5432/dbname',  # Example for Postgres
    modules={'models': ['app.models']},
    generate_schemas=True,
    add_exception_handlers=True,
)

# Include routers
app.include_router(auth.router)
app.include_router(blog.router)
app.include_router(media.router)
app.include_router(seo.router)
app.include_router(comments.router)
app.include_router(subscriptions.router)
app.include_router(products.router)

@app.get("/")
async def read_root():
    return {"message": "Welcome to FastAPI Admin!"}
EOL

# Populate models.py
cat <<EOL > zola-admin/app/models.py
from tortoise import Model, fields

class BlogPost(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255)
    content = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

class Media(Model):
    id = fields.IntField(pk=True)
    filename = fields.CharField(max_length=255)
    filepath = fields.CharField(max_length=255)

class Comment(Model):
    id = fields.IntField(pk=True)
    post_id = fields.ForeignKeyField("models.BlogPost", related_name="comments")
    content = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)

class Subscription(Model):
    id = fields.IntField(pk=True)
    email = fields.CharField(max_length=255, unique=True)

class Product(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    description = fields.TextField()
    price = fields.DecimalField(max_digits=10, decimal_places=2)
    stock = fields.IntField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
EOL

# Populate auth.py
cat <<EOL > zola-admin/app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from tortoise.exceptions import DoesNotExist
from app.models import User  # Assuming you have a User model

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/token")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user = await User.get(username=form.username)
    if not user or not user.verify_password(form.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"access_token": user.username, "token_type": "bearer"}

@router.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    # Add logic to retrieve user info from token
    return {"token": token}
EOL

# Populate blog.py
cat <<EOL > zola-admin/app/routers/blog.py
from fastapi import APIRouter, HTTPException
from app.models import BlogPost
from tortoise.queryset import Prefetch

router = APIRouter()

@router.get("/posts")
async def get_posts():
    posts = await BlogPost.all()
    return posts

@router.post("/posts")
async def create_post(post: BlogPost):
    post_obj = await BlogPost.create(**post.dict())
    return post_obj

@router.get("/posts/{post_id}")
async def get_post(post_id: int):
    post = await BlogPost.get(id=post_id)
    return post

@router.put("/posts/{post_id}")
async def update_post(post_id: int, post: BlogPost):
    existing_post = await BlogPost.get(id=post_id)
    existing_post.title = post.title
    existing_post.content = post.content
    await existing_post.save()
    return existing_post

@router.delete("/posts/{post_id}")
async def delete_post(post_id: int):
    post = await BlogPost.get(id=post_id)
    await post.delete()
    return {"message": "Post deleted"}
EOL

# Populate media.py
cat <<EOL > zola-admin/app/routers/media.py
from fastapi import APIRouter, UploadFile, File
import os
from fastapi.responses import FileResponse

router = APIRouter()

@router.post("/upload")
async def upload_media(file: UploadFile = File(...)):
    file_location = f"static/uploads/{file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
    return {"filename": file.filename, "file_location": file_location}

@router.get("/media/{filename}")
async def get_media(filename: str):
    file_location = f"static/uploads/{filename}"
    return FileResponse(file_location)
EOL

# Populate seo.py
cat <<EOL > zola-admin/app/routers/seo.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/seo-suggestions")
async def get_seo_suggestions():
    # Add logic for SEO suggestions here
    return {"suggestions": "SEO suggestions go here."}
EOL

# Populate comments.py
cat <<EOL > zola-admin/app/routers/comments.py
from fastapi import APIRouter
from app.models import Comment

router = APIRouter()

@router.post("/comments")
async def add_comment(comment: Comment):
    comment_obj = await Comment.create(**comment.dict())
    return {"message": "Comment added!", "comment": comment_obj}
EOL

# Populate subscriptions.py
cat <<EOL > zola-admin/app/routers/subscriptions.py
from fastapi import APIRouter
from app.models import Subscription

router = APIRouter()

@router.post("/subscribe")
async def subscribe(subscription: Subscription):
    subscription_obj = await Subscription.create(**subscription.dict())
    return {"message": "Subscribed!", "subscription": subscription_obj}
EOL

# Populate products.py
cat <<EOL > zola-admin/app/routers/products.py
from fastapi import APIRouter, HTTPException
from app.models import Product

router = APIRouter()

@router.get("/products")
async def get_products():
    products = await Product.all()
    return products

@router.post("/products")
async def create_product(product: Product):
    product_obj = await Product.create(**product.dict())
    return product_obj

@router.get("/products/{product_id}")
async def get_product(product_id: int):
    product = await Product.get(id=product_id)
    return product

@router.put("/products/{product_id}")
async def update_product(product_id: int, product: Product):
    existing_product = await Product.get(id=product_id)
    existing_product.name = product.name
    existing_product.description = product.description
    existing_product.price = product.price
    existing_product.stock = product.stock
    await existing_product.save()
    return existing_product

@router.delete("/products/{product_id}")
async def delete_product(product_id: int):
    product = await Product.get(id=product_id)
    await product.delete()
    return {"message": "Product deleted"}
EOL

# Populate .env
cat <<EOL > zola-admin/.env
DB_URL=postgres://username:password@localhost:5432/dbname
EOL

# Populate requirements.txt
cat <<EOL > zola-admin/requirements.txt
fastapi
uvicorn
tortoise-orm
jinja2
python-dotenv
EOL

# Print success message
echo "FastAPI project structure with all functionality created successfully!"
