import requests
import pandas as pd
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import yfinance as yf

# Load environment variables from .env file
load_dotenv()

# Fetch the API key from the environment
fred_api_key = os.getenv('FRED_API_KEY')

# Series IDs for different Treasury maturities (excluding 30-Year)
series_ids = {
    'DGS1MO': '1-Month',
    'DGS3MO': '3-Month',
    'DGS6MO': '6-Month',
    'DGS1': '1-Year',
    'DGS3': '3-Year',
    'DGS5': '5-Year',
    'DGS10': '10-Year'
}

# Calculate the date one year ago
today = datetime.today()
one_year_ago = today - timedelta(days=365)
observation_start = one_year_ago.strftime('%Y-%m-%d')

# Initialize an empty DataFrame for Treasury yields
df_treasury = pd.DataFrame()

# Loop over each series ID to fetch and process Treasury data
for series_id, label in series_ids.items():
    url = (
        f'https://api.stlouisfed.org/fred/series/observations?'
        f'series_id={series_id}&'
        f'observation_start={observation_start}&'
        f'api_key={fred_api_key}&file_type=json'
    )
    response = requests.get(url)
    data = response.json()
    
    if 'observations' in data:
        df = pd.DataFrame(data['observations'])
        df = df.drop(columns=['realtime_start', 'realtime_end'])
        df['date'] = pd.to_datetime(df['date'])
        df[label] = pd.to_numeric(df['value'], errors='coerce')
        df = df[['date', label]]
        
        if df_treasury.empty:
            df_treasury = df
        else:
            df_treasury = pd.merge(df_treasury, df, on='date', how='outer')
    else:
        print(f"No data returned for series ID {series_id}")

# Sort and clean the Treasury yields data
df_treasury = df_treasury.sort_values('date')
df_treasury = df_treasury.dropna(subset=series_ids.values(), how='all').reset_index(drop=True)

# Calculate daily changes for each maturity
for label in series_ids.values():
    if label in df_treasury.columns:
        df_treasury[label + '_change'] = df_treasury[label].diff().abs()

# Plot Treasury Yields with top 10 largest daily changes highlighted
fig, ax = plt.subplots(figsize=(12, 6))

# Plot each Treasury yield
for label in series_ids.values():
    if label in df_treasury.columns:
        ax.plot(df_treasury['date'], df_treasury[label], label=label)
        
        # Identify top 10 largest daily changes
        top_10_changes = df_treasury.nlargest(10, label + '_change')
        
        # Highlight these points on the plot
        ax.scatter(top_10_changes['date'], top_10_changes[label], color='red', zorder=5)

ax.set_title('Treasury Yields Over the Past Year with Top 10 Largest Daily Changes Highlighted')
ax.set_xlabel('Date')
ax.set_ylabel('Yield (%)')
ax.legend(title="Treasury Maturities")
ax.grid(True)
ax.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.show()
