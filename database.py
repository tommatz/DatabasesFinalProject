import sqlite3
import uuid
import yfinance as yf
import pandas as pd

cur = None
con = None

def readSQLFile(filename):
    with open('sqlfiles/'+filename, 'r') as sql_file:
        return(sql_file.read())

def initializeDB():
    global cur, con
    con = sqlite3.connect("financials.db")
    cur = con.cursor()
    cur.execute(readSQLFile("CreateCustomerTable.sql"))
    cur.execute(readSQLFile("CreateOrderHistoryTable.sql"))
    cur.execute(readSQLFile("CreateStrategiesTable.sql"))
    con.commit()

def addCustomer(uuid, f_name, l_name, cash):
    global cur, con
    cur.execute("""INSERT INTO CUSTOMER VALUES (?,?,?,?,?);""", (str(uuid), f_name, l_name, cash, cash))
    con.commit()

def addStrat(uuid, ticker, strat, percentage, s_date, e_date):
    global cur, con
    cur.execute("""INSERT INTO STRATEGIES VALUES (?,?,?,?);""", (str(uuid), strat, ticker, percentage))
    dowloadTickerInfo(ticker, s_date, e_date)
    con.commit()

def addNewClient(f_name, l_name, cash, ticker, strat, percentage, s_date, e_date):
    random_uuid = uuid.uuid4()
    addCustomer(random_uuid, f_name, l_name, cash)
    addStrat(random_uuid, ticker, strat, percentage, s_date, e_date)

def getCustomers():
    global cur, con
    res = cur.execute(readSQLFile("ViewAllCustomer.sql"))
    return res.fetchall()

def createTickerTable(ticker):
    global cur, con
    cur.execute("CREATE TABLE IF NOT EXISTS " + ticker + " (date PRIMARY KEY, open, high, low, close, adj_close, volume);")
    con.commit()

def insertOnTickerTable(ticker, date, open, high, low, close, adj_close, volume):
    global cur, con
    cur.execute("INSERT INTO " + ticker + " VALUES (?,?,?,?,?,?,?);", (str(date), open, high, low, close, adj_close, volume))
    con.commit()

def validateTicker(ticker):
    ticker = yf.Ticker(ticker)
    try:
        ticker.info
    except:
        return False
    return True

def dowloadTickerInfo(ticker, s_date, e_date):
    df = yf.download(ticker, s_date, e_date)
    createTickerTable(ticker)
    for x in df.index:
        insertOnTickerTable(ticker, x, df.loc[x]['Open'], df.loc[x]['High'], df.loc[x]['Low'], df.loc[x]['Close'], df.loc[x]['Adj Close'], df.loc[x]['Volume'])


def dropTable(ticker):
    global cur, con
    cur.execute("DROP TABLE IF EXISTS " + ticker+ ";")
    con.commit()

def datesUpdated(s_date, e_date):
    global cur, con
    res = cur.execute("""SELECT name FROM sqlite_master WHERE type='table';""")
    ticker_names = []
    for x in res.fetchall():
        x = list(x)
        if x[0] != 'CUSTOMER' and x[0] != 'ORDER_HISTORY' and x[0] != 'STRATEGIES':
            ticker_names.append(x[0])

    for x in ticker_names:
        dropTable(x)
        dowloadTickerInfo(x, s_date, e_date)