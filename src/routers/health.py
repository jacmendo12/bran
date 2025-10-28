"""
Router para health check del servidor
"""
from fastapi import APIRouter
from src.services.health import HealthService

router = APIRouter(prefix="/health", tags=["Health"])

# Instanciar el servicio
health_service = HealthService()


@router.get("")
async def health_check():
    """
    Endpoint para verificar que el servidor está funcionando correctamente
    
    Returns:
        dict: Estado del servidor con información completa
    """
    return health_service.get_health_status()


@router.get("/liveness")
async def liveness():
    """
    Endpoint para verificar si el servicio está vivo
    Útil para Kubernetes liveness probes
    
    Returns:
        dict: Estado de liveness del servicio
    """
    return health_service.get_liveness()
