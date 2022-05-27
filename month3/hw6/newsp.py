from bs4 import BeautifulSoup
import requests

Url = 'https://rezka.ag/?filter=last'

header = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36"
}


def get_html(url, params=''):
    req = requests.get(url, headers=header, params=params)
    return req


def get_data(html):
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all(class_='b-content__inline_item-link')
    news = []
    print(items)
    for item in items:
        news.append({
                'title': item.find("a").getText(),
                'origin': item.find("div").getText(),
                'link': item.find("a").get("href")
        })
    return news


def parser():
    html = get_html(Url)
    if html.status_code == 200:
        news = []
        for page in range(1, 3):
            html = get_html(f"https://rezka.ag/page/{page}/?filter=last")
            news.extend(get_data(html.text))
        return news
    else:
        raise Exception("Error in parser!")

