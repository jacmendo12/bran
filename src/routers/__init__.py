"""
Centralizador de todos los routers de la API
"""
from fastapi import APIRouter
from .estrategia_bran_v1 import router as estrategia_bran_v1_router

# Router principal que agrupa todos los routers
api_router = APIRouter()

# Incluir solo el router del dashboard
api_router.include_router(estrategia_bran_v1_router)


def get_api_router() -> APIRouter:
    """
    Obtiene el router principal con todas las rutas configuradas
    
    Returns:
        APIRouter: Router principal de la API
    """
    return api_router
