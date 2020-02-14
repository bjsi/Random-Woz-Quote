from bs4 import BeautifulSoup
import csv
import requests
import time


def clean_quote(quote):
    quote = quote.strip('\"')
    quote = quote.strip('\n')
    quote = quote.replace('\n', ' ')
    if not (quote.endswith('.') or quote.endswith('!') or quote.endswith('?')):
        quote += '.'
    return quote


def parse_html(response):
    """
    Parse the html page for the yellow boxes Woz keeps his quotes in.
    The yellow boxes are div elements with 'bs-callout-highlight' as the class.
    """
    page = response.content
    soup = BeautifulSoup(page, "html.parser")
    url = response.url
    # Find the article title
    title = soup.find("h1", {"class": "firstHeading"})
    # Each article can contain multiple quotes so we use a list.
    woz_quotes = []
    for quote_div in soup.find_all("div",
                                   class_='bs-callout-highlight'):
        quote_obj = {}
        quote_obj['quote'] = clean_quote(quote_div.get_text())
        quote_obj['author'] = "Piotr Wozniak"
        quote_obj['url'] = url
        quote_obj['title'] = title.get_text().strip()
        woz_quotes.append(quote_obj)
    return woz_quotes


# Save a list of quotes to a tab-separated file
def save_to_tsv(quotes):
    with open('quotes.tsv', 'a', newline='') as f:
        fieldnames = ['quote', 'author', 'url', 'title']
        writer = csv.DictWriter(f, delimiter='\t', fieldnames=fieldnames)
        for quote in quotes:
            writer.writerow(quote)


def get_page_links():
    # These links hold many links to woz's articles
    urls = ["https://supermemo.guru/wiki/SuperMemo_Guru",
            'https://supermemo.guru/wiki/Pleasure_of_learning',
            'https://supermemo.guru/wiki/Problem_of_Schooling']
    # Using a set to only keep unique urls
    scraped_urls = set()
    for url in urls:
        response = requests.get(url)
        page = response.content
        soup = BeautifulSoup(page, "html.parser")
        # find all the a elements (links)
        for a in soup.find_all("a", href=True):
            # Add the base url to relative urls
            if a['href'].startswith('/'):
                scraped_urls.add("https://supermemo.guru" + a['href'])
            # Skip # fragment identifiers
            elif a['href'].startswith("#"):
                pass
            # Skip urls not from supermemo.guru
            elif 'supermemo.guru' not in a['href']:
                pass
            else:
                scraped_urls.add(a['href'])
    # Write the urls to a text file
    with open('urls.txt', 'a') as f:
        for item in scraped_urls:
            f.write(f"{item}\n")


def get_quotes():
    with open('urls.txt') as f:
        count = 0
        try:
            for url in f.readlines():
                count += 1
                url = url.strip()
                res = requests.get(url)
                quotes = parse_html(res)
                print(f"Parsing url #{count}: {url}")
                if quotes:
                    print(f"Found {len(quotes)} quote(s).")
                    for idx, quote in enumerate(quotes):
                        print(f"#{idx}: {quote}")
                    # save each page's quotes to .tsv file
                    save_to_tsv(quotes)
                else:
                    print("Didn't find any quotes.")
            # sleep for 2 seconds between requests.
            time.sleep(2)
        except Exception as e:
            print(f"Failed at url #{count}: {url}. Exception: {e}")
