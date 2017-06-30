import os, sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), os.pardir))+'/strategy/')
from bot_indicators import BotIndicators
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), os.pardir))+'/utilities/')
from bot_log import BotLog
from bot_trades import BotTrades

class BotStrategy(object):
	def __init__(self):
		self.output = BotLog()
		self.prices = []
		self.trades = []
		self.currentPrice = ""
		self.numberOfTrades = 1

		self.indicators = BotIndicators()

	# for every point from API, tick is called
	def tick(self, candlestick):
		self.currentPrice = float(candlestick['weightedAverage'])
		self.prices.append(self.currentPrice)		

		self.output.log('Price: '+str(candlestick['weightedAverage'])+'\tMoving Average: '+str(self.indicators.movingAverage(self.prices,15)))
		
		self.evaluatePositions()	
		self.showPositions()

	def evaluatePositions(self):
		openTrades = []
		for trade in self.trades:
			if trade.status == 'OPEN':
				openTrades.append(trade)

		if len(openTrades) < self.numberOfTrades:
			if self.currentPrice < self.indicators.movingAverage(self.prices,15):
				self.trades.append(BotTrades(self.currentPrice))

		for trade in openTrades:
			if self.currentPrice > self.indicators.movingAverage(self.prices,15):
				trade.close(self.currentPrice)				
	
	def showPositions(self):
		for trade in self.trades:
			trade.showTradeDetails()


