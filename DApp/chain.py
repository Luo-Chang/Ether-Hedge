from web3 import Web3, HTTPProvider
from solc import compile_source
import time
# import 量化策略

w3 = Web3(HTTPProvider("http://localhost:8545"))

# 新建资金池账户并解锁，注意：之前的 -1 账户此时为 -2
# fund_pool = w3.personal.newAccount('fund_pool')
# w3.personal.unlockAccount(fund_pool, 'fund_pool')

# 指定最后一个账户为默认账户，并且为资金池
w3.eth.defaultAccount = w3.eth.accounts[-1]
fund_pool = w3.eth.accounts[-1]
# print("我擦啊啊啊来", w3.eth.defaultAccount)
# print(w3.eth.getBalance(w3.eth.defaultAccount))

def get_contract(file_name):
	with open(file_name) as f:
		return compile_source(f.read())

# 部署 Share 合约
# share_contract = get_contract('contracts/Share.sol')
# interface = eht_contract['<stdin>:Ether_Hedge_Token']
# Share_Contract = w3.eth.contract(bytecode=interface['bin'], abi=interface['abi'])
# share_hash = Share_Contract.constructor().transact()
# share_receipt = w3.eth.waitForTransactionReceipt(share_hash)

# share_address = share_receipt.contractAddress
# share = w3.eth.contract(address=share_receipt.contractAddress, abi=interface['abi'])

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

def allocate_profits(profits, perc):
	allocation = []
	for i in perc:
		allocation.append(i * profits)
	return allocation
