from web3 import Web3
import ipfsApi
import json
from web3 import Web3
import os
from Crypto.PublicKey import RSA
from dotenv import load_dotenv
from Crypto.PublicKey import DSA
from base64 import b64encode,b64decode
from Encryption import Symmetric_Encryption, Symmetric_Decryption,Assymmetric_Decryption, Assymmetric_Encryption, sign_document, verify_digital_signature, decrypt_symmetric_key, prepare_file,receive_file

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
    with open(os.path.join(os.getcwd(),"Encryption_Keys","public_key2.pem").replace("\\","/"),'rb') as f:
        doctor_public_key = RSA.importKey(f.read())
    file_name = os.path.basename(file)
    prepare_file("private_key3.pem","public_key2.pem",file_name)
    ipfshash = upload_ipfs(host,port,os.path.join(os.getcwd(),"Medical_Records",file_name+"Encrypted.txt"))
    encrypted_ipfshash = b64encode(Assymmetric_Encryption(doctor_public_key,ipfshash.encode('utf-8'))).decode('utf-8')
    tx = contract.functions.uploadFile(encrypted_ipfshash,doctorAddress,patientAddress).buildTransaction({'nonce': web3.eth.getTransactionCount(account_address), 'from': account_address,"gasPrice": web3.eth.gas_price})

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
    encrypted_ipfshash_list = contract.functions.retrieveFile(doctorAddress,patientAddress).call()
    with open(os.path.join(os.getcwd(),"Encryption_Keys","private_key2.pem").replace("\\","/"),'rb') as f:
        private_key = RSA.importKey(f.read())
    for i in range(len(encrypted_ipfshash_list)):
        encrypted_ipfshash = encrypted_ipfshash_list[i]
        encrypted_ipfshash = b64decode(encrypted_ipfshash.encode('utf-8'))
        ipfshash = Assymmetric_Decryption(private_key,encrypted_ipfshash).decode('utf-8')
        retrieve_ipfs(host,port,ipfshash)
        os.rename(str(ipfshash),"MedicalFile" + str(i) + ".txt")
        receive_file("MedicalFile" + str(i) + ".txt","public_key2.pem","MedicalFile" + str(i))
    
def retrieve_publicKey(abi,url,host,port,address,contract_address):
    web3 = Web3(Web3.HTTPProvider(url,request_kwargs={'timeout': 600}))
    contract = web3.eth.contract(
        address=contract_address,
        abi=abi,
    )
    
    load_dotenv()
    publicKeyIPFSHash = contract.functions.getPublicKey(address).call()
    retrieve_ipfs(host,port,publicKeyIPFSHash)
    with open(publicKeyIPFSHash) as f:
        public_key = DSA.importKey(f.read())
    return public_key

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

