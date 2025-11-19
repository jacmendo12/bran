"""
Router para la Estrategia Bran V1
Endpoints para el dashboard
"""
from fastapi import APIRouter, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from typing import Optional
from src.services.estrategia_bran_v1.estrategia_bran_v1_service import estrategia_service

# Configurar templates
templates = Jinja2Templates(directory="src/templates")

# Router para el dashboard
router = APIRouter(tags=["Dashboard"])


@router.get("/dashboard", response_class=HTMLResponse)
async def get_dashboard(request: Request):
    """
    Renderiza el dashboard principal de la estrategia Bran V1
    """
    return templates.TemplateResponse(
        "estrategia_bran_v1_dashboard.html",
        {"request": request}
    )


@router.get("/api/estrategia-bran-v1/data")
async def get_dashboard_data(
    asset: str = Query(default="GC=F", description="Símbolo del activo (ej: GC=F, MSFT, AAPL, EURUSD=X)"),
    interval: str = Query(default="1h", description="Intervalo temporal (1m, 5m, 15m, 1h, 1d)"),
    limit: int = Query(default=1000, ge=1, le=1000, description="Número de velas a obtener"),
    start_time: Optional[int] = Query(default=None, description="Tiempo de inicio en milisegundos"),
    minimum_tresure: float = Query(default=0.21, description="Umbral mínimo para detección de pullbacks")
):
    """
    Endpoint para obtener datos del mercado con detección de pullbacks
    
    Args:
        asset: Símbolo del activo (ejemplo: GC=F, EURUSD=X, MSFT, AAPL)
        interval: Intervalo temporal (1m, 5m, 15m, 1h, 1d, etc.)
        limit: Número de velas a obtener (1-1000)
        start_time: Tiempo de inicio en milisegundos (opcional)
        minimum_tresure: Umbral mínimo para detección de pullbacks (por defecto 0.21)
        
    Returns:
        JSON con los datos del mercado, estadísticas y pullbacks detectados
    """
    result = estrategia_service.get_dashboard_data(
        asset=asset,
        interval=interval,
        limit=limit,
        start_time=start_time,
        minimum_tresure=minimum_tresure
    )
    
    return JSONResponse(content=result)
