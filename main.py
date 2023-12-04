import time
from datetime import date, datetime, timedelta
from menus import *
from database import *

simulation_start_date = "2022-01-01"
simulation_end_date = str(date.today())

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
    rollInOptions(menus["Info"], 1)
    print(line)
    rollInOptions(menus["InfoMenu"], .1)
    runMenu(menu_mappings["InfoMenu"])

def runSimulationParamsMenu():
    print(line)
    rollInOptions(menus["SimulationParametersMenu"], .1)
    runMenu(menu_mappings["SimulationParametersMenu"])

def runSimulationExecution(run_exec = None):
    print(line)
    if run_exec != False:
        #consider adding a multithreaded loading symbol
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
            simulation_start_date = datetime.strptime(str(dateObject), '%Y-%m-%d %H:%M:%S')
            if dateObject < (datetime.now() - timedelta(days=1)):
                s_date = dateObject
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
            simulation_end_date = datetime.strptime(str(dateObject), '%Y-%m-%d %H:%M:%S')
            if dateObject > s_date and dateObject < datetime.now():
                break
            print(line)
            print("End Date Must Come After Start Date and Must be in the Past!")
        except ValueError:
            print(line)
            print("Incorrect data format, should be YYYY-MM-DD")

    datesUpdated(simulation_start_date, simulation_end_date)
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


menu_mappings = {

    "StartUpMenu" : {
        '1':runInfo,
        '2':runSimulationParamsMenu,
        '3':runSimulationExecution,
        '4':exit_pro
    },

    "InfoMenu" : {
        '1':returnMainMenu,
        '2':exit_pro
    },

    "SimulationParametersMenu" : {
        '1':viewCustomers,
        '2':addCustomer,
        '3':removeCustomerMenu,
        '4':editSimDates,
        '5':returnMainMenu,
        '6':exit_pro
    },

    "SimulationExecutionMenu" : {
        '1':viewCustomersExec,
        '2':print,
        '3':print,
        '4':print,
        '5':print,
        '6':print,
        '7':print,
        '8':print,
        '9':returnMainMenu,
        '10':exit_pro
    },

}

def main():
    initializeDB()
    rollInOptions(menus["StartUpMenu"], .1)
    runMenu(menu_mappings["StartUpMenu"])

main()