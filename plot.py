import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from datetime import datetime
from database import calculatePortfolioValue

def currency_format(x, pos):
    return "${:,.0f}".format(x)

def generatePortfolioPlot(uuid, dates):
    dates = [datetime.strptime(date, "%Y-%m-%d") for date in dates]

    cash_values = [calculatePortfolioValue(uuid, str(date)) for date in dates]

    fig, ax = plt.subplots()
    ax.plot(dates, cash_values, linestyle='-', color='g')
    ax.yaxis.set_major_formatter(FuncFormatter(currency_format))

    plt.title('Portfolio Value Over Time')
    plt.xlabel('Date')
    plt.ylabel('Cash Value')
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.show()