import pandas as pd
import os
import time

from pkg.ConfigLoader import config
from utils.utils import get_current_price,get_OHLCV,get_klines
from utils.indicator import ExponentialMovingAverage,MACD,StochasticRSI


ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
CONFIG_DIR = os.path.join(ROOT, 'config')
STRATEGY_CONFIG = os.path.join(CONFIG_DIR, 'strategy.json')

class StochRSI(object):
    def __init__(self) :
        """ initialized strategy parameters """
        STRATEGY_NAME = 'stoch_rsi'
        self.config = config(STRATEGY_CONFIG).load_config()[STRATEGY_NAME]
        self.symbols = self.config['symbol']
        self.timeframe = self.config['timeframe']
        self.limit = self.config['limit']
        self.param = self.config['param']
        self.data = get_klines(self.symbols,self.timeframe,self.limit)
        """
        self.data: pandas.Dataframe, close price
                               BTCUSDT  ETHUSDT  BNBUSDT
        Datetime
        2024-11-15 21:30:00  89941.78  3098.17   619.01
        2024-11-15 21:45:00  90148.00  3102.85   619.63
        2024-11-15 22:00:00  89763.98  3089.00   616.30
        2024-11-15 22:15:00  89324.67  3069.81   612.79
        2024-11-15 22:30:00  88891.98  3052.98   609.69 
        """
        self.indicators = self.compute_indicators()

    def compute_indicators(self):
        indicators={}
        for symbol in self.symbols:
            data = self.data[symbol].to_frame(name =symbol)
            df = pd.DataFrame()
            df['stoch'] = StochasticRSI(data,symbol,self.param['stoch_period']).get_stochastic_rsi()*100
            df['ema']  = ExponentialMovingAverage(data,symbol,self.param['ema_period']).get_ema()
            macd = macd=MACD(data,symbol,self.param['macd_short_period'],self.param['macd_long_period'],self.param['macd_signal_period'])
            df['macd'] = macd.get_MACD()
            df['signal'] = macd.get_signal()
            indicators[symbol]=df
        return indicators

    def run(self):
        """ Generate signal for every symbol """
        signal ={}
        for symbol in self.symbols:
            indicator_df = self.indicators[symbol]
            if len(indicator_df) < 2:
                signal[symbol] = 0
                continue
            macd_current = indicator_df['macd'].iloc[-1]
            macd_prev = indicator_df['macd'].iloc[-2]
            signal_current = indicator_df['signal'].iloc[-1]
            signal_prev = indicator_df['signal'].iloc[-2]
            is_uptrend = (macd_prev < signal_prev) and (macd_current > signal_current) and (macd_current < 0)
            is_downtrend = (macd_prev > signal_prev) and (macd_current < signal_current) and (macd_current > 0)
            current_stochRSI = indicator_df['stoch'].iloc[-1]
            current_ema = indicator_df['ema'].iloc[-1]
            if is_downtrend and current_stochRSI<20 and self.data[symbol].iloc[-1]<=current_ema:
                signal[symbol]=1
            elif is_uptrend and current_stochRSI>80 and self.data[symbol].iloc[-1]>=current_ema:
                signal[symbol]=-1
            else:
                signal[symbol]=0
        """ signal={"BTCUSDT":0, "ETHUSDT":1,"BNBUSDT":-1} : 1:buy signal, -1: sell siganl, 0:nothing """
        print(signal)
        return signal
        

