"""
Servicio para la estrategia Bran V1
Maneja la lógica de negocio y obtención de datos de Yahoo Finance (GC=F por defecto)
"""
from typing import Dict, Any, Optional
import pandas as pd
import math
from src.utils.dataExtractor.YahooFinanceDataFetcher import YahooFinanceDataFetcher
from src.utils.indicadores.pullback_detection import PullbackDetection


class EstrategiaBranV1Service:
    """
    Servicio que encapsula la lógica de la estrategia de trading Bran V1
    Ahora usa Yahoo Finance para obtener datos de acciones
    """
    
    def __init__(self):
        """
        Inicializa el servicio
        """
        pass
        
    def get_dashboard_data(self, 
                          asset: str = "GC=F", 
                          interval: str = "1h", 
                          limit: int = 1000,
                          start_time: Optional[int] = None,
                          minimum_tresure: float = 2.1) -> Dict[str, Any]:
        """
        Obtiene datos del mercado y detecta pullbacks para el dashboard
        
        Args:
            asset: Símbolo del activo (por defecto "GC=F" para Oro)
            interval: Intervalo temporal (1m, 5m, 15m, 1h, 4h, 1d, etc.)
            limit: Número de velas a obtener
            start_time: Tiempo de inicio en milisegundos (opcional)
            minimum_tresure: Umbral mínimo para detección de pullbacks (por defecto 2.1)
            
        Returns:
            Diccionario con los datos del mercado, estadísticas y pullbacks detectados
        """
        try:
            # Crear fetcher para el activo (GC=F por defecto)
            fetcher = YahooFinanceDataFetcher(asset=asset, interval=interval)
            
            # Obtener datos
            df = fetcher.get_data(start_time=start_time, end_time=None, limit=limit)
            
            if df.empty:
                return {
                    "success": False,
                    "error": "No se pudieron obtener datos del mercado",
                    "data": None
                }
            
            # Preparar datos para pullback detection
            df['parteAlta'] = df.apply(lambda row: max(row['open'], row['close']), axis=1)
            df['parteBaja'] = df.apply(lambda row: min(row['open'], row['close']), axis=1)
            df['altos'] = math.nan
            df['bajos'] = math.nan
            df['pocAltos'] = math.nan
            df['pocBajos'] = math.nan
            df['pivotAlto'] = math.nan
            df['pivotBajo'] = math.nan
            df['tendencia'] = 0
            
            # Detectar pullbacks
            pullback_detector = PullbackDetection(df, minimum_tresure=minimum_tresure)
            df_with_pullbacks, rangos = pullback_detector.detect_pullbacks(df, minimum_tresure=minimum_tresure)
            print(df_with_pullbacks.iloc[0])
            print(rangos)
            # Calcular estadísticas
            stats = self._calculate_statistics(df_with_pullbacks)
            
            # Convertir DataFrame a formato JSON-friendly
            # Reemplazar NaN, inf y -inf con None antes de convertir
            import numpy as np
            df_clean = df_with_pullbacks.copy()
            
            # Reemplazar todos los valores problemáticos
            df_clean = df_clean.replace([np.inf, -np.inf], None)
            df_clean = df_clean.where(pd.notna(df_clean), None)
            
            # Convertir a diccionario
            data_dict = df_clean.to_dict('records')
            
            # Limpieza adicional: asegurar que cada valor numérico sea válido para JSON
            for record in data_dict:
                # Convertir timestamp
                if record.get('time') is not None:
                    try:
                        record['time'] = record['time'].isoformat()
                    except:
                        record['time'] = None
                
                # Limpiar todos los campos numéricos
                for key, value in list(record.items()):
                    if isinstance(value, float):
                        if pd.isna(value) or np.isinf(value):
                            record[key] = None
            
            # Limpiar rangos también
            rangos_clean = {}
            for key, value in rangos.items():
                if isinstance(value, (int, float)):
                    if pd.isna(value) or value == float('inf') or value == float('-inf'):
                        rangos_clean[key] = None
                    else:
                        rangos_clean[key] = float(value) if not pd.isna(value) else None
                else:
                    rangos_clean[key] = value
            
            return {
                "success": True,
                "asset": asset,
                "interval": interval,
                "total_candles": len(df_with_pullbacks),
                "statistics": stats,
                "rangos": rangos_clean,
                "data": data_dict
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "data": None
            }
    
    def _calculate_statistics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Calcula estadísticas sobre los datos del mercado
        
        Args:
            df: DataFrame con los datos OHLCV
            
        Returns:
            Diccionario con estadísticas calculadas
        """
        if df.empty:
            return {}
        
        try:
            current_price = float(df['close'].iloc[-1])
            price_change = float(df['close'].iloc[-1] - df['open'].iloc[0])
            price_change_pct = (price_change / float(df['open'].iloc[0])) * 100
            
            return {
                "current_price": current_price,
                "highest_price": float(df['high'].max()),
                "lowest_price": float(df['low'].min()),
                "average_price": float(df['close'].mean()),
                "price_change": price_change,
                "price_change_percentage": price_change_pct,
                "total_volume": float(df['volume'].sum()),
                "average_volume": float(df['volume'].mean()),
                "first_time": df['time'].iloc[0].isoformat(),
                "last_time": df['time'].iloc[-1].isoformat()
            }
        except Exception as e:
            return {"error": f"Error calculando estadísticas: {str(e)}"}


# Instancia global del servicio
estrategia_service = EstrategiaBranV1Service()
