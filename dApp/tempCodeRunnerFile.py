doctorAddress = Web3.toChecksumAddress("0xca843569e3427144cead5e4d5999a3d0ccf92b8e")
doctorID = 202001283
doctorName = 'John'
doctorSurname = 'Doe'
tx = register_doctor(abi,url,doctorAddress,contract_address,doctorID,doctorName,doctorSurname)
print(tx)