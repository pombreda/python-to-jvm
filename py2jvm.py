import sys

from python.tokenizer import tokenize_python

if len(sys.argv) == 1:
    print("You must specify a filename to convert to Java byte code")
    sys.exit(1)
with open(sys.argv[1], 'r') as f:
    lines = f.readlines()
tokens = tokenize_python(lines)
