import requests
from twilio.rest import Client

VIRTUAL_TWILIO_NUMBER = "YOUR TWILIO VIRTUAL NUMBER"
VERIFIED_NUMBER = "YOUR NUMBER"

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "STOCK'S API KEY"
NEWS_API_KEY = "NEWMS WEBSITE'S API KEY"
TWILIO_SID = "YOUR TWILIO SID"
TWILIO_AUTH_TOKEN = "YOUR TWILIO AUTH TOKEN"

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
