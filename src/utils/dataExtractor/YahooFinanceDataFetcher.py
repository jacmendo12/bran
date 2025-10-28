import pandas as pd
from datetime import datetime
import pytz
import yfinance as yf

class YahooFinanceDataFetcher:
    def __init__(self, asset="GC=F", interval="1h"):
        """
        Inicializa el fetcher de datos de Yahoo Finance
        
        Parameters:
        - asset: Símbolo del activo (por defecto "GC=F" para Oro)
        - interval: Intervalo de tiempo (1m, 5m, 15m, 1h, 1d, etc.)
        """
        self.asset = asset
        self.interval = interval

    def get_data(self, start_time=None, end_time=None, limit=500):
        """
        Obtiene datos de Yahoo Finance para el activo y intervalo dados.
        
        Parameters:
        - start_time: Tiempo de inicio opcional en milisegundos
        - end_time: Tiempo de fin opcional en milisegundos
        - limit: Número de velas a recuperar (por defecto: 500)
        
        Returns:
        - DataFrame con datos OHLCV
        """
        try:
            # Convertir milisegundos a datetime si se proporcionan
            if start_time:
                start_date = pd.to_datetime(start_time, unit='ms')
            else:
                # Si no hay start_time, calcular basado en limit e interval
                start_date = self._calculate_start_date(limit)
            
            if end_time:
                end_date = pd.to_datetime(end_time, unit='ms')
            else:
                end_date = datetime.now(pytz.UTC)
            
            # Crear objeto ticker de Yahoo Finance
            ticker = yf.Ticker(self.asset)
            
            # Mapear intervalos de Binance a Yahoo Finance
            yf_interval = self._map_interval(self.interval)
            
            # Descargar datos históricos
            df = ticker.history(
                start=start_date,
                end=end_date,
                interval=yf_interval,
                auto_adjust=False
            )
            
            if df.empty:
                print(f"No se obtuvieron datos para {self.asset} con intervalo {self.interval}")
                return pd.DataFrame()
            
            # Renombrar y reorganizar columnas para coincidir con el formato de Binance
            ticks_frame = pd.DataFrame()
            ticks_frame['time'] = df.index.values  # Usar .values para evitar problemas de índice
            ticks_frame['open'] = df['Open'].values.astype(float)
            ticks_frame['high'] = df['High'].values.astype(float)
            ticks_frame['low'] = df['Low'].values.astype(float)
            ticks_frame['close'] = df['Close'].values.astype(float)
            ticks_frame['volume'] = df['Volume'].values.astype(float)
            
            # Resetear el índice para tener 'time' como columna
            ticks_frame = ticks_frame.reset_index(drop=True)
            
            # Asegurar que time sea timezone-aware
            if ticks_frame['time'].dt.tz is None:
                ticks_frame['time'] = ticks_frame['time'].dt.tz_localize('UTC')
            else:
                ticks_frame['time'] = ticks_frame['time'].dt.tz_convert('UTC')
            
            # Estimación de buy_volume y sell_volume (50% cada uno)
            # Yahoo Finance no provee esta información directamente
            ticks_frame['buy_volume'] = ticks_frame['volume'] * 0.5
            ticks_frame['sell_volume'] = ticks_frame['volume'] * 0.5
            
            # Calcular delta de volumen
            ticks_frame['volume_delta'] = ticks_frame['buy_volume'] - ticks_frame['sell_volume']
            
            # Limitar a la cantidad de registros solicitada
            if len(ticks_frame) > limit:
                ticks_frame = ticks_frame.tail(limit)
            
            return ticks_frame
            
        except Exception as e:
            print(f"Error obteniendo o procesando datos: {e}")
            import traceback
            traceback.print_exc()
            return pd.DataFrame()

    def _map_interval(self, interval):
        """
        Mapea intervalos de estilo Binance a Yahoo Finance
        
        Parameters:
        - interval: Intervalo en formato Binance (1m, 5m, 15m, 1h, 1d, etc.)
        
        Returns:
        - Intervalo en formato Yahoo Finance
        """
        # Yahoo Finance soporta: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
        interval_map = {
            '1m': '1m',
            '2m': '2m',
            '5m': '5m',
            '15m': '15m',
            '30m': '30m',
            '1h': '1h',
            '2h': '1h',  # Yahoo no tiene 2h, usar 1h
            '4h': '1h',  # Yahoo no tiene 4h, usar 1h
            '6h': '1h',  # Yahoo no tiene 6h, usar 1h
            '8h': '1h',  # Yahoo no tiene 8h, usar 1h
            '12h': '1h', # Yahoo no tiene 12h, usar 1h
            '1d': '1d',
            '3d': '1d',  # Yahoo no tiene 3d, usar 1d
            '1w': '1wk',
            '1M': '1mo'
        }
        
        return interval_map.get(interval, '1h')
    
    def _calculate_start_date(self, limit):
        """
        Calcula la fecha de inicio basada en el límite y el intervalo
        
        Parameters:
        - limit: Número de velas a obtener
        
        Returns:
        - Fecha de inicio calculada
        """
        now = datetime.now(pytz.UTC)
        
        if self.interval.endswith('m'):
            multiplier = int(self.interval[:-1])
            return now - pd.Timedelta(minutes=limit * multiplier)
        elif self.interval.endswith('h'):
            multiplier = int(self.interval[:-1])
            return now - pd.Timedelta(hours=limit * multiplier)
        elif self.interval.endswith('d'):
            multiplier = int(self.interval[:-1])
            return now - pd.Timedelta(days=limit * multiplier)
        elif self.interval.endswith('w'):
            multiplier = int(self.interval[:-1])
            return now - pd.Timedelta(weeks=limit * multiplier)
        elif self.interval.endswith('M'):
            multiplier = int(self.interval[:-1])
            return now - pd.Timedelta(days=limit * multiplier * 30)
        else:
            return now - pd.Timedelta(days=30)

    @staticmethod
    def calculate_time_increment(interval):
        """
        Calcula el incremento de tiempo basado en el intervalo.
        """
        if interval.endswith('m'):
            multiplier = int(interval[:-1])
            return pd.Timedelta(minutes=500 * multiplier)
        elif interval.endswith('h'):
            multiplier = int(interval[:-1])
            return pd.Timedelta(hours=500 * multiplier)
        elif interval.endswith('d'):
            multiplier = int(interval[:-1])
            return pd.Timedelta(days=500 * multiplier)
        elif interval.endswith('w'):
            multiplier = int(interval[:-1])
            return pd.Timedelta(weeks=500 * multiplier)
        else:
            return pd.Timedelta(days=30)
