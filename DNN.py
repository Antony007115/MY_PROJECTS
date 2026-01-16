import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import tensorflow as tf
import requests
from datetime import datetime, timedelta

# --------------------------
# TensorFlow settings to reduce logs
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
# --------------------------

# ----- CONFIG -----
DATA_FILE = "iot_data.csv"
TIME_COL = "timestamp"   # exact column name in CSV
POLLUTION_COL = "pm25"   # exact column name in CSV
API_KEY = "YOUR_REAL_OPENWEATHERMAP_API_KEY"  # Replace with your real API key
LAT = 12.9716
LON = 77.5946
FORECAST_HOURS = 6

# ----- LOAD DATA -----
print("Loading IoT data...")
df = pd.read_csv(DATA_FILE)

# Print CSV columns to verify names
print("CSV columns:", df.columns.tolist())

# Verify if column names exist
if TIME_COL not in df.columns or POLLUTION_COL not in df.columns:
    # Try lowercase match if column has weird capitalization
    df.columns = [c.lower() for c in df.columns]
    if TIME_COL not in df.columns or POLLUTION_COL not in df.columns:
        raise ValueError(f"Check your CSV column names. Need '{TIME_COL}' and '{POLLUTION_COL}'.")

print(f"Loaded {len(df)} rows from {DATA_FILE}")

# Convert timestamp to datetime
df[TIME_COL] = pd.to_datetime(df[TIME_COL])

# Resample to hourly and interpolate missing values
df2 = df.set_index(TIME_COL).resample('1h').mean().interpolate().reset_index()
print(f"Resampled to hourly: {len(df2)} rows.")

# Normalize data
scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(df2[[POLLUTION_COL]])

# ----- Prepare training data -----
X = scaled_data[:-1]
y = scaled_data[1:]  # Next step prediction

# Build DNN
model = Sequential([
    Dense(128, activation='relu', input_shape=(X.shape[1],)),
    Dense(64, activation='relu'),
    Dense(32, activation='relu'),
    Dense(1)
])

model.compile(optimizer='adam', loss='mse', metrics=['mae'])
model.summary()

# Train model
print("Training model...")
history = model.fit(X, y, epochs=40, batch_size=16, validation_split=0.2, verbose=1)

# Predict next hours
last_value = scaled_data[-1].reshape(1, -1)
forecast_scaled = []
for _ in range(FORECAST_HOURS):
    next_pred = model.predict(last_value, verbose=0)
    forecast_scaled.append(next_pred[0][0])
    last_value = next_pred.reshape(1, -1)

forecast = scaler.inverse_transform(np.array(forecast_scaled).reshape(-1, 1))

# Print forecast
print("Forecast (next hours):")
for i in range(FORECAST_HOURS):
    ts = df2[TIME_COL].iloc[-1] + timedelta(hours=i+1)
    val = forecast[i][0]
    if val <= 50:
        category = "Moderate"
    elif val <= 100:
        category = "Unhealthy for Sensitive Groups"
    else:
        category = "Unhealthy"
    print(f"{ts} {val:.2f} µg/m3 {category}")

# ----- Fetch live weather -----
try:
    url = f"https://api.openweathermap.org/data/2.5/onecall?lat={LAT}&lon={LON}&appid={API_KEY}&units=metric&exclude=minutely,alerts"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    current_temp = data['current']['temp']
    current_hum = data['current']['humidity']
    print(f"Current weather: {current_temp:.1f} °C, {current_hum}% humidity")
except Exception as e:
    print("Live weather fetch failed:", e)

# ----- Plot forecast -----
plt.figure(figsize=(10,5))
plt.plot(df2[TIME_COL], df2[POLLUTION_COL], label="Historical PM2.5")
future_times = [df2[TIME_COL].iloc[-1] + timedelta(hours=i+1) for i in range(FORECAST_HOURS)]
plt.plot(future_times, forecast, 'ro-', label="Forecast PM2.5")
plt.xlabel("Time")
plt.ylabel("PM2.5 (µg/m³)")
plt.title("PM2.5 Forecast")
plt.legend()
plt.grid(True)
plt.show()

