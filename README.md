export $(grep -v '^#' .env | xargs)

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

curl -X GET "https://api.stlouisfed.org/fred/series/observations?series_id=RRPONTSYD&observation_start=2024-11-22&observation_end=2024-12-30&api_key=${FRED_API_KEY}&file_type=json" | jq '.observations[] | {date: .date, value: .value}'

trading volume of big 7 to represent current market sentiment emotion


curl -X GET "https://pro-api.coinmarketcap.com/v1/cryptocurrency/ohlcv/historical?id=825&time_start=2024-10-01&time_end=2024-11-11&interval=daily" \
  -H "X-CMC_PRO_API_KEY: ${COINMARKETCAP_API_KEY}" | jq

curl -X GET "https://newsapi.org/v2/everything?q=tesla&apiKey=${NEWS_API_KEY}&sortBy=publishedAt&language=en&pageSize=5" \
     -H "Accept: application/json" | jq

curl -X GET "https://api.diffbot.com/v3/article?query=Tesla&size=5&sort=published&token=${DIFFBOT_TOKEN}"

curl -X GET "https://api.diffbot.com/v3/search?token=${DIFFBOT_TOKEN}&col=GLOBAL-INDEX&query=type:article%20tags.label:Tesla%20sortby:date"


curl -X GET "https://api.diffbot.com/v3/search?token=${DIFFBOT_TOKEN}&col=GLOBAL-INDEX&query=Tesla%20sortby:date"

curl -X GET "https://api.polygon.io/v2/reference/news?ticker=TSLA&limit=5&order=desc&sort=published_utc" \
     -H "Authorization: Bearer ${POLYGONIO_API_KEY}" | jq

curl -X GET "https://newsapi.org/v2/everything?q=nvidia&apiKey=${NEWS_API_KEY}&sortBy=publishedAt&language=en&pageSize=3" \
     -H "Accept: application/json" | jq

curl -X GET "https://newsapi.org/v2/everything?q=bitcoin&apiKey=${NEWS_API_KEY}&sortBy=publishedAt&language=en&pageSize=5" \
     -H "Accept: application/json" | jq

curl -X GET "https://newsapi.org/v2/everything?q=ethereum&apiKey=${NEWS_API_KEY}&sortBy=publishedAt&language=en&pageSize=5" \
     -H "Accept: application/json" | jq

curl -X GET "https://newsapi.org/v2/everything?q=solana&apiKey=${NEWS_API_KEY}&sortBy=relevancy&language=en&pageSize=3" \
     -H "Accept: application/json" | jq


curl --request GET \
	--url 'https://yahoo-finance166.p.rapidapi.com/api/news/list-by-symbol?s=NVDA&region=US&snippetCount=5' \
	--header 'x-rapidapi-host: yahoo-finance166.p.rapidapi.com' \
	--header 'x-rapidapi-key: 3005c31d10msh2fa4415583a1e50p1a9e32jsnbc18f48c4d94' | jq '.data.main.stream[] | { 
      id: .content.id, 
      title: .content.title, 
      pubDate: .content.pubDate, 
      url: .content.clickThroughUrl.url, 
      provider: .content.provider.displayName, 
      thumbnail: (.content.thumbnail.resolutions[0]?.url // "N/A") 
    }'

curl --request GET \
	--url 'https://yahoo-finance166.p.rapidapi.com/api/news/list-by-symbol?s=BTC&region=US&snippetCount=5' \
	--header 'x-rapidapi-host: yahoo-finance166.p.rapidapi.com' \
	--header 'x-rapidapi-key: 3005c31d10msh2fa4415583a1e50p1a9e32jsnbc18f48c4d94' | jq '.data.main.stream[] | { 
      id: .content.id, 
      title: .content.title, 
      pubDate: .content.pubDate, 
      url: .content.clickThroughUrl.url, 
      provider: .content.provider.displayName, 
      thumbnail: (.content.thumbnail.resolutions[0]?.url // "N/A") 
    }'

11-11 3.7
11-12 2.83
11-13 2.83
11-14 2.31