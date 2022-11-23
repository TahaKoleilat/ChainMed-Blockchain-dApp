from web3 import Web3
import ipfsApi
import json
from web3 import Web3
import os
from dotenv import load_dotenv
from hashlib import sha256


def get_private_key(url):
    web3 = Web3(Web3.HTTPProvider(url))
    key_loc = os.getenv("PRIVATE_KEY")
    keyfile = os.path.join(os.getcwd(),os.path.join("testing_keys",key_loc))
    with open(keyfile.replace("\\",'/')) as f:
        key_data = json.load(f)
    private_key = web3.eth.account.decrypt(key_data,"").hex()
    return private_key

def upload_ipfs(host,port,file):
    api = ipfsApi.Client(host=host,port=port)
    ipfs_result = api.add(file)
    ipfs_hash = ipfs_result['Hash']
    return ipfs_hash

def retrieve_ipfs(host,port,ipfshash):
    api = ipfsApi.Client(host=host,port=port)
    api.get(ipfshash)


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

def upload_file(abi,url,host,port,file,doctorAddress,patientAddress,contract_address):

    web3 = Web3(Web3.HTTPProvider(url,request_kwargs={'timeout': 600}))
    contract = web3.eth.contract(
        address=contract_address,
        abi=abi,
    )
    
    load_dotenv()
    account_address = Web3.toChecksumAddress(os.getenv("ACCOUNT_ADDRESS"))
    private_key = get_private_key(url)
    ipfshash = upload_ipfs(host,port,file)
    tx = contract.functions.uploadFile(ipfshash,doctorAddress,patientAddress).buildTransaction({'nonce': web3.eth.getTransactionCount(account_address), 'from': account_address,"gasPrice": web3.eth.gas_price})

    signed_tx = web3.eth.account.signTransaction(tx, private_key=private_key)

    tx_transact = web3.eth.sendRawTransaction(signed_tx.rawTransaction)


    tx_receipt = web3.eth.waitForTransactionReceipt(tx_transact)
        
    
    return tx_receipt

def retrieve_file(abi,url,host,port,doctorAddress,patientAddress,contract_address):
    web3 = Web3(Web3.HTTPProvider(url,request_kwargs={'timeout': 600}))
    contract = web3.eth.contract(
        address=contract_address,
        abi=abi,
    )
    
    load_dotenv()
    account_address = Web3.toChecksumAddress(os.getenv("ACCOUNT_ADDRESS"))
    private_key = get_private_key(url)
    tx = contract.functions.retrieveFile(doctorAddress,patientAddress).buildTransaction({'nonce': web3.eth.getTransactionCount(account_address), 'from': account_address,"gasPrice": web3.eth.gas_price})
    signed_tx = web3.eth.account.signTransaction(tx, private_key=private_key)
    tx_transact = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    tx_receipt = web3.eth.waitForTransactionReceipt(tx_transact)
    encrypted_ipfshash = contract.functions.retrieveFile(doctorAddress,patientAddress).call(tx_receipt)
    ipfshash = encrypted_ipfshash
    ipfshash = retrieve_ipfs(host,port,ipfshash)
    
    return tx_receipt

def set_file_allowed(abi,url,doctorAddress,patientAddress,contract_address,files_nb):
    web3 = Web3(Web3.HTTPProvider(url,request_kwargs={'timeout': 600}))
    contract = web3.eth.contract(
        address=contract_address,
        abi=abi,
    )
    
    load_dotenv()
    account_address = Web3.toChecksumAddress(os.getenv("ACCOUNT_ADDRESS"))
    private_key = get_private_key(url)
    
    tx = contract.functions.setFileAllowed(doctorAddress,patientAddress,files_nb).buildTransaction({'nonce': web3.eth.getTransactionCount(account_address), 'from': account_address,"gasPrice": web3.eth.gas_price})
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

