import requests
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import matplotlib.pyplot as plt

# Load environment variables from .env file
load_dotenv()

# Fetch the FRED API key from the environment
fred_api_key = os.getenv('FRED_API_KEY')

# Define the FRED series IDs and their corresponding descriptions
series_info = {
    'WTREGEN': 'Liabilities: U.S. Treasury, General Account: Week Average',
    'WALCL': 'Total Assets (Less Eliminations from Consolidation): Wednesday Level',
    'RRPONTSYD': 'Overnight Reverse Repurchase Agreements: Treasury Securities Sold'
}

# Calculate the start date for recent 6 months
today = datetime.today()
six_months_ago = today - timedelta(days=180)
observation_start = six_months_ago.strftime('%Y-%m-%d')

# Function to fetch data from FRED API and apply forward fill for missing values
def fetch_fred_data(series_id, api_key, start_date, multiply_by_1000=False):
    url = (
        f'https://api.stlouisfed.org/fred/series/observations?'
        f'series_id={series_id}&'
        f'observation_start={start_date}&'
        f'api_key={api_key}&file_type=json'
    )
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'observations' in data:
            df = pd.DataFrame(data['observations'])
            df['date'] = pd.to_datetime(df['date'])
            df['value'] = pd.to_numeric(df['value'], errors='coerce')
            # Multiply values by 1000 if specified
            if multiply_by_1000:
                df['value'] *= 1000
            # Keep only the 'date' and 'value' columns
            df = df[['date', 'value']].rename(columns={'value': series_id})
            df.set_index('date', inplace=True)
            # Forward fill missing values in this individual series
            df.fillna(method='ffill', inplace=True)
            return df
        else:
            print(f"No observations found for series {series_id}")
            return pd.DataFrame()
    else:
        print(f"Error fetching data for series {series_id}: {response.status_code}")
        return pd.DataFrame()

# Fetch data for each series, applying multiplication and forward fill as needed
wtregen_df = fetch_fred_data('WTREGEN', fred_api_key, observation_start, multiply_by_1000=True)
walcl_df = fetch_fred_data('WALCL', fred_api_key, observation_start)
rrpontsyd_df = fetch_fred_data('RRPONTSYD', fred_api_key, observation_start, multiply_by_1000=True)

# Merge dataframes on date index, using WALCL as the standard
if not walcl_df.empty and not wtregen_df.empty and not rrpontsyd_df.empty:
    combined_df = walcl_df.join(wtregen_df, how='left').join(rrpontsyd_df, how='left')
    combined_df.reset_index(inplace=True)

    # Calculate WALCL - WTREGEN - RRPONTSYD
    combined_df['WALCL - WTREGEN - RRPONTSYD'] = combined_df['WALCL'] - combined_df['WTREGEN'] - combined_df['RRPONTSYD']

    # Save to a single CSV file
    output_filename = f"combined_fred_data_{datetime.now().strftime('%Y%m%d')}.csv"
    combined_df.to_csv(output_filename, index=False)
    print(f"Data saved to {output_filename}")

    # Display the combined data
    print(combined_df)

    # Plot only WALCL - WTREGEN - RRPONTSYD
    plt.figure(figsize=(12, 6))
    plt.plot(combined_df['date'], combined_df['WALCL - WTREGEN - RRPONTSYD'], label='WALCL - WTREGEN - RRPONTSYD', color='purple', marker='o', linestyle='-')
    plt.title('WALCL - WTREGEN - RRPONTSYD Over the Past 6 Months')
    plt.xlabel('Date')
    plt.ylabel('Difference')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
else:
    print("Data for one or more series could not be retrieved.")
