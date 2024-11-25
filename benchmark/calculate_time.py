#!/usr/local/bin/python

from datetime import datetime
from sys import argv
from datetime import datetime

def calculate_time_difference(datetime_str1, datetime_str2, format_str="%Y-%m-%d %H:%M:%S"):
    # Convert datetime strings to datetime objects
    datetime1 = datetime.strptime(datetime_str1, format_str)
    datetime2 = datetime.strptime(datetime_str2, format_str)

    # Calculate time difference
    time_difference = datetime2 - datetime1

    # Calculate time difference in seconds
    time_difference_seconds = time_difference.total_seconds()

    return time_difference_seconds

# Example datetime strings
datetime_str1 = argv[1]
datetime_str2 = argv[2]

# Calculate time difference
result = calculate_time_difference(datetime_str1, datetime_str2)

# Print the result
print(f'Time difference between the two datetimes: {result} seconds')
