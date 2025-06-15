# Stock Price Movement Predictor

This project is a machine learning pipeline that predicts whether a stock's price will go up or down tomorrow using technical indicators and LSTM + Random Forest models. It includes a Python backend served with Flask and a JavaScript frontend for user interaction.

---

## Features

* Fetches historical stock data from Polygon.io
* Calculates 15+ technical indicators (RSI, MACD, Bollinger Bands, etc.)
* Uses LSTM neural networks to extract time-series features
* Uses a Random Forest classifier to make binary predictions (up/down)
* Flask REST API endpoint `/predict`
* Simple HTML + JS frontend to show prediction results

---

## Technology Stack

| Component       | Technology                                     |
| --------------- | ---------------------------------------------- |
| Data Source     | Polygon.io API                                 |
| Data Processing | pandas, pandas\_ta                             |
| Feature Scaling | MinMaxScaler                                   |
| ML Models       | TensorFlow (LSTM), scikit-learn (RandomForest) |
| Backend API     | Flask, Flask-CORS                              |
| Frontend        | HTML, CSS, JavaScript                          |

---

## How It Works

### 1. Training the Model

Run `train_model()` to:

* Fetch historical stock data
* Apply technical indicators
* Train LSTM layers to generate feature representations
* Use Random Forest on the features to classify future price movement
* Save the trained scaler, LSTM feature extractor, and RF model

```bash
python train_model.py
```

Saved files:

* `models/scaler.pkl`
* `models/lstm_feature_extractor.keras`
* `models/stock_predictor_final_model.pkl`

### 2. Running the API

```bash
python app.py
```

Endpoint:

```
GET /predict?ticker=AAPL
```

Response JSON:

```json
{
  "ticker": "AAPL",
  "predicted_price": 1,
  "confidence": 0.78,
  "timestamp": "2025-06-15T14:00:00",
  "history": [1, 0, 1, ...]  // Last 50 days up/down
}
```

### 3. Frontend Usage

Open `index.html` in a browser. Input a stock symbol. The frontend makes a fetch request and displays:

* Prediction (Up/Down)
* Confidence score
* Chart of last 50-day movements using 📈 / 📉

---

## Installation

1. Python 3.8+
2. Install dependencies:

```bash
pip install -r requireme
```
