from alpha_vantage.timeseries import TimeSeries
from dotenv import load_dotenv
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load environment variables from .env file
load_dotenv()

# Fetch the API key from the environment
api_key = os.getenv('ALPHA_VANTAGE_API_KEY')

# Initialize Alpha Vantage TimeSeries object with API key
ts = TimeSeries(key=api_key, output_format='pandas')

# Retrieve full 15-minute interval data for NVIDIA (NVDA) to cover the desired date range
data, meta_data = ts.get_intraday(symbol='tsla', interval='15min', outputsize='full')

# Ensure the data is sorted by time
data = data.sort_index()

# Filter data to keep only from October 15, 2024, to November 8, 2024
start_date = '2024-10-15'
end_date = '2024-11-08'
date_range_data = data[(data.index >= start_date) & (data.index <= end_date)]

# Check if there’s data for the specified date range
if not date_range_data.empty:
    # Calculate 15-minute returns
    date_range_data['Return'] = date_range_data['4. close'].pct_change()

    # Calculate intraday volatility as the standard deviation of 15-minute returns over the date range
    intraday_volatility = date_range_data['Return'].std()

    # Annualize the intraday volatility (optional)
    annualized_intraday_volatility = intraday_volatility * np.sqrt(1 * (390 / 15))

    # Print the number of data points for the date range
    print(f"Number of data points from {start_date} to {end_date}: {len(date_range_data)}")

    print(f"Intraday Volatility (15-minute) from {start_date} to {end_date}: {intraday_volatility}")
    print(f"Annualized Intraday Volatility (15-minute) from {start_date} to {end_date}: {annualized_intraday_volatility}")

    # Plotting the 15-minute closing prices for the specified date range
    plt.figure(figsize=(12, 6))
    plt.plot(date_range_data.index, date_range_data['4. close'], label='15-Minute Close Price')
    plt.title(f'NVIDIA (NVDA) 15-Minute Close Prices from {start_date} to {end_date}')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    plt.show()
else:
    print(f"No data available from {start_date} to {end_date}.")
