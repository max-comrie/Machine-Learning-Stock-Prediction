from flask import Flask, request, jsonify
from flask_cors import CORS
from inference import predict_price  # type: ignore
from data_utils import fetch_stock_data_polygon # type: ignore
from tensorflow.keras.models import load_model  # type: ignore
import joblib

app = Flask(__name__)
CORS(app)

# Load once on startup
scaler = joblib.load("models/scaler.pkl")
rf_model = joblib.load("models/stock_predictor_final_model.pkl")
feature_extractor = load_model("models/lstm_feature_extractor.keras")



@app.route('/predict', methods=['GET'])
def predict():
    ticker = request.args.get('ticker', '').upper()
    if not ticker:
        return jsonify({"error": "Ticker is required"}), 400

    result = predict_price(ticker, scaler, feature_extractor, rf_model)
    if result is None:
        return jsonify({"error": "Not enough data"}), 400

    return jsonify({
        "ticker": result['ticker'],
        "predicted_price": result['prediction'],
        "confidence": result.get('confidence'),
        "timestamp": result.get('timestamp'),
        "history": result.get('history', []),
    })

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
