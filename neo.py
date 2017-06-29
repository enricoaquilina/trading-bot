import time
import sys, getopt
import datetime
import datetime
from poloniex import Poloniex

def main(argv):
    period = 10
    pair = "BTC_ETH"
    prices = []
    lengthofma = 10
    starttime = False
    endtime = False
    historicaldata = False
    MA = 0
    localmax = []
    tradeplaced = False
    typeoftrade= False
    datapoints = []
    datadate = ""
    currentresistance = 0.018

    try:
        opts, args = getopt.getopt(argv, "hp:c:m:s:e:", ["period=", "currency=", "ma="])
    except getopt.GetoptError:
        print("neo.py -p <period> -c <currency pair> -m <moving average period> -s <start time> -e <end time>")
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            print("nep.py -p <period> -c <currency pair> -m <moving average period> -s <start time> -e <end time>")
            sys.exit()
        elif opt in ("-p", "--period"):
            if int(arg) in [300, 900, 1800, 7200, 14400, 86400]:
                period = arg
            else:
                print("Poloniex requires period values among (300, 900, 1800, 7200, 14400, 86400) second increments")
                sys.exit(2)
        elif opt in ("-c", "--currency"):
            pair = arg
        elif opt in ("-m", "--ma"):
            lengthofma = int(arg)
        elif opt in "-s":
            starttime = arg
        elif opt in "-e":
            endtime = arg

    polo = Poloniex("GG7WHRPQ-J7HEGPKN-ITAJAEBQ-H73W8K9F",
                    "4e1714667f572cf8f743b00f7b1d33390dab70929cb979f80ec3122e8fb75c742"
                    "dfcc8b4e7bdada779505ad043905f710d3aed2ae0824558cb15da09fcbe4dee")

    output = open('output.html', 'w')
    output.truncate()
    output.write(
        """<html><head><script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script><script type="text/javascript">google.charts.load('current', {'packages':['corechart']});google.charts.setOnLoadCallback(drawChart);function drawChart() {var data = new google.visualization.DataTable();data.addColumn('string', 'time');data.addColumn('number', 'value');data.addColumn({type: 'string', role:'annotation'});data.addColumn({type: 'string', role:'annotationText'});data.addColumn('number', 'trend');data.addRows([""")

    if starttime:
        historicaldata = polo.returnChartData(pair, period, starttime, endtime)

    while True:
        # check if we want to process historic
        if starttime and historicaldata:
            currentpoint = historicaldata.pop(0)
            lastpairprice = currentpoint['weightedAverage']
            datadate = datetime.datetime.fromtimestamp(int(currentpoint['date'])).strftime('%Y-%m-%d %H:%M:%S')
        elif starttime and not historicaldata:
            for point in datapoints:
                output.write("['" + point['date'] + "'," + point['price'] + "," + point['label']
                             + "," + point['desc'] + "," + point['trend'])
                output.write("],\n")
            output.write(
                """]);var options = {title: 'Price Chart',legend: { position: 'bottom' }};
                var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));
                chart.draw(data, options);}</script></head><body><div id="curve_chart" 
                style="width: 100%; height: 100%"></div></body></html>""")
            exit()
        else:
            currentvalues = polo.returnTicker()[pair]
            lastpairprice = str(currentvalues["last"])
            datadate = datetime.datetime.now()

        datapoints.append({'date': datadate, 'price': str(lastpairprice),
                           'trend': str(currentresistance), 'label': 'null', 'desc': 'null'})

        if len(datapoints) > 2 and \
                (datapoints[-2]['price'] > datapoints[-1]['price']) and (datapoints[-2]['price'] > datapoints[-3]['price']):

            datapoints[-2]['label'] = "'MAX'"
            datapoints[-2]['desc'] = "'This is a local maximum'"

            numberofsimilarlocalmaxes = 0
            for oldmax in localmax:
                if float(oldmax) > float(datapoints[-2]['price']) - 0.0001 and \
                   float(oldmax) < float(datapoints[-2]['price']) + 0.0001:
                    numberofsimilarlocalmaxes = numberofsimilarlocalmaxes + 1

            if numberofsimilarlocalmaxes > 2:
                currentresistance = datapoints[-2]['price']
                datapoints[-2]['trend'] = datapoints[-2]['price']
                datapoints[-1]['trend'] = datapoints[-2]['price']
            localmax.append(datapoints[-2]['price'])


        # Place buy/sell order
        if len(prices) > 0:
            MA = sum(prices) / float(len(prices))
            lastprice = prices[-1]
            if not tradeplaced:
                if (lastpairprice > MA) and (lastpairprice < lastprice):
                    print('Sell order')
                    tradeplaced = True
                    typeoftrade = "short"
                elif (lastpairprice < MA) and (lastpairprice > lastprice):
                    print('Buy order')
                    tradeplaced = True
                    typeoftrade = "long"
            elif typeoftrade == 'short':
                if lastpairprice < MA:
                    print("Exit trade")
                    tradeplaced = False
                    typeoftrade = False
            elif typeoftrade == 'long':
                if lastpairprice > MA:
                    print("Exit trade")
                    tradeplaced = False
                    typeoftrade = False
        else:
            lastprice = 0

        prices.append(float(lastpairprice))
        prices = prices[-lengthofma:]

        print("{:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now()) +
            " \t Period: %ss \t %s: %s \t Moving average: %s" % (period, pair, lastpairprice, MA))

        if not starttime:
            time.sleep(int(period))

if __name__ == "__main__":
    main(sys.argv[1:])
