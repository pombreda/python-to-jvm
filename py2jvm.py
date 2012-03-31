import sys

from python.tokenizer import tokenize_python
from python.parser import parse_tokens
from java.codegenerator import generate_byte_code

if len(sys.argv) == 1:
    print("You must specify a filename to convert to Java byte code")
    sys.exit(1)

python_file = sys.argv[1]
with open(python_file, 'r') as f:
    lines = f.readlines()

tokens = tokenize_python(lines)
data = parse_tokens(tokens)
generate_byte_code(data, 'PythonSample.class')
