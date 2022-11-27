from web3 import Web3
import ipfsApi
import json
from web3 import Web3
import os
from dotenv import load_dotenv
from hashlib import sha256
from Encryption import *

def get_private_key(url):
    web3 = Web3(Web3.HTTPProvider(url))
    key_loc = os.getenv("PRIVATE_KEY")
    keyfile = os.path.join(os.getcwd(),os.path.join("testing_keys",key_loc))
    with open(keyfile.replace("\\",'/')) as f:
        key_data = json.load(f)
    private_key = web3.eth.account.decrypt(key_data,"").hex()
    Asymmetric_Encryption()
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

def register_doctor(abi,url,doctorAddress,contract_address,doctorID,doctorName,doctorSurname):
    
    web3 = Web3(Web3.HTTPProvider(url,request_kwargs={'timeout': 600}))
    contract = web3.eth.contract(
        address=contract_address,
        abi=abi,
    )
    
    load_dotenv()
    account_address = Web3.toChecksumAddress(os.getenv("ACCOUNT_ADDRESS"))
    private_key = get_private_key(url)

    tx = contract.functions.registerDoctor(doctorID,doctorName,doctorSurname,doctorAddress).buildTransaction({'nonce': web3.eth.getTransactionCount(account_address), 'from': account_address,"gasPrice": web3.eth.gas_price})

    signed_tx = web3.eth.account.signTransaction(tx, private_key=private_key)

    tx_transact = web3.eth.sendRawTransaction(signed_tx.rawTransaction)


    tx_receipt = web3.eth.waitForTransactionReceipt(tx_transact)
        
    
    return tx_receipt

def register_patient(abi,url,patientID,patientAddress,contract_address):
    
    web3 = Web3(Web3.HTTPProvider(url,request_kwargs={'timeout': 600}))
    contract = web3.eth.contract(
        address=contract_address,
        abi=abi,
    )
    
    load_dotenv()
    account_address = Web3.toChecksumAddress(os.getenv("ACCOUNT_ADDRESS"))
    private_key = get_private_key(url)

    tx = contract.functions.registerPatient(patientID,patientAddress).buildTransaction({'nonce': web3.eth.getTransactionCount(account_address), 'from': account_address,"gasPrice": web3.eth.gas_price})

    signed_tx = web3.eth.account.signTransaction(tx, private_key=private_key)

    tx_transact = web3.eth.sendRawTransaction(signed_tx.rawTransaction)


    tx_receipt = web3.eth.waitForTransactionReceipt(tx_transact)
        
    
    return tx_receipt

def remove_patient(abi,url,patientAddress,contract_address):
    
    web3 = Web3(Web3.HTTPProvider(url,request_kwargs={'timeout': 600}))
    contract = web3.eth.contract(
        address=contract_address,
        abi=abi,
    )
    
    load_dotenv()
    account_address = Web3.toChecksumAddress(os.getenv("ACCOUNT_ADDRESS"))
    private_key = get_private_key(url)

    tx = contract.functions.removePatient(patientAddress).buildTransaction({'nonce': web3.eth.getTransactionCount(account_address), 'from': account_address,"gasPrice": web3.eth.gas_price})

    signed_tx = web3.eth.account.signTransaction(tx, private_key=private_key)

    tx_transact = web3.eth.sendRawTransaction(signed_tx.rawTransaction)


    tx_receipt = web3.eth.waitForTransactionReceipt(tx_transact)
        
    
    return tx_receipt


def remove_doctor(abi,url,doctorAddress,contract_address):
    
    web3 = Web3(Web3.HTTPProvider(url,request_kwargs={'timeout': 600}))
    contract = web3.eth.contract(
        address=contract_address,
        abi=abi,
    )
    web3.eth.defaultAccount.enc
    load_dotenv()
    account_address = Web3.toChecksumAddress(os.getenv("ACCOUNT_ADDRESS"))
    private_key = get_private_key(url)

    tx = contract.functions.removeDoctor(doctorAddress).buildTransaction({'nonce': web3.eth.getTransactionCount(account_address), 'from': account_address,"gasPrice": web3.eth.gas_price})

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

#Register a doctor using the following lines of code
# doctorAddress = Web3.toChecksumAddress("0xca843569e3427144cead5e4d5999a3d0ccf92b8e")
# doctorID = 202001283
# doctorName = 'John'
# doctorSurname = 'Doe'
# tx = register_doctor(abi,url,doctorAddress,contract_address,doctorID,doctorName,doctorSurname)
# print(tx)

#Register a patient using the following lines of code
# patientAddress = Web3.toChecksumAddress("0x0fbdc686b912d7722dc86510934589e0aaf3b55a")
# patientID = 202001282
# tx = register_patient(abi,url,patientID,patientAddress,contract_address)
# print(tx)
web3 = Web3(Web3.HTTPProvider(url))
print(web3.eth.accounts[0])