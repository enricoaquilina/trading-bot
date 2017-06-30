from bot_log import BotLog

class BotTrades(object):
	def __init__(self,currentPrice):
		self.output = BotLog()
		self.status = 'OPEN'
		self.entryPrice = currentPrice
		self.exitPrice = ""
		self.output.log('Trade opened')

	def close(self,currentPrice):
		self.status = 'CLOSED'
		self.exitPrice = currentPrice
		self.output.log('Trade closed')

	def showTradeDetails(self):
		tradeStatus = 'Entry Price: '+str(self.entryPrice)+'\tStatus: '+str(self.status)+'\tExit Price: '+str(self.exitPrice)
		
		if self.status == 'CLOSED':
			tradeStatus = tradeStatus + "\t Profit: "
			if self.exitPrice > self.entryPrice:
				tradeStatus = tradeStatus + '\033[92m'
			else:
				tradeStatus = tradeStatus + '\033[91m'

			tradeStatus = tradeStatus+str(self.exitPrice-self.entryPrice)+'\033[0m'
		
		self.output.log(tradeStatus)			
