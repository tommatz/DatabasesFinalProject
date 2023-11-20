import time
from colors import *
from menus import *

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

def returnMainMenu():
    rollInOptions(menus["StartUpMenu"], .1)
    runMenu(menu_mappings["StartUpMenu"])

menu_mappings = {
    
    "StartUpMenu" : {
        '1':runInfo,
        '2':runSimulationParamsMenu,
        '3':print,
        '4':exit_pro
    },

    "InfoMenu" : {
        '1':returnMainMenu,
        '2':exit_pro
    },

    "SimulationParametersMenu" : {
        '1':print,
        '2':print,
        '3':print,
        '4':print,
        '5':returnMainMenu,
        '6':exit_pro
    },

}

def main():
    rollInOptions(menus["StartUpMenu"], .1)
    runMenu(menu_mappings["StartUpMenu"])

main()

