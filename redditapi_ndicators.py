from transformers import pipeline
import praw

def get_reddit_sentiment():   # ✅ this matches the import in combined_analysis.py

    # AI sentiment analysis using FinBERT
    sentiment = pipeline(
        task="sentiment-analysis",
        model="ProsusAI/finbert"
    )

    # --- REDDIT AUTH ---
    reddit = praw.Reddit(
        client_id="Rzf4ZZa7EfGHaPBCM3nGyw",
        client_secret="xLS2M2Y3tkJ6jgEvhRPzYZ2PaP5nyg",
        user_agent="sentiment_bot"
    )

    subreddit = reddit.subreddit("SPY")  # or "investing", "wallstreetbets"

    positive = 0
    negative = 0
    neutral = 0

    for post in subreddit.hot(limit=100):   # limit to avoid API rate problems
        text = post.title + " " + (post.selftext or "")  # title + body text

        result = sentiment(text[:512])[0]  # limit text
        label = result["label"].lower()

        # sentiment scoring
        if label == "positive":
            positive += 1
        elif label == "negative":
            negative += 1
        else:
            neutral += 1

    total = positive + negative + neutral

    if total == 0:
        return 0  # avoid division by zero if no posts were scanned

    reddit_sentiment_score = (positive - negative) / total * 100

    return reddit_sentiment_score  # ✅ return score, don't print here
