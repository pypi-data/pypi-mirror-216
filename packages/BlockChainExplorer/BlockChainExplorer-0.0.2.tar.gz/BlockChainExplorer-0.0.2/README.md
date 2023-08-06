This package is a simple library to access the blockchain scanners for Ethereum, Binance Smart Chain, Polygon and Avalanche.

### getABI(self, address: str)
  Takes contract address as a string and returns the json of the ABI
### getBalance(self, address: str)
  Takes a single address as a string or a list of upto 20 addresses and returns the native token balance(s)
### getBlockByTimestamp(self, timestamp: int)
  Takes a unix timestamp as an int and turns the block number for that timestamp
### getContractCreation(self, address: str)
  Takes a single contract address as a string or a list of upto 5 contract addresses and returns the creator wallet and transaction hash as a list of dicts
### getInternalTransactionList(self, contract_address: str, address: str, start_block: int = 0, end_block: int = 99999999)
  Takes contract_address or wallet address as a string note - one needs to be set to None. Returns all the 'internal' transacations as a list of dicts
### getInternalTransactionsByTx(self, tx: str)
  Takes a transaction hash as a string and returns the internal transactions as a list of dicts
### getSource(self, address: str)
  Takes contract address as a string and returns the source code
### getTransactionList(self, contract_address: str, address: str, start_block: int = 0, end_block: int = 99999999)
  Takes contract_address or wallet address as a string note - one needs to be set to None. Returns all the 'normal' transacations as a list of dicts
### getTransactions(self, contract_address: str, address: str, start_block: int = 0, end_block: int = 99999999)
  Takes contract_address or wallet address as a string note - one needs to be set to None. Returns all the token transacations as a dict
