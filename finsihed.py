from binance.client import Client
from telegram import telegram_bot_sendtext as mesaj_at
import pandas as pd
import talib
import pandas_ta as ta
import time


client=Client(None,None)

def symbols():
    response =client.get_exchange_info()
    a = list(map(lambda symbol: symbol["symbol"],response["symbols"]))
    usdtpairs=[]
    for symbol in a:
        if "USDT" in symbol and "UP" not in symbol and "DOWN" not in symbol:
            usdtpairs.append(symbol)
    return usdtpairs

coin_data = symbols()


def klinesCoin(coinName:str,period:str,limit:int):
    kline=client.get_klines(symbol=str(coinName),interval=str(period),limit=limit)
    return kline


def symbols_data(coinName:str,period:str,limit:int):
    kline = klinesCoin(coinName=coinName,period=period,limit=limit)
    converted = pd.DataFrame(kline,columns=["open_time","open","high","low","close","volume","close_time","qav","nat","tbbav","tbqav","ignore"],dtype=float)
    return converted

#btc_data = symbols_data(coinName="BTCUSDT",period="1h",limit=200)

def last(data):
    """Return the last value of the data series."""
    return data[-1]
def crossAbove(series_a,series_b):
    pre_short = series_a[len(series_a)-2]
    short = series_a[len(series_a)-1]

    pre_long = series_b[len(series_b)-2]
    long= series_b[len(series_b)-1]

    if pre_short<pre_long and short>long:
        return True
    else:
        return False


def rsiema_strategy(coinList):
    result=[]
    while True:
        try:
            for coin in coinList:
                data = symbols_data(coinName=coin,period="15m",limit=150)
                close=data["close"]
                rsi=ta.rsi(data["close"],14)               
                rsi_ema=ta.ema(rsi,50)
                ema=ta.ema(data["close"],30)
                if crossAbove(rsi,rsi_ema) and rsi[len(rsi)-1] > 35 and close[len(close)-1] > ema[len(ema)-1]:
                    result.append(coin)
                    mesaj_at(f"{coin} 'de sinyal var",1033220757)
                    print(f"{coin} 'de rsi emayi yukari keser")
                
        except:
            pass
        print("##################")
        mesaj_at("TARAMA BİTTİ",1033220757)
        time.sleep(900)

rsiema_strategy(coin_data)