import time
from datetime import date, datetime, timedelta
from menus import *
from database import *
from plot import *

simulation_start_date = "2022-01-01"
simulation_end_date = str(date.today())

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

def rollInOptions(text, delay):
    start = 0
    for i in range(len(text)):
        if text[i] == '\n':
            time.sleep(delay)
            sub = text[start:i]
            print(sub)
            start = i+1
            
    time.sleep(delay)
    sub = text[start:len(text)]
    print(sub)    

def runMenu(menu_mapping):
    val = None
    while val == None:
        print(line)
        val = input("Navigate to: ")
        if val in menu_mapping:
            menu_mapping[val]()
        else:
            print("Invalid Navigation, Try Again")
            val = None

def exit_pro():
    print(color.RED + "Exiting Program" + color.END)
    return

def runInfo():
    print(line)
    rollInOptions(menus["Info"], .1)
    enterToContinue()
    rollInOptions(menus["StartUpMenu"], .1)
    runMenu(menu_mappings["StartUpMenu"])

def runSimulationParamsMenu():
    print(line)
    rollInOptions(menus["SimulationParametersMenu"], .1)
    runMenu(menu_mappings["SimulationParametersMenu"])

def runSimulationExecution(run_exec = None):
    print(line)
    if run_exec != False:
        executeSimulation()
    rollInOptions(menus["SimulationExecutionMenu"], .1)
    runMenu(menu_mappings["SimulationExecutionMenu"])  

def returnMainMenu():
    rollInOptions(menus["StartUpMenu"], .1)
    runMenu(menu_mappings["StartUpMenu"])

def stratNumToText(num):
    if num == 1:
        return "everyday at market close"
    elif num == 2:
        return "every red day at market close"
    elif num == 3:
        return "every green day at market close"
    elif num == 4:
        return "every day there is at least a 1" + "%" + " drop"
    
def enterToContinue():
    while True:
        print(line)
        f_name = input("Please Press ENTER to Continue...")
        if f_name != None:
            break
        print("How did we even end up here")

def viewCustomers(isSimParam = None):
    customers = getCustomers()
    for x in customers:
        print(line)
        uuid_c = x[0]
        f_name = x[1]
        l_name = x[2]
        s_cash = "{:.2f}".format(x[3])
        c_cash = "{:.2f}".format(x[4])
        strats = getCustomerStrategies(uuid_c)
        print(f"Customer {f_name} {l_name} with uuid: {uuid_c}")
        time.sleep(.1)
        print(f"started with ${s_cash} and currently has ${c_cash} in cash.")
        print(white_line)
        time.sleep(.1)
        print(f"{f_name}'s Trading Strategy:")
        time.sleep(.1)
        print(white_line)
        for y in strats:
            time.sleep(.1)
            strat_type = stratNumToText(int(y[1]))
            ticker = y[2]
            percent = y[3]
            print(f"{f_name} is trading ticker symbol: {ticker} with the strategy of spending")
            time.sleep(.1)
            print(f"{percent}% of their cash while buying {strat_type}.")

        enterToContinue()

    if isSimParam != False:
        runSimulationParamsMenu()
    else:
        runSimulationExecution(False)

def viewCustomersExec():
    viewCustomers(False)

def editSimDates():
    global simulation_start_date, simulation_end_date
    rollInOptions(menus["EditSimDatesMenu"], .1)

    s_date = None
    while True:
        print(line)
        s_date = input("Define Simulation Start Date (YYYY-MM-DD): ")
        date_format = '%Y-%m-%d'
        try:
            dateObject = datetime.strptime(s_date, date_format)
            if dateObject < (datetime.now() - timedelta(days=1)):
                s_date = dateObject
                simulation_start_date = str(s_date.date())
                break
            print(line)
            print("Start Date Must be in the Past!")
        except ValueError:
            print(line)
            print("Incorrect data format, should be YYYY-MM-DD")

    e_date = None
    while True:
        print(line)
        e_date = input("Define Simulation End Date (YYYY-MM-DD): ")
        date_format = '%Y-%m-%d'
        try:
            dateObject = datetime.strptime(e_date, date_format)
            if dateObject > s_date and dateObject < datetime.now():
                e_date = dateObject
                simulation_end_date = str(e_date.date())
                break
            print(line)
            print("End Date Must Come After Start Date and Must be in the Past!")
        except ValueError:
            print(line)
            print("Incorrect data format, should be YYYY-MM-DD")

    datesUpdated(s_date, e_date)
    print(line)
    print("Successfully updated simulation dates")
    runSimulationParamsMenu()

def addCustomer():
    rollInOptions(menus["AddCustomersMenu"], .1)

    f_name = None
    while True:
        print(line)
        f_name = input("Define Customer's First Name: ")
        if f_name.isalpha():
            break
        print("Only valid letter selections are permitted")

    l_name = None
    while True:
        print(line)
        l_name = input("Define Customer's Last Name: ")
        if l_name.isalpha():
            break
        print("Only valid letter selections are permitted")

    starting_cash = None
    while True:
        print(line)
        starting_cash = input("Define Starting Cash Balance: $")
        if starting_cash.isnumeric():
            break
        print("This must be a valid number, please exclude commas.")

    ticker = None
    while True:
        print(line)
        ticker = input("Input a Valid Stock Ticker: ")
        ticker = ticker.upper()
        if validateTicker(ticker):
            break
        print("This ticker was not valid. Please try again.")

    print(line)
    rollInOptions(menus["Strategies"], .1)

    strategy = None
    while True:
        print(line)
        strategy = input("Choose a Strategy: ")
        if strategy.isnumeric() and int(strategy) <= 4:
            break
        print("Please Make a Valid Selection")

    investment_percentage = None
    while True:
        print(line)
        investment_percentage = input("Define Percentage to Invest per Order: ")
        if investment_percentage.replace(".", "").isnumeric() and float(investment_percentage) <= 100:
            break
        print("This must be a valid percentage. Do not include the percentage sign.")

    try:
        addNewClient(f_name, l_name, starting_cash, ticker, strategy, investment_percentage, simulation_start_date, simulation_end_date)
    except:
        print("Something went wrong adding your selection. Exiting Program")
        return -1
    
    print(line)
    print("Successfully added " + f_name + " " + l_name + " to the database")
    runSimulationParamsMenu()

def removeCustomerMenu():
    rollInOptions(menus["RemoveCustomerMenu"], .1)

    uuid_input = None
    while True:
        print(line)
        uuid_input = input("Please Input a Valid UUID or '1' to Go Back: ")
        if uuid_input == '1' or validateCustomer(uuid_input):
            break
        print("This Customer Does Not Exist. Please Try Again")

    if uuid_input != '1':
        removeCustomer(uuid_input)
        print("Successfully Removed " + uuid_input + " From the Database")

    print(line)
    rollInOptions(menus["SimulationParametersMenu"], .1)
    runMenu(menu_mappings["SimulationParametersMenu"])

def getDateFrame(end_date):
    start = datetime.strptime(simulation_start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    dates = []
    current_date = start

    while current_date <= end:
        dates.append(str(current_date.date()))
        current_date += timedelta(days=1)

    return dates

def reportCustomerPortfolioValue():
    rollInOptions(menus["CustomerReportMenu"], .1)

    uuid_input = None
    while True:
        print(line)
        uuid_input = input("Please Input a Valid UUID or '1' to Go Back: ")
        if uuid_input == '1' or validateCustomer(uuid_input):
            break
        print("This Customer Does Not Exist. Please Try Again")

    if uuid_input != '1':
        port_value = calculatePortfolioValue(uuid_input, simulation_end_date)
        customer = getCustomer(uuid_input)
        print(line)
        print(f"{customer[1]} {customer[2]} started with ${round(customer[3],2)} after the simulation \ntheir net portfolio value is ${round(port_value, 2)}.")
        dates = getDateFrame(simulation_end_date)
        generatePortfolioPlot(uuid_input, dates)
        
    print(line)
    rollInOptions(menus["SimulationExecutionMenu"], .1)
    runMenu(menu_mappings["SimulationExecutionMenu"])

def outputSimulatedStocks():
    rollInOptions(menus["SimulatedStocksMenu"], .1)
    print(line)

    tickers = getSimulatedStocks()
    for ticker in tickers:
        print(translateBackTicker(ticker))
        print(white_line)

    enterToContinue()
    rollInOptions(menus["SimulationExecutionMenu"], .1)
    runMenu(menu_mappings["SimulationExecutionMenu"])


def outputBestPerformingStock():
    rollInOptions(menus["BestPerformingStockMenu"], .1)
    print(line)

    result = getBestPerformingStock(simulation_start_date, simulation_end_date, False)
    print(f"The best performing stock from the simulation was {translateBackTicker(result[0])}.")
    time.sleep(.1)
    print(f"{translateBackTicker(result[0])} started with a value of ${round(result[2], 2)} and ended with a value of ${round(result[3], 2)}.")
    time.sleep(.1)
    print(f"This resulted in a {round(result[1] ,2)}% percent change from {simulation_start_date} to {simulation_end_date}.")
    time.sleep(.1)

    enterToContinue()
    rollInOptions(menus["SimulationExecutionMenu"], .1)
    runMenu(menu_mappings["SimulationExecutionMenu"])

def outputWorstPerformingStock():
    rollInOptions(menus["WorstPerformingStockMenu"], .1)
    print(line)

    result = getBestPerformingStock(simulation_start_date, simulation_end_date, True)
    print(f"The worst performing stock from the simulation was {translateBackTicker(result[0])}.")
    time.sleep(.1)
    print(f"{translateBackTicker(result[0])} started with a value of ${round(result[2], 2)} and ended with a value of ${round(result[3], 2)}.")
    time.sleep(.1)
    print(f"This resulted in a {round(result[1] ,2)}% percent change from {simulation_start_date} to {simulation_end_date}.")
    time.sleep(.1)

    enterToContinue()
    rollInOptions(menus["SimulationExecutionMenu"], .1)
    runMenu(menu_mappings["SimulationExecutionMenu"])

def outputBestStockDay():
    rollInOptions(menus["BestStockDayMenu"], .1)
    tickers = getSimulatedStocks()

    ticker = None
    while True:
        print(line)
        ticker = input("Input a Stock Ticker in the Simulation or '1' for Back: ")
        ticker = ticker.upper()
        ticker = translateTicker(ticker)
        if ticker == '1' or ticker in tickers:
            break
        print("This ticker was not valid. Please try again.")

    if ticker != '1':
        print(white_line)
        result = getStocksBestValue(ticker)
        print(f"{translateBackTicker(ticker)} had its highest value on {result[1][:-9]} where it achieved a peak value of ${round(result[0], 2)}.")

    enterToContinue()
    rollInOptions(menus["SimulationExecutionMenu"], .1)
    runMenu(menu_mappings["SimulationExecutionMenu"])

def outputWorstStockDay():
    rollInOptions(menus["WorstStockDayMenu"], .1)
    tickers = getSimulatedStocks()

    ticker = None
    while True:
        print(line)
        ticker = input("Input a Stock Ticker in the Simulation or '1' for Back: ")
        ticker = ticker.upper()
        ticker = translateTicker(ticker)
        if ticker == '1' or ticker in tickers:
            break
        print("This ticker was not valid. Please try again.")

    if ticker != '1':
        print(white_line)
        result = getStocksWorstValue(ticker)
        print(f"{translateBackTicker(ticker)} had its lowest value on {result[1][:-9]} where it fell to a value of ${round(result[0], 2)}.")

    enterToContinue()
    rollInOptions(menus["SimulationExecutionMenu"], .1)
    runMenu(menu_mappings["SimulationExecutionMenu"])

def addTradingStrategy():
    rollInOptions(menus["AddStrategyMenu"], .1)

    uuid_input = None
    while True:
        print(line)
        uuid_input = input("Please Input a Valid UUID or '1' to Go Back: ")
        if uuid_input == '1' or validateCustomer(uuid_input):
            break
        print("This Customer Does Not Exist. Please Try Again")

    if uuid_input != '1':
        ticker = None
        while True:
            print(line)
            ticker = input("Input a Valid Stock Ticker: ")
            ticker = ticker.upper()
            if validateTicker(ticker):
                break
            print("This ticker was not valid. Please try again.")

        print(line)
        rollInOptions(menus["Strategies"], .1)

        strategy = None
        while True:
            print(line)
            strategy = input("Choose a Strategy: ")
            if strategy.isnumeric() and int(strategy) <= 4:
                break
            print("Please Make a Valid Selection")

        investment_percentage = None
        while True:
            print(line)
            investment_percentage = input("Define Percentage to Invest per Order: ")
            if investment_percentage.replace(".", "").isnumeric() and float(investment_percentage) <= 100:
                break
            print("This must be a valid percentage. Do not include the percentage sign.")

        addStrat(uuid_input, ticker, strategy, investment_percentage, simulation_start_date, simulation_end_date)
        print("Successfully added new trading strategy")

    print(line)
    rollInOptions(menus["SimulationParametersMenu"], .1)
    runMenu(menu_mappings["SimulationParametersMenu"])
    
def reportCustomerPortfolioValueOnDate():
    rollInOptions(menus["CustomerReportMenu"], .1)

    uuid_input = None
    while True:
        print(line)
        uuid_input = input("Please Input a Valid UUID or '1' to Go Back: ")
        if uuid_input == '1' or validateCustomer(uuid_input):
            break
        print("This Customer Does Not Exist. Please Try Again")

    if uuid_input != '1':
        
        s_date = None
        while True:
            print(line)
            s_date = input("Date (YYYY-MM-DD): ")
            date_format = '%Y-%m-%d'
            try:
                dateObject = datetime.strptime(s_date, date_format)
                start_date = datetime.strptime(simulation_start_date, date_format)
                end_date = datetime.strptime(simulation_end_date, date_format)
                if dateObject <= end_date and dateObject >= start_date:
                    s_date = dateObject
                    break
                print(line)
                print("Date be between simulation dates! " + simulation_start_date + " - " + simulation_end_date)

            except ValueError:
                print(line)
                print("Incorrect data format, should be YYYY-MM-DD")

        customer = getCustomer(uuid_input)
        port_value = calculatePortfolioValue(uuid_input, s_date)
        print(line)
        print(f"{customer[1]} {customer[2]} started with ${round(customer[3],2)}, on {str(s_date)[:-9]} their \nnet portfolio value is ${round(port_value, 2)}.")
        dates = getDateFrame(str(s_date)[:-9])
        generatePortfolioPlot(uuid_input, dates)

    print(line)
    rollInOptions(menus["SimulationExecutionMenu"], .1)
    runMenu(menu_mappings["SimulationExecutionMenu"])


menu_mappings = {

    "StartUpMenu" : {
        '1':runInfo,
        '2':runSimulationParamsMenu,
        '3':runSimulationExecution,
        '4':exit_pro
    },

    "SimulationParametersMenu" : {
        '1':viewCustomers,
        '2':addCustomer,
        '3':addTradingStrategy,
        '4':removeCustomerMenu,
        '5':editSimDates,
        '6':returnMainMenu,
        '7':exit_pro
    },

    "SimulationExecutionMenu" : {
        '1':viewCustomersExec,
        '2':outputSimulatedStocks,
        '3':reportCustomerPortfolioValue,
        '4':reportCustomerPortfolioValueOnDate,
        '5':outputBestPerformingStock,
        '6':outputWorstPerformingStock,
        '7':outputBestStockDay,
        '8':outputWorstStockDay,
        '9':returnMainMenu,
        '10':exit_pro
    },

}

def main():
    initializeDB()
    rollInOptions(menus["StartUpMenu"], .1)
    runMenu(menu_mappings["StartUpMenu"])

main()