# Importing the yfinance package
import yfinance as yf
import pandas as pd

# Set the start and end date
start_date = '2020-01-01'
end_date = '2023-03-01'
 
# Set the ticker
ticker = 'GOOGL'
 
# Get the data
df = yf.download(ticker, start_date, end_date)
 
print(df)

import time
symbols = ['⣾', '⣷', '⣯', '⣟', '⡿', '⢿', '⣻', '⣽']
i = 0
while True:
    i = (i + 1) % len(symbols)
    print('\r\033[K%s loading...' % symbols[i], flush=True, end='')
    time.sleep(0.1)