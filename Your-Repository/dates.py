#TASKS
from datetime import datetime, timedelta

# 1. Subtract five days from current date
current_date = datetime.now()
new_date = current_date - timedelta(days=5)
print("1.")
print("Current date:", current_date)
print("5 days ago:", new_date)

# 2. Print yesterday, today, tomorrow
today = datetime.now().date()
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)
print("\n2.")
print("Yesterday:", yesterday)
print("Today:", today)
print("Tomorrow:", tomorrow)

# 3. Drop microseconds from datetime
current_datetime = datetime.now()
without_microseconds = current_datetime.replace(microsecond=0)
print("\n3.")
print("With microseconds:", current_datetime)
print("Without microseconds:", without_microseconds)

# 4. Calculate two date difference in seconds
date1 = datetime(2025, 2, 1, 12, 0, 0)
date2 = datetime(2025, 2, 3, 15, 30, 0)
difference = date2 - date1
seconds = difference.total_seconds()
print("\n4.")
print("Difference in seconds:", seconds)


x = datetime.datetime.now()

print(x)

#2026-02-26 15:57:11.721704 
#my time

#The method is called strftime(), and takes one parameter, format, to specify the format of the returned string:
print(x.year)           #2026
print(x.strftime("%A")) #Day of week

import datetime

x = datetime.datetime(2020, 5, 17)

print(x) #2020-05-17 00:00:00

#time differences
from datetime import datetime

# Define two datetime objects
start_time = datetime(2024, 7, 24, 10, 30, 0)
end_time = datetime(2024, 7, 24, 11, 45, 15)

# Calculate the difference
time_difference = end_time - start_time

print(time_difference)
# Output: 1:15:15 (1 hour, 15 minutes, 15 seconds)
