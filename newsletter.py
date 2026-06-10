import requests
import time
from collections import deque
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
from apscheduler.schedulers.background import BackgroundScheduler

# Store only the latest 10 articles
news_queue = deque(maxlen=10)

def fetch_cybersecurity_news():
    """Fetches, updates, and maintains only the latest 10 cybersecurity news articles."""
    print("\n=== Fetching Latest Cybersecurity News ===\n")

    count_before = len(news_queue)

    # Fetch from DuckDuckGo News
    try:
        with DDGS() as ddgs:
            results = list(ddgs.news("cybersecurity latest news", max_results=7))  # Fetch more articles
            for res in results:
                add_news_to_queue(res.get("title", "No title"), res.get("url", ""))
    except Exception as e:
        print(f"Error fetching DDG news: {e}")

    # Fetch from The Hacker News
    try:
        scrape_hacker_news()
    except Exception as e:
        print(f"Error fetching Hacker News: {e}")

    # Ensure at least 10 articles are stored
    if len(news_queue) < 10:
        print(f"⚠ Only {len(news_queue)} articles fetched. Retrying...")
        fetch_backup_news()

    # Display updated queue
    display_news()

def fetch_backup_news():
    """Fetches additional cybersecurity articles if queue is below 10."""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.news("cybersecurity latest", max_results=5))  # Try again with 5 more
            for res in results:
                if len(news_queue) >= 10:
                    break
                add_news_to_queue(res.get("title", "No title"), res.get("url", ""))
    except Exception as e:
        print(f"Error fetching backup news: {e}")

def add_news_to_queue(title, link):
    """Fetches article content and adds it to the queue."""
    if not link:
        return

    content = scrape_news(link)
    if not content:
        content = "Content unavailable. Click to read full article."

    news_queue.appendleft({"title": title, "link": link, "content": content[:500]})  # Store first 500 chars

def scrape_news(url):
    """Scrapes content from a news URL."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract article content
        article = soup.find("article") or soup
        paragraphs = article.find_all(["p", "div.article-text"], limit=10)
        content = " ".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))

        return content if len(content) > 50 else None  # Reduce threshold to 50 chars
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

def scrape_hacker_news():
    """Scrapes The Hacker News and adds articles to the queue."""
    try:
        url = "https://thehackernews.com/"
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        articles = soup.find_all("div", class_="body-post clear")
        if not articles:
            print("⚠ No articles found on The Hacker News!")
            return

        for article in articles[:7]:  # Fetch more articles
            try:
                title = article.find("h2", class_="home-title").text.strip()
                link = article.find("a", class_="story-link")["href"]
                add_news_to_queue(title, link)
            except Exception as e:
                print(f"Error processing Hacker News article: {e}")
    except Exception as e:
        print(f"Error fetching Hacker News: {e}")

def display_news():
    """Displays the 10 most recent news articles."""
    print("\n=== Latest Cybersecurity News (Top 10) ===\n")
    for i, news in enumerate(news_queue, 1):
        print(f"{i}. {news['title']}\n   {news['content']}...\n   [Read More]({news['link']})\n")

# Initialize scheduler
scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(fetch_cybersecurity_news, "interval", hours=1)  # Updates every hour
scheduler.start()

if __name__ == "__main__":
    print("Cybersecurity News Monitor starting...\n")
    fetch_cybersecurity_news()  # Initial update
    try:
        while True:
            time.sleep(3600)  # Keep running
    except KeyboardInterrupt:
        print("\nStopping monitor...")
        scheduler.shutdown()