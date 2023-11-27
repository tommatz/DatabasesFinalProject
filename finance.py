import yfinance as yf
import pandas as pd

def validateTicker(ticker):
    ticker = yf.Ticker(ticker)
    try:
        ticker.info
    except:
        return False
    return True
