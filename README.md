# Random-Woz-Quote

Scrapes a bunch of the yellow box quotes from Woz's articles at supermemo.guru.

1. Get page links to articles by running the `get_page_links` function. Links will be saved to urls.txt.

2. Run the `get_quotes` function. Quotes will be saved to quotes.tsv

3. Run `awk -i inplace -F'\t' '!seen[$1]++' quotes.tsv` to remove duplicate quotes that appear in different articles.

This could easily be adapted to get the Anecdotes, Mottos, Metaphors etc that Woz keeps on supermemo.guru.
