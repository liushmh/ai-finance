import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime

# Define the date range
start_date = '2023-11-15'
end_date = '2024-11-08'

# Fetch S&P 500 index data (^GSPC) using yfinance
spx_data = yf.download('^GSPC', start=start_date, end=end_date, interval='1d')

# Check if there’s data for the specified date range
if not spx_data.empty:
    # Rename the adjusted close column for convenience
    spx_data = spx_data.rename(columns={'Adj Close': 'Adjusted Close'})

    # Print the number of data points
    print(f"Number of data points for S&P 500 (^GSPC) from {start_date} to {end_date}: {len(spx_data)}")
    
    # Plotting the daily adjusted close prices for the specified date range
    plt.figure(figsize=(12, 6))
    plt.plot(spx_data.index, spx_data['Adjusted Close'], label='S&P 500 Daily Adjusted Close')
    plt.title(f'S&P 500 Daily Adjusted Close from {start_date} to {end_date}')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
else:
    print(f"No data available for S&P 500 from {start_date} to {end_date}.")
