# for symmetric we will use AES, as it is used for medical records and DES is no longer effective and triple DES is following suite.
# for asymmetric we will use RSA since it is the most popular for encrypting a file or a message, which is what we are dealing with here.
# https://www.trentonsystems.com/blog/symmetric-vs-asymmetric-encryption source
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_v1_5
import os
from base64 import b64encode,b64decode


def Symmetric_Encryption(plain_text,public_key):
    symmetric_key = os.urandom(16)
    cipher = AES.new(symmetric_key, AES.MODE_EAX)
    encrypted_text, tag = cipher.encrypt_and_digest(plain_text.encode('utf-8'))
    nonce = cipher.nonce
    encrypted_symmetric_key = encrypt_symmetric_key(symmetric_key,public_key)
    return encrypted_text,encrypted_symmetric_key, nonce

def Assymmetric_Encryption(public_key,plain_text):
    encryptor = PKCS1_OAEP.new(public_key)
    encrypted_text = encryptor.encrypt(plain_text)
    return encrypted_text

def Assymmetric_Decryption(private_key,cipher_text):
    decryptor = PKCS1_OAEP.new(private_key)
    plain_text = decryptor.decrypt(cipher_text)
    return plain_text

def Symmetric_Decryption(encrypted_text, symmetric_key,nonce):
    cipher = AES.new(symmetric_key, AES.MODE_EAX,nonce=nonce)
    plaintext = cipher.decrypt(encrypted_text)
    return plaintext

def sign_document(plain_text,private_key_file,):
    with open(private_key_file) as f:
        private_key = RSA.importKey(f.read())
    hash = SHA256.new(plain_text)
    signer = PKCS1_v1_5.new(private_key)
    signature = signer.sign(hash)
    return hash,signature

def decrypt_symmetric_key(text_file,private_key_file):
    with open(private_key_file) as f:
        private_key = RSA.importKey(f.read())
    with open(text_file, 'r') as f:
        encrypted_symmetric_key = f.readline().strip("\n")
        signature = f.readline().strip("\n")
        nonce = f.readline().strip("\n")
        encrypted_text = f.readline()
    encrypted_symmetric_key = b64decode(encrypted_symmetric_key.encode('utf-8'))
    signature = b64decode(signature.encode('utf-8'))
    nonce = b64decode(nonce.encode('utf-8'))
    encrypted_text = b64decode(encrypted_text.encode('utf-8'))
    decryptor = PKCS1_OAEP.new(private_key)
    symmetric_key = decryptor.decrypt(encrypted_symmetric_key)
    return symmetric_key,encrypted_text,signature, nonce



def encrypt_symmetric_key(symmetric_key,public_key):
    encryptor = PKCS1_OAEP.new(public_key)
    encrypted_symmetric_key = encryptor.encrypt(symmetric_key)
    return encrypted_symmetric_key

def verify_digital_signature(plain_text, signature,public_key_file):
    with open(public_key_file,'rb') as f:
        public_key = RSA.importKey(f.read())
    hash = SHA256.new(plain_text)
    verifier = PKCS1_v1_5.new(public_key)
    try:
        verifier.verify(hash, signature)
        print("This message is verified")
    except ValueError:
        print("This message is not authentic")

def prepare_file(private_file,public_file,file_name):
    with open(os.path.join(os.getcwd(),"Encryption_Keys",public_file).replace("\\","/"),'rb') as f:
        public_key = RSA.importKey(f.read())
    with open(os.path.join(os.getcwd(),"Encryption_Keys",private_file).replace("\\","/"),'rb') as f:
        private_key = RSA.importKey(f.read())
    with open(file_name, "r") as f:
        plain_text = f.read()
    encrypted_content, encrypted_symmetric_key, nonce = Symmetric_Encryption(plain_text,public_key)
    hash,digital_signature = sign_document(plain_text.encode(),os.path.join(os.getcwd(),"Encryption_Keys",private_file))
    with open(os.path.join(os.getcwd(),"Medical_Records",file_name+"Encrypted.txt"),'w') as f:
        f.write(b64encode(encrypted_symmetric_key).decode('utf-8') + "\n")
        f.write(b64encode(digital_signature).decode('utf-8') + "\n")
        f.write(b64encode(nonce).decode('utf-8') + "\n")
        f.write(b64encode(encrypted_content).decode('utf-8'))
        
def receive_file(file,public_file,file_name):
    symmetric_key,encrypted_text,signature,nonce = decrypt_symmetric_key(file,os.path.join(os.getcwd(),"Encryption_Keys","private_key2.pem"))
    plaintext = Symmetric_Decryption(encrypted_text,symmetric_key,nonce)
    verify_digital_signature(plaintext,signature,os.path.join(os.getcwd(),"Encryption_Keys",public_file))
    with open(os.path.join(os.getcwd(),"Medical_Records",file_name+"Decrypted.txt"),'w') as f:
        f.write(plaintext.decode('utf-8'))


# Generate Public and Private Keys for Encryption
# key = RSA.generate(1024)
# with open(os.path.join(os.getcwd(),"Encryption_Keys","public_key1.pem").replace("\\","/"), "wb") as f: #The Public Key of the Admin
#     f.write(key.publickey().exportKey(format='PEM'))
# with open(os.path.join(os.getcwd(),"Encryption_Keys","private_key1.pem").replace("\\","/"), "wb") as f:
#     f.write(key.exportKey('PEM'))
# key = RSA.generate(1024)
# with open(os.path.join(os.getcwd(),"Encryption_Keys","public_key2.pem").replace("\\","/"), "wb") as f: #The Public Key of the Doctor
#     f.write(key.publickey().exportKey(format='PEM'))
# with open(os.path.join(os.getcwd(),"Encryption_Keys","private_key2.pem").replace("\\","/"), "wb") as f:
#     f.write(key.exportKey('PEM'))
# key = RSA.generate(1024)
# with open(os.path.join(os.getcwd(),"Encryption_Keys","public_key3.pem").replace("\\","/"), "wb") as f: #The Public Key of the Patient
#     f.write(key.publickey().exportKey(format='PEM'))
# with open(os.path.join(os.getcwd(),"Encryption_Keys","private_key3.pem").replace("\\","/"), "wb") as f:
#     f.write(key.exportKey('PEM'))



