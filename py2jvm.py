import sys

from python.tokenizer import tokenize_python
from python.parser import parse_tokens
from java.codegenerator import write_class_file

if len(sys.argv) == 1:
    print("You must specify a filename to convert to Java byte code")
    sys.exit(1)

python_file = sys.argv[1]
with open(python_file, 'r') as f:
    lines = f.readlines()

tokens = tokenize_python(lines)
data = parse_tokens(tokens)
write_class_file(data, 'PythonSample.class')
