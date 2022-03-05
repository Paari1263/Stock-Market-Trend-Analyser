import requests
from twilio.rest import Client

VIRTUAL_TWILIO_NUMBER = "+18126338878"
VERIFIED_NUMBER = "+918870166755"

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "9OCOOZ5OUH5OKY9W"
NEWS_API_KEY = "461830ae643c447887cd6f9856f2d2ce"
TWILIO_SID = "AC4dc7e5a723d650f89ade64ad79f8054c"
TWILIO_AUTH_TOKEN = "c47bd6131cc5685a7027ddede864e5e9"

stock_params = {
    "function":"TIME_SERIES_DAILY",
    "symbol":STOCK_NAME,
    "apikey":STOCK_API_KEY
}

response = requests.get(url=STOCK_ENDPOINT,params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for(key,value) in data.items()]

yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]

day_before_yesterday_data = data_list[0]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]

difference  = abs(float(yesterday_closing_price)-float(day_before_yesterday_closing_price))

up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

diff_percent = (difference/float(yesterday_closing_price))*100

if(diff_percent > 1):
    news_params = {
        "apiKey":NEWS_API_KEY,
        "q":COMPANY_NAME
    }
    news_response = requests.get(url=NEWS_API_KEY,params=news_params)
    articles = news_response.json()["articles"]
    three_articles = articles[:3]
    formatted_articles = [f"{STOCK_NAME}: {up_down}{diff_percent}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]

    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_=VIRTUAL_TWILIO_NUMBER,
            to=VERIFIED_NUMBER
        )

    print(message.status)