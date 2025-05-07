import requests
from bs4 import BeautifulSoup

def get_bbc_news():
    url = 'https://vnexpress.net/'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    articles = []

    # Search for headlines wrapped in the 'gs-c-promo-heading' class
    for item in soup.find_all('a', class_='gs-c-promo-heading'):
        title = item.get_text(strip=True)
        link = 'https://www.bbc.com' + item.get('href')
        articles.append({'title': title, 'link': link})

    return articles
