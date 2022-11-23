import PyPDF2
import hashlib
from Crypto.Cipher import AES
import os

def encrypt(file,key):
    cipher = AES.new(key, AES.MODE_EAX)
    pdfFileObj = open(file, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    pdf_writer = PyPDF2.PdfFileWriter()
    for page in range(pdfReader.numPages):
        pageObj = pdfReader.getPage(page)
        ciphertext, tag = cipher.encrypt_and_digest(pageObj.extractText().encode())
        print(ciphertext)
    pdfFileObj.close()
    
    
    # with open("encrypted"+file,"wb") as f:
    #     [ f.write(x) for x in (cipher.nonce, tag, ciphertext) ]

encrypt('calendar2022-2023.pdf',os.urandom(32))
