import requests
from transformers import pipeline

def get_news_sentiment():   # <-- NO SPACES BEFORE THIS LINE
    API_KEY = "d25b33df55234f19b90d112029882452"

    url = (
        "https://newsapi.org/v2/everything?"
        "q=S%26P+500 OR SPY&"
        "language=en&"
        "pageSize=100&"
        "sortBy=publishedAt&"
        f"apiKey={API_KEY}"
    )

    response = requests.get(url)
    news_data = response.json()

    if "articles" not in news_data:
        print("No articles returned by NewsAPI")
        print(news_data)
        return 0

    sentiment = pipeline("sentiment-analysis", model="ProsusAI/finbert")

    positive = 0
    negative = 0
    neutral  = 0

    for article in news_data["articles"]:
        text = article.get("content") or article.get("description") or article["title"]

        result = sentiment(text[:512])[0]
        label = result["label"].lower()

        if label == "positive":
            positive += 1
        elif label == "negative":
            negative += 1
        else:
            neutral += 1

    total = positive + negative + neutral

    if total == 0:
        return 0

    news_sentiment_score = (positive - negative) / total * 100

    return news_sentiment_score  # MUST be inside the function






