import os.path, sys, getopt

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), os.pardir))+'/utilities/')
from bot_chart import BotChart

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), os.pardir))+'/strategy/')
from bot_strategy import BotStrategy

def main(argv):
    chart = BotChart("poloniex", "BTC_XMR", 300)

    strategy = BotStrategy()

    for candlestick in chart.getPoints():
        strategy.tick(candlestick)

if __name__ == "__main__":
	main(sys.argv[1:])




