# 根据投票结果选取相应策略
from chain import get_strategy
from multiprocessing import Process, Queue


current_strategy = get_strategy()

with open("strategies/__init__.py", "w") as f:
	f.write("from ." + current_strategy + " import strategy")

from strategies import strategy
print("量化策略载入完成:", current_strategy)
q = Queue()


def trading(amount):
	strategy(q, amount)


def start_trading(amount):
	print("启动交易进程...")
	trading_process = Process(target=trading, args=(amount,))
	trading_process.start()
	return trading_process


def get_current_profit():
	return q.get(True)