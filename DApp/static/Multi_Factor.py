# 多因子策略
import os, time, random
import tushare as ts

# q 是消息队列
def get_price():
	return float(ts.get_realtime_quotes('hs300')['price'])

def strategy(q, amount):
	print("多因子策略运行中...")
	init_price = get_price()
	# 运行策略并向消息队列里面投放信息
	while True:
		current_price = get_price()
		profit = abs(((current_price - init_price) / init_price)) * amount
		q.put(profit)
		time.sleep(1)