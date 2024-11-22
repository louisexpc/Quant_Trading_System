import ccxt
import pandas as pd
import time
from datetime import datetime, timedelta

def get_klines(symbols:list,timeframe:str='15m',limit:int=5):
    df = pd.DataFrame()
    for symbol in symbols:
        df_tmp = get_OHLCV(symbol,timeframe,limit)
        df[symbol]=df_tmp['Close'].astype(float)
    #print(df)
    return df

def get_OHLCV(symbol='BTCUSDT',timeframe = "1m",limit = 5):
    '''
    'timeframes':15s, 30s, 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 1d, 3d, 1w, 1M
    'limit': 回傳的 k 線數量
    '''
    exchange = ccxt.binance()
    data_jason = exchange.fetch_ohlcv(symbol,timeframe,limit=limit)
    col = ['Timestamp','Open','High','Low','Close','Volume']
    df = pd.DataFrame(data_jason,columns=col)
    df['Datetime'] = df['Timestamp'].apply(lambda x:timeTrans(x))
    df.set_index('Datetime',inplace=True)
    df.drop('Timestamp',inplace=True,axis=1)
    #print(df)
    return df
    '''
    Return:pandas.Dataframe
    Frame as follow: 
                            Open      High       Low     Close    Volume
    Datetime
    2024-11-15 16:57:00  88140.00  88140.90  88121.25  88121.26  15.96510
    2024-11-15 16:58:00  88121.25  88165.91  88121.25  88151.51   7.19347
    2024-11-15 16:59:00  88151.51  88151.52  88082.95  88082.96  19.69828
    2024-11-15 17:00:00  88082.96  88107.38  88024.40  88107.36  25.07887
    2024-11-15 17:01:00  88107.36  88107.36  88077.30  88077.30   1.02725
    '''
    
def get_current_price(symbol='BTCUSDT'):
    exchange = ccxt.binance()
    ticker = exchange.fetch_ticker(symbol)
    formattedTime = timeTrans(ticker['timestamp'])
    lastPrice = ticker['last']
    print(f"{formattedTime}: last price: {lastPrice}")
    return lastPrice
    '''
    Output Format:
    2024-11-15 17:02:40: last price: 88173.68
    Return: (float)lastPrice
    '''


def timeTrans(timestamp_ms):
    utc_time = datetime.utcfromtimestamp(timestamp_ms / 1000)
    # Convert to UTC+8 by adding 8 hours
    utc_plus_8_time = utc_time + timedelta(hours=8)
    # Format as a readable string
    formatted_time = utc_plus_8_time.strftime('%Y-%m-%d %H:%M:%S')
    return formatted_time
    '''
    UTF+8
    timestamp_ms: Unix timestamp (in milliseconds)
    formatted_time: string ,eg.2024-11-10 17:35:01
    '''
def time_match(timeframe):
    current_time = datetime.now()
    if timeframe =='5m':
        return current_time.minute % 5 == 0
    elif timeframe =='15m':
        return current_time.minute % 15 == 0
    elif timeframe == '1h':
        return current_time.hour % 1 == 0
    elif timeframe == '2h':
        return current_time.hour % 2 == 0
    elif timeframe == '3h':
        return current_time.hour % 3 == 0
    elif timeframe == '4h':
        return current_time.hour % 4 == 0
    elif timeframe == '6h':
        return current_time.hour % 6 == 0
    elif timeframe == '8h':
        return current_time.hour % 8 == 0
    elif timeframe == '12h':
        return current_time.hour % 12 == 0
    elif timeframe == '1d':
        return current_time.hour == 0
    else:
        return False


if __name__=="__main__":
    time_match(15)