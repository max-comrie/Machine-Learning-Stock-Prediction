import numpy as np
from datetime import datetime
from data_utils import fetch_stock_data_polygon, add_technical_indicators

def create_sequences(df, features, seq_length=40):
    X = []
    for i in range(len(df) - seq_length):
        X.append(df.iloc[i:i+seq_length][features].to_numpy())
    return np.array(X)

def predict_price(ticker, scaler, feature_extractor, rf_model):
    df = fetch_stock_data_polygon(ticker)
    df = add_technical_indicators(df)
    df.dropna(inplace=True)

    features = [
        '10_day_MA', '5_day_MA', '3_day_MA',
        '1_day_pct_change', '3_day_pct_change', '5_day_pct_change', '10_day_pct_change',
        'RSI', 'MACD', 'MACD_Signal', 'MACD_Hist',
        'BBL', 'BBM', 'BBU',
        'ATR', 'SlowK', 'SlowD',
        'OBV'
    ]

    if len(df) < 41:
        return None

    df[features] = scaler.transform(df[features])
    X = create_sequences(df, features)
    if len(X) == 0:
        return None

    lstm_features = feature_extractor.predict(X)
    y_probs = rf_model.predict_proba(lstm_features)[:, 1]
    confidence = y_probs[-1]
    prediction = int(confidence > 0.5)

    # ✅ Add this line to fetch last 50 closing prices
    #fifty_day_history = # 1 if price went up from previous day, else 0
    fifty_day_history = np.where(df["1_day_pct_change"].iloc[-50:] > 0, 1, 0).tolist()


    return {
        "ticker": ticker,
        "prediction": prediction,
        "confidence": confidence,
        "timestamp": str(datetime.now()),
        "history": fifty_day_history
    }
