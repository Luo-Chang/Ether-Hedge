# 多因子策略
import os, time, random

# q 是消息队列
def strategy(q, amount):
	print("多因子策略运行中...")

	# 运行策略并向消息队列里面投放信息
	while True:
		q.put(random.randint(amount*0.01, amount*0.05))
		time.sleep(random.random()*2)