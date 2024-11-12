concurrent processing:
    for each image, text pair:
        1. convert text to audio
        2. combine audio and image to create video
    
    after all videos are created:
        3. combine all videos to create a single video
        4. upload the video to youtube



玄策财经 每日市场 2024-11-08

curl -X GET "https://api.stlouisfed.org/fred/series/observations?series_id=WTREGEN&observation_start=2024-11-01&api_key=${FRED_API_KEY}&file_type=json" | jq

curl -X GET "https://api.stlouisfed.org/fred/series/observations?series_id=WALCL&observation_start=2024-11-01&api_key=${FRED_API_KEY}&file_type=json" | jq

curl -X GET "https://api.stlouisfed.org/fred/series/observations?series_id=RRPONTSYD&observation_start=2024-11-01&api_key=${FRED_API_KEY}&file_type=json" | jq '.observations[] | {date: .date, value: .value}'


trading volume of big 7 to represent current market sentiment emotion


curl -X GET "https://pro-api.coinmarketcap.com/v1/cryptocurrency/ohlcv/historical?id=825&time_start=2023-01-01&time_end=2023-12-31&interval=daily" \
  -H "X-CMC_PRO_API_KEY: ${COINMARKETCAP_API_KEY}" | jq


