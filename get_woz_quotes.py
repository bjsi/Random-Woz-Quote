from bs4 import BeautifulSoup
import csv
import requests, random


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
    for quote_div in soup.find_all("div", {"class": "bs-callout-highlight"}):
        quote_obj = {}
        quote_obj['quote'] = quote_div.get_text()
        quote_obj['author'] = "Piotr Wozniak"
        quote_obj['url'] = url
        quote_obj['title'] = title.get_text()
        woz_quotes.append(quote_obj)
    return woz_quotes


def main():
    found_quotes = False
    while not found_quotes:
        page = get_random_page()
        if page:
            quotes = parse_html(page)
            if quotes:
                break
    with open('quotes.csv', 'w', newline='') as f:
        fieldnames = ['quote', 'author', 'url', 'title']
        writer = csv.DictWriter(f, delimiter='|', fieldnames=fieldnames)
        writer.writeheader()
        for quote in quotes:
            writer.writerow(quote)


if __name__ == "__main__":
    main()
