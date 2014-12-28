import csv
import json

tickers_dict = {}

with open('WIKI_tickers.csv', 'rU') as f:
    reader = csv.reader(f)
    next(reader)  # skip the header
    for code, name in reader:
        ticker = code.split('/')[1]
        tickers_dict[ticker] = name

json.dump(tickers_dict, open("tickers_dict.json", "wb"), indent=2)