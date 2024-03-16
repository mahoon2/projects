import requests
from bs4 import BeautifulSoup

# URL of the FDA Press Announcements page
url = "https://www.fda.gov/news-events/fda-newsroom/press-announcements"

def fetch_latest_articles(url):
    # Fetch the webpage content
    response = requests.get(url)
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    # Find all article links or titles (adjust the selector as needed)
    articles = soup.find_all('div', class_='views-field views-field-title')
    # Extract and return the article titles or URLs
    return [article.text.strip() for article in articles]

if __name__ == "__main__":
    latest_articles = fetch_latest_articles(url)
    print("Latest FDA Press Announcements:")
    for article in latest_articles:
        print(article)