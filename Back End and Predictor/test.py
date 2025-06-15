import requests
from datetime import datetime
import pandas as pd

API_KEY = "vichhOoRa9YbkUt8YsNYKh4mnEQhVGXu"  # Replace with your actual key
ticker = "AAPL"

start_date = "2020-01-01"
end_date = datetime.now().strftime("%Y-%m-%d")

url = (
    f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/"
    f"{start_date}/{end_date}"
    f"?adjusted=true&sort=asc&limit=50000&apiKey={API_KEY}"
)

res = requests.get(url)
print("Response status code:", res.status_code)

data = res.json()

# Check for errors
if res.status_code != 200 or "results" not in data:
    print("Error from Polygon:", data)
else:
    # Convert to DataFrame and print
    df = pd.DataFrame(data["results"])
    df["timestamp"] = pd.to_datetime(df["t"], unit="ms")
    df.set_index("timestamp", inplace=True)

    df.rename(columns={
        "o": "Open",
        "h": "High",
        "l": "Low",
        "c": "Close",
        "v": "Volume"
    }, inplace=True)

    print(df[["Open", "High", "Low", "Close", "Volume"]].head())
