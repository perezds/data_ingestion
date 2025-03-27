from fastapi import APIRouter
from api.v1.endpoints import transformers

api_router = APIRouter()

api_router.include_router(transformers.router, prefix="/personagem", tags=["Personagem"])

