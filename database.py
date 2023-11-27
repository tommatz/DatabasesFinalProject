import sqlite3

def readSQLFile(filename):
    with open('sqlfiles/'+filename, 'r') as sql_file:
        return(sql_file.read())


def initializeDB():
    con = sqlite3.connect("financials.db")
    cur = con.cursor()
    cur.execute(readSQLFile("CreateCustomerTable.sql"))
    cur.execute(readSQLFile("CreateOrderHistoryTable.sql"))
    cur.execute(readSQLFile("CreateStrategiesTable.sql"))

