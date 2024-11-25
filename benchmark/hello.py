#!/usr/local/bin/python

# Packages
import os
import time
from sys import argv
from datetime import datetime

start = str(argv[1])
end = str(argv[2])

print(start + "-" + end)

time.sleep(200)
current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print("current datetime is: " + current_datetime)