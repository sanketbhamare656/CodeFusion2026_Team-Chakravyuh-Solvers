import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS

def scrape_duckduckgo():
    """Fetch cybersecurity news using DuckDuckGo search."""
    with DDGS() as ddgs:
        results = list(ddgs.news("cybersecurity latest news", max_results=7))
    return [{"title": res.get("title", "No title"), "url": res.get("url", "")} for res in results]

def scrape_hacker_news(news_queue):
    """Scrapes The Hacker News and adds articles to the queue."""
    url = "https://thehackernews.com/"
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        articles = soup.find_all("div", class_="body-post clear")
        if not articles:
            print("⚠ No articles found on The Hacker News!")
            return

        for article in articles[:7]:
            title = article.find("h2", class_="home-title").text.strip()
            link = article.find("a", class_="story-link")["href"]
            news_queue.appendleft({"title": title, "link": link})
    except Exception as e:
        print(f"Error scraping The Hacker News: {e}")
