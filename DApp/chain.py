from web3 import Web3, HTTPProvider
from solc import compile_source
import time
# from strategies.current_strategy 

w3 = Web3(HTTPProvider("http://localhost:8545"))

# 指定最后一个账户为默认账户，并且为资金池
w3.eth.defaultAccount = w3.eth.accounts[-1]
fund_pool = w3.eth.accounts[-1]


def get_contract(file_name):
	with open(file_name) as f:
		return compile_source(f.read())


# 部署 Info 合约
info_contract = get_contract('contracts/Info.sol')
info_interface = info_contract['<stdin>:Info']
Info_Contract = w3.eth.contract(bytecode=info_interface['bin'], abi=info_interface['abi'])

info_hash = Info_Contract.constructor().transact()
info_receipt = w3.eth.waitForTransactionReceipt(info_hash)
info_address = info_receipt.contractAddress
# 编译并部署完成后的智能合约入口
info = w3.eth.contract(address=info_receipt.contractAddress, abi=info_interface['abi'])


def get_strategy():
	return info.functions.getStrategy().call()


# 部署 Vote 合约
vote_contract = get_contract('contracts/Vote.sol')
vote_interface = vote_contract['<stdin>:Vote']
Vote_Contract = w3.eth.contract(bytecode=vote_interface['bin'], abi=vote_interface['abi'])

# Vote 合约需要在 Info 合约的基础上部署
vote_hash = Vote_Contract.constructor(info_address).transact()
vote_receipt = w3.eth.waitForTransactionReceipt(vote_hash)

voote = w3.eth.contract(address=vote_receipt.contractAddress, abi=vote_interface['abi'])


# 部署 EHT 合约
eht_contract = get_contract('contracts/EHT.sol')
interface = eht_contract['<stdin>:Ether_Hedge_Token']
EHT_Contract = w3.eth.contract(bytecode=interface['bin'], abi=interface['abi'])

tx_hash = EHT_Contract.constructor().transact()
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

# 编译并部署完成后的智能合约入口
hedge = w3.eth.contract(address=tx_receipt.contractAddress, abi=interface['abi'])


# 转 Token
def transfer_eht(_from, _to, _value):
	hexbytes = hedge.functions.transferFrom(
		w3.toChecksumAddress(_from), w3.toChecksumAddress(_to), _value).transact()
	return hexbytes

for ac in w3.eth.accounts:
	transfer_eht(w3.toChecksumAddress(w3.eth.defaultAccount), w3.toChecksumAddress(ac), 1000000)


# 转以太币
def transfer_fund(_from, _to, _value):
	result = w3.eth.sendTransaction({"from": w3.toChecksumAddress(_from),
                                    "to": w3.toChecksumAddress(_to), "value": _value})
	return result


def calc_share(_account, _amount):
	total = sum(_amount)
	perc = []
	for i in _amount:
		perc.append(i / total)
	return perc, total


def add_share(_address, _amount):
	return info.functions.addShare(_address, _amount).transact()


def get_share(_address):
	return info.functions.getShare(_address).call()


def allocate_profits(profits, perc):
	allocation = []
	for i in perc:
		allocation.append(i * profits)
	return allocation


def vote_strategy(_address, proposal):
	return voote.functions.vote(_address, proposal).transact()


def declare_winner():
	return voote.functions.winningProposal().transact()

