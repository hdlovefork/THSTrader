class PositionStocks:
    def __init__(self, stocks=None):
        if stocks is None:
            stocks = []
        self.stocks = stocks

    def append(self, *stock):
        self.stocks.append(*stock)

    def remove(self, *stock):
        self.stocks.remove(*stock)

    def to_quot_list(self):
        return list((stock.market_code,stock.stock_code) for stock in self.stocks)
