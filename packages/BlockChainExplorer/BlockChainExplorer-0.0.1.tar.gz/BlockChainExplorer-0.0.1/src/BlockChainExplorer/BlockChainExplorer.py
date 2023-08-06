
import requests
import json


class Explorer:
	#requires chain id - supports avax, bsc, polygon & eth, also requires api key for the appropriate blockchain explorer
	def __init__(self, chain, api_key):
	    self.api_key = api_key
	    chain_dict = {'avax' : 'https://api.snowtrace.io/api',
	    				   'bsc' : 'https://api.bscscan.com/api',
	    				   'polygon' : 'https://api.polygonscan.com/api',
	    				   'eth' : 'https://api.etherscan.io/api' }

	    self.chain = chain_dict[chain]

	def convResponse(self, data):
		byte_str = data.content
		dict_str = byte_str.decode("UTF-8")
		return eval(dict_str)

	#takes contract address and returns the json of the ABI
	def getABI(self, address):
		request_url = f"{self.chain}?module=contract&action=getabi&address={address}&apikey={self.api_key}"
		response = requests.get(request_url)
		abi = json.loads(self.convResponse(response)['result'])
		return abi
		
	#takes contract address and returns the source code	
	def getSource(self, address):
		request_url = f"{self.chain}?module=contract&action=getsourcecode&address={address}&apikey={self.api_key}"
		response = requests.get(request_url).json()
		if response['message'] == "OK":
			return response['result'][0]
		else:
			print(response)
			return None


	#takes contract_address or wallet address note - one needs to be set to None. Returns all the token transacations
	def getTransactions(self, contract_address, address, start_block = 0, end_block = 99999999):
		request_url = f"{self.chain}?module=account&action=tokentx"
		if contract_address is not None:
			request_url += f"&contractaddress={contract_address}"
		if address is not None:
			request_url += f"&address={address}"
		request_url += f"&startblock={start_block}&endblock={end_block}&sort=asc&apikey={self.api_key}"

		response = requests.get(request_url)
		#print(response.content)
		txs = self.convResponse(response)
		return txs['result']

	#takes contract_address or wallet address note - one needs to be set to None. Returns all the 'normal' transacations
	def getTransactionList(self, contract_address, address, start_block = 0, end_block = 99999999):
		request_url = f"{self.chain}?module=account&action=txlist"
		if contract_address is not None:
			request_url += f"&contractaddress={contract_address}"
		if address is not None:
			request_url += f"&address={address}"
		request_url += f"&startblock={start_block}&endblock={end_block}&sort=asc&apikey={self.api_key}"

		response = requests.get(request_url)
		#print(response.content)
		txs = self.convResponse(response)
		return txs['result']

	#takes contract_address or wallet address note - one needs to be set to None. Returns all the 'internal' transacations
	def getInternalTransactionList(self, contract_address, address, start_block = 0, end_block = 99999999):
		request_url = f"{self.chain}?module=account&action=txlistinternal"
		if contract_address is not None:
			request_url += f"&contractaddress={contract_address}"
		if address is not None:
			request_url += f"&address={address}"
		request_url += f"&startblock={start_block}&endblock={end_block}&sort=asc&apikey={self.api_key}"

		response = requests.get(request_url)
		#print(response.content)
		txs = self.convResponse(response)
		return txs['result']

	#takes a unix timestamp and turns the block number for that timestamp
	def getBlockByTimestamp(self, timestamp):
		request_url = f"{self.chain}?module=block&action=getblocknobytime&timestamp={timestamp}&closest=before&apikey={self.api_key}"
		response = requests.get(request_url).json()
		return int(response['result'])

	#takes a single address or a list of upto 20 addresses and returns the native token balance(s)
	def getBalance(self, address):
		if isinstance(address, list):
			if not (len(address) > 20):
				addressStr = address[0]
				for addy in address:
					addressStr += ', ' + addy
				request_url = f"{self.chain}?module=account&action=balancemulti&address={addressStr}&tag=latest&apikey={self.api_key}"
				response = requests.get(request_url).json()
				return response['result']
		else:
			request_url = f"{self.chain}?module=account&action=balance&address={address}&tag=latest&apikey={self.api_key}"
			response = requests.get(request_url).json()
			return response['result']

		return -1

	#takes a single contract address or a list of upto 5 contract addresses and returns the creator wallet and transaction hash
	def getContractCreation(self, address):
		if isinstance(address, list):
			if not (len(address) > 5):
				addressStr = address[0]
				for addy in address:
					addressStr += ', ' + addy
				request_url = f"{self.chain}?module=contract&action=getcontractcreation&address={addressStr}&tag=latest&apikey={self.api_key}"
				response = requests.get(request_url).json()
				return response['result']
		else:
			request_url = f"{self.chain}?module=contract&action=getcontractcreation&address={address}&tag=latest&apikey={self.api_key}"
			response = requests.get(request_url).json()
			return response['result']

		return -1		

	def getInternalTransactionsByTx(tx):
		request_url = f'{self.chain}?module=account&action=txlistinternal&txhash={tx}&apikey={self.api_key}'
		response = requests.get(request_url).json()
		return response