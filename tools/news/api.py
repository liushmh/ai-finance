import requests

# Your API key
API_KEY = 'UBjRHjyGAxl0WmuHtYr07k96iOrQnAVp'

# URL for latest financial news
url = f'https://financialmodelingprep.com/api/v3/stock_news?tickers=NVDA,TSLA&from=2024-11-05&to=2024-11-06&limit=10&apikey={API_KEY}'

# Fetch the data
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    news_data = response.json()
    for article in news_data:
        print(f"Title: {article['title']}")
        print(f"Published Date: {article['publishedDate']}")
        print(f"Content: {article['text']}")
        print(f"URL: {article['url']}")
        print("-" * 50)
else:
    print("Failed to fetch data:", response.status_code)
