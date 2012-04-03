
def generate_bytecode(data):
    bytecode = []
    for instr in data:
        if instr.item_type == 'assignment':
            n = int(instr.digit)
            i1 = "11" # sipush
            i2 = hex(n >> 8)[2:].rjust(2, '0')
            i3 = hex(n & 0xFF)[2:].rjust(2, '0')
            i4 = "3C" # istore_1
            bytecode.extend([i1, i2, i3, i4])
    bytecode.append("B1") # return
    return ''.join(bytecode)
