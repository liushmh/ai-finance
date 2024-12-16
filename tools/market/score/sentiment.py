import yfinance as yf
import pandas as pd

# Big 7 Tickers
# tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA']
tickers = ['NVDA', 'TSLA', 'COIN']

# Download last 5 trading days of data
data = yf.download(tickers, period='5d', group_by='ticker')

# Function to calculate daily sentiment as a real number
def calculate_daily_sentiment(stock_data, price_weight=0.5, volume_weight=0.5):
    """
    Calculates daily sentiment score based on price and volume changes.
    If price change is negative, sentiment will be negative regardless of volume change.
    """
    sentiment_scores = []
    
    for i in range(1, len(stock_data)):
        # Calculate price and volume changes using .iloc for position-based indexing
        price_change = (stock_data['Close'].iloc[i] - stock_data['Open'].iloc[i]) / stock_data['Open'].iloc[i] * 100
        volume_change = (stock_data['Volume'].iloc[i] - stock_data['Volume'].iloc[i - 1]) / stock_data['Volume'].iloc[i - 1] * 100

        # Calculate sentiment score based on price change sign
        if price_change > 0:
            sentiment = (price_weight * price_change) + (volume_weight * volume_change)
        elif price_change < 0:
            sentiment = -(abs(price_weight * price_change) + abs(volume_weight * volume_change))
        else:
            sentiment = 0  # Neutral sentiment if no change in price

        sentiment_scores.append(sentiment)
    
    return sentiment_scores

# Initialize an empty DataFrame to store sentiment scores
sentiment_df = pd.DataFrame(index=data.index[1:])

# Calculate sentiment for each stock
for ticker in tickers:
    stock_data = data[ticker]
    sentiment_df[ticker] = calculate_daily_sentiment(stock_data)

# Sum sentiment scores across all stocks for each day
sentiment_df['Daily Sentiment Score'] = sentiment_df.sum(axis=1)

# Apply decay factor
decay_factor = 0.9
sentiment_df['Decayed Sentiment Score'] = [
    score * (decay_factor ** i) for i, score in enumerate(sentiment_df['Daily Sentiment Score'][::-1])
]

# Calculate the overall decayed sentiment score over the period
overall_sentiment_score = sentiment_df['Decayed Sentiment Score'].sum()

print(f"Overall Sentiment Score (with decay): {overall_sentiment_score:.2f}")

# Adjust min and max scores with decay
max_score_daily = 25
num_days = len(sentiment_df)  # Number of trading days

# Calculate decayed min and max scores over all days
decayed_max_scores = [max_score_daily * decay_factor ** i for i in range(num_days)]
decayed_min_scores = [-max_score_daily * decay_factor ** i for i in range(num_days)]
max_score = sum(decayed_max_scores) * len(tickers)
min_score = sum(decayed_min_scores) * len(tickers)

# Normalize the score to a range of 0-5
normalized_score = 5 * (overall_sentiment_score - min_score) / (max_score - min_score)
normalized_score = max(0, min(5, normalized_score))

# Output the result
print(f"Market Sentiment (0 to 5 scale, with decay): {normalized_score:.2f}")
