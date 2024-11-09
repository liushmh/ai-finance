import requests
import pandas as pd
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# Load environment variables from .env file
load_dotenv()

# Fetch the API key from the environment
api_key = os.getenv('FRED_API_KEY')

# Series IDs for different maturities
series_ids = {
    'DGS1MO': '1-Month',
    'DGS3MO': '3-Month',
    'DGS6MO': '6-Month',
    'DGS1': '1-Year',
    'DGS3': '3-Year',
    'DGS5': '5-Year',
    'DGS10': '10-Year',
    'DGS30': '30-Year'
}

# Calculate the date three months ago
today = datetime.today()
three_months_ago = today - timedelta(days=90)
observation_start = three_months_ago.strftime('%Y-%m-%d')

# Initialize an empty DataFrame
df_main = pd.DataFrame()

# Loop over each series ID to fetch and process data
for series_id, label in series_ids.items():
    # API URL with observation_start parameter
    url = (
        f'https://api.stlouisfed.org/fred/series/observations?'
        f'series_id={series_id}&'
        f'observation_start={observation_start}&'
        f'api_key={api_key}&file_type=json'
    )
    
    # Fetch data
    response = requests.get(url)
    data = response.json()
    
    # Check if data is available
    if 'observations' in data:
        # Convert to DataFrame and exclude 'realtime_start' and 'realtime_end'
        df = pd.DataFrame(data['observations'])
        df = df.drop(columns=['realtime_start', 'realtime_end'])
        df['date'] = pd.to_datetime(df['date'])
        df[label] = pd.to_numeric(df['value'], errors='coerce')
        df = df[['date', label]]
        
        # Merge with main DataFrame
        if df_main.empty:
            df_main = df
        else:
            df_main = pd.merge(df_main, df, on='date', how='outer')
    else:
        print(f"No data returned for series ID {series_id}")

# Sort the DataFrame by date
df_main = df_main.sort_values('date')

# Drop rows where all yield values are NaN
df_main = df_main.dropna(subset=series_ids.values(), how='all')

# Reset the index
df_main = df_main.reset_index(drop=True)

# Display the DataFrame
print(df_main)

# Export the DataFrame to a CSV file
output_filename = 'treasury_yields_last_3_months.csv'
df_main.to_csv(output_filename, index=False)
print(f"\nData has been exported to '{output_filename}'")
