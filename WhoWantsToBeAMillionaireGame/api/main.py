from fastapi import APIRouter

from api.routes import game

api_router = APIRouter()
api_router.include_router(game.router, tags=["game"])