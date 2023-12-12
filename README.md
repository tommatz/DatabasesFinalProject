<div align="center">
  <h3> Stock Backtesting Simulation - Databases Final Project</h3>
  <h4> Tom Matz </h4>
</div>

------------------


[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/download.html)


## Overview
The goal of this program is to backtest stocks with different asset allocation strategies. This was designed as a final project for my databases class (2023 Fall Semester.) The simulator allows you to add multiple customers to the database with different asset allocation strategies. Customers can run more than one strategy at a time. The simulation's start and end date can also be easily manipulated. After customizing the parameters, you are able to execute the simulation and view interesting reports from the backtest.


## Running Instructions
### Install Dependencies
Navigate to the project directory and run <code>pip install -r requirements.txt</code>. (Or pip3 if applicable)

### Run the Program
From the project directory, run <code>python main.py</code>. (Or python3 if applicable)

### Running Your First Simulation
1. Add a Customer to the Database
    - Select Option 2 in the main menu
    - Select Option 2 in the simulation parameters sub-menu
    - Follow Prompts 
2. Define Additional Strategies (Optional)
    - Select Option 3 from the simulation parameters sub-menu
    - Follow Prompts
3. Change Simulation Dates (Optional)
    - Selection Option 5 from the simulation parameters sub-menu
    - Follow Prompts
4. Return to Main Menu
5. Execute Simulation
    - Select Option 3 from the main menu
    - View reports from the simulation
    - Please note: in order to view customer specific reports, you must first have their UUID.
    - You can view customer's UUID's by selecting option 1 in the report menu.
