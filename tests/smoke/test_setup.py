import os
import datetime
import pyautogui
import schedule
import time

print("Python libraries are working!")

# Simple test function
def say_hello():
    print(f"Hello! Current time is: {datetime.datetime.now()}")

# Test pyautogui screen size
width, height = pyautogui.size()
print(f"Screen size detected: {width} x {height}")

# Test scheduling
schedule.every(2).seconds.do(say_hello)

print("Running scheduler test for 10 seconds...")
start_time = time.time()
while time.time() - start_time < 10:
    schedule.run_pending()
    time.sleep(1)

print("Test completed successfully!")
