from flask import Flask, request, render_template
from web3 import Web3, HTTPProvider
from chain import fund_pool, transfer_eht, calc_share, get_contract, get_strategy, vote_strategy, declare_winner, add_share, get_share
import time
import os
from quant import start_trading, get_current_profit


app = Flask("Ether-Hedge")
w3 = Web3(HTTPProvider("http://localhost:8545"))

# 当期的持有情况统计
class Issuance():
	# _account 与 _amount 一一对应
	_account = []
	_amount = []
	total = 0

	current_profit = 0

	perc = []
	allocation = []

	trading_process = None


# 初始化智能合约
fund = Issuance()


@app.route('/', methods=['GET'])
def home():
	# transfer_eht(w3.eth.accounts[-1], fund_pool, 100000000)
	return render_template('phase_1.html', current_strategy="当前策略："+get_strategy())


@app.route('/', methods=['POST'])
def investment():
	fund._account.append(request.form['_account'])
	fund._amount.append(int(request.form['_amount']))
	print(fund._account, fund._amount)
	transfer_eht(request.form['_account'], fund_pool, int(request.form['_amount']))
	add_share(request.form['_account'], int(request.form['_amount']))
	return render_template('phase_1.html', current_strategy="当前策略："+get_strategy())


@app.route('/phase_2', methods=['POST'])
def init_phase():
	print('来到 phase_2')
	fund.perc, fund.total = calc_share(fund._account, fund._amount)
	# start trading
	fund.trading_process = start_trading(fund.total)
	return render_template('phase_2.html', account_1=fund._account[0], 
		account_2=fund._account[1], account_3=fund._account[2], v_all=fund.total)


@app.route('/phase_2', methods=['GET'])
def show_profits():
	# get current profit
	fund.current_profit = get_current_profit()

	return render_template('phase_2.html', account_1=fund._account[0], 
		account_2=fund._account[1], account_3=fund._account[2],
		v_all=fund.total, p_all=fund.current_profit, v_1=fund._amount[0], 
		v_2=fund._amount[1], v_3=fund._amount[2], p_1=int(fund.current_profit*fund.perc[0]), 
		p_2=int(fund.current_profit*fund.perc[1]), p_3=int(fund.current_profit*fund.perc[2]))
	# return render_template('phase_2.html', content=_amount[0])


@app.route('/phase_3', methods=['POST'])
def allocate_profits():
	# Stop trading
	fund.trading_process.terminate()
	
	for i, acc in enumerate(fund._account):
		transfer_eht(fund_pool, acc, int(fund.current_profit*fund.perc[i])+fund._amount[i])

	return render_template('phase_3.html', account_1=fund._account[0], 
		account_2=fund._account[1], account_3=fund._account[2],
		balance_all=fund.total+fund.current_profit, profit_all=fund.current_profit,
		profit_1=fund.current_profit*fund.perc[0], profit_2=fund.current_profit*fund.perc[1], 
		profit_3=fund.current_profit*fund.perc[2], balance_1=fund._amount[0]+fund.current_profit*fund.perc[0], 
		balance_2=fund._amount[1]+fund.current_profit*fund.perc[1], balance_3=fund._amount[2]+fund.current_profit*fund.perc[2])


@app.route('/vote', methods=['GET'])
def vote():
	return render_template('vote.html')


@app.route('/vote', methods=['POST'])
def voting():
	vote_strategy(request.form['inputAccount'], int(request.form['inputProposal']))
	return render_template('vote.html')


@app.route('/result', methods=['POST'])
def show_result():
	winner = declare_winner()
	print(get_strategy())
	return render_template('vote.html', vote_result="获胜策略："+get_strategy())


if __name__ == '__main__':
	os.system('open -a "Google Chrome" http://localhost:5000')
	app.run()

