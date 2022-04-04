# Detect the presence of 3 candlestick pattern: 
# 38.2% Candle (Upward or downward), Engulfing Candle (Upward or downward), Close above/below candle

def candle_382(open_price_list, high_price_list, low_price_list, close_price_list):
    """
    Detect the presence for 38.2% candle pattern
    Return <boolean whether it is a 382 candle>, <boolean whether it is upward for downward>
    """
    # Maximum price difference of a candlestick
    max_price_diff = high_price_list[-1] - low_price_list[-1]
    # Price difference between the open price and the minimumum price of the candlestick
    price_diff = open_price_list[-1] - low_price_list[-1]

    # Detect for downward 38.2% candle
    if close_price_list[-1] < open_price_list[-1]:
        
        if price_diff <= (max_price_diff * 0.382):
            return True, False # True for being 38.2% candle, False for being downward
        else:
            return False, False

    # Detect for upward 38.2% candle
    elif close_price_list[-1] > open_price_list[-1]:
        if price_diff >= (max_price_diff * 0.618):
            return True, True # 1st True for being 38.2% candle, 2nd True for being upward
        else:
            return False, False

    # Just incase in very very extreme situation where open price is the same as closing price
    else:
        return False, False

def candle_engulf(open_price_list, close_price_list):
    """
    Detect the presence of engulfing candle
    Return <boolean whether it is an engulfing candle>, <upward or downward>
    For non engulfing candle, it doesn't matter if the second candle is upward(True) or downward(False)
    """
    # Testing whether the current candlestick is larger than the previous candlestick
    if abs(open_price_list[-1] - close_price_list[-1]) > abs(open_price_list[-2] - close_price_list[-2]):
        if ( (close_price_list[-1] - open_price_list[-1]) > 0 ) and ( (close_price_list[-2] - open_price_list[-2]) < 0 ):
            return True, True # 1st True for being engulfing candle, 2nd True for being upward candle
            
        elif ( (close_price_list[-1] - open_price_list[-1]) < 0 ) and ( (close_price_list[-2] - open_price_list[-2]) > 0 ):
            return True, False # True for being engulfing candle, False for being downward candle
        else:
            return False, False
    else:
        return False, False


def candle_close_above_below(high_price_list, low_price_list, close_price_list):
    """
    Detect the presence of close above/below candle
    Return <boolean whether it is an close above/below candle>, <upward, close above or downward, close below>
    """
    if close_price_list[-1] < low_price_list[-2]:
        return True, False
    elif close_price_list[-1] > high_price_list[-2]:
        return True, True
    else:
        return False, False

# Sample used to test the function
o = [3060.48, 3063.74, 3063.89, 3064.99, 3073.72, 3072.24, 3071.14, 3070.0, 3070.0, 3070.01, 3200.00, 3150.00]
h = [3063.15, 3063.89, 3065.0, 3076.17, 3075.63, 3075.41, 3071.14, 3070.09, 3070.01, 3070.26, 3300.43, 3063.93]
l = [3060.48, 3062.17, 3063.89, 3064.99, 3070.36, 3071.14, 3070.0, 3070.0, 3070.0, 3070.0, 3063.37, 3063.41]
c = [3063.15, 3063.89, 3065.0, 3075.12, 3075.63, 3071.14, 3070.0, 3070.0, 3070.01, 3070.0, 3120.00, 3000.00]

