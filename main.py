import pandas as pd
import telegram
import pyupbit
import numpy as np

a = 1

tickers = pyupbit.get_tickers(fiat="KRW")

while True:
    def condition(ticker):

        data = pyupbit.get_ohlcv(ticker, interval="minute15", count=100)

        df = pd.DataFrame(data)

        df = pd.Series(df['close'].values)

        price = pyupbit.get_current_price(ticker)

        period = 14

        delta = df.diff()

        up, down = delta.copy(), delta.copy()
        up[up < 0] = 0
        down[down > 0] = 0

        _gain = up.ewm(com=(period - 1), min_periods=period).mean()
        _loss = down.abs().ewm(com=(period - 1), min_periods=period).mean()

        RS = _gain / _loss

        rsi = round(pd.Series(100 - (100 / (1 + RS)), name="RSI").iloc[-1])

        chat_id = '985647682'
        bot = telegram.Bot(token='1600653008:AAHo9es0G96B2Ypr50VWr4V0ffpDgHcRd5s')

        stockK = stockrsi(ticker, 14, 3, 3)

        if rsi < 35 and stockK < 40:
            print(rsi)
            text = str(ticker) + '\n' + 'rsi : '  + str(rsi) + '\n' + 'stock : ' + str(stockK)
            print(text)
            bot.sendMessage(chat_id=chat_id, text=text)


    def stockrsi(symbol, p1, k1, d1):
        data = pyupbit.get_ohlcv(ticker, interval="minute15", count=100)

        df = pd.DataFrame(data)

        series = pd.Series(df['close'].values)

        period = p1
        smoothK = k1
        smoothD = d1

        delta = series.diff().dropna()
        ups = delta * 0
        downs = ups.copy()
        ups[delta > 0] = delta[delta > 0]
        downs[delta < 0] = -delta[delta < 0]
        ups[ups.index[period - 1]] = np.mean(ups[:period])
        ups = ups.drop(ups.index[:(period - 1)])
        downs[downs.index[period - 1]] = np.mean(downs[:period])
        downs = downs.drop(downs.index[:(period - 1)])
        rs = ups.ewm(com=period - 1, min_periods=0, adjust=False, ignore_na=False).mean() / \
             downs.ewm(com=period - 1, min_periods=0, adjust=False, ignore_na=False).mean()
        rsi = 100 - 100 / (1 + rs)

        stochrsi = (rsi - rsi.rolling(period).min()) / (rsi.rolling(period).max() - rsi.rolling(period).min())
        stochrsi_K = stochrsi.rolling(smoothK).mean()
        stochrsi_D = stochrsi_K.rolling(smoothD).mean()

        print(symbol, p1, k1, d1)
        print('upbit 10 minute stoch_rsi_K: ', round(stochrsi_K.iloc[-1] * 100))
        print('upbit 10 minute stoch_rsi_D: ', stochrsi_D.iloc[-1] * 100)
        print('')

        return round(stochrsi_K.iloc[-1] * 100)

    for ticker in tickers:
        condition(ticker)