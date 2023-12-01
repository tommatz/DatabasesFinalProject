from database import *

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
