from binascii import unhexlify

from java.bytecode import generate_bytecode

CONSTANT_TAGS = {
    'Utf8': "01",
    'Class': "07",
    'String': "08",
    'Fieldref': "09",
    'Methodref': "0A",
    'NameAndType': "0C",
}


def _write_int(i, width=4):
    return unhexlify(hex(i)[2:].rjust(width, '0'))


def _write_indices(*indices):
    result = bytes()
    for index in indices:
        result += _write_int(index)
    return result


def write_CONSTANT(tag, *data):
    result = unhexlify(CONSTANT_TAGS[tag])
    if tag == 'Utf8':
        result += _write_int(len(data[0])) + bytes(data[0].encode())
    else:
        result += _write_indices(*data)
    return result 


def write_constant_pool(data):
    pool = {}
    # this_class
    pool[1] = write_CONSTANT('Class', 2)
    pool[2] = write_CONSTANT('Utf8', "PythonSample")
    # super_class
    pool[3] = write_CONSTANT('Class', 4)
    pool[4] = write_CONSTANT('Utf8', "java/lang/Object")
    # constructor from Object
    pool[5] = write_CONSTANT('Methodref', 3, 6)
    pool[6] = write_CONSTANT('NameAndType', 7, 8)
    pool[7] = write_CONSTANT('Utf8', "<init>")
    pool[8] = write_CONSTANT('Utf8', "()V")
    # Code attribute
    pool[9] = write_CONSTANT('Utf8', "Code")
    # public static void main(String[] args)
    pool[10] = write_CONSTANT('Methodref', 1, 11)
    pool[11] = write_CONSTANT('NameAndType', 12, 13)
    pool[12] = write_CONSTANT('Utf8', "main")
    pool[13] = write_CONSTANT('Utf8', "([Ljava/lang/String;)V")
    return pool


def write_class_data(data, pool, f):
    pass


def write_constructor():
    # constructor from Object
    return (unhexlify("0001") + # method access_flags
        _write_int(7) + # method name_index
        _write_int(8) + # method descriptor_index
        _write_int(1) + # method attributes_count
        _write_int(9) + # attribute_name_index (Code attribute)
        _write_int(17, width=8) + # attribute_length
        _write_int(1) + # max_stack
        _write_int(1) + # max_locals
        _write_int(5, width=8) + # code_length
        unhexlify("2AB70005B1") + # code
        _write_int(0) + # exception_table_length
        _write_int(0) # attribute_count
    )

def write_main_method(data):
    code = generate_bytecode(data)
    return (unhexlify("0009") + # ACC_PUBLIC, ACC_STATIC
        _write_int(12) + # method name_index
        _write_int(13) + # method descriptor_index
        _write_int(1) + # method attributes_count
        _write_int(9) + # attribute_name_index (Code attribute)
        _write_int(13, width=8) + # attribute_length
        _write_int(1) + # max_stack
        _write_int(1) + # max_locals
        _write_int(int(len(code) / 2), width=8) + # code_length
        unhexlify(code) + # code
        _write_int(0) + # exception_table_length
        _write_int(0) # attribute_count
    )


def write_class_file(data, filename):
    with open(filename, 'wb') as f:
        f.write(unhexlify("CAFEBABE"))
        f.write(unhexlify("0000"))
        f.write(unhexlify("0032")) # Java 6
        pool = write_constant_pool(data)
        f.write(_write_int(len(pool) + 1))
        for key in sorted(pool.keys()):
            f.write(pool[key])
        f.write(unhexlify("0021")) # access_flags
        f.write(unhexlify("0001")) # this_class
        f.write(unhexlify("0003")) # super_class
        f.write(unhexlify("0000")) # interfaces_count
        f.write(unhexlify("0000")) # fields_count
        f.write(unhexlify("0002")) # method_count
        f.write(write_constructor())
        f.write(write_main_method(data))
        # attributes
        f.write(unhexlify("0000")) # attribute_count
