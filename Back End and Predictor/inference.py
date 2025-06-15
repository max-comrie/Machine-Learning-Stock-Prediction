import pandas as pd
import numpy as np
from datetime import datetime
from data_utils import fetch_stock_data_polygon, add_technical_indicators # type: ignore
from train_model import create_sequences # type: ignore
import joblib



def predict_price(ticker, scaler, feature_extractor, rf_model):
    df = fetch_stock_data_polygon(ticker)
    df = add_technical_indicators(df)
    df["Price Movement"] = np.where(df["1_day_pct_change"] > 0, 1, 0)
    df.dropna(inplace=True)

    if len(df) < 41:
        return None
    
    
    feature_cols = joblib.load("models/feature_cols.pkl")
    df[feature_cols] = scaler.fit_transform(df[feature_cols])
    X,y = create_sequences(df, feature_cols)
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

if __name__ == '__main__':
    predict_price('AAPL')