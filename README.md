# Crypto-Trading-Bot-with-KrakenAPI
Real-time financial data is obtained through Kraken WebSocket connection whereas the Interactions (e.g. Buy, sell, etc) are done through Kraken REST connection.

### Indicator ###
The algorithm basically works by buying/selling after spotting and/or predicting a reversal sign when the price is falling/rising. The indicator of the algorithm can be decomposed into 3 components:  
1) Uptrend index, influenced by:  
__ a. Buy pressure index, influenced by:  
____ i. increasing relative strength index (Current RSI > previous RSI)  
____ ii. Candlestick pattern  
______ 1) 38.2%  
______ 2) Close above/below  
______ 3) Engulfing  
__ b. Uptrend score  
____ i. Detect the uptrend slope of the graph and contribute a score that is proportional to the magnitude of the slope

2) Downtrend index, influenced by:  
__ a. Sell pressure index, influenced by:  
____ i. Decreasing relative strength index (Current RSI < previous RSI)  
____ ii. Candlestick pattern  
______ 1) 38.2%  
______ 2) Close above/below  
______ 3) Engulfing  
__ b. Downtrend score  
____ i. Detect the downtrend slope of the graph and contribute a score that is proportional to the magnitude of the slope  

3) Reversal index, influenced by:  
__ a. Crossover  
____ i. When the current price moves in opposite direction of the simple moving average  
____ ii. When the difference between uptrend index and downtrend index is below a certain threshold  
__ b. RSI (above overbought threshold or below oversold threshold)

### For buying/selling:  ###
1) Switch on buy/sell signal when:  
__ a. Uptrend index, downtrend index as well as the difference between both indexes are within the specific ranges, respectively.  
__ b. Reversal index is high and within a specific range.  

2) When sell signal is up:  
__ a. Continues to hold when the price is still rising, only sell when:  
____ i. The price difference between the maximum price (over the last few ticks) and the current closing price is greater than the average true range  
____ ii. Selling price is greater than the bought price (guaranteed to have profit even after considering the estimated transaction fees)  
  Similar method is also used for making buy order

3) The method above aims at objectifying the appropriate moment to buy/sell. ALternative condition for buying/selling is also determiend to cover up for scenarios where the method above failed to identify the appropriate time to buy/sell



Had no prior knowledge on financial trading/algorithmic trading and have only watched a few youtube videos of trading tutorial. The project is carried out with the objectives of explore algorithmic trading and gain financial knowledge, **NOT** for generating profit. Cryptocurrency is chosen due to its low entry barrier. Technically, the bot yields a positive return after a day trading but not when the transaction fees charged are considered. Further measures were taken to try generating positive return considering the transaction fees charged  (e.g. not selling when yields a net negative return after deducting the transaction fees). Regardless, negligible profits are generated but this was a pretty interesting learning experience for me. The code is more of a collections of thoughts and notes instead of being presentable.

**NOTE:** config.py needs to be filled with Kraken API key and Secret key
