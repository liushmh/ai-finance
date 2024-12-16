import requests
import pandas as pd
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
fred_api_key = os.getenv('FRED_API_KEY')

# Define the FRED series ID for SOFR
repo_series_id = 'SOFR'

# Define the date range (last year)
today = datetime.today()
one_year_ago = today - timedelta(days=365)
observation_start = one_year_ago.strftime('%Y-%m-%d')

# Construct the API URL for the repo rate
url = (
    f'https://api.stlouisfed.org/fred/series/observations?'
    f'series_id={repo_series_id}&'
    f'observation_start={observation_start}&'
    f'api_key={fred_api_key}&file_type=json'
)

# Fetch the data
response = requests.get(url)
data = response.json()

# Process the data if observations are found
if 'observations' in data:
    df_repo = pd.DataFrame(data['observations'])
    df_repo['date'] = pd.to_datetime(df_repo['date'])
    df_repo['SOFR'] = pd.to_numeric(df_repo['value'], errors='coerce')
    df_repo = df_repo[['date', 'SOFR']]
    
    # Display the data
    print("Repo Rate (SOFR) Data:")
    print(df_repo)
else:
    print("No data returned for the repo rate series.")
