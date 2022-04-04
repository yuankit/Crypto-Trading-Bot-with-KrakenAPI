########## For REST API ###########
import time
from matplotlib.pyplot import close
import numpy as np
import urllib
import hashlib
import base64
import hmac
import requests
import numpy
########## For REST API ###########

########## For Trading Strategy ##########
from scipy.signal import argrelextrema
import talib
########## For Trading Strategy ##########

########## From Other Scripts ##########
import config
import api_enum
import candlestick_id
import algo_func
########## From Other Scripts ##########


########## For WebSocket ###########
import websocket
import json
import datetime
########## For WebSocket ###########


########## For REST API ###########
# Define the constants, which are the API URL, API key and API secret key
API_URL = "https://api.kraken.com"
API_KEY = config.API_KEY
API_SECRET_KEY = config.PRIVATE_KEY
TRADE_PAIR = "ETHUSD"
########## For REST API ###########


########## For WebSocket ###########
SOCKET = 'wss://ws.kraken.com'
########## For WebSocket ###########

########## CONSTANTS ##########
# For receiving pricing data
close_price_list = []
open_price_list = []
high_price_list = []
low_price_list = []
temp_open_price = 1.0
temp_high_price = 1.0
temp_low_price = 1.0
temp_close_price = 1.0
# For candlestick data
candle_382_list = [np.nan]
candle_engulfing_list = [np.nan]
candle_close_ab_list = [np.nan]
num_candlestick = -1
CANDLE_382_IMP = 0.80
CANDLE_ENGULFING_IMP = 0.80
CANDLE_CLOSE_AB_IMP = 0.80
CANDLE_PERIOD_FOR_TREND = 10 # To adjust how many of the past candlesticks are relevant
candle_endtime_old = 'reference_endtime' # Set a random number just to allow the candle endtime checking logic
# For RSI
RSI_PERIOD = 14
RSI_PERIOD_FOR_TREND = 6
RSI_OVERBOUGHT = 75
RSI_OVERSOLD = 25
# For determining price trend
TREND_PERIOD = 40 # This should be relating to ATR or some sort instead of a constant
price_trend = [np.nan for i in range(TREND_PERIOD)]
global_support_resistance = 1.0
SMA_PERIOD = 10 # To adjust how many of the past closing price are relevant in calculating the MA
PULLBACK_NUM = 8 # This identifies the number of pullback in a single trend
# For Uptrend/Downtrend Index
BUY_PRESSURE_INDEX_LIST = [np.nan for i in range(np.maximum((RSI_PERIOD_FOR_TREND+RSI_PERIOD), TREND_PERIOD))] # Based on candlestick pattern, RSI and trend
SELL_PRESSURE_INDEX_LIST = [np.nan for i in range(np.maximum((RSI_PERIOD_FOR_TREND+RSI_PERIOD), TREND_PERIOD))] # Based on candlestick pattern, RSI and trend
REVERSAL_INDEX_LIST = [np.nan for i in range(np.maximum((RSI_PERIOD_FOR_TREND+RSI_PERIOD), TREND_PERIOD))] # Based on BUY/SELL pressure index, support/resistance and crossover of real price & MA
UPTREND_INDEX_LIST = [np.nan for i in range(np.maximum((RSI_PERIOD_FOR_TREND+RSI_PERIOD), TREND_PERIOD))]
DOWNTREND_INDEX_LIST = [np.nan for i in range(np.maximum((RSI_PERIOD_FOR_TREND+RSI_PERIOD), TREND_PERIOD))]
TREND_SCORE_THRESHOLD = 0.70
UPTREND_PERIOD = 6
DOWNTREND_PERIOD = 6
spt_rst_time_id = 0
# For Reversal Index
ABOVE_SMA = True # Initialsie the variable with a random boolean, this does not matter if it's True or False
REVERSAL_PERIOD = 6
# For Buy/Sell Processes
BUY_SIGNAL = False
SELL_SIGNAL = False
MIN_PRICE = 50000.0
MAX_PRICE = 1.0
SOLD = 0.0
BOUGHT = 0.0
IN_POSITION = False
IN_POSITION_2 = True
BUY_LOWER_THRESHOLD = 0.00
BUY_LOWER_MIDDLE_THRESHOLD = 3.50
BUY_UPPER_MIDDLE_THRESHOLD = 9.0
BUY_UPPER_THRESHOLD = 20.00
SELL_LOWER_THRESHOLD = 0.00
SELL_LOWER_MIDDLE_THRESHOLD = 3.80
SELL_UPPER_MIDDLE_THRESHOLD = 9.0
SELL_UPPER_THRESHOLD = 20.0
SELL_SEC_UP_THRESHOLD = 11.0
SELL_SEC_DOWN_THRESHOLD = 4.0
SELL_SEC_REVERSAL_THRESHOLD = 0.5
LOWER_DOWN_UP_DIFF = 3.50
UPPER_DOWN_UP_DIFF = 20.00
LOWER_UP_DOWN_DIFF = 3.50
UPPER_UP_DOWN_DIFF = 20.00
BUY_REVERSAL_UPPER_THRESHOLD = 2.40
BUY_REVERSAL_LOWER_THRESHOLD = 0.50
SELL_REVERSAL_UPPER_THRESHOLD = 2.00
SELL_REVERSAL_LOWER_THRESHOLD = 0.50
QUANTITY = 0.004
BOUGHT_HIST = []
BOUGHT_TIME = []
SECOND_BOUGHT_TIME = []
SOLD_HIST = []
SOLD_TIME = []
SECOND_SOLD_TIME = []
FINAL_UPTREND_INDEX_LIST = []
FINAL_DOWNTREND_INDEX_LIST = []
FINAL_REVERSAL_INDEX_LIST = []
BUY_SIGNAL_TIME = []
SELL_SIGNAL_TIME = []
KRAKEN_FEES = 0.290 / 100 # 0.579% of the sold quantity, 0.289% for each transaction (buy & sell)
STOP_LOSS_THRESHOLD = 30.0
BOUGHT_PER_UNIT = 0.0
BOUGHT_PER_UNIT_LIST = []
SOLD_PER_UNIT = 0.0
SOLD_PER_UNIT_LIST = []
ORDER_TIMES = 1
########## CONSTANTS ##########


########## For WebSocket ###########
def on_open(ws):
    print("Opened Connection")
    # Send the data as string, NOTE: All msg sent and received via WebSockets are encoded in JSON format
    # json.dumps serialise object to a JSON formatted string
    ws.send(json.dumps(payload))

def on_close(ws):
    print("Closed Connection")

def on_message(ws, message):
    global candle_endtime_old
    global IN_POSITION
    global temp_open_price
    global temp_high_price
    global temp_low_price
    global temp_close_price
    global num_candlestick
    global global_support_resistance
    global buy_pressure_index
    global sell_pressure_index
    global reversal_index
    global uptrend_index
    global downtrend_index
    global ABOVE_SMA
    global BOUGHT_PRICE
    global BUY_SIGNAL
    global SELL_SIGNAL
    global MIN_PRICE
    global MAX_PRICE
    global SOLD
    global SOLD_PER_UNIT
    global SOLD_PER_UNIT_LIST
    global BOUGHT
    global BOUGHT_PER_UNIT
    global BOUGHT_PER_UNIT_LIST
    global spt_rst_time_id

    buy_pressure_index = 0
    sell_pressure_index = 0
    reversal_index = 0
    uptrend_index = 0
    downtrend_index = 0

    # Deserialise the received data (in JSON format) to Python object
    loaded_msg = json.loads(message)

    # Note that the processed message sent to us will be in the type of list and dictionary
    # list for the message from the subscribed stream, dictionary for heartbeat (when there's no subscription traffic within 1 sec)
    if type(loaded_msg) == list:
        #print("Received Message")
        #print(loaded_msg)

        # Check if the newly received message is an update of the same candle or an entire new candle of different timestamp
        # Append to the list whenever there is a new candlestick
        candle_endtime_now = loaded_msg[1][1] # output: str, candlestick endtime

        if candle_endtime_now != candle_endtime_old:
            # This is to isolate the very first message received where the prices could be still updating or already updated
            if num_candlestick == -1:
                candle_endtime_old = candle_endtime_now
                num_candlestick += 1
                print("Received the very first price but not sure if they are the finalised price or will still be updated")
            else:
                # Append the previously stored (finalised) prices into the list
                open_price_list.append(temp_open_price) # For opening price, remain the same throughout the timeframe
                high_price_list.append(temp_high_price) # For highest price of the candlestick
                low_price_list.append(temp_low_price) # For lowest price of the candlestick
                close_price_list.append(temp_close_price) # For closing price
                candle_endtime_old = candle_endtime_now
                num_candlestick += 1
                timenow = datetime.datetime.now()
                print(timenow.strftime("Day: %Y-%m-%d Time: %H%M%S"))
                #print("Different candlestick endtime, meaning the previous prices are finalised, appended the finalised price into the list")
                #print("Candlestick Opening Price: {}".format(open_price_list))
                #print("Candlestick High Price: {}".format(high_price_list))
                #print("Candlestick Low Price: {}".format(low_price_list))
                #print("Candlestick Closing Price: {}".format(close_price_list))
                print("Number of Candlestick: {}".format(len(close_price_list)))

            # Store a temporary variable of the price, only append to the list once the price is finalised
            temp_open_price = float(loaded_msg[1][2])
            temp_high_price = float(loaded_msg[1][3])
            temp_low_price = float(loaded_msg[1][4])
            temp_close_price = float(loaded_msg[1][5])

            # Detect the pattern of 38.2%, Engulfing and Close above/below candle
            # Will ignore the updating candlestick, only deal with the finalised one
            if len(close_price_list) > 1:
                is_candle_382 = candlestick_id.candle_382(open_price_list=open_price_list, high_price_list=high_price_list,
                                                          low_price_list=low_price_list, close_price_list=close_price_list)
                candle_382_list.append(is_candle_382)
                #print("Candle 38.2% Pattern: {}".format(candle_382_list))

                is_candle_engulfing = candlestick_id.candle_engulf(open_price_list=open_price_list,
                                                                   close_price_list=close_price_list)
                candle_engulfing_list.append(is_candle_engulfing)  
                #print("Engulfing Candle Pattern: {}".format(candle_engulfing_list))     

                is_candle_close = candlestick_id.candle_close_above_below(high_price_list=high_price_list,
                                                                          low_price_list=low_price_list,
                                                                          close_price_list=close_price_list)
                candle_close_ab_list.append(is_candle_close)
                #print("Close Above/Below Candle Pattern: {}".format(candle_close_ab_list)) 

                if len(close_price_list) > CANDLE_PERIOD_FOR_TREND:
                    # Starts calculating for the number of times a certain candle pattern appears in the market
                    # Output: (0.8, 0.4) --> 0.8 frequency of certain candlestick indicating the existence of buy pressure
                    # 0.4 frequency of certain candlestick indicating the existence of sell pressure
                    candle_382_score = np.array(algo_func.find_num_bool(list=candle_382_list, 
                                                                            timeperiod=CANDLE_PERIOD_FOR_TREND)) * CANDLE_382_IMP
                    print("Candle 38.2% Score: {}".format(candle_382_score))
                    candle_engulfing_score = np.array(algo_func.find_num_bool(list=candle_engulfing_list, 
                                                                                timeperiod=CANDLE_PERIOD_FOR_TREND)) * CANDLE_ENGULFING_IMP
                    print("Engulfing Candle Score: {}".format(candle_engulfing_score))
                    candle_close_ab_score = np.array(algo_func.find_num_bool(list=candle_close_ab_list, 
                                                                                timeperiod=CANDLE_PERIOD_FOR_TREND)) * CANDLE_CLOSE_AB_IMP
                    print("Close Above/Below Candle Score: {}".format(candle_close_ab_score))

                    # Sum up all the buy pressure and sell pressure score from the different type of candle
                    buy_sell_array = np.round(np.sum([candle_382_score, candle_engulfing_score, candle_close_ab_score], axis=0), 2)
                    print("candlestick Buy/Sell Score: {}".format(buy_sell_array))
                    buy_pressure_index += buy_sell_array[0]
                    sell_pressure_index += buy_sell_array[1]

            # Detect whether the market is on an uptrend or downtrend
            if len(close_price_list) > TREND_PERIOD:
                uptrend_perc = trend_id(high_price_list=high_price_list, low_price_list=low_price_list, 
                                        close_price_list=close_price_list, timeperiod=TREND_PERIOD, number=PULLBACK_NUM)
                price_trend.append(uptrend_perc[:2])
                #print("Trends recorded so far: {}".format(price_trend))

                # Define the support or resistance
                is_support, support_resistance_value = uptrend_perc[-1]
                spt_rst_time_id = len(close_price_list)
                print("Support Detected at nth candlestick: {}".format(spt_rst_time_id))
                print("Support: {}".format(is_support))
                print("Support/Resistance Value: {}".format(support_resistance_value[0]))
                
                # Context manager to avoid the current price be identified as a resistance/support
                # if (len(close_price_list) - spt_rst_time_id) > 15:
                #     global_support_resistance =

                # if is_support == True:


                # NOTE: uptrend_perc[0] is boolean whether it is uptrend
                # NOTE: uptrend_perc[1] is the confidence score on the current trend
                # On version 4, remove the TREND_SCORE_THRESHOLDD, straight away use the uptrend_perc[1] as the score of down/up trend index
                if (uptrend_perc[0] == True):
                    uptrend_index += uptrend_perc[1]
                    print("Uptrend Score: +{}".format(uptrend_perc[1]))
                elif (uptrend_perc[0] == False):
                    downtrend_index += uptrend_perc[1]
                    print("Downtrend Score: +{}".format(uptrend_perc[1]))

                # Calculate Moving Average 20
                high_price_list_array = np.array(high_price_list).astype(np.float64)
                low_price_list_array = np.array(low_price_list).astype(np.float64)
                close_price_list_array = np.array(close_price_list).astype(np.float64)

                sma = talib.SMA(close_price_list_array, timeperiod=SMA_PERIOD)
                #print("SMA: {}".format(sma))
                if len(REVERSAL_INDEX_LIST) == np.maximum((RSI_PERIOD_FOR_TREND + RSI_PERIOD), TREND_PERIOD):
                    if sma[-1] > close_price_list[-1]:
                        ABOVE_SMA = True
                        print("Current Price is below SMA")
                    else:
                        ABOVE_SMA = False
                        print("Current Price is above SMA")
                else:
                    if sma[-1] > close_price_list[-1]:
                        NEW_ABOVE_SMA = True
                        print("Current price is below the latest SMA")
                    else:
                        NEW_ABOVE_SMA = False
                        print("Current price is above the latest SMA")
                    # There's a sign of reversal if there's a intersection between the MA and the closing price
                    if NEW_ABOVE_SMA != ABOVE_SMA:
                        reversal_index += 0.50
                        print("Intersection of MA and closing price so Reversal Index: +0.50")
                        ABOVE_SMA = NEW_ABOVE_SMA
                        print("There's a reversal of trend")
                        print("Current trend above SMA: {}".format(NEW_ABOVE_SMA))
                    else:
                        print("There's no reversal of trend")
                        print("Current trend above SMA: {}".format(NEW_ABOVE_SMA))

                # Calculate the Average True Range
                atr = talib.ATR(high=high_price_list_array, low=low_price_list_array, close=close_price_list_array, timeperiod=14)
                print("ATR calculated so far: {}".format(atr))
                print("Current ATR: {}".format(atr[-1]))

            # When there's at least <RSI_PERIOD> number of closing price data, we starts calculating the RSI for it
            if len(close_price_list) > (RSI_PERIOD + RSI_PERIOD_FOR_TREND):
                np_close_price = np.array(close_price_list).astype(np.float64) # Convert to numpy as required by talib library
                rsi = talib.RSI(np_close_price, RSI_PERIOD)
                #print("RSI calculated so far: {}".format(rsi))
                print("Current RSI: {}".format(rsi[-1]))

                # Add points to the buy/sell pressure index when current RSI is greater/lower than the previous few RSI
                if rsi[-1] > rsi[-RSI_PERIOD_FOR_TREND]:
                    buy_pressure_index += 0.1
                    print("Current RSI is greater than previous RSI so Buy Pressure Index: +0.10")
                else:
                    sell_pressure_index += 0.1
                    print("Current RSI is smaller than previous RSI so Sell Pressure Index: +0.10")

                # Possbility of having reversal increases when there's oversold or overbought situation
                if (rsi[-1] > RSI_OVERBOUGHT) or (rsi[-1] < RSI_OVERSOLD):
                    reversal_index += 0.2
                    print("Overbought/Oversold so Reversal Index: +0.2")

                
                
            ########## Combine all the indicators and strategy used here ###########
            if len(close_price_list) > np.maximum((RSI_PERIOD_FOR_TREND+RSI_PERIOD), TREND_PERIOD):
                print("Uptrend Index = Buy Pressure Index (RSI + Candle Pattern) + Uptrend Score")
                print("Downtrend Index = Sell Pressure Index (RSI + Candle Pattern) + Downtrend Score")
                BUY_PRESSURE_INDEX_LIST.append(buy_pressure_index)
                SELL_PRESSURE_INDEX_LIST.append(sell_pressure_index)
                #print("All Buy Pressure Index: {}".format(BUY_PRESSURE_INDEX_LIST))
                #print("All Sell Pressure Index: {}".format(SELL_PRESSURE_INDEX_LIST))
                # Uptrend index consists of the buy pressure index and the uptrend score itself
                uptrend_index += buy_pressure_index
                downtrend_index += sell_pressure_index
                UPTREND_INDEX_LIST.append(uptrend_index)
                DOWNTREND_INDEX_LIST.append(downtrend_index)

                # Add score to the reversal index when the difference between uptrend index and downtrend index are small
                if abs(UPTREND_INDEX_LIST[-1] - DOWNTREND_INDEX_LIST[-1]) <= 0.4:
                    reversal_index += 0.40
                    print("Small diff between uptrend and downtrend index, reversal index: +0.40")


                #print("All Uptrend Index: {}".format(UPTREND_INDEX_LIST))
                #print("All Downtrend Index: {}".format(DOWNTREND_INDEX_LIST))
                REVERSAL_INDEX_LIST.append(reversal_index)
                #print("All Reversal Index: {}".format(REVERSAL_INDEX_LIST))

                # Take the sum of the past e.g. 6 candlesticks reversal index as the final index, this could be greater than one
                final_reversal_index = np.sum(np.array(REVERSAL_INDEX_LIST[-REVERSAL_PERIOD:]))
                print("Final Reversal Index for the last {} candlestick: {}".format(REVERSAL_PERIOD, final_reversal_index))
                # The same for uptrend index and downtrend index
                final_uptrend_index = np.sum(np.array(UPTREND_INDEX_LIST[-UPTREND_PERIOD:]))
                final_downtrend_index = np.sum(np.array(DOWNTREND_INDEX_LIST[-DOWNTREND_PERIOD:]))

                print("Final uptrend index for the last {} candlestick: {}".format(UPTREND_PERIOD, final_uptrend_index))
                print("Final downtrend index for the last {} candlestick: {}".format(DOWNTREND_PERIOD, final_downtrend_index))

                if IN_POSITION == True:
                    print("In position...")
                    
                    # Stop loss backup plan
                    if ((BOUGHT_PER_UNIT - close_price_list[-1]) > STOP_LOSS_THRESHOLD):
                        print("The price keeps falling..sell now to stop losses")
                        SOLD_PER_UNIT = close_price_list[-1]
                        SOLD_PER_UNIT_LIST.append(SOLD_PER_UNIT)
                        SOLD = QUANTITY * close_price_list[-1]
                        for i in range(ORDER_TIMES):
                            # resp_sold = kraken_request(url_path=api_enum.USER_TRADING['ADD_ORDER'], 
                            #                             data={
                            #                             "nonce": nonce_generator(),
                            #                             "ordertype": "market",
                            #                             "type": "sell",
                            #                             "volume": QUANTITY,
                            #                             "pair": TRADE_PAIR,
                            #                             }, 
                            #                             api_key=API_KEY,
                            #                             api_sec=API_SECRET_KEY)
                            # resp_sold = resp_sold.json()
                            resp_sold = {'error': []}

                            # Check if the response returns any error
                            if resp_sold['error'] == []:
                                print("ORDER SUCCEED")
                                #print("Response: {}".format(resp_sold['result']))
                                print("Sold {} USD at {} per ETH".format(SOLD, close_price_list[-1]))
                                print("Sold {} USD at {} per ETH".format(SOLD, SOLD_PER_UNIT))
                                IN_POSITION = False
                                SELL_SIGNAL = False
                                SOLD_HIST.append(SOLD)
                                SOLD_TIME.append((timenow.strftime("%Y%m%d_%H%M%S"), "SL"))
                            else:
                                print("ORDER FAILED")
                                print("Error: {}".format(resp_sold['error']))

                    else:
                        print("The current price is still above the stop-loss price..Proceed as usual")

                        if SELL_SIGNAL == False:
                            # Sell when uptrend/downtrend index indicating an uptrend and the reversal index is high
                            if (final_uptrend_index >= SELL_UPPER_MIDDLE_THRESHOLD) and (final_uptrend_index <= SELL_UPPER_THRESHOLD) and (final_downtrend_index >= SELL_LOWER_THRESHOLD) and (final_downtrend_index <= SELL_LOWER_MIDDLE_THRESHOLD) and ((final_uptrend_index - final_downtrend_index) >= LOWER_UP_DOWN_DIFF) and ((final_uptrend_index - final_downtrend_index) <= UPPER_UP_DOWN_DIFF):
                                print("FUI, {} in between {} and {} ----- FDI, {} in between {} and {}".format(final_uptrend_index, SELL_UPPER_MIDDLE_THRESHOLD, SELL_UPPER_THRESHOLD,
                                                                                                            final_downtrend_index, SELL_LOWER_THRESHOLD, SELL_LOWER_MIDDLE_THRESHOLD))
                                print("Final uptrend index - Final downtrend index, {} in between {} and {}".format((final_uptrend_index-final_downtrend_index), LOWER_UP_DOWN_DIFF, UPPER_UP_DOWN_DIFF))
                                if (final_reversal_index >= SELL_REVERSAL_LOWER_THRESHOLD) and (final_reversal_index <= SELL_REVERSAL_UPPER_THRESHOLD):
                                    print("Final Reversal Index, {} in between {} and {}".format(final_reversal_index, SELL_REVERSAL_LOWER_THRESHOLD, SELL_REVERSAL_UPPER_THRESHOLD))
                                    print("Sell signal is switched on now")
                                    SELL_SIGNAL = True
                                    SELL_SIGNAL_TIME.append(timenow.strftime("%Y%m%d_%H%M%S"))
                                    MAX_PRICE = close_price_list[-1]

                                else:
                                    print("Final Reversal Index, {} NOT in between {} and {}".format(final_reversal_index, SELL_REVERSAL_LOWER_THRESHOLD, SELL_REVERSAL_UPPER_THRESHOLD))
                                    print("Reversal Condition not met...")
                            else:
                                print("Final uptrend index and/or Final downtrend index not met requirement")
                                print("Check on second set of selling conditions...FUI >= 11.0, FDI <= 4.0, FRI >= 0.5")
                            
                                if (final_uptrend_index >= SELL_SEC_UP_THRESHOLD) and (final_downtrend_index <= SELL_SEC_DOWN_THRESHOLD) and (final_reversal_index >= SELL_SEC_REVERSAL_THRESHOLD):
                                    print("Second set of selling conditions are satisfied")
                                    print("Final uptrend index, {} > {} ----- Final downtrend index, {} < {} ----- Final reversal index, {} > {}".format(final_uptrend_index, SELL_SEC_UP_THRESHOLD, final_downtrend_index, SELL_SEC_DOWN_THRESHOLD, final_reversal_index, SELL_SEC_REVERSAL_THRESHOLD))
                                    print("Sell since we already in position and it is a good time to sell")
                                    print("Condition satisfied:")

                                    SOLD = QUANTITY * close_price_list[-1]

                                    if (SOLD - BOUGHT) > 0.0:
                                        print("Selling price is greater than the bought price...can proceed")
                                        print("Must have at least {} USD of return to have net profit".format((SOLD*KRAKEN_FEES) + (BOUGHT*KRAKEN_FEES)))
                                        print("Current Return: {}".format((SOLD - BOUGHT)))

                                        if (SOLD - BOUGHT) > ((SOLD * KRAKEN_FEES) + (BOUGHT * KRAKEN_FEES)):
                                            print("Selling price yields profit even after deducting the trading fees")

                                            print("Making Sell Order")
                                            for i in range(ORDER_TIMES):
                                                # resp_sold = kraken_request(url_path=api_enum.USER_TRADING['ADD_ORDER'], 
                                                #                         data={
                                                #                         "nonce": nonce_generator(),
                                                #                         "ordertype": "market",
                                                #                         "type": "sell",
                                                #                         "volume": QUANTITY,
                                                #                         "pair": TRADE_PAIR,
                                                #                         }, 
                                                #                         api_key=API_KEY,
                                                #                         api_sec=API_SECRET_KEY)
                                                # resp_sold = resp_sold.json()
                                                resp_sold = {'error': []}
                                                # Check if the response returns any error
                                                if resp_sold['error'] == []:
                                                    print("ORDER SUCCEED")
                                                    #print("Response: {}".format(resp_sold['result']))
                                                    print("Sold {} USD at {} per ETH".format(SOLD, close_price_list[-1]))
                                                    SOLD_HIST.append(SOLD)
                                                    SOLD_PER_UNIT = close_price_list[-1]
                                                    SOLD_PER_UNIT_LIST.append(SOLD_PER_UNIT)
                                                    SOLD_TIME.append(timenow.strftime("%Y%m%d_%H%M%S"))
                                                    SECOND_SOLD_TIME.append(timenow.strftime("%Y%m%d_%H%M%S"))
                                                    IN_POSITION = False
                                                    FINAL_UPTREND_INDEX_LIST.append(final_uptrend_index)
                                                    FINAL_DOWNTREND_INDEX_LIST.append(final_downtrend_index)
                                                    FINAL_REVERSAL_INDEX_LIST.append(final_reversal_index)
                                                else:
                                                    print("ORDER FAILED")
                                                    print("Error: {}".format(resp_sold['error']))

                                        else:
                                            print("Selling price does not yield profit after deducting trading fees..Will not sell now")

                                    else:
                                        print("Won't sell yet as the current price is lower than bought price although condition satisfied")
                                    
                                else:
                                    print("Second set of selling condition not met...Will not sell...")

                        elif SELL_SIGNAL == True:
                            print("Sell signal is up..Will sell once the prices starts falling")

                            MAX_PRICE = close_price_list[-1] if close_price_list[-1] > MAX_PRICE else MAX_PRICE
                            print("Maximum price: {}".format(MAX_PRICE))
                            print("Current price: {}".format(close_price_list[-1]))
                            print("Last atr: {}".format(atr[-1]))
                            print("Price difference: {}".format(MAX_PRICE - close_price_list[-1]))

                            if ((MAX_PRICE - close_price_list[-1]) < atr[-1]):
                                print("Hold first since the price is still rising")
                                print("Price diff is smaller than atr")
                            else:
                                print("Price diff is greater than atr")
                                print("Prices are decreasing significantly..Sell now")
                                # Only sell when we have profit
                                #BOUGHT_PRICE = close_price_list[-1]
                                print("Sell since we already in position and it is a good time to sell")
                                print("Condition satisfied:")

                                SOLD = QUANTITY * close_price_list[-1]
                                
                                if (SOLD - BOUGHT) > 0.0:
                                    print("Selling price is greater than the bought price...can proceed")
                                    print("Must have at least {} USD of return to have net profit".format((SOLD*KRAKEN_FEES) + (BOUGHT*KRAKEN_FEES)))
                                    print("Current Return (USD): {}".format((SOLD - BOUGHT)))

                                    # Sell when there's profit even after deducting the kraken transaction fees
                                    if (SOLD - BOUGHT) > ((SOLD * KRAKEN_FEES) + (BOUGHT * KRAKEN_FEES)):
                                        print("Selling price yields profit even after deducting the trading fees")
                                        print("Bought Price: {}".format(BOUGHT))
                                        print("Current price is greater than the bought price..Can sell")

                                        print("Making Sell Order")
                                        for i in range(ORDER_TIMES):
                                            print("Order {}:".format(i))
                                            # resp_sold = kraken_request(url_path=api_enum.USER_TRADING['ADD_ORDER'], 
                                            #                         data={
                                            #                         "nonce": nonce_generator(),
                                            #                         "ordertype": "market",
                                            #                         "type": "sell",
                                            #                         "volume": QUANTITY,
                                            #                         "pair": TRADE_PAIR,
                                            #                         }, 
                                            #                         api_key=API_KEY,
                                            #                         api_sec=API_SECRET_KEY)
                                            # resp_sold = resp_sold.json()
                                            resp_sold = {'error': []}
                                            # Check if the response returns any error
                                            if resp_sold['error'] == []:
                                                print("ORDER SUCCEED")
                                                #print("Response: {}".format(resp_sold['result']))
                                                SOLD_PER_UNIT = close_price_list[-1]
                                                SOLD_PER_UNIT_LIST.append(SOLD_PER_UNIT)
                                                print("Sold {} USD at {} per ETH".format(SOLD, SOLD_PER_UNIT))
                                                SOLD_HIST.append(SOLD)
                                                SOLD_TIME.append(timenow.strftime("%Y%m%d_%H%M%S"))
                                                IN_POSITION = False
                                                FINAL_UPTREND_INDEX_LIST.append(final_uptrend_index)
                                                FINAL_DOWNTREND_INDEX_LIST.append(final_downtrend_index)
                                                FINAL_REVERSAL_INDEX_LIST.append(final_reversal_index)
                                                SELL_SIGNAL = False

                                            else:
                                                print("ORDER FAILED")
                                                print("Error: {}".format(resp_sold['error']))

                                    else:
                                        print("Selling price does not yield profit after deducting trading fees")
                                        print("Will not sell for now...")
                                else:
                                    print("Won't sell yet as the current price is lower than bought price although condition satisfied")
                                    print("Will monitor the price, if drops below the stop-loss price, will sell immediately")
                                


                elif IN_POSITION == False:
                    print("Not in position...")

                    if BUY_SIGNAL == False:
                        # Check if the average true range is above average true range upper threshold, if yes then don't buy first
                        if (atr[-1] > 4.00):
                            print("ATR is above 4.00, dont buy yet")
                        else:
                            print("ATR is not greater than 4.00 or FDI < FUI, will buy if condition satisfied")
                            if (final_downtrend_index >= BUY_UPPER_MIDDLE_THRESHOLD) and (final_downtrend_index <= BUY_UPPER_THRESHOLD) and (final_uptrend_index >= BUY_LOWER_THRESHOLD) and (final_uptrend_index <= BUY_LOWER_MIDDLE_THRESHOLD) and ((final_downtrend_index - final_uptrend_index) >= LOWER_DOWN_UP_DIFF) and ((final_downtrend_index - final_uptrend_index) <= UPPER_DOWN_UP_DIFF):
                                print("FDI, {} in between {} and {} ----- FUI, {} in between {} and {}".format(final_downtrend_index, BUY_UPPER_MIDDLE_THRESHOLD, BUY_UPPER_THRESHOLD,
                                                                                                            final_uptrend_index, BUY_LOWER_THRESHOLD, BUY_LOWER_MIDDLE_THRESHOLD))
                                print("Final downtrend index - Final uptrend index, {} in between {} and {}".format((final_downtrend_index-final_uptrend_index), LOWER_DOWN_UP_DIFF, UPPER_DOWN_UP_DIFF))
                                if (final_reversal_index >= BUY_REVERSAL_LOWER_THRESHOLD) and (final_reversal_index <= BUY_REVERSAL_UPPER_THRESHOLD):
                                    print("Final Reversal Index, {} in between {} and {}".format(final_reversal_index, BUY_REVERSAL_LOWER_THRESHOLD, BUY_REVERSAL_UPPER_THRESHOLD))
                                    print("Buy signal is switched on now")
                                    BUY_SIGNAL = True
                                    BUY_SIGNAL_TIME.append(timenow.strftime("%Y%m%d_%H%M%S"))
                                    MIN_PRICE = close_price_list[-1]

                                else:
                                    print("Final Reversal Index, {} NOT in between {} and {}".format(final_reversal_index, BUY_REVERSAL_LOWER_THRESHOLD, BUY_REVERSAL_UPPER_THRESHOLD))
                                    print("Reversal Condition not met...")
                            else:
                                print("Final uptrend index and/or Final downtrend index not met requirement")
                                print("Check with second sets of buying condition, this is for detecting slow and steady uptrend")

                                if (final_uptrend_index >= 7.0) and (final_uptrend_index <= 7.5) and (final_downtrend_index >= 5.0) and (final_downtrend_index <= 5.5) and (final_reversal_index >= 1.8) and (final_reversal_index <= 3.0):
                                    print("Second set of buying conditions are satisfied...Will buy")
                                    BOUGHT = QUANTITY * close_price_list[-1]
                                    BOUGHT_PER_UNIT = close_price_list[-1]

                                    print("Making Buy Order...")
                                    for i in range(ORDER_TIMES):
                                        print("Order {}:".format(i))
                                        # resp_bought = kraken_request(url_path=api_enum.USER_TRADING['ADD_ORDER'], 
                                        #                             data={
                                        #                             "nonce": nonce_generator(),
                                        #                             "ordertype": "market",
                                        #                             "type": "buy",
                                        #                             "volume": QUANTITY,
                                        #                             "pair": TRADE_PAIR,
                                        #                             }, 
                                        #                             api_key=API_KEY,
                                        #                             api_sec=API_SECRET_KEY)
                                        # resp_bought = resp_bought.json()
                                        resp_bought = {'error': []}
                                        # Check if there's any error
                                        if resp_bought['error'] == []:
                                            print("ORDER SUCCEED")
                                            #print("Response: {}".format(resp_bought['result']))
                                            print("Bought {} USD at {} per ETH".format(BOUGHT, BOUGHT_PER_UNIT))
                                            BOUGHT_HIST.append(BOUGHT)
                                            BOUGHT_TIME.append(timenow.strftime("%Y%m%d_%H%M%S"))
                                            SECOND_BOUGHT_TIME.append(timenow.strftime("%Y%m%d_%H%M%S"))
                                            BOUGHT_PER_UNIT_LIST.append(BOUGHT_PER_UNIT)
                                            IN_POSITION = True
                                            BOUGHT_PRICE = close_price_list[-1]
                                            FINAL_UPTREND_INDEX_LIST.append(final_uptrend_index)
                                            FINAL_DOWNTREND_INDEX_LIST.append(final_downtrend_index)
                                            FINAL_REVERSAL_INDEX_LIST.append(final_reversal_index)
                                    
                                        else:
                                            print("ORDER FAILED")
                                            print("Error: {}".format(resp_bought['error']))

                                else:
                                    print("Second sets of buying condition not satsified...")

                    elif BUY_SIGNAL == True:
                        if (atr[-1] < 4.00):
                            print("ATR is below 4.00 and buy signal is up")
                            print("Buy signal is up..will buy when the price starts rising")
                            MIN_PRICE = close_price_list[-1] if close_price_list[-1] < MIN_PRICE else MIN_PRICE
                            print("Last atr: {}".format(atr[-1]))
                            print("Price difference: {}".format(close_price_list[-1] - MIN_PRICE))

                            if ((close_price_list[-1] - MIN_PRICE) < atr[-1]):
                                print("Hold first since the price is still reducing")
                                print("Price diff smaller than atr")
                            else:
                                print("Price diff is greater than atr")
                                print("Prices are increasing significantly now so buy...")
                                print("Buy since we are not in position and it is a good time to buy")
                                print("Condition satisfied:")
                                BOUGHT = QUANTITY * close_price_list[-1]
                                BOUGHT_PER_UNIT = close_price_list[-1]

                                print("Making Buy Order...")
                                for i in range(ORDER_TIMES):
                                    print("Order {}:".format(i))
                                    # resp_bought = kraken_request(url_path=api_enum.USER_TRADING['ADD_ORDER'], 
                                    #                             data={
                                    #                             "nonce": nonce_generator(),
                                    #                             "ordertype": "market",
                                    #                             "type": "buy",
                                    #                             "volume": QUANTITY,
                                    #                             "pair": TRADE_PAIR,
                                    #                             }, 
                                    #                             api_key=API_KEY,
                                    #                             api_sec=API_SECRET_KEY)
                                    # resp_bought = resp_bought.json()
                                    resp_bought = {'error': []}
                                    # Check if there's any error
                                    if resp_bought['error'] == []:
                                        print("ORDER SUCCEED")
                                        #print("Response: {}".format(resp_bought['result']))
                                        print("Bought {} USD at {} per ETH".format(BOUGHT, BOUGHT_PER_UNIT))
                                        BOUGHT_HIST.append(BOUGHT)
                                        BOUGHT_TIME.append(timenow.strftime("%Y%m%d_%H%M%S"))
                                        BOUGHT_PER_UNIT_LIST.append(BOUGHT_PER_UNIT)
                                        IN_POSITION = True
                                        BUY_SIGNAL = False
                                        BOUGHT_PRICE = close_price_list[-1]
                                        FINAL_UPTREND_INDEX_LIST.append(final_uptrend_index)
                                        FINAL_DOWNTREND_INDEX_LIST.append(final_downtrend_index)
                                        FINAL_REVERSAL_INDEX_LIST.append(final_reversal_index)
                                
                                    else:
                                        print("ORDER FAILED")
                                        print("Error: {}".format(resp_bought['error']))
                        else:
                            print("ATR is above 4.00, Don't buy yet although buy signal is up")


                else:
                    print("This message should not be appearing.....Please debug")
                

                print("FUI List: {}".format(FINAL_UPTREND_INDEX_LIST))
                print("FDI List: {}".format(FINAL_DOWNTREND_INDEX_LIST))
                print("FRI List: {}".format(FINAL_REVERSAL_INDEX_LIST))
                print("Buy Price Per Unit: {}".format(BOUGHT_PER_UNIT_LIST))
                print("Buy History: {}".format(BOUGHT_HIST))
                print("Buy signal time: {}".format(BUY_SIGNAL_TIME))
                print("Buy time: {}".format(BOUGHT_TIME))
                print("Second Buy time: {}".format(SECOND_BOUGHT_TIME))
                print("Sell Price Per Unit: {}".format(SOLD_PER_UNIT_LIST))
                print("Sell History: {}".format(SOLD_HIST))
                print("Sell signal time: {}".format(SELL_SIGNAL_TIME))
                print("Sell time: {}".format(SOLD_TIME))
                print("Second Sell time: {}".format(SECOND_SOLD_TIME))

                if len(SOLD_HIST) == len(BOUGHT_HIST):
                    PROFIT_HIST = np.array(SOLD_HIST) - np.array(BOUGHT_HIST)
                    print("Profit History: {}".format(PROFIT_HIST))
                    NET_PROFIT_HIST = PROFIT_HIST - (np.array(SOLD_HIST) * KRAKEN_FEES) - (np.array(BOUGHT_HIST) * KRAKEN_FEES)
                    print("Net Profit History: {}".format(NET_PROFIT_HIST))
                    TOTAL_PROFIT = np.sum(PROFIT_HIST)
                    print("Total Profit: {}".format(TOTAL_PROFIT))
                    TOTAL_NET_PROFIT = np.sum(NET_PROFIT_HIST)
                    print("Total Net Profit: {}".format(TOTAL_NET_PROFIT))
                else:
                    PROFIT_HIST = np.array(SOLD_HIST) - np.array(BOUGHT_HIST[:-1])
                    print("Profit History: {}".format(PROFIT_HIST))
                    NET_PROFIT_HIST = PROFIT_HIST - (np.array(SOLD_HIST) * KRAKEN_FEES) - (np.array(BOUGHT_HIST) * KRAKEN_FEES)
                    print("Net Profit History: {}".format(NET_PROFIT_HIST))
                    TOTAL_PROFIT = np.sum(PROFIT_HIST)
                    print("Total Profit: {}".format(TOTAL_PROFIT))
                    TOTAL_NET_PROFIT = np.sum(NET_PROFIT_HIST)
                    print("Total Net Profit: {}".format(TOTAL_NET_PROFIT))
                
                print("=============================================================================================================")


        elif candle_endtime_now == candle_endtime_old:
            # Do nothing if the price remains the same within the same candlestick timeframe
            # Only update the price when there's a newer price
            #print("Message received are still under the same candlestick endtime")
            temp_open_price = float(loaded_msg[1][2]) if temp_open_price != float(loaded_msg[1][2]) else temp_open_price
            temp_high_price = float(loaded_msg[1][3]) if temp_high_price != float(loaded_msg[1][3]) else temp_high_price
            temp_low_price = float(loaded_msg[1][4]) if temp_low_price != float(loaded_msg[1][4]) else temp_low_price
            temp_close_price = float(loaded_msg[1][5]) if temp_close_price != float(loaded_msg[1][5]) else temp_close_price
            #print("Updating the candlestick price, will only append to the list when the price is finalised")

    else:
        pass
      

########## For WebSocket ###########


########## For REST API ###########
def nonce_generator():
    """
    Generates a 14-digit nonce (Number you only used once) by modifying the unix time stamp.
    This nonce will be used for every type of HTTP request that is sent to the server
    According to Kraken API, nounce must be continuously increasing, there's no way to reset
    the nounce for the API key to a lower value.
    """
    unix_time = time.time() # e.g. 1629104436.5457473
    # Incase more than one HTTP request is sent within 1 second
    mod_unix_time = int(unix_time * 10000) # e.g. 16291044365457
    
    return mod_unix_time


def get_kraken_signature(urlpath, data, api_secret_key):
    """
    Generate a kraken signature based on nonce, order data and API secret key.
    The kraken siganture will be used for every HTTP request communicated through the Kraken REST API
    Authenticated request should be signed with "API-Sign" header, using a signature generated with
    private key, nonce, encoded payload and URL path according to:
    HMAC-SHA512 of (URI path + SHA256(nonce + POST data)) and base64 decoded secret API key
    """
    # Encode the data into a string pertaining nonce and the order information
    url_encoded = urllib.parse.urlencode(data)
    # Combine both strings together and convert it into a byte object
    encoded = (str(data['nonce']) + url_encoded).encode() # ENCODE: str to byte
    # Convert the encoded byte object into a hash. 
    # NOTE: Hash allwos the verification of the authenticity of the message
    # NOTE: HMAC allows the verification of the autehtnticty and the originator of the message
    hashed_message = urlpath.encode() + hashlib.sha256(encoded).digest()

    # HMAC, Hash-based Message Authentication Code, basically provides a cryptographic key to the 
    # client and the server, this key is only known to the specific client and the specific server
    #  Convert the HMAC object into a bytes object by hash_mac.digest()
    # e.g. output b'\xfe\x84P\16\xd1\xb3b\x1a\xd0\xc2\xaf2
    hash_mac = hmac.new(key=base64.b64decode(api_secret_key), msg=hashed_message, digestmod=hashlib.sha512).digest()
    # Encode the 64 character-HMAC into a bytes object
    # e.g .output b'/oRQn+ckRzevMg=='
    sigdigest = base64.b64encode(hash_mac)
    # Return the string of the byte object, ENCODE = str to byte, DECODE = byte to str
    return sigdigest.decode()


def kraken_request(url_path, data, api_key, api_sec):
    headers = {}
    # Get the API key
    headers['API-Key'] = api_key
    # Get the Kraken Signature
    headers['API-Sign'] = get_kraken_signature(urlpath=url_path, data=data, api_secret_key=API_SECRET_KEY)
    req = requests.post(url=(API_URL + url_path), headers=headers, data=data)
    return req
########## For REST API ###########


########## For Trading Strategy ###########
def trend_id( high_price_list, low_price_list, close_price_list, timeperiod=20, number=5 ):
    """
    Detect whether the market is going on an uptrend or downtrend based on the highest high
    and the lowest low within the time period
    Uptrend only when the impulsive move (current highest high) doesn't fall below the pullback (lowest low) 
    Downtrend only when the impulsive move (current lowest low) doesn't rise above the pullback (highest high)
    Return <boolean whether there is an uptrend or downtrend>, 
    <Confidence score of being the specific trend>
    <Most extreme value in the group>
    """
    # Return the index of the lowest low prices (Which contains many pullback for uptrending price)
    low_index = argrelextrema(data = np.array(low_price_list[-timeperiod:]), comparator=np.less, mode='clip')
    # Price of the lowest low within the defined time period
    low_array = np.array([low_price_list[-timeperiod:][i] for i in low_index[0]]) 
    # Return the index of the highest high prices (Which contains many pullback for downtrending price)
    high_index = argrelextrema(data = np.array(high_price_list[-timeperiod:]), comparator=np.greater, mode='clip')
    # Price of the highest high within the defined time period
    high_array = np.array([high_price_list[-timeperiod:][i] for i in high_index[0]])

    print("##### Trend Detector: #####")
    #if close_price_list[-1] > low_array[0]:
    if close_price_list[-1] > close_price_list[-timeperiod]:
        # Defined number of the lowest low within the defined time period
        # print("Greater than the very first pullback neckline")
        print("Greater than the very first closing price (oldest closing price) of the time period")
        # Use "try" incase there's not enough minima/maxima for "find_extr_value" function
        # NOTE: the "lowest_array" is also a support or a potential resistance
        lowest_array = algo_func.find_extr_value(arr=low_array, 
                                                    number=(len(low_array) if number > len(low_array) else number), 
                                                    max=False)
        print("Major uptrend pullback: {}".format(lowest_array))
        print("##### Trend Detector #####")
        trend_perc = np.round(np.sum(np.greater(close_price_list[-1], lowest_array) * 1.0) / len(lowest_array), 2)
        if trend_perc < 0.5:
            trend_perc = 1 - trend_perc
            return False, trend_perc, (True, lowest_array) # Second boolean indicating support/resistance, True=spt, False=resistance
        else:
            return True, trend_perc, (True, lowest_array)

    else:
        print("Smaller than the very first closing price (oldest closing price) of the time period ")
        # NOTE: the "highest_array" is also a resistance or a potential support
        highest_array = algo_func.find_extr_value(arr=high_array, 
                                                    number=(len(high_array) if number > len(high_array) else number), 
                                                    max=True)
        print("Major downtrend pullback: {}".format(highest_array))
        print("##### Trend Detector: #####")
        trend_perc = np.round(np.sum(np.less(close_price_list[-1], highest_array) * 1.0) / len(highest_array), 2)
        if trend_perc < 0.5:
            trend_perc = 1 - trend_perc
            return True, trend_perc, (False, highest_array) # Second boolean indicating support/resistance, True=spt, False=resistance
        else:
            return False, trend_perc, (False, highest_array) 


########## For Trading Strategy ###########


# Define the payload that will be sent for subscription to the websocket
payload = {
  "event": "subscribe",
  "pair": [
    "ETH/USD"
  ],
  "subscription": {
    "name": "ohlc"
  }
}

# Initialise the websocket application
ws = websocket.WebSocketApp(url=SOCKET, on_open=on_open, on_message=on_message, on_close=on_close)
# Connect to the socket and remains forever connected until interrupted
ws.run_forever()
