"""
Data Visualization Project

Parse data from an ugly CSV or Excel file, and render it in
JSON-like form, visualize in graphs, and plot on Google Maps.

Part II: Take the data we just parsed and visualize it using popular
Python math libraries.
"""

from collections import Counter

import csv

# I added pprint to recall the structure of parsed_data
import pprint
import matplotlib.pyplot as plt
import numpy.numarray as na

# In the tutorial, she recreates the parse function 
# rather than importing the parse module.
import parse


MY_FILE = parse.MY_FILE


def visualize_days(parsed_data):
    """Visualize data by day of week"""
    
    # Make a new variable, 'counter', from iterating through
    # each line of data in the parsed data, and count how
    # many incidents happen on each day of week
    counter = Counter(item["DayOfWeek"] for item in parsed_data)
    
    # Challenge was to re-create counter using a for loop,
    # rather than a list comprehension.
    list_for_counter = []
    
    for item in parsed_data:
        list_for_counter.append(item["DayOfWeek"])
    
    counter_from_loop = Counter(list_for_counter)
    
    # Separate the x-axis data (the days of the week) from the
    # 'counter' variable from the y-axis data (the number of
    # incidents for each day).
    # Day of week labels need to be a tuple for plt.xticks()
    day_tuple = tuple(["Mon", "Tues", "Wed", "Thurs", "Fri", "Sat", "Sun"])
    data_list = [
                counter["Monday"],
                counter["Tuesday"],
                counter["Wednesday"],
                counter["Thursday"],
                counter["Friday"],
                counter["Saturday"],
                counter["Sunday"]
                ]
    
    # Assign the y-axis data to a matplotlib instance.
    plt.plot(data_list)
    
    # Create the amount of ticks needed for our x-axis, and
    # assign the labels.
    plt.xticks(range(len(day_tuple)), day_tuple)
    
    # Show the plot!
    plt.show()


def visualize_type(parsed_data):
    """Visualize data by category in a bar graph"""
    
    # Make a new variable, 'counter', from iterating through
    # each line of data in the parsed data, and count how
    # many incidents happen by category
    counter = Counter(item["Category"] for item in parsed_data)
    
    # Set the labels which are based on the keys of our counter.
    # Since order doesn't matter, we can just use counter.keys()
    # Needs to be a tuple for plt.xticks()
    labels = tuple(counter.keys())
    
    # Set exactly where the labels hit the x-axis
    xlocations = na.array(range(len(labels))) + 0.5
    
    # Width of each bar that will be plotted
    width = 0.5
    
    # Assign data to a bar plot (similar to plt.plot()!)
    plt.bar(xlocations, counter.values(), width=width)
    
    # Assign labels and tick location to x-axis
    plt.xticks(xlocations + width / 2, labels, rotation=90)
    
    # Give some more room so the x-axis labels aren't cut off
    # in the graph
    plt.subplots_adjust(bottom=0.4)
    
    # Make the overall graph/figure larger
    plt.rcParams['figure.figsize'] = 12, 8
    
    # Render the graph!
    plt.show()
    

def main():
#     visualize_days(parsed_data)
    visualize_type(parsed_data)


if __name__ == '__main__':
    parsed_data = parse.parse(MY_FILE, ',')
    main()