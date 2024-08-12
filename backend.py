import time
from web3 import Web3
import os
from dotenv import load_dotenv
import json

# Load ABI from file
with open('abi.json', 'r') as file:
    abi = json.load(file)

# Load environment variables
load_dotenv()
endpoint = os.getenv("RPC_ENDPOINT")
web3 = Web3(Web3.HTTPProvider(endpoint))

if web3.is_connected():
    print("Connected to", endpoint)
else:
    print("Connection failed")

# Set up caller and account information
caller = '0x86fDC5685b533923e5E7Cd4F7154D692A5643677'
nonce = web3.eth.get_transaction_count(caller)

contract = web3.eth.contract(address=os.getenv('CONTRACT_ADDRESS'), abi=abi)
account = web3.eth.account.from_key(os.getenv('PRIVATE_KEY'))
chain_id = web3.eth.chain_id

# Get current time as a string
current_time = str(int(time.time()))  # Use integer time and convert to string

# Build the transaction dictionary
transaction = contract.functions.storeData(
    3,
    'this data is store in blockchain',
    current_time
).build_transaction({
    'chainId': chain_id,
    'from': caller,
    'nonce': nonce,
})

# Sign the transaction using the private key
signed_tx = web3.eth.account.sign_transaction(transaction, private_key=account.key)

# Send the transaction
tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
print(f'Transaction hash: {web3.to_hex(tx_hash)}')

get_data = contract.functions.getData(1).call()
print(get_data)
