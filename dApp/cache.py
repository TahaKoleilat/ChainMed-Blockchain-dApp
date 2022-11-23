from web3 import Web3
import ipfsApi
import json
from web3 import Web3
import os
from decimal import Decimal
from dotenv import load_dotenv
from hashlib import sha256

def get_private_key(url):
    web3 = Web3(Web3.HTTPProvider(url))
    keyfile = os.path.join(os.getcwd(),os.path.join("testing_keys","key1"))
    with open(keyfile) as f:
        key_data = json.load(f)
    private_key = web3.eth.account.decrypt(key_data,"").hex()
    return private_key

def deploy_contract(abi,bytecode,url):

    web3 = Web3(Web3.HTTPProvider(url))
    
    load_dotenv()
    account_address = Web3.toChecksumAddress(os.getenv("ACCOUNT_ADDRESS"))
    private_key = get_private_key(url)

    contract = web3.eth.contract(abi=abi, bytecode=bytecode)

    tx = contract.constructor().buildTransaction({'nonce': web3.eth.getTransactionCount(account_address), 'from': account_address,"gasPrice": web3.eth.gas_price})

    signed_tx = web3.eth.account.signTransaction(tx, private_key=private_key)

    tx_transact = web3.eth.sendRawTransaction(signed_tx.rawTransaction)


    tx_receipt = web3.eth.waitForTransactionReceipt(tx_transact)
    
    return tx_receipt

def upload_(abi,url,messageID,expiry,businessRequirement,contract_address,messageSubject,messageContent,messageDate,keyID):

    web3 = Web3(Web3.HTTPProvider(url,request_kwargs={'timeout': 600}))
    contract = web3.eth.contract(
        address=contract_address,
        abi=abi,
    )
    
    load_dotenv()
    account_address = Web3.toChecksumAddress(os.getenv("ACCOUNT_ADDRESS"))
    private_key = get_private_key(url)
    messageSubjectHash = sha256(messageSubject.encode('utf-8')).hexdigest()
    messageContentHash = sha256(messageContent.encode('utf-8')).hexdigest()
    keyIDHash = sha256(keyID.encode('utf-8')).hexdigest()
    
    tx = contract.functions.createContract(messageID,expiry,businessRequirement,messageContentHash,messageDate,keyIDHash).buildTransaction({'nonce': web3.eth.getTransactionCount(account_address), 'from': account_address,"gasPrice": web3.eth.gas_price})

    signed_tx = web3.eth.account.signTransaction(tx, private_key=private_key)

    tx_transact = web3.eth.sendRawTransaction(signed_tx.rawTransaction)


    tx_receipt = web3.eth.waitForTransactionReceipt(tx_transact)
    
    
    return tx_receipt




load_dotenv()
bytecode = os.getenv('BYTECODE')
url = os.getenv('URL')
abi = os.getenv('ABI')
account_address = Web3.toChecksumAddress(os.getenv('ACCOUNT_ADDRESS'))
private_key = get_private_key(url)
contract_address = os.getenv("Contract_Address")


#The Smart Contract will be deployed using the following lines of code
# tx = deploy_contract(abi,bytecode,url)
# print(tx["contractAddress"])
api = ipfsApi.Client("127.0.0.1",port=8080)
# print(api.add('test.txt'))
api.get('QmSarkrjRiobiPB9Ymur5bWUYjiQQLsyamC8d9kGuTD1Tu')
