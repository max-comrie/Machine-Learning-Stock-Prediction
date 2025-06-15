import joblib
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential, Model # type: ignore
from tensorflow.keras.layers import LSTM, Dense, Dropout # type: ignore
from tensorflow.keras.callbacks import EarlyStopping # type: ignore
from data_utils import fetch_stock_data_polygon, add_technical_indicators # type: ignore


def create_sequences(df, features, seq_length=40):
    X, y = [], []
    for i in range(len(df) - seq_length):
        X.append(df.iloc[i:i+seq_length][features].to_numpy())
        y.append(df.iloc[i+seq_length]["Price Movement"])
    return np.array(X), np.array(y)


def train_model(ticker):
    df = fetch_stock_data_polygon(ticker)
    df = add_technical_indicators(df)
    df["Price Movement"] = np.where(df["1_day_pct_change"] > 0, 1, 0)
    df.dropna(inplace=True)


    scaler = MinMaxScaler()
    feature_cols = [col for col in df.columns if col != "Price Movement"]
    df[feature_cols] = scaler.fit_transform(df[feature_cols])

    X, y = create_sequences(df, feature_cols)
    X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=False, test_size=0.2)

    model = Sequential([
        LSTM(64, return_sequences=True, input_shape=(X.shape[1], X.shape[2])),
        LSTM(64),
        Dense(64, activation='relu'),
        Dropout(0.2),
        Dense(32, activation='relu'),
        Dropout(0.2),
        Dense(1, activation='sigmoid')
    ])

    early_stopping = EarlyStopping(
    monitor='val_loss',     # <- what to watch
    patience=50,         # <- how many bad epochs to tolerate
    restore_best_weights=True  # <- optional, but useful
    )

    model.compile(optimizer='adam', loss='binary_crossentropy')
    history = model.fit(X_train, y_train, epochs=1000, batch_size=32, callbacks=[early_stopping],verbose=1,validation_split=0.2)

    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.title('Training vs Validation Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.show()

    feature_extractor = Model(inputs=model.layers[0].input, outputs=model.layers[-2].output)
    train_features = feature_extractor.predict(X_train)

    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(train_features, y_train)

    joblib.dump(scaler, "models/scaler.pkl")
    joblib.dump(rf_model, "models/stock_predictor_final_model.pkl")
    joblib.dump(feature_cols, "models/feature_cols.pkl")
    feature_extractor.save("models/lstm_feature_extractor.keras")
    print("✅ Models saved.")

if __name__ == "__main__":
    train_model("SPY")
