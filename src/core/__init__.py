"""
Inicializador de servicios compartidos
"""
import logging
from concurrent.futures import ThreadPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler

from .config import MAX_WORKERS, LOGGING_LEVEL, TELEGRAM_BOT_TOKEN
# from ..modulos.estrategia_qqe_mod.notificaciones import Notificaciones  # Módulo no existe

# Configurar logging
logging.basicConfig(level=getattr(logging, LOGGING_LEVEL))
logger = logging.getLogger(__name__)

# Inicializar servicios compartidos
executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)
scheduler = BackgroundScheduler()
# notificaciones = Notificaciones(TELEGRAM_BOT_TOKEN)  # Deshabilitado temporalmente

__all__ = ['executor', 'scheduler', 'logger']  # Removido 'notificaciones'
