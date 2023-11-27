import time
from colors import *
from menus import *
from database import *
from finance import *

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

def runSimulationExecution():
    print(line)
    rollInOptions(menus["SimulationExecutionMenu"], .1)
    runMenu(menu_mappings["SimulationExecutionMenu"])  

def returnMainMenu():
    rollInOptions(menus["StartUpMenu"], .1)
    runMenu(menu_mappings["StartUpMenu"])

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
        addNewClient(f_name, l_name, starting_cash, ticker, strategy, investment_percentage)
    except:
        print("Something went wrong adding your selection. Exiting Program")
        return -1
    
    print(line)
    print("Successfully added " + f_name + " " + l_name + " to the database")
    runSimulationParamsMenu()

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
        '1':print,
        '2':addCustomer,
        '3':print,
        '4':print,
        '5':returnMainMenu,
        '6':exit_pro
    },

    "SimulationExecutionMenu" : {
        '1':print,
        '2':print,
        '3':print,
        '4':print,
        '5':print,
        '6':print,
        '7':print,
        '8':returnMainMenu,
        '9':exit_pro
    },

}

def main():
    initializeDB()
    rollInOptions(menus["StartUpMenu"], .1)
    runMenu(menu_mappings["StartUpMenu"])

main()