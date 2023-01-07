import time
import os

instances = []

while True:
	for i in range(max(0, len(instances) - 11)):
		instances.pop(0)

	start = time.time() * 1000

	os.system("python main.py > /dev/null")

	instances.append(time.time() * 1000 - start)
	print(f"\r{round(sum(instances) / len(instances))}ms     ", end="")

	time.sleep(0.2)
