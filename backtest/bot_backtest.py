import os.path, sys, getopt

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), os.pardir))+'/utilities/')
from bot_chart import BotChart
from bot_arguments import BotArguments

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), os.pardir))+'/strategy/')
from bot_strategy import BotStrategy

def main(argv):
    args = BotArguments(argv)

    chart = BotChart(args.exchange, args.pair,
                    args.period, args.starttime,
                    args.endtime)

    strategy = BotStrategy()
    for candlestick in chart.getPoints():
        strategy.tick(candlestick)

    strategy.showProfit()
    strategy.showPrices()
    strategy.showEMAs()
    strategy.showSMAs()

if __name__ == "__main__":
    main(sys.argv[1:])




