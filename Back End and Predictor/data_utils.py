import pandas as pd
import requests
from datetime import datetime
import pandas_ta as ta
from flask import jsonify

def fetch_stock_data_polygon(ticker):
    API_KEY = "vichhOoRa9YbkUt8YsNYKh4mnEQhVGXu"
    start_date = "2010-01-01"
    end_date = datetime.now().strftime("%Y-%m-%d")
    url = (
        f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/"
        f"{start_date}/{end_date}?adjusted=true&sort=asc&limit=50000&apiKey={API_KEY}"
    )
    res = requests.get(url)
    data = res.json()
    try:
        if res.status_code != 200 or "results" not in data:
            raise Exception(f"Polygon API error: {data}")
    
    except Exception:
        return f"{ticker} is not a valid ticker", 500


    df = pd.DataFrame(data["results"])
    df["timestamp"] = pd.to_datetime(df["t"], unit="ms")
    df.set_index("timestamp", inplace=True)
    df.rename(columns={"o": "Open", "h": "High", "l": "Low", "c": "Close", "v": "Volume"}, inplace=True)
    return df[["Open", "High", "Low", "Close", "Volume"]]

def add_technical_indicators(df):
    df["10_day_MA"] = df["Close"].rolling(window=10).mean()
    df["5_day_MA"] = df["Close"].rolling(window=5).mean()
    df["3_day_MA"] = df["Close"].rolling(window=3).mean()
    df["1_day_pct_change"] = df["Close"].pct_change() * 100
    df["3_day_pct_change"] = df["Close"].pct_change(periods=3) * 100
    df["5_day_pct_change"] = df["Close"].pct_change(periods=5) * 100
    df["10_day_pct_change"] = df["Close"].pct_change(periods=10) * 100
    df["RSI"] = ta.rsi(close=df["Close"], window=14)
    macd = ta.macd(close=df["Close"])
    df["MACD"] = macd["MACD_12_26_9"]
    df["MACD_Signal"] = macd["MACDs_12_26_9"]
    df["MACD_Hist"] = macd["MACDh_12_26_9"]
    bbands = ta.bbands(close=df["Close"])
    df["BBL"] = bbands["BBL_5_2.0"]
    df["BBM"] = bbands["BBM_5_2.0"]
    df["BBU"] = bbands["BBU_5_2.0"]
    df["ATR"] = ta.atr(high=df["High"], low=df["Low"], close=df["Close"])
    stoch = ta.stoch(high=df["High"], low=df["Low"], close=df["Close"])
    df["SlowK"] = stoch["STOCHk_14_3_3"]
    df["SlowD"] = stoch["STOCHd_14_3_3"]
    df["OBV"] = ta.obv(close=df["Close"], volume=df["Volume"])
    return df
