
import requests
import json


class Explorer:
	"""requires chain id - supports avax, bsc, polygon & eth, also requires api key for the appropriate blockchain explorer"""
	def __init__(self, chain: str, api_key: str):
	    self.api_key = api_key
	    """Your api key for the blockchain explorer you're trying to access"""
	    chain_dict = {'avax' : 'https://api.snowtrace.io/api',
	    				   'bsc' : 'https://api.bscscan.com/api',
	    				   'polygon' : 'https://api.polygonscan.com/api',
	    				   'eth' : 'https://api.etherscan.io/api' }

	    self.chain = chain_dict[chain]
	    """ 'eth', 'bsc', 'polygon' or 'avax' for the chain you're trying to access"""

	def convResponse(self, data):
		byte_str = data.content
		dict_str = byte_str.decode("UTF-8")
		return eval(dict_str)


	def responseCheck(self, response):
		if response["message"] == "OK":
			return response['result']
		else:
			raise Exception(response["message"])

	
	def getABI(self, address: str):
		"""takes contract address as a string and returns the json of the ABI"""
		request_url = f"{self.chain}?module=contract&action=getabi&address={address}&apikey={self.api_key}"
		response = requests.get(request_url)
		return self.responseCheck(response)
		
	
	def getSource(self, address: str):
		"""takes contract address as a string and returns the source code"""
		request_url = f"{self.chain}?module=contract&action=getsourcecode&address={address}&apikey={self.api_key}"
		response = requests.get(request_url).json()
		return self.responseCheck(response)[0]


	
	def getTransactions(self, contract_address: str, address: str, start_block: int = 0, end_block: int = 99999999):
		"""takes contract_address or wallet address as a string note - one needs to be set to None. Returns all the token transacations as a dict"""
		request_url = f"{self.chain}?module=account&action=tokentx"
		if contract_address is not None:
			request_url += f"&contractaddress={contract_address}"
		if address is not None:
			request_url += f"&address={address}"
		request_url += f"&startblock={start_block}&endblock={end_block}&sort=asc&apikey={self.api_key}"
		response = requests.get(request_url)
		txs = self.convResponse(response)
		return self.responseCheck(txs)

	
	def getTransactionList(self, contract_address: str, address: str, start_block: int = 0, end_block: int = 99999999):
		"""takes contract_address or wallet address as a string note - one needs to be set to None. Returns all the 'normal' transacations as a list of dicts"""
		request_url = f"{self.chain}?module=account&action=txlist"
		if contract_address is not None:
			request_url += f"&contractaddress={contract_address}"
		if address is not None:
			request_url += f"&address={address}"
		request_url += f"&startblock={start_block}&endblock={end_block}&sort=asc&apikey={self.api_key}"

		response = requests.get(request_url)
		txs = self.convResponse(response)
		return self.responseCheck(txs)

	
	def getInternalTransactionList(self, contract_address: str, address: str, start_block: int = 0, end_block: int = 99999999):
		"""takes contract_address or wallet address as a string note - one needs to be set to None. Returns all the 'internal' transacations as a list of dicts"""
		request_url = f"{self.chain}?module=account&action=txlistinternal"
		if contract_address is not None:
			request_url += f"&contractaddress={contract_address}"
		if address is not None:
			request_url += f"&address={address}"
		request_url += f"&startblock={start_block}&endblock={end_block}&sort=asc&apikey={self.api_key}"

		response = requests.get(request_url)
		txs = self.convResponse(response)
		return self.responseCheck(txs)

	
	def getBlockByTimestamp(self, timestamp: int):
		"""takes a unix timestamp as an int and turns the block number for that timestamp"""
		request_url = f"{self.chain}?module=block&action=getblocknobytime&timestamp={timestamp}&closest=before&apikey={self.api_key}"
		response = requests.get(request_url).json()
		return self.responseCheck(response)

	
	def getBalance(self, address: str):
		"""takes a single address as a string or a list of upto 20 addresses and returns the native token balance(s)"""
		if isinstance(address, list):
			if not (len(address) > 20):
				addressStr = address[0]
				for addy in address:
					addressStr += ', ' + addy
				request_url = f"{self.chain}?module=account&action=balancemulti&address={addressStr}&tag=latest&apikey={self.api_key}"
				response = requests.get(request_url).json()
				return self.responseCheck(response)
		else:
			request_url = f"{self.chain}?module=account&action=balance&address={address}&tag=latest&apikey={self.api_key}"
			response = requests.get(request_url).json()
			return self.responseCheck(response)

		return -1

	
	def getContractCreation(self, address: str):
		"""takes a single contract address as a string or a list of upto 5 contract addresses and returns the creator wallet and transaction hash as a list of dicts"""
		if isinstance(address, list):
			if not (len(address) > 5):
				addressStr = address[0]
				for addy in address:
					addressStr += ', ' + addy
				request_url = f"{self.chain}?module=contract&action=getcontractcreation&address={addressStr}&tag=latest&apikey={self.api_key}"
				response = requests.get(request_url).json()
				return responseCheck(response)
		else:
			request_url = f"{self.chain}?module=contract&action=getcontractcreation&address={address}&tag=latest&apikey={self.api_key}"
			response = requests.get(request_url).json()
			return self.responseCheck(response)

		return -1		

	
	def getInternalTransactionsByTx(self, tx: str):
		"""Takes a transaction hash as a string and returns the internal transactions as a list of dicts"""
		request_url = f'{self.chain}?module=account&action=txlistinternal&txhash={tx}&apikey={self.api_key}'
		response = requests.get(request_url).json()
		return self.responseCheck(response)

