from binascii import unhexlify

def _write_indices(*indices):
    result = bytes()
    for index in indices:
        result += unhexlify(hex(index)[2:].rjust(4, '0'))
    return result

def write_CONSTANT_Utf8(s):
    attribute_type = unhexlify("01")
    attribute_length = unhexlify(hex(len(s))[2:].rjust(4, '0'))
    attribute_data = bytes(s.encode())
    return attribute_type + attribute_length + attribute_data

def write_CONSTANT_Class(index):
    return unhexlify("07") + _write_indices(index)

def write_CONSTANT_String(index):
    return unhexlify("08") + _write_indices(index)

def write_CONSTANT_Fieldref(index1, index2):
    return unhexlify("09") + _write_indices(index1, index2)

def write_CONSTANT_NameAndType(index1, index2):
    return unhexlify("0C") + _write_indices(index1, index2)

def write_CONSTANT_Methodref(index1, index2):
    return unhexlify("10") + _write_indices(index1, index2)

def write_constant_pool(data, f):
    pass

def write_class_data(data, pool, f):
    pass

def generate_byte_code(data, filename):
    with open(filename, 'wb') as f:
        f.write(unhexlify("CAFEBABE"))
        f.write(write_CONSTANT_NameAndType(19, 20))
        return
        f.write(unhexlify("0000"))
        f.write(unhexlify("0032")) # Java 6
        pool = write_constant_pool(data, f)
        f.write(unhexlify("0021")) # access_flags
        write_class_data(data, pool, f)
        #f.write(write_CONSTANT_Utf8("0"))
