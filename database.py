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
    cur.execute("""INSERT INTO CUSTOMER VALUES (?,?,?,?,?);""", (str(uuid), f_name, l_name, int(cash), int(cash)))
    con.commit()

def addStrat(uuid, ticker, strat, percentage, s_date, e_date):
    global cur, con
    cur.execute("""INSERT INTO STRATEGIES VALUES (?,?,?,?);""", (str(uuid), strat, ticker, float(percentage)))
    dowloadTickerInfo(ticker, s_date, e_date)
    con.commit()

def addNewClient(f_name, l_name, cash, ticker, strat, percentage, s_date, e_date):
    random_uuid = uuid.uuid4()
    addCustomer(random_uuid, f_name, l_name, cash)
    addStrat(random_uuid, ticker, strat, percentage, s_date, e_date)

def getCustomers():
    global cur, con
    res = cur.execute("SELECT * FROM CUSTOMER;")
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

def addOrder(uuid, ticker, date, order_type, cash_amount, execution_time):
    global cur, con
    cur.execute("INSERT INTO ORDER_HISTORY VALUES (?,?,?,?,?,?);", (uuid, ticker, date, order_type, cash_amount, execution_time))
    con.commit()

def validateCustomer(uuid):
    global cur, con
    res = cur.execute("SELECT * FROM CUSTOMER WHERE uuid = ?;", (uuid,))
    if (len(res.fetchall()) > 0):
        return True
    return False

def removeCustomer(uuid):
    global cur, con
    cur.execute("DELETE FROM CUSTOMER WHERE uuid = ?;", (uuid,))
    cur.execute("DELETE FROM STRATEGIES WHERE uuid = ?;", (uuid,))
    con.commit()

def clearOrderTable():
    global cur, con
    cur.execute("DELETE FROM ORDER_HISTORY;")
    con.commit()

def retrieveStrategies():
    global cur, con
    res = cur.execute("SELECT * FROM STRATEGIES;")
    return (list(res.fetchall()))

def retrieveCustomerStrategies(uuid):
    global cur, con
    res = cur.execute("SELECT * FROM STRATEGIES WHERE uuid = ?;", (uuid,))
    return (list(res.fetchall()))

def getAllDates(ticker):
    global cur, con
    res = cur.execute(f"SELECT date FROM {ticker};")
    return (list(res.fetchall()))

def getRedDates(ticker):
    global cur, con
    res = cur.execute(f"SELECT date FROM {ticker} WHERE open < close;")
    return (list(res.fetchall()))

def getGreenDates(ticker):
    global cur, con
    res = cur.execute(f"SELECT date FROM {ticker} WHERE open > close;")
    return (list(res.fetchall()))

def getOnePercentDropDates(ticker):
    global cur, con
    res = cur.execute(f"SELECT date FROM {ticker} WHERE open < 0.99 * close;")
    return (list(res.fetchall()))

def getCustomerCash(uuid):
    global cur, con
    res = cur.execute("SELECT starting_cash, current_cash FROM CUSTOMER WHERE uuid = ?;", (uuid,))
    return res.fetchone()

def setCustomerCash(uuid, val):
    global cur, con
    cur.execute("UPDATE CUSTOMER SET current_cash = ? WHERE uuid = ?;", (val, uuid))
    con.commit()

def resetCustomerCash():
    global cur, con
    cur.execute("UPDATE CUSTOMER SET current_cash = starting_cash;")
    con.commit()

def getStockValueOnDate(ticker, date):
    global cur, con
    res = cur.execute(f"SELECT close FROM {ticker} WHERE date = ?;", (date,))
    return (res.fetchone())

def getStockMaxDate(ticker):
    global cur, con
    res = cur.execute(f"SELECT date FROM {ticker} WHERE date = (SELECT MAX(date) FROM {ticker});")
    return (res.fetchone())

def getCustomerStrategies(uuid_c):
    global cur, con
    res = cur.execute("SELECT * FROM STRATEGIES WHERE uuid = ?;", (uuid_c,))
    return (list(res.fetchall()))  

def getCustomerCurrentCash(uuid_c):
    global cur, con
    res = cur.execute("SELECT current_cash FROM CUSTOMER WHERE uuid = ?;", (uuid_c,))
    return (res.fetchone())

def executeTradesOnDateTable(strat, date_table):
    starting_cash, current_cash = getCustomerCash(strat[0])
    for date in date_table:
        if current_cash <= 0:
            break

        cash_order_size = round(starting_cash*(strat[3]/100), 2)
        if cash_order_size > current_cash:
            cash_order_size = current_cash

        addOrder(strat[0], strat[2], date[0], "BUY", cash_order_size, "CLOSE")
        current_cash -= cash_order_size

    setCustomerCash(strat[0], current_cash)

def executeSimulation():
    resetCustomerCash()
    clearOrderTable()
    strats = retrieveStrategies()
    for strat in strats:
        if strat[1] == '1': #Buy Every Day
            date_table = getAllDates(strat[2])
            executeTradesOnDateTable(strat, date_table)

        elif strat[1] == '2': #Buy Every Red Day
            date_table = getRedDates(strat[2])
            executeTradesOnDateTable(strat, date_table)

        elif strat[1] == '3': #Buy Every Green Day
            date_table = getGreenDates(strat[2])
            executeTradesOnDateTable(strat, date_table)

        elif strat[1] == '4': #Buy Every Day of 1% Drop
            date_table = getOnePercentDropDates(strat[2])
            executeTradesOnDateTable(strat, date_table)

def calculatePortfolioValue(uuid, date):
    simulatated_tickers = []
    strats = retrieveCustomerStrategies(uuid)
    for strat in strats:
        simulatated_tickers.append(strat[2])

    if len(simulatated_tickers) <= 0:
        current_cash = getCustomerCurrentCash(uuid)
        return current_cash[0]

    query = "SELECT"

    for ticker in simulatated_tickers:
        query += (" SUM(ORDER_HISTORY.cash_amount/" + ticker + ".close)")

    query += " FROM ORDER_HISTORY"

    for ticker in simulatated_tickers:
        query += (", " + ticker)

    query += f" WHERE ORDER_HISTORY.uuid = '{uuid}' AND "

    for i in range(len(simulatated_tickers)):
        if i > 0:
            query += " OR "
        query += (f"(ORDER_HISTORY.ticker = '{simulatated_tickers[i]}' AND ORDER_HISTORY.date = {simulatated_tickers[i]}.date)")

    query += ";"

    res = cur.execute(query)
    results_list = (list(res.fetchall()))

    true_holdings = []
    portfolio_value = 0

    for i in range(len(simulatated_tickers)):
        true_holdings.append([simulatated_tickers[i], results_list[i][0]])

    for i in range(len(true_holdings)):
        end_value = getStockValueOnDate(true_holdings[i][0], date)

        if end_value == None:
            max_date = getStockMaxDate(true_holdings[i][0])
            end_value = getStockValueOnDate(true_holdings[i][0], max_date[0])

        cash_value = round(end_value[0] * true_holdings[i][1], 2)
        portfolio_value += cash_value

    current_cash = getCustomerCurrentCash(uuid)

    portfolio_value += current_cash[0]
    return portfolio_value
