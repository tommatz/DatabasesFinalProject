class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

line = color.BLUE + "---------------------------------"  + color.END

white_line = "---------------------------------"

menus = {
    "StartUpMenu" : 
        color.BOLD + color.GREEN + "\nWelcome To The Stockbroker Simulation!" + color.END + color.END + "\n" +
        line +
        "\nPlease Choose an Option Below \n" + line + "\n" +
        color.GREEN + "1." + color.END + " Info \n" + 
        color.GREEN + "2." + color.END + " Update Simulation Parameters \n" + 
        color.GREEN + "3." + color.END + " Execute Simulation" + "\n" +
        color.GREEN + "4." + color.END + " Quit",

    "Info" : "This program was created to simulate markets and test different asset allocation strategies.\nIt works by pulling real data from yahoo finance and uploading that data into an SQL database.\nThis data is then used to simulate trades and analyze performance from those trades.\nTo get started, try setting up new simulation parameters by selecting option 2 in the main menu.",

    "InfoMenu" : 
        color.GREEN + "1." + color.END + " Back \n" + 
        color.GREEN + "2." + color.END + " Quit",


    "SimulationParametersMenu" : 
        color.BOLD + color.GREEN + "\nSimulation Parameters" + color.END + color.END + "\n" +
        line + "\n" +
        color.GREEN + "1." + color.END + " View Customers in the Database \n" + 
        color.GREEN + "2." + color.END + " Add Customers to the Database \n" + 
        color.GREEN + "3." + color.END + " Remove Customers from the Database \n" + 
        color.GREEN + "4." + color.END + " Update Simulation Dates \n" + 
        color.GREEN + "5." + color.END + " Back \n" + 
        color.GREEN + "6." + color.END + " Quit",

    "SimulationExecutionMenu" : 
        color.BOLD + color.GREEN + "\nSimulation Reports" + color.END + color.END + "\n" +
        line + "\n" +
        color.GREEN + "1." + color.END + " View Customers in the Database \n" + 
        color.GREEN + "2." + color.END + " View Simulated Stocks \n" + 
        color.GREEN + "3." + color.END + " Report Customer Portfolio Value \n" + 
        color.GREEN + "4." + color.END + " Report Customer Portfolio Value on Specific Date \n" + 
        color.GREEN + "5." + color.END + " Report Best Performing Stock From Simulation \n" + 
        color.GREEN + "6." + color.END + " Report Worst Performing Stock From Simulation \n" + 
        color.GREEN + "7." + color.END + " Report Stock's Highest Value From Simulation \n" + 
        color.GREEN + "8." + color.END + " Report Stock's Lowest Value From Simulation \n" + 
        color.GREEN + "9." + color.END + " Back \n" + 
        color.GREEN + "10." + color.END + " Quit",

    "AddCustomersMenu" : color.BOLD + color.GREEN + "\nAdd Customer" + color.END + color.END,

    "Strategies" : color.BOLD + color.GREEN + "\nPlease Select a Strategy" + color.END + color.END + "\n" +
        line + "\n" +
        color.GREEN + "1." + color.END + " Buy Every Day at Market Close\n" + 
        color.GREEN + "2." + color.END + " Buy Every Red Day at Market Close \n" + 
        color.GREEN + "3." + color.END + " Buy Every Green Day at Market Close \n" + 
        color.GREEN + "4." + color.END + " Buy Every Day There is at least a 1" + "%" + " drop at Market Close",

    "EditSimDatesMenu" : color.BOLD + color.GREEN + "\nEdit Simulation Dates" + color.END + color.END,

    "RemoveCustomerMenu" : color.BOLD + color.GREEN + "\nRemove Customer" + color.END + color.END,

    "CustomerReportMenu" : color.BOLD + color.GREEN + "\nCustomer Report" + color.END + color.END,

}