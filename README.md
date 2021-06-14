# proxyscraper
Simple Proxy Scraper

This simple proxy scraper allows the user to scrape proxies from four different sites to a CSV filename and directory they chose.
Once the CSV file is saved after scraping, there is a Ping test functionality which will allow the user to select one of the generated CSV files containing the scraped proxies, the user will be able to select a filename and path to save a new CSV file which will contain the list of proxies with the status UP or Down noted beside them.

Dependencies:

- sys
- csv
- subprocess
- os
- requests
- bs4 (beautifulsoup)
- tkinter


Script is extremely basic for now, but I plan to add much more functionality when possible.

