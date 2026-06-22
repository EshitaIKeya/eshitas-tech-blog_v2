import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.models import Role, User, Category, Post, Comment, ReactionType, Reaction
from app.routers import (
    auth_router, role_router, category_router,
    post_router, comment_router, reaction_router, user_router,
)
from app.seed import seed_data

app = FastAPI(
    title="Eshita\'s Tech Blog API",
    description="A personal blog API with AI-powered summaries, built with FastAPI and PostgreSQL",
    version="2.0.0",
)


@app.on_event("startup")
def on_startup():
    """Create tables and seed default data when the server actually starts.

    This runs on startup (not at import time) so that test files can import
    `app` and swap in a different database before any real connection happens.
    """
    Base.metadata.create_all(bind=engine)
    seed_data()


frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url, "http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(role_router.router)
app.include_router(category_router.router)
app.include_router(post_router.router)
app.include_router(comment_router.router)
app.include_router(reaction_router.router)
app.include_router(user_router.router)


@app.get("/")
def home():
    return {"message": "Eshita\'s Tech Blog API is running!"}
