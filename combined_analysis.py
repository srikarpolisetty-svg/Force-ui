import newsapi_indicators
print("\nDEBUG:", dir(newsapi_indicators))


from redditapi_ndicators import get_reddit_sentiment
from newsapi_indicators import get_news_sentiment


reddit_score = get_reddit_sentiment()
news_score = get_news_sentiment()

final_score = reddit_score + news_score

print("Reddit Score:", reddit_score)
print("News Score:", news_score)
print("Final Combined Score:", final_score)