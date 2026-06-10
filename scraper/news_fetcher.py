from collections import deque
from scraper.scraper import scrape_hacker_news, scrape_duckduckgo

# Store only the latest 10 articles
news_queue = deque(maxlen=10)

def get_latest_news():
    """Fetch and return the latest cybersecurity news."""
    if not news_queue:  # Fetch if empty
        fetch_cybersecurity_news()
    return list(news_queue)

def fetch_cybersecurity_news():
    """Fetch cybersecurity news from various sources."""
    print("\n=== Fetching Latest Cybersecurity News ===\n")

    try:
        results = scrape_duckduckgo()
        for res in results:
            add_news_to_queue(res["title"], res["url"])
    except Exception as e:
        print(f"Error fetching DDG news: {e}")

    try:
        scrape_hacker_news(news_queue)
    except Exception as e:
        print(f"Error fetching Hacker News: {e}")

def add_news_to_queue(title, link):
    """Adds article to the queue."""
    if not link:
        return
    news_queue.appendleft({"title": title, "link": link})
