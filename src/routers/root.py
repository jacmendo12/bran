"""
Router para endpoints raíz y de información general de la API
"""
from fastapi import APIRouter
from src.services.health import HealthService

router = APIRouter(tags=["Root"])

# Instanciar el servicio de health
health_service = HealthService()


@router.get("/")
async def root():
    """
    Endpoint raíz de la API
    Muestra la estructura de endpoints disponibles y el estado actual del servidor
    
    EXPLICACIÓN:
    - Este endpoint SÍ llama al servicio de health para obtener el estado real
    - health_service.get_health_status() ejecuta la lógica del servicio
    - Retorna tanto información de la API como el estado actual del servidor
    """
    # AQUÍ SÍ LLAMAMOS al servicio de health para obtener datos reales
    health_status = health_service.get_health_status()
    
    return {
        "message": "Bienvenido a Bran API",
        "version": "1.0.0",
        # "documentation": "/docs",  # Eliminado
        "server_status": health_status,  # Datos reales del servicio health
        "endpoints": {
            "health": {
                "description": "Health check y monitoreo del servicio",
                "routes": {
                    "status": "/health",
                    "liveness": "/health/liveness"
                }
            }
        }
    }
