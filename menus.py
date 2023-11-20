from colors import *

line = color.BLUE + "---------------------------------"  + color.END

menus = {
    "StartUpMenu" : 
        color.BOLD + color.GREEN + "\nWelcome To The Stock Broker Simulation!" + color.END + color.END + "\n" +
        line +
        "\nPlease Choose an Option Below \n" + line + "\n" +
        color.GREEN + "1." + color.END + " Info \n" + 
        color.GREEN + "2." + color.END + " Update Simulation Parameters \n" + 
        color.GREEN + "3." + color.END + " Execute Simulation" + "\n" +
        color.GREEN + "4." + color.END + " Quit",

    "Info" : "This program was created to simulate markets and test different asset allocation strategies.\nIt works by pulling real data from yahoo finance and uploading that data into an SQL database.\nThis data is then used to simulate trades an analyze performance from those trades.\nTo get started, try setting up new simulation parameters in the menu menu by selecting option 2.",

    "InfoMenu" : 
        color.GREEN + "1." + color.END + " Back \n" + 
        color.GREEN + "2." + color.END + " Quit",


    "SimulationParametersMenu" : 
        color.GREEN + "\nSimulation Parameters" + color.END + "\n" +
        line + "\n" +
        color.GREEN + "1." + color.END + " View Customers in the Database \n" + 
        color.GREEN + "2." + color.END + " Add Customers to the Database \n" + 
        color.GREEN + "3." + color.END + " Remove Customers from the Database \n" + 
        color.GREEN + "4." + color.END + " Update Simulation Dates \n" + 
        color.GREEN + "5." + color.END + " Back \n" + 
        color.GREEN + "6." + color.END + " Quit",
}