from bs4 import BeautifulSoup
import csv
import requests, random
import time


def get_random_page():
    url = "https://supermemo.guru/wiki/Special:Random"
    response = requests.get(url)
    return response


def parse_html(response):
    page = response.content
    soup = BeautifulSoup(page, "html.parser")
    url = response.url
    title = soup.find("h1", {"class": "firstHeading"})
    woz_quotes = []
    for quote_div in soup.find_all("div",
                                   class_='bs-callout-highlight'):
        quote_obj = {}
        quote_obj['quote'] = quote_div.get_text()
        quote_obj['author'] = "Piotr Wozniak"
        quote_obj['url'] = url
        quote_obj['title'] = title.get_text()
        woz_quotes.append(quote_obj)
    return woz_quotes


def save_to_csv(quotes):
    with open('quotes.csv', 'a', newline='') as f:
        fieldnames = ['quote', 'author', 'url', 'title']
        writer = csv.DictWriter(f, delimiter='|', fieldnames=fieldnames)
        for quote in quotes:
            writer.writerow(quote)


def get_page_links():
    urls = ["https://supermemo.guru/wiki/SuperMemo_Guru",
            'https://supermemo.guru/wiki/Pleasure_of_learning',
            'https://supermemo.guru/wiki/Problem_of_Schooling']
    scraped_urls = set()
    for url in urls:
        response = requests.get(url)
        page = response.content
        soup = BeautifulSoup(page, "html.parser")
        for a in soup.find_all("a", href=True):
            if a['href'].startswith('/') or a['href'].startswith("#"):
                scraped_urls.add("https://supermemo.guru" + a['href'])
            else:
                scraped_urls.add(a['href'])
    with open('urls.txt', 'a') as f:
        for item in scraped_urls:
            f.write(f"{item}\n")


if __name__ == "__main__":
    with open('urls.txt') as f:
        for url in f.readlines():
            url = url.strip()
            res = requests.get(url)
            quotes = parse_html(res)
            print(quotes)
            save_to_csv(quotes)
            time.sleep(1)
