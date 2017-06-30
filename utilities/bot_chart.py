from poloniex import Poloniex

class BotChart(object):
	def __init__(self, exchange, pair, period):
		self.polo = Poloniex("GG7WHRPQ-J7HEGPKN-ITAJAEBQ-H73W8K9F",
                    "4e1714667f572cf8f743b00f7b1d33390dab70929cb979f80ec3122e8fb75c742"
                    "dfcc8b4e7bdada779505ad043905f710d3aed2ae0824558cb15da09fcbe4dee")
		self.pair = pair
		self.period = period
		self.start_time = 1491048000
		self.end_time = 1491591200

		# if start_time:
		# 	self.start_time = start_time
		# if end_time:
		# 	self.end_time = end_time

		self.data = self.polo.returnChartData(pair, period, self.start_time, self.end_time)

	def getPoints(self):
		return self.data