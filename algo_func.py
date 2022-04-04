# Functions that are used inside the trading bot algorithm
import numpy as np

# Find a specified number of minimum value from an array
def find_extr_value(arr, number, max=True):
    """
    Find a specified number of minimum/maximum value from the given array
    Return <param>list<param>: List of lowest/highest value
    """
    extr_value_list = []

    for i in range(number):
        # Extract the lowest value and its index
        extr_value = np.max(arr) if max else np.min(arr)
        extr_value_index = np.argmax(arr) if max else np.argmin(arr)
        # Append the extreme value to the list and delete the extracted value from the array
        extr_value_list.append(extr_value)
        arr = np.delete(arr, [extr_value_index])

    return extr_value_list


# Find the number of times "True" and "False" appears in the list
def find_num_bool(list, timeperiod=5):
    buy_pressure = 0
    sell_pressure = 0
    extracted_list = list[-timeperiod:]

    for i in range(timeperiod):
        if extracted_list[i][0] == True:
            if extracted_list[i][1] == True:
                buy_pressure += 0.2
            else:
                sell_pressure += 0.2
        else:
            pass
    
    return buy_pressure, sell_pressure



