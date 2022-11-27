# for symmetric we will use AES, as it is used for medical records and DES is no longer effective and triple DES is following suite.
# for asymmetric we will use DSS since it is the most popular for encrypting a file or a message, which is what we are dealing with here.
# https://www.trentonsystems.com/blog/symmetric-vs-asymmetric-encryption source
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS
from Crypto.PublicKey import DSA
from Crypto.Random import get_random_bytes


def Symmetric_Encryption(plain_text, symmetric_key):
    cipher = AES.new(symmetric_key, AES.MODE_EAX)
    nonce = cipher.nonce
    encrypted_text, tag = cipher.encrypt_and_digest(plain_text)
    return encrypted_text, nonce, tag


def Symmetric_Decryption(encrypted_text, symmetric_key, nonce, tag):
    cipher = AES.new(symmetric_key, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt(encrypted_text)
    try:
        cipher.verify(tag)
        print("The message is verified:", plaintext)
    except ValueError:
        print("Incorrect key or message corrupted")


def Asymmetric_Encryption(plain_text,key):
    #private_key = ECC.import_key(open('key1.der').read())
    private_key = key
    encrypted_text = SHA256.new(plain_text)
    signer = DSS.new(private_key, 'fips-186-3')
    signature = signer.sign(encrypted_text)
    return encrypted_text,signature


def Asymmetric_Decryption(encrypted_text, signature,key):
    #public_key = ECC.import_key(open('key1.der').read())
    public_key = key.public_key()
    plain_text = SHA256.new(encrypted_text)
    verifier = DSS.new(public_key, 'fips-186-3')
    try:
        verifier.verify(plain_text, signature)
        print("This message is verified")
    except ValueError:
        print("This message is not authentic")
x= Symmetric_Encryption(b'Hello',b'1001011011001101')
print(x)
y= Symmetric_Decryption(x[0],b'1001011011001101',x[1],x[2])

private_key = DSA.generate(2048)
x1 = Asymmetric_Encryption(b'Hello',private_key)
print(x1)
y1 = Asymmetric_Decryption(b'x1[0]',x1[1],private_key)


