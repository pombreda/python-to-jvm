import binascii

def generate_byte_code(data, filename):
    with open(filename, 'wb') as f:
        f.write(binascii.unhexlify("CAFEBABE"))
        f.write(binascii.unhexlify("0000"))
        f.write(binascii.unhexlify("0032")) # Java 6
