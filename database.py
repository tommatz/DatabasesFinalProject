import sqlite3
import uuid
import yfinance as yf
import pandas as pd
from datetime import date, datetime, timedelta

cur = None
con = None

def translateTicker(raw_yfinance_ticker):
    translation = raw_yfinance_ticker
    translation = translation.replace("^","I_")
    translation = translation.replace("=","EQ_")
    translation = translation.replace("-","D_")
    translation = translation.replace(".","P_")
    return translation

def translateBackTicker(transed_yfinance_ticker):
    translation = transed_yfinance_ticker
    translation = translation.replace("I_","^")
    translation = translation.replace("EQ_","=")
    translation = translation.replace("D_","-")
    translation = translation.replace("P_",".")
    return translation

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

def getSimulatedStocks():
    global cur, con
    res = cur.execute("""SELECT name FROM sqlite_master WHERE type='table';""")
    ticker_names = []
    for x in res.fetchall():
        x = list(x)
        if x[0] != 'CUSTOMER' and x[0] != 'ORDER_HISTORY' and x[0] != 'STRATEGIES' and x[0][-4:] != 'NEWS':
            ticker_names.append(x[0])

    return(ticker_names)

def addStrat(uuid, ticker, strat, percentage, s_date, e_date):
    global cur, con
    cur.execute("""INSERT INTO STRATEGIES VALUES (?,?,?,?);""", (str(uuid), strat, ticker, float(percentage)))
    tickers = getSimulatedStocks()
    if not ticker in tickers:
        dowloadTickerInfo(ticker, s_date, e_date)
    con.commit()

def addNewClient(f_name, l_name, cash, ticker, strat, percentage, s_date, e_date):
    random_uuid = uuid.uuid4()
    addCustomer(random_uuid, f_name, l_name, cash)
    addStrat(random_uuid, ticker, strat, percentage, s_date, e_date)

def createNewsTable(ticker):
    global cur, con
    ticker = translateTicker(ticker)
    cur.execute("CREATE TABLE IF NOT EXISTS " + ticker + "_NEWS (ticker NOT NULL, title NOT NULL, publisher, link NOT NULL, PRIMARY KEY (link));")
    con.commit()

def getCustomers():
    global cur, con
    res = cur.execute("SELECT * FROM CUSTOMER;")
    return res.fetchall()

def getCustomer(uuid):
    global cur, con
    res = cur.execute(f"SELECT * FROM CUSTOMER WHERE uuid = '{uuid}';")
    return res.fetchone()

def createTickerTable(ticker):
    global cur, con
    ticker = translateTicker(ticker)
    cur.execute("CREATE TABLE IF NOT EXISTS " + ticker + " (date PRIMARY KEY, open, high, low, close, adj_close, volume);")
    con.commit()

def insertOnTickerTable(ticker, date, open, high, low, close, adj_close, volume):
    global cur, con
    ticker = translateTicker(ticker)
    cur.execute("INSERT INTO " + ticker + " VALUES (?,?,?,?,?,?,?);", (str(date), open, high, low, close, adj_close, volume))
    con.commit()

def insertNews(ticker, title, publisher, link):
    global cur, con
    ticker = translateTicker(ticker)
    cur.execute("INSERT INTO " + ticker + "_NEWS VALUES (?,?,?,?);", (ticker, title, publisher, link))
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
    
    createNewsTable(ticker)
    tick = yf.Ticker(ticker)
    news = tick.news

    for i in range(len(news)):
        if i < 3:
            insertNews(ticker, news[i]["title"], news[i]["publisher"], news[i]["link"])
        else:
            break

def dropTable(ticker):
    global cur, con
    cur.execute("DROP TABLE IF EXISTS " + ticker+ ";")
    con.commit()

def datesUpdated(s_date, e_date):
    global cur, con
    res = cur.execute("""SELECT name FROM sqlite_master WHERE type='table';""")
    ticker_names = []
    ticker_names_translated = []

    for x in res.fetchall():
        x = list(x)
        if x[0] != 'CUSTOMER' and x[0] != 'ORDER_HISTORY' and x[0] != 'STRATEGIES':
            ticker_names.append(translateBackTicker(x[0]))
            ticker_names_translated.append(x[0])

    for x in ticker_names_translated:
        dropTable(x)

    for x in ticker_names:
        if x[-4:] != "NEWS":
            dowloadTickerInfo(x, s_date, e_date)

def addOrder(uuid, ticker, date, order_type, cash_amount, execution_time):
    global cur, con
    ticker = translateTicker(ticker)
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

def getStockNearestDate(ticker, date):
    global cur, con
    res = cur.execute(f"SELECT date FROM {ticker} WHERE date = (SELECT MAX(date) FROM {ticker} WHERE date <= '{date}');")
    return (res.fetchone())

def getStockNearestDateLower(ticker):
    global cur, con
    res = cur.execute(f"SELECT Min(date) FROM {ticker};")
    return (res.fetchone())

def getCustomerStrategies(uuid_c):
    global cur, con
    res = cur.execute("SELECT * FROM STRATEGIES WHERE uuid = ?;", (uuid_c,))
    return (list(res.fetchall()))  

def getCustomerStartingCash(uuid_c):
    global cur, con
    res = cur.execute("SELECT starting_cash FROM CUSTOMER WHERE uuid = ?;", (uuid_c,))
    return (res.fetchone())

def getStocksBestValue(ticker):
    global cur, con
    res = cur.execute(f"SELECT MAX(high), date FROM {ticker};")
    return list(res.fetchone())

def getStocksWorstValue(ticker):
    global cur, con
    res = cur.execute(f"SELECT MIN(low), date FROM {ticker};")
    return list(res.fetchone())

def getBestPerformingStock(s_date, e_date, worst):
    global cur, con
    tickers = getSimulatedStocks()

    query = "SELECT"

    for i in range(len(tickers)):
        if i > 0:
            query += ","
        query += f" {tickers[i]}_start.close AS {tickers[i]}_start_close, {tickers[i]}_end.close AS {tickers[i]}_end_close"

    query += " FROM"

    for i in range(len(tickers)):
        real_s_date = getStockNearestDate(tickers[i], s_date)
        if real_s_date == None:
            real_s_date = getStockNearestDateLower(tickers[i])

        real_e_date = getStockNearestDate(tickers[i], e_date)
        if real_e_date == None:
            real_e_date = getStockNearestDateLower(tickers[i])

        if i > 0:
            query += ","
        query += f" (SELECT close FROM {tickers[i]} WHERE date = '{real_s_date[0]}') AS {tickers[i]}_start,"
        query += f" (SELECT close FROM {tickers[i]} WHERE date = '{real_e_date[0]}') AS {tickers[i]}_end"

    query += ";"
    
    res = cur.execute(query)
    res =  list(res.fetchone())
    final_results = []

    for i in range(0, len(res), 2):
        v1 = res[i]
        v2 = res[i + 1]
        percent_change = ((v2 - v1)/abs(v1))*100
        final_results.append([tickers[int(i/2)], percent_change, v1, v2])

    best_chg = final_results[0][1]
    best = final_results[0]

    for i in range(1, len(final_results)):
        if worst != True:
            if final_results[i][1] > best_chg:
                best_chg = final_results[i][1]
                best = final_results[i]
        else:
            if final_results[i][1] < best_chg:
                best_chg = final_results[i][1]
                best = final_results[i]

    return best

def executeTradesOnDateTable(date_table, uuid):
    starting_cash, current_cash = getCustomerCash(uuid)
    for i in range(len(date_table)):
        date = date_table[i][0]
        strat = date_table[i][1]
        
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
    customers = list(getCustomers())

    for customer in customers:
        full_date_table = []
        for strat in strats:

            if strat[0] == customer[0]:

                if strat[1] == '1': #Buy Every Day
                    date_table = getAllDates(translateTicker(strat[2]))

                elif strat[1] == '2': #Buy Every Red Day
                    date_table = getRedDates(translateTicker(strat[2]))

                elif strat[1] == '3': #Buy Every Green Day
                    date_table = getGreenDates(translateTicker(strat[2]))

                elif strat[1] == '4': #Buy Every Day of 1% Drop
                    date_table = getOnePercentDropDates(translateTicker(strat[2]))
                
                for date in date_table:
                    full_date_table.append([date, strat])

        full_date_table.sort()

        executeTradesOnDateTable(full_date_table, customer[0])

    
def calculatePortfolioValue(uuid, date):
    simulatated_tickers = []
    strats = retrieveCustomerStrategies(uuid)
    for strat in strats:
        simulatated_tickers.append(translateTicker(strat[2]))

    if len(simulatated_tickers) <= 0:
        current_cash = getCustomerStartingCash(uuid)
        return current_cash[0]
    
    true_holdings = []

    for i in range(len(simulatated_tickers)):
        query = ("SELECT SUM(ORDER_HISTORY.cash_amount/" + simulatated_tickers[i] + ".close)")
        query += f" FROM ORDER_HISTORY, {simulatated_tickers[i]}"
        query += f" WHERE ORDER_HISTORY.uuid = '{uuid}' AND ORDER_HISTORY.date <= '{date}' AND "
        query += (f"(ORDER_HISTORY.ticker = '{simulatated_tickers[i]}' AND ORDER_HISTORY.date = {simulatated_tickers[i]}.date);")

        res = cur.execute(query)
        results_list = res.fetchone()[0]
        if results_list == None:
            true_holdings.append([simulatated_tickers[i], 0])
        else:
            true_holdings.append([simulatated_tickers[i], results_list])

    portfolio_value = 0

    for i in range(len(true_holdings)):
        real_date = getStockNearestDate(true_holdings[i][0], date)

        if real_date == None:
            real_date = getStockNearestDateLower(true_holdings[i][0])

        end_value = getStockValueOnDate(true_holdings[i][0], real_date[0])
        cash_value = round(end_value[0] * true_holdings[i][1], 2)
        portfolio_value += cash_value

    starting_cash = getCustomerStartingCash(uuid)[0]

    res = cur.execute("SELECT SUM(cash_amount) FROM ORDER_HISTORY WHERE uuid = ? and date <= ?;", (uuid, date, ))
    spent = res.fetchone()[0]
    if spent != None:
        starting_cash -= spent

    portfolio_value += starting_cash
    return round(portfolio_value, 2)


def getCustomerNews(uuid):
    global cur, con
    tickers = []
    strats = retrieveCustomerStrategies(uuid)
    for strat in strats:
        tickers.append(translateTicker(strat[2]))
    
    query = ""
    for i in range(len(tickers)):
        if i > 0:
            query += " UNION ALL "

        query += "SELECT * FROM "
        query += (tickers[i] + "_NEWS ")

    query += ";"
    res = cur.execute(query)
    return list(res.fetchall())
