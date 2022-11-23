# for symmetric we will use AES, as it is used for medical records and DES is no longer effective and triple DES is following suite.
# for asymmetric we will use DSS since it is the most popular for encrypting a file or a message, which is what we are dealing with here.
# https://www.trentonsystems.com/blog/symmetric-vs-asymmetric-encryption source
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS


def Symmetric_Encryption(plain_text, symmetric_key):
    cipher = AES.new(symmetric_key, AES.MODE_EAX)
    nonce = cipher.nonce
    encrypted_text, tag = cipher.encrypt_and_digest(plain_text)
    return encrypted_text, tag, nonce


def Symmetric_Decryption(encrypted_text, symmetric_key, nonce, tag):
    cipher = AES.new(symmetric_key, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt(encrypted_text)
    try:
        cipher.verify(tag)
        print("The message is verified:", plaintext)
    except ValueError:
        print("Incorrect key or message corrupted")


def Asymmetric_Encryption(plain_text):
    plain_text = bytes(plain_text, 'uft-8')
    private_key = ECC.import_key(open('privkey.der').read())
    h = SHA256.new(plain_text)
    signer = DSS.new(private_key, 'fips-186-3')
    signature = signer.sign(h)
    return signature


def Asymmetric_Decryption(encrypted_text, signature):
    public_key = ECC.import_key(open('pubkey.der').read())
    h = SHA256.new(encrypted_text)
    verifier = DSS.new(public_key, 'fips-186-3')
    try:
        verifier.verify(h, signature)
        print("This message is verified")
    except ValueError:
        print("This message is not authentic")
