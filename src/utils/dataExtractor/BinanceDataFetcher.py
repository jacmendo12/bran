import pandas as pd
from datetime import datetime
import pytz
import time
from binance import BinanceSync as Client

class BinanceDataFetcher:
    def __init__(self, asset, interval, client=None):
        self.asset = asset
        self.interval = interval
        self.client = client if client else Client()

    def get_data(self, start_time=None, end_time=None, limit=500):
        """
        Fetch data from Binance API for the given asset and interval.
        Uses the Binance client with fetchOHLCV method.
        
        Parameters:
        - start_time: Optional start time in milliseconds
        - end_time: Optional end time in milliseconds
        - limit: Number of klines to retrieve (default: 500)
        
        Returns:
        - DataFrame with kline data
        """
        try:
            # fetchOHLCV format: symbol, timeframe, since (optional), limit (optional)
            # El resultado es: [[timestamp, open, high, low, close, volume], ...]
            params = {}
            if start_time:
                ohlcv = self.client.fetchOHLCV(
                    symbol=self.asset,
                    timeframe=self.interval,
                    since=start_time,
                    limit=limit,
                    params=params
                )
            else:
                ohlcv = self.client.fetchOHLCV(
                    symbol=self.asset,
                    timeframe=self.interval,
                    limit=limit,
                    params=params
                )
                
            if not ohlcv:
                print(f"No data returned for {self.asset} with interval {self.interval}")
                return pd.DataFrame()
            
            # OHLCV format from CCXT: [timestamp, open, high, low, close, volume]
            ticks_frame = pd.DataFrame(ohlcv, columns=['time', 'open', 'high', 'low', 'close', 'volume'])
            ticks_frame['time'] = pd.to_datetime(ticks_frame['time'], unit='ms')
            ticks_frame[['open', 'high', 'low', 'close', 'volume']] = ticks_frame[['open', 'high', 'low', 'close', 'volume']].astype(float)

            # Para buy_volume y sell_volume, necesitamos hacer una estimación
            # ya que CCXT no provee esta información directamente
            # Usaremos el 50% como estimación (esto es una aproximación)
            ticks_frame['buy_volume'] = ticks_frame['volume'] * 0.5
            ticks_frame['sell_volume'] = ticks_frame['volume'] * 0.5
            
            # Calculate volume delta
            ticks_frame['volume_delta'] = ticks_frame['buy_volume'] - ticks_frame['sell_volume']
            
            return ticks_frame
            
        except Exception as e:
            print(f"Error fetching or processing data: {e}")
            import traceback
            traceback.print_exc()
            return pd.DataFrame()

    @staticmethod
    def calculate_time_increment(interval):
        """
        Calculate time increment based on the interval.
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
