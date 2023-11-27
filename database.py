import sqlite3
import uuid

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

def addStrat(uuid, ticker, strat, percentage):
    global cur, con
    cur.execute("""INSERT INTO STRATEGIES VALUES (?,?,?,?);""", (str(uuid), strat, ticker, percentage))
    con.commit()

def addNewClient(f_name, l_name, cash, ticker, strat, percentage):
    random_uuid = uuid.uuid4()
    addCustomer(random_uuid, f_name, l_name, cash)
    addStrat(random_uuid, ticker, strat, percentage)