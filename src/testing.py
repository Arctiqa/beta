from datetime import datetime, timedelta

test_time = datetime.now()
t = '2023-11-09 00:14:35.210970'
actual_time = datetime.strptime(t[:19], "%Y-%m-%d %H:%M:%S")

dt = test_time - actual_time
time = timedelta(seconds=0.03)
print(dt)
print(time)
print(dt - time)
