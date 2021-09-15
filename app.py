import ccxt
import config
import pandas as pd
import numpy as np
from datetime import datetime
import time

bybit = ccxt.bybit({
    "apiKey":config.API_KEY,
    "secret":config.API_SECRET
})

#tr to calculate atr
def tr(data):
    data['previous_close'] = data['close'].shift(1)
    data['high-low'] = abs(data['high'] - data['low'])
    data['high-pc'] = abs(data['high'] - data['previous_close'])
    data['low-pc'] = abs(data['low'] - data['previous_close'])

    tr = data[['high-low', 'high-pc', 'low-pc']].max(axis=1)

    return tr

#atr for stoploss
def atr(data, period):
    data['tr'] = tr(data)
    atr = data['tr'].rolling(period).mean()

    return atr

def start():
    #fetch data for in dataframe with variable timeframe
    bars = bybit.fetch_ohlcv('BTCUSDT', timeframe='1m', limit=100)
    df = pd.DataFrame(bars[:-1], columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    candle_data = tr(df)
    print(candle_data)

if __name__ == "__main__":
    start()
